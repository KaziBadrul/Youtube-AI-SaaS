import multiprocessing as mp,os,statistics,tempfile,time
from core import Store
from fixtures import install_fixture
from evidence import run
CTX=mp.get_context('fork')

def actor(root,action,i,barrier,out,job=None,fence=None):
 try:
  s=Store(root);barrier.wait(timeout=15);start=time.perf_counter()
  if action=='edit':r=s.edit(1,0,f'accepted-{i}')
  elif action=='duplicate_admit':r=s.admit('same-key')
  elif action=='capacity_admit':r=s.admit(f'key-{i}',maximum=3000)
  elif action=='claim':r=s.claim()
  elif action=='register':r=s.register('a')
  elif action=='delete_claim':
   try:r=s.delete(1,100) if i%2 else s.claim()
   except PermissionError:r='already_deleted_denied'
  elif action=='render_edit':r=s.edit(1,0,f'edit-{i}') if i%2 else s.claim()
  elif action=='cancel_select':r=s.cancel(job) if i%2 else s.select('a',fence)
  elif action=='progress':
   times=[]
   for k in range(100):
    begin=time.perf_counter();s.progress(job,f'{i}:{k}');times.append(time.perf_counter()-begin)
   r=times
  else:raise AssertionError(action)
  out.put({'i':i,'result':r,'seconds':time.perf_counter()-start})
 except BaseException as e:out.put({'i':i,'error':repr(e)})

def race(root,action,job=None,fence=None):
 barrier=CTX.Barrier(9);out=CTX.Queue();children=[CTX.Process(target=actor,args=(str(root),action,i,barrier,out,job,fence)) for i in range(8)]
 for p in children:p.start()
 barrier.wait(timeout=15)
 result=[out.get(timeout=30) for _ in children]
 for p in children:p.join(timeout=5);assert p.exitcode==0,p.exitcode
 assert not any('error' in r for r in result),result
 return result

def crash_tx(root,kind):
 s=Store(root)
 with s.tx() as c:
  if kind=='reservation':c.execute('UPDATE account SET held=held+900 WHERE id=1')
  elif kind=='render_lock':c.execute("UPDATE projects SET render_job='incomplete' WHERE id=1")
  elif kind=='edit':c.execute("UPDATE scenes SET words='uncommitted' WHERE id=1")
  os._exit(77)

def experiment():
 results=[];transaction_times=[]
 for repeat in range(20):
  for action in ['edit','duplicate_admit','capacity_admit','claim','register','delete_claim','render_edit','cancel_select']:
   with tempfile.TemporaryDirectory(prefix='alpha-s2-') as tmp:
    s=Store(tmp);s.initialize();job=fence=None
    if action in ['claim','register','delete_claim','render_edit','cancel_select']:
     job=s.admit('job',kind='render' if action=='render_edit' else 'generate')
    if action in ['register','cancel_select']:
     _,fence=s.claim();install_fixture(s,job,fence)
     if action=='cancel_select':s.register('a')
    rows=race(tmp,action,job,fence);r=[x['result'] for x in rows]
    if action=='edit':assert r.count('saved')==1 and r.count('conflict')==7;assert s.read('SELECT words,rev FROM scenes WHERE id=1')[0]['rev']==1
    if action=='duplicate_admit':assert len(set(r))==1;assert s.read('SELECT held FROM account')[0]['held']==100;assert len(s.read('SELECT * FROM jobs'))==1
    if action=='capacity_admit':assert r.count('budget_blocked')==5;assert s.read('SELECT held FROM account')[0]['held']==9000
    if action=='claim':assert sum(x is not None for x in r)==1
    if action=='register':assert len(s.read("SELECT * FROM ledger WHERE kind='delivered'"))==1;assert s.read('SELECT spent,consumed FROM account')[0]=={'spent':100,'consumed':100}
    if action=='delete_claim':
     p=s.read('SELECT * FROM projects WHERE id=1')[0];lane=s.read('SELECT * FROM lane')[0]
     assert not(p['deleted'] is not None and lane['job'])
     if p['deleted'] is not None:assert s.claim() is None
    if action=='render_edit':
     p=s.read('SELECT * FROM projects WHERE id=1')[0];scene=s.read('SELECT * FROM scenes WHERE id=1')[0]
     assert not(p['render_job'] and scene['rev']>0)
     if p['render_job']:
      lane=s.read('SELECT * FROM lane')[0];assert not s.finish(job,lane['fence'],False);assert s.finish(job,lane['fence'],True);assert not s.read('SELECT render_job FROM projects WHERE id=1')[0]['render_job']
    if action=='cancel_select':assert not s.select('a',fence);assert s.read('SELECT words FROM scenes WHERE id=2')[0]['words']=='Sibling approved words.'
    s.audit();results.append({'repeat':repeat,'race':action,'workers':8,'max_seconds':max(x['seconds'] for x in rows),'results':r})
 with tempfile.TemporaryDirectory(prefix='alpha-s2-contention-') as tmp:
  s=Store(tmp);s.initialize();job=s.admit('stress');rows=race(tmp,'progress',job)
  transaction_times=[t for row in rows for t in row['result']];assert len(s.read('SELECT * FROM progress'))==800
  assert max(transaction_times)<5;assert sorted(transaction_times)[int(.99*len(transaction_times))-1]<2;s.audit()
 interrupted=[]
 for kind in ['reservation','render_lock','edit']:
  with tempfile.TemporaryDirectory(prefix='alpha-s2-crash-') as tmp:
   s=Store(tmp);s.initialize();before=[s.read('SELECT * FROM '+t) for t in ['account','projects','scenes']]
   p=CTX.Process(target=crash_tx,args=(tmp,kind));p.start();p.join(5);assert p.exitcode==77
   assert before==[s.read('SELECT * FROM '+t) for t in ['account','projects','scenes']];s.audit();interrupted.append(kind)
 with tempfile.TemporaryDirectory(prefix='alpha-s2-stale-') as tmp:
  s=Store(tmp);s.initialize();job=s.admit('x');_,f=s.claim();install_fixture(s,job,f);s.register('a');s.edit(1,0,'newer words');assert not s.select('a',f)
  # Explicit corruption attempt: selection must reject mismatched project identity.
  with s.tx() as c:c.execute('UPDATE artifacts SET project=2 WHERE id=?',('a',))
  assert not s.select('a',f)
  with s.tx() as c:c.execute('UPDATE artifacts SET project=1 WHERE id=?',('a',))
  assert not s.select('a',f-1);s.audit()
 return {'race_repeats':20,'concurrency':8,'race_families':8,'race_results':results,'contention_transactions':800,'transaction_p50_seconds':statistics.median(transaction_times),'transaction_p99_seconds':sorted(transaction_times)[791],'transaction_max_seconds':max(transaction_times),'interrupted_transactions':interrupted,'checks':['WAL_FULL_foreign_keys','exactly_one_claim','atomic_idempotent_reservation','budget_allowance_integer_limits','autosave_CAS','ledger_replay_once','delete_claim_exclusion','render_lock_edit_exclusion_confirmed_release','cancel_fence_input_project_selection_guards','rollback_on_process_exit'],'limitations':['Tiny local fixtures, 8 concurrent writers; not arbitrary scale or target-host capacity.','The witness uses sqlite3 BEGIN IMMEDIATE, not select_for_update; production ORM/query integration still needs acceptance tests.','Provider calls and media copying are outside all transactions; no real provider or FFmpeg execution.']}
if __name__=='__main__':run('S2',experiment)
