import json,subprocess,sys,tempfile
from pathlib import Path
from core import Store
from publication import PHASES,FakeProvider,execute,recover
from evidence import BASE,run
from supervision import running,stop_verified

def killed(root,job,fence,phase,kind='audio'):
 r=subprocess.run([sys.executable,str(BASE/'publication.py'),str(root),job,str(fence),'a',phase,kind],capture_output=True,text=True)
 assert r.returncode==91,(r.returncode,r.stderr)

def experiment():
 cases=[]
 for repeat in range(3):
  for phase in PHASES[:-1]:
   with tempfile.TemporaryDirectory(prefix='alpha-s3-') as tmp:
    s=Store(tmp);s.initialize();job=s.admit('first');_,f=s.claim();killed(tmp,job,f,phase)
    p=FakeProvider(tmp);outcome=recover(tmp,'a',f)
    if phase in ['prepared','before_submission','submission_started']:
     assert outcome=='unknown';assert s.read('SELECT held,allowheld FROM account')[0]=={'held':100,'allowheld':100}
     second=s.admit('second',scene=2);assert second not in ['budget_blocked','reconciliation_required'];assert s.claim() is None
     assert s.read('SELECT guard FROM lane')[0]['guard']=='unknown'
    else:
     assert outcome in ['selected','history'];assert p.count('a')==1
     assert len(s.read("SELECT * FROM ledger WHERE kind='delivered'"))==1
     recover(tmp,'a',f);assert p.count('a')==1
    assert s.read('SELECT words FROM scenes WHERE id=2')[0]['words']=='Sibling approved words.';s.audit()
    cases.append({'repeat':repeat,'crash':phase,'recovery':outcome,'fake_submissions':p.count('a')})
 outcomes=[]
 for behavior in ['success','definite_failure','timeout_before','timeout_after','delayed']:
  with tempfile.TemporaryDirectory(prefix='alpha-s3-provider-') as tmp:
   s=Store(tmp);s.initialize();job=s.admit('first');_,f=s.claim();result=execute(tmp,job,f,'a',behavior=behavior);p=FakeProvider(tmp)
   if behavior in ['timeout_after','delayed']:
    assert result=='unknown' and s.claim() is None
    s.cancel(job);assert s.claim() is None
    assert s.read('SELECT held FROM account')[0]['held']==100
    p.complete('a');assert recover(tmp,'a',f)=='history';assert s.read('SELECT * FROM selections')==[];assert s.read('SELECT state FROM jobs')[0]['state']=='cancelled'
   if behavior=='definite_failure':assert s.read('SELECT spent,held,consumed FROM account')[0]=={'spent':40,'held':0,'consumed':0}
   if behavior=='timeout_before':assert p.count('a')==0 and s.read('SELECT spent,held FROM account')[0]=={'spent':0,'held':0}
   s.audit();outcomes.append({'behavior':behavior,'result':result,'calls':p.count('a')})
 with tempfile.TemporaryDirectory(prefix='alpha-s3-fence-') as tmp:
  s=Store(tmp);s.initialize();job=s.admit('first');_,f=s.claim();execute(tmp,job,f,'a',behavior='delayed');p=FakeProvider(tmp);p.complete('a')
  with s.tx() as c:c.execute("UPDATE lane SET fence=fence+1,guard='active' WHERE id=1")
  assert recover(tmp,'a',f)=='history';assert not s.select('a',f);assert not s.read('SELECT * FROM selections')
  assert not s.finish(job,f,True);assert s.finish(job,f+1,True);s.audit()
 child_evidence=[]
 for repeat in range(3):
  with tempfile.TemporaryDirectory(prefix='alpha-s3-child-') as tmp:
   s=Store(tmp);s.initialize();job=s.admit('render',kind='render');_,f=s.claim();recordpath=Path(tmp)/'child.json'
   worker=subprocess.run([sys.executable,str(BASE/'supervision.py'),'parent',str(recordpath)],capture_output=True);assert worker.returncode==92
   record=json.loads(recordpath.read_text())
   try:
    assert running(record['pid'])
    s.uncertainty(job)
    # Lease expiry is only recovery inspection; no second claim or unlock.
    assert s.claim() is None;assert not s.finish(job,f,False)
    wrong=dict(record,start='wrong-start-identity');assert not stop_verified(wrong);assert running(record['pid'])
    assert stop_verified(record);assert all(not running(pid) for pid in record['members'])
    assert s.finish(job,f,True);assert s.read('SELECT render_job FROM projects WHERE id=1')[0]['render_job'] is None
    nextjob=s.admit('after-stop',scene=2);assert s.claim()[0]==nextjob;s.audit()
    child_evidence.append({'repeat':repeat,'worker_exit':92,'surviving_group_members':len(record['members']),'identity_mismatch_refused':True,'confirmed_group_exit_before_replacement':True})
   finally:
    if running(record['pid']):stop_verified(record)
 return {'crash_cases':cases,'provider_outcomes':outcomes,'child_supervision':child_evidence,'checks':['no_blind_duplicate_submissions','unknown_holds_and_lane_preserved','late_cancel_result_history_only','fencing_prevents_current_selection','received_bytes_reused','replayed_delivery_charged_once','boot_start_identity_checked','old_group_observed_stopped_before_replacement'],'limitations':['Fake provider has authoritative local receipts for tests; real retrieval/cancel/cost certainty remains S4.','Real process exit/SIGTERM escalation demonstrated locally; target-host supervisor configuration and boot failure require deployment evidence.','Publication metadata and delivery ledger are deliberately one transaction; no false filesystem/DB atomicity claim.']}
if __name__=='__main__':run('S3',experiment)
