"""Local encrypted snapshot/deletion-authority experiment; no cloud integration."""
import contextlib,fcntl,hashlib,io,json,os,sqlite3,tempfile,zipfile
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from core import Store,durable
DAY=86400
class Backup:
 def __init__(self,root,destination,key):
  self.root=Path(root);self.dest=Path(destination);self.dest.mkdir(parents=True,exist_ok=True);self.key=key;self.journal=self.dest/'deletion.authority';self.head=self.dest/'deletion.latest-head'
 @contextlib.contextmanager
 def maintenance(self):
  self.root.mkdir(parents=True,exist_ok=True)
  with open(self.root/'maintenance.lock','a+b') as f:
   fcntl.flock(f,fcntl.LOCK_EX)
   try:yield
   finally:fcntl.flock(f,fcntl.LOCK_UN)
 def seal(self,data,label):
  nonce=os.urandom(12);return nonce+AESGCM(self.key).encrypt(nonce,data,label)
 def open(self,data,label):return AESGCM(self.key).decrypt(data[:12],data[12:],label)
 def initialize(self):
  if self.journal.exists():raise ValueError('authority already exists')
  data=self.seal(json.dumps({'seq':0,'events':[]}).encode(),b'deletion');durable(self.journal,data);durable(self.head,self.seal(json.dumps({'seq':0,'hash':hashlib.sha256(data).hexdigest()}).encode(),b'head'))
 def authority(self):
  # No empty fallback: missing/corrupt independent recovery authority fails closed.
  data=self.journal.read_bytes();j=json.loads(self.open(data,b'deletion'));head=json.loads(self.open(self.head.read_bytes(),b'head'))
  if head['seq']!=j['seq'] or head['hash']!=hashlib.sha256(data).hexdigest():raise PermissionError('incomplete/rolled-back deletion authority')
  return j
 def event(self,project,kind,at):
  j=self.authority();j['seq']+=1;j['events'].append({'id':j['seq'],'project':project,'kind':kind,'at':at})
  data=self.seal(json.dumps(j).encode(),b'deletion');durable(self.journal,data);durable(self.head,self.seal(json.dumps({'seq':j['seq'],'hash':hashlib.sha256(data).hexdigest()}).encode(),b'head'));return j['seq']
 def states(self):
  result={}
  for e in self.authority()['events']:
   old=result.get(e['project'])
   if old and old['kind']=='purge':continue
   result[e['project']]=e
  return result
 def visible(self,project):
  e=self.states().get(project)
  if e and e['kind'] in ['delete','purge']:return False
  s=Store(self.root)
  if s.read("SELECT value FROM meta WHERE key='access_reconciled'")==[{'value':'0'}]:return False
  with s.tx() as c:
   try:s.project(c,project);return True
   except PermissionError:return False
 def delete(self,project,now,stop=None):
  with self.maintenance():
   s=Store(self.root)
   # SQLite claim exclusion remains held through durable local journal intent.
   with s.tx() as c:
    p=s.project(c,project)
    if p['render_job'] or c.execute("SELECT 1 FROM jobs WHERE project=? AND state IN ('running','cancelling','recovery_required')",(project,)).fetchone():raise PermissionError('execution not stopped')
    self.event(project,'delete',now)
    if stop=='after_authority':os._exit(93)
    c.execute('UPDATE projects SET deleted=? WHERE id=?',(now,project))
    queued=c.execute("SELECT * FROM jobs WHERE project=? AND state='queued'",(project,)).fetchall()
    for j in queued:
     c.execute("UPDATE jobs SET cancel=1,state='cancelled' WHERE id=?",(j['id'],))
     c.execute('UPDATE account SET held=held-?,allowheld=allowheld-? WHERE id=1',(j['maximum'],j['maximum']))
 def reconcile_deletion_intents(self):
  # Recovery gate applies authority before any worker claims after an interrupted intent.
  s=Store(self.root)
  with s.tx() as c:
   for project,e in self.states().items():
    if e['kind'] in ['delete','purge']:
     c.execute('UPDATE projects SET deleted=? WHERE id=?',(e['at'],project))
     for j in c.execute("SELECT * FROM jobs WHERE project=? AND state='queued'",(project,)).fetchall():
      c.execute("UPDATE jobs SET cancel=1,state='cancelled' WHERE id=?",(j['id'],));c.execute('UPDATE account SET held=held-?,allowheld=allowheld-? WHERE id=1',(j['maximum'],j['maximum']))
 def restore_project(self,project,now):
  with self.maintenance():
   e=self.states().get(project)
   if not e or e['kind']!='delete' or now>=e['at']+7*DAY:raise PermissionError('restoration window expired')
   s=Store(self.root)
   with s.tx() as c:c.execute('UPDATE projects SET deleted=NULL WHERE id=? AND purged=0',(project,))
   self.event(project,'restore',now)
 def purge_project(self,project):
  s=Store(self.root);assets=s.read('SELECT key FROM artifacts WHERE project=?',(project,));attempts=s.read('SELECT a.id FROM attempts a JOIN jobs j ON j.id=a.job WHERE j.project=?',(project,))
  with s.tx() as c:
   c.execute('DELETE FROM selections WHERE project=?',(project,));c.execute('DELETE FROM artifacts WHERE project=?',(project,))
   c.execute('DELETE FROM progress WHERE job IN (SELECT id FROM jobs WHERE project=?)',(project,));c.execute('DELETE FROM attempts WHERE job IN (SELECT id FROM jobs WHERE project=?)',(project,))
   c.execute('DELETE FROM jobs WHERE project=?',(project,));c.execute('DELETE FROM scenes WHERE project=?',(project,));c.execute('UPDATE projects SET deleted=coalesce(deleted,0),purged=1,render_job=NULL WHERE id=?',(project,))
  for a in assets:(s.media/a['key']).unlink(missing_ok=True)
  for a in attempts:
   for p in (s.root/'spool').glob(a['id']+'.*'):p.unlink(missing_ok=True)
 def purge_due(self,now):
  with self.maintenance():
   for project,e in self.states().items():
    if e['kind']=='delete' and now>=e['at']+7*DAY:self.event(project,'purge',e['at']+7*DAY);self.purge_project(project)
    elif e['kind']=='purge':self.purge_project(project)
 def manifest(self,path):
  raw=self.open(Path(path).read_bytes(),b'snapshot')
  with zipfile.ZipFile(io.BytesIO(raw)) as z:return json.loads(z.read('manifest.json'))
 def cycle(self,now,fail=None):
  self.purge_due(now)
  with self.maintenance():
   purged={p for p,e in self.states().items() if e['kind']=='purge'}
   # Purge historical copies independently BEFORE attempting a replacement backup.
   for path in self.dest.glob('snapshot-*.enc'):
    if purged.intersection(self.manifest(path)['content_projects']):path.unlink()
   for partial in self.dest.glob('*.tmp'):partial.unlink()
   if fail=='before_snapshot':raise OSError('injected backup unavailable')
   return self.snapshot_locked(now,fail)
 def snapshot(self,now,fail=None):
  with self.maintenance():return self.snapshot_locked(now,fail)
 def snapshot_locked(self,now,fail):
  s=Store(self.root);authority=self.authority()
  with tempfile.TemporaryDirectory(prefix='alpha-backup-stage-') as tmp:
   db=Path(tmp)/'state.sqlite3'
   with contextlib.closing(s.connection()) as source,sqlite3.connect(db) as target:source.backup(target)
   c=sqlite3.connect(db);c.row_factory=sqlite3.Row
   projects=[r[0] for r in c.execute('SELECT id FROM projects WHERE purged=0')]
   paths=[('media/'+r['key'],s.media/r['key']) for r in c.execute('SELECT key FROM artifacts')]
   for r in c.execute('SELECT id FROM attempts'):
    paths.extend(('spool/'+p.name,p) for p in (self.root/'spool').glob(r['id']+'.*') if not p.name.endswith('.tmp'))
   c.close();paths.insert(0,('state.sqlite3',db))
   manifest={'at':now,'journal_seq':authority['seq'],'content_projects':projects,'files':{}}
   raw=io.BytesIO()
   with zipfile.ZipFile(raw,'w',zipfile.ZIP_DEFLATED) as z:
    for name,path in paths:
     data=path.read_bytes();manifest['files'][name]=hashlib.sha256(data).hexdigest();z.writestr(name,data)
    z.writestr('manifest.json',json.dumps(manifest))
   encrypted=self.seal(raw.getvalue(),b'snapshot');target=self.dest/f'snapshot-{now}.enc'
   if fail=='partial_write':durable(self.dest/'incomplete.tmp',encrypted[:17]);raise OSError('injected interrupted backup')
   durable(target,encrypted);return target
 def restore_snapshot(self,path,empty,now):
  authority=self.authority();manifest=self.manifest(path)
  if authority['seq']<manifest['journal_seq']:raise PermissionError('deletion authority behind snapshot cutoff')
  empty=Path(empty)
  if empty.exists() and any(empty.iterdir()):raise ValueError('restore requires empty storage')
  empty.mkdir(parents=True,exist_ok=True)
  raw=self.open(Path(path).read_bytes(),b'snapshot')
  with zipfile.ZipFile(io.BytesIO(raw)) as z:
   for name,digest in manifest['files'].items():
    if name.startswith('/') or '..' in Path(name).parts:raise ValueError('unsafe archive path')
    data=z.read(name)
    if hashlib.sha256(data).hexdigest()!=digest:raise ValueError('snapshot hash mismatch')
    durable(empty/name,data)
  restored=Backup(empty,self.dest,self.key);s=Store(empty)
  with s.tx() as c:
   c.execute("INSERT OR REPLACE INTO meta VALUES('reconciled','0')");c.execute("INSERT OR REPLACE INTO meta VALUES('access_reconciled','0')")
   c.execute("UPDATE lane SET guard='unknown' WHERE job IS NOT NULL")
   c.execute("UPDATE jobs SET state='recovery_required' WHERE state IN ('running','cancelling')")
  restored.purge_due(now)
  with s.tx() as c:
   for project,e in restored.states().items():
    if e['kind']=='delete':c.execute('UPDATE projects SET deleted=? WHERE id=?',(e['at'],project))
    elif e['kind']=='restore':c.execute('UPDATE projects SET deleted=NULL WHERE id=? AND purged=0',(project,))
   c.execute("UPDATE meta SET value='1' WHERE key='access_reconciled'")
  s.audit();return {'age_seconds':now-manifest['at'],'within_24h':0<=now-manifest['at']<=DAY,'manifest':manifest,'restored':restored}
 def reconcile(self,actual_spend,unknown_liability=0,actual_consumed=None):
  # Owner-supplied authoritative external total: never silently reset real charges.
  s=Store(self.root)
  with s.tx() as c:
   old=c.execute('SELECT * FROM account').fetchone()
   if actual_spend<old['spent']:raise ValueError('external spend incomplete')
   if actual_consumed is None or actual_consumed<old['consumed']:raise ValueError('allowance reconciliation incomplete')
   delta=actual_spend-old['spent'];c.execute('INSERT OR REPLACE INTO ledger VALUES(?,?,?)',('restore-reconcile','external_adjustment',delta))
   c.execute('UPDATE account SET spent=?,held=max(held,?),consumed=? WHERE id=1',(actual_spend,unknown_liability,actual_consumed))
   if c.execute("SELECT 1 FROM jobs WHERE state='recovery_required'").fetchone() or unknown_liability:return 'blocked_unknown'
   c.execute("UPDATE meta SET value='1' WHERE key='reconciled'");return 'ready'
