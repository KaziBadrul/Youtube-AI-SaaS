import contextlib,json,multiprocessing,os,sqlite3,subprocess,sys,tempfile,threading
from pathlib import Path
from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from core import Store,durable
from publication import execute,FakeProvider
from backup import Backup,DAY
from evidence import BASE,run

def experiment():
 checks=[]
 with tempfile.TemporaryDirectory(prefix='alpha-s8-') as tmp:
  base=Path(tmp);live=base/'live';offhost=base/'independent-local-destination';key=AESGCM.generate_key(bit_length=256)
  # Key deliberately separate from backup artifact. Production key custody not selected.
  durable(base/'separate-test-key',key);s=Store(live);s.initialize();b=Backup(live,offhost,key);b.initialize();initial_authority=b.journal.read_bytes();initial_head=b.head.read_bytes();now=100*DAY
  first=s.admit('one');_,f=s.claim();execute(live,first,f,'one');s.progress(first,'completed')
  second=s.admit('pending',scene=2);_,f2=s.claim();execute(live,second,f2,'two',behavior='delayed')
  stop=threading.Event();errors=[]
  def writer():
   try:
    for n in range(80):s.progress(second,'tick:'+str(n))
   except Exception as e:errors.append(str(e))
  thread=threading.Thread(target=writer);thread.start();snapshot=b.snapshot(now);thread.join();assert not errors
  manifest=b.manifest(snapshot);assert manifest['files'] and 'state.sqlite3' in manifest['files'];assert b'First approved words.' not in snapshot.read_bytes()
  restored=b.restore_snapshot(snapshot,base/'restore-unknown',now+100);r=Store(base/'restore-unknown');assert restored['within_24h']
  assert r.read('SELECT * FROM artifacts')==s.read('SELECT * FROM artifacts');assert r.read('SELECT * FROM account')==s.read('SELECT * FROM account')
  assert r.read('SELECT * FROM ledger')==s.read('SELECT * FROM ledger');assert r.read('SELECT * FROM attempts')==s.read('SELECT * FROM attempts')
  assert r.read('SELECT * FROM scenes')==s.read('SELECT * FROM scenes');assert r.read('SELECT guard FROM lane')[0]['guard']=='unknown'
  assert r.admit('forbidden')=='reconciliation_required';assert r.claim() is None
  assert restored['restored'].reconcile(100,100,100)=='blocked_unknown';assert r.admit('still-forbidden')=='reconciliation_required';checks.append('consistent_snapshot_under_80_concurrent_writes_and_unknown_attempt_restore')
  tampered=base/'tampered.enc';data=bytearray(snapshot.read_bytes());data[-1]^=1;durable(tampered,data)
  try:b.manifest(tampered);raise AssertionError('ciphertext accepted')
  except InvalidTag:pass
  checks.append('authenticated_encryption_tamper_rejected')
  # Reconcile original uncertainty, then take known-complete baseline.
  FakeProvider(live).complete('two');from publication import recover
  recover(live,'two',f2);clean=b.snapshot(now+200)
  # Known external spending after backup must not be erased by restoration.
  third=s.admit('post-backup');_,f3=s.claim();execute(live,third,f3,'three')
  known=b.restore_snapshot(clean,base/'restore-known',now+300);k=Store(base/'restore-known');assert k.admit('no')=='reconciliation_required'
  assert known['restored'].reconcile(300,actual_consumed=300)=='ready';assert k.read('SELECT spent FROM account')[0]['spent']==300;assert k.read('SELECT consumed FROM account')[0]['consumed']==300;assert k.admit('after-reconcile') not in ['reconciliation_required','budget_blocked']
  checks.append('external_post_snapshot_spend_reconciled_before_admission')
  # Failed partial backup never supersedes last valid encrypted snapshot.
  try:b.snapshot(now+400,'partial_write');raise AssertionError('failure not injected')
  except OSError:pass
  assert clean.exists() and b.manifest(clean)['at']==now+200;assert len(list(offhost.glob('incomplete.tmp')))==1
  try:b.manifest(offhost/'incomplete.tmp');raise AssertionError('partial ciphertext accepted')
  except InvalidTag:pass
  stale=b.restore_snapshot(clean,base/'restore-stale',now+200+DAY+1);assert not stale['within_24h'];assert Store(base/'restore-stale').admit('no')=='reconciliation_required';checks.append('failed_backup_keeps_valid_snapshot_and_overdue_RPO_detected')
  # Crash after journal durability but before DB hide cannot resurrect visible content.
  p=subprocess.run([sys.executable,str(BASE/'s8.py'),'delete-crash',str(live),str(offhost),str(base/'separate-test-key'),str(now+500)],capture_output=True)
  assert p.returncode==93,(p.returncode,p.stderr)
  assert not b.visible(1);assert s.read('SELECT deleted FROM projects WHERE id=1')[0]['deleted'] is None
  aftercrash=b.restore_snapshot(clean,base/'restore-delete-crash',now+501);assert not aftercrash['restored'].visible(1)
  # Finish intent locally; restoration available strictly before seven-day cutoff.
  queued=s.admit('during-pending-delete');b.reconcile_deletion_intents();assert s.claim() is None;assert s.read('SELECT state FROM jobs WHERE id=?',(queued,))[0]['state']=='cancelled'
  b.restore_project(1,now+500+7*DAY-1);assert b.visible(1)
  b.delete(1,now+600);assert not b.visible(1)
  try:b.restore_project(1,now+600+7*DAY);raise AssertionError('expired restore accepted')
  except PermissionError:pass
  checks.append('durable_deletion_intent_survives_crash_and_exact_seven_day_window')
  oldcopy=base/'old-snapshot-for-resurrection-test.enc';durable(oldcopy,clean.read_bytes())
  purge_at=now+600+7*DAY;b.purge_due(purge_at)
  assert s.read('SELECT purged FROM projects WHERE id=1')[0]['purged']==1;assert not s.read('SELECT * FROM scenes WHERE project=1');assert not s.read('SELECT * FROM artifacts WHERE project=1');assert not list((live/'media').glob('*'));assert not list((live/'spool').glob('*'))
  assert s.read('SELECT * FROM ledger');assert b.visible(2)
  # Next cycle purge happens even if new backup fails; all old content archives removed.
  try:b.cycle(purge_at+DAY,'before_snapshot');raise AssertionError('failed cycle not injected')
  except OSError:pass
  assert not list(offhost.glob('snapshot-*.enc'))
  # Residual interrupted ciphertext is not a valid recoverable snapshot but purge it too.
  assert not list(offhost.glob('*.tmp'))
  old=b.restore_snapshot(oldcopy,base/'restore-old-after-purge',purge_at+DAY);o=Store(base/'restore-old-after-purge')
  assert not old['restored'].visible(1);assert not o.read('SELECT * FROM scenes WHERE project=1');assert not list(o.media.glob('*'));assert old['restored'].visible(2);oldcopy.unlink()
  fresh=b.cycle(purge_at+DAY+1);assert 1 not in b.manifest(fresh)['content_projects'];s.audit();checks.append('live_and_next_cycle_backup_purge_despite_backup_failure_no_old_snapshot_resurrection')
  # Missing authority denies both old-snapshot restoration and content access.
  authority=b.journal.read_bytes();b.journal.unlink()
  try:b.restore_snapshot(fresh,base/'restore-missing',purge_at+DAY+2);raise AssertionError('missing authority accepted')
  except FileNotFoundError:pass
  try:b.visible(2);raise AssertionError('missing journal access accepted')
  except FileNotFoundError:pass
  durable(b.journal,authority)
  corrupt=bytearray(authority);corrupt[-1]^=1;durable(b.journal,corrupt)
  try:b.restore_snapshot(fresh,base/'restore-corrupt',purge_at+DAY+3);raise AssertionError('corrupt authority accepted')
  except InvalidTag:pass
  durable(b.journal,initial_authority)
  try:b.restore_snapshot(fresh,base/'restore-rollback',purge_at+DAY+4);raise AssertionError('rolled-back authority accepted')
  except PermissionError:pass
  current_head=b.head.read_bytes();durable(b.head,initial_head)
  try:b.restore_snapshot(fresh,base/'restore-old-cutoff',purge_at+DAY+5);raise AssertionError('authority behind cutoff accepted')
  except PermissionError:pass
  durable(b.head,current_head)
  durable(b.journal,authority);checks.append('missing_corrupt_or_rolled_back_independent_authority_fails_closed')
  return {'checks':checks,'concurrent_snapshot_writes':80,'encryption':'AES-256-GCM; random per-artifact nonce; key outside ciphertext','backup_interval_seconds':DAY,'deletion_window_seconds':7*DAY,'backup_purge_delay_tested_seconds':DAY,'restored_file_count':len(manifest['files']),'local_destination_only':True,'limitations':['Latest-head receipt detects journal-only rollback. The independent authority and its current head must be recovered from their own latest durable destination, never from the database snapshot. Total loss/rollback of that destination cannot be proven safe locally and must fail closed operationally.','Temporary local destination models an independent off-host store; actual geographic/failure-domain independence, key custody, immutable provider histories and monthly costs remain S9/operator decisions.','Tiny fixtures prove protocol structure, not full-sized backup throughput or scheduler reliability. Daily monitoring must report missed/overdue backups; a failed cycle cannot guarantee a 24-hour RPO.','External spend is authoritative fake input. Actual provider outcome/charge reconciliation remains S4.','Maintenance lock coordinates snapshot/purge; immutable publication files permit concurrent writes. Production implementation must apply the same exclusion to all destructive maintenance and secure restore access before startup.']}
if __name__=='__main__':
 if len(sys.argv)>1:
  Backup(sys.argv[2],sys.argv[3],Path(sys.argv[4]).read_bytes()).delete(1,int(sys.argv[5]),'after_authority')
 else:run('S8',experiment)
