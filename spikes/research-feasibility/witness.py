"""S4-R disposable bounded research witness. Synthetic HTTP and content only."""
import os,socket,json,sqlite3,tempfile,hashlib,sys
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal,ROUND_CEILING
from urllib.parse import urlsplit
os.environ.clear()
def deny(*a,**k):raise AssertionError('NETWORK FORBIDDEN')
socket.create_connection=deny;socket.getaddrinfo=deny;socket.socket.connect=deny
import httpx
import importlib.metadata
OUT=Path('docs/architecture/evidence/research-feasibility')
SEARCH_RATE=8000 # microUSD/credit; conservative PAYGO tariff, no free discount
BODY_MAX=32768;RESULT_MAX=3;SNIPPET_MAX=1500;EVIDENCE_MAX=20000
results=[]
class Refused(Exception):pass

def validate_plan(obj,n):
 if type(obj)!=dict or set(obj)!={'queries'} or type(obj['queries'])!=list or not 1<=len(obj['queries'])<=n:raise Refused('invalid bounded plan')
 q=obj['queries']
 if any(type(x)!=str or not x.strip() or len(x.encode())>400 or len(x.split())>50 for x in q):raise Refused('invalid query')
 if len({x.strip().casefold() for x in q})!=len(q):raise Refused('duplicate query')
 return [x.strip() for x in q]

def trim(s,b):return str(s).encode()[:b].decode(errors='ignore')
class Store:
 def __init__(self,path,n,queries=None,quota=1000):
  self.db=sqlite3.connect(path);self.db.row_factory=sqlite3.Row
  self.db.executescript('CREATE TABLE IF NOT EXISTS policy(id INTEGER PRIMARY KEY,n INTEGER,quota INTEGER,queries TEXT); CREATE TABLE IF NOT EXISTS attempts(id TEXT PRIMARY KEY,op INTEGER,state TEXT,held INTEGER,credits INTEGER,receipt TEXT); CREATE TABLE IF NOT EXISTS evidence(id TEXT PRIMARY KEY,attempt TEXT,body TEXT);')
  if not self.db.execute('SELECT 1 FROM policy').fetchone():
   self.db.execute('INSERT INTO policy VALUES(1,?,?,?)',(n,quota,json.dumps(validate_plan(queries,n))));self.db.commit()
 def begin(self,op,aid):
  self.db.execute('BEGIN IMMEDIATE')
  try:
   p=self.db.execute('SELECT * FROM policy').fetchone()
   if self.db.execute('SELECT 1 FROM attempts WHERE id=?',(aid,)).fetchone():raise Refused('duplicate attempt')
   if self.db.execute("SELECT 1 FROM attempts WHERE state IN ('started','unknown')").fetchone():raise Refused('unknown lane')
   q=json.loads(p['queries'])
   if type(op)!=int or not 0<=op<len(q):raise Refused('operation not planned')
   old=list(self.db.execute('SELECT * FROM attempts WHERE op=?',(op,)))
   if len(old)>=3 or any(a['state']!='known_zero_submission' for a in old):raise Refused('unsafe/exhausted retry')
   if p['quota']<1:raise Refused('quota hold unavailable')
   self.db.execute('UPDATE policy SET quota=quota-1')
   self.db.execute('INSERT INTO attempts VALUES(?,?,?,?,?,NULL)',(aid,op,'prepared',SEARCH_RATE,1));self.db.commit();return q[op]
  except BaseException:self.db.rollback();raise
 def state(self,aid,state,receipt=None):
  self.db.execute('UPDATE attempts SET state=?,receipt=? WHERE id=?',(state,json.dumps(receipt) if receipt is not None else None,aid));self.db.commit()
 def zero(self,aid):
  self.db.execute('BEGIN IMMEDIATE')
  row=self.db.execute('SELECT * FROM attempts WHERE id=?',(aid,)).fetchone()
  assert row['state']=='prepared'
  self.db.execute("UPDATE attempts SET state='known_zero_submission',held=0,credits=0 WHERE id=?",(aid,));self.db.execute('UPDATE policy SET quota=quota+1');self.db.commit()
 def dump(self):return {t:[dict(x) for x in self.db.execute('SELECT * FROM '+t)] for t in ['policy','attempts','evidence']}
 def close(self):self.db.close()

def normalize(store,aid,query,data):
 if data.get('query')!=query:raise Refused('returned query differs')
 items=data.get('results')
 if type(items)!=list:raise Refused('invalid results')
 ev=[]
 for i,r in enumerate(items[:RESULT_MAX]):
  if type(r)!=dict or type(r.get('url'))!=str or type(r.get('content'))!=str or type(r.get('title'))!=str:raise Refused('invalid evidence')
  u=urlsplit(r['url'])
  if u.scheme not in ['http','https'] or not u.hostname or u.username or len(r['url'].encode())>2048:raise Refused('invalid source URL')
  e={'id':aid+':'+str(i),'query':query,'url':r['url'],'title':trim(r['title'],256),'snippet':trim(r['content'],SNIPPET_MAX),'retrieved_at':datetime.now(timezone.utc).isoformat(),'provider':'Tavily Search basic','provider_request_id':data.get('request_id'),'attempt_id':aid,'partial':len(items)>RESULT_MAX or len(r['content'].encode())>SNIPPET_MAX}
  ev.append(e)
 if len(json.dumps(ev).encode())>EVIDENCE_MAX:raise Refused('evidence budget')
 for e in ev:store.db.execute('INSERT OR IGNORE INTO evidence VALUES(?,?,?)',(e['id'],aid,json.dumps(e)))
 store.db.commit();return ev

def search(store,op,aid,behavior='success',preflight=False):
 query=store.begin(op,aid);sends=[]
 if preflight:
  store.zero(aid);return {'sends':[],'state':'known_zero_submission'}
 store.state(aid,'started') # Durable before leaving transaction; never span HTTP.
 def fake(req):
  assert not store.db.in_transaction
  body=json.loads(req.content);sends.append({'method':req.method,'url':str(req.url),'body':body})
  if behavior=='timeout':raise httpx.ReadTimeout('possible receipt; unknown',request=req)
  if type(behavior)==int:return httpx.Response(behavior,json={'error':'synthetic'},headers={'retry-after':'1'})
  if behavior=='redirect':return httpx.Response(307,headers={'location':'https://unexpected.invalid/search'})
  d={'query':query,'request_id':'synthetic-'+aid,'usage':{'credits':1},'results':[{'title':'Fixture title','url':'https://example.org/source/'+str(i),'content':'Fixture evidence, not a verified fact. '*70} for i in range(6)]}
  if behavior=='missing_usage':d.pop('usage')
  if behavior=='bad_query':d['query']='injected'
  if behavior=='bad_url':d['results'][0]['url']='file:///etc/passwd'
  if behavior=='overcharge':d['usage']['credits']=2
  if behavior=='oversize':return httpx.Response(200,stream=httpx.ByteStream(b'x'*(BODY_MAX+1)))
  return httpx.Response(200,json=d)
 hc=httpx.Client(transport=httpx.MockTransport(fake),timeout=5,trust_env=False,follow_redirects=False)
 try:
  with hc.stream('POST','https://api.tavily.com/search',headers={'Authorization':'Bearer S4-R-DUMMY'},json={'query':query,'search_depth':'basic','auto_parameters':False,'max_results':RESULT_MAX,'chunks_per_source':3,'topic':'general','include_answer':False,'include_raw_content':False,'include_images':False,'include_usage':True}) as resp:
   if resp.status_code!=200:raise Refused('HTTP outcome requires classification/reconciliation')
   buf=bytearray()
   for part in resp.iter_bytes(chunk_size=1024):
    buf.extend(part)
    if len(buf)>BODY_MAX:raise Refused('response byte budget exceeded')
   d=json.loads(buf)
   # Capture receipt before result validation; invalid content never means zero spending.
   store.state(aid,'received',{'request_id':d.get('request_id'),'usage':d.get('usage'),'sha256':hashlib.sha256(buf).hexdigest()})
   ev=normalize(store,aid,query,d)
   observed=d.get('usage',{}).get('credits')
   if type(observed)==int and observed>1:
    store.db.execute('UPDATE attempts SET held=?,credits=? WHERE id=?',(observed*SEARCH_RATE,observed,aid));store.db.execute('UPDATE policy SET quota=quota-?',(observed-1,));store.db.commit() # Contract violation: visible increased exposure, never expanded authority.
   if observed!=1:raise Refused('missing or unexpected credit usage')
   store.state(aid,'complete',{'request_id':d['request_id'],'usage':d['usage'],'invoice_actual_microUSD':None})
   return {'sends':sends,'state':'complete','evidence':ev}
 except (httpx.HTTPError,Refused,ValueError):
  store.state(aid,'unknown');return {'sends':sends,'state':'unknown'}
 finally:hc.close()

def validate_check(obj,known,script):
 if 'script' in obj:raise Refused('checker cannot overwrite words')
 for w in obj.get('warnings',[]):
  if set(w.get('evidence_ids',[]))-set(known):raise Refused('citation not retrieved')
 return {'warnings':obj.get('warnings',[]),'original_script':script,'proposed_changes':obj.get('proposed_changes',[]),'requires_creator_approval':bool(obj.get('proposed_changes'))}

def expect_refused(fn):
 try:fn()
 except Refused:return
 raise AssertionError('expected refusal')

for obj in [{'queries':['q']*5},{'queries':[]},{'queries':['Q','q']},{'queries':['x'*401]},{'queries':['q'],'max_queries':99},{'queries':[4]}]:
 expect_refused(lambda:validate_plan(obj,4))
results.append({'case':'planner_adversarial','pass':True,'rejected_plans':6,'provider_submissions':0})
for n in [2,4,8]:
 with tempfile.TemporaryDirectory() as td:
  s=Store(Path(td)/'db',n,{'queries':['query '+str(i) for i in range(n)]});sends=0
  for op in range(n):
   for retry in range(2):search(s,op,f'{op}-{retry}',preflight=True)
   r=search(s,op,f'{op}-2');sends+=len(r['sends']);assert r['state']=='complete'
   expect_refused(lambda:search(s,op,f'{op}-3'));expect_refused(lambda:search(s,op,f'{op}-2'))
  expect_refused(lambda:search(s,n,'outside-plan'))
  dump=s.dump();assert len(dump['attempts'])==3*n and sends==n and len(dump['evidence'])==RESULT_MAX*n
  s.close();s=Store(Path(td)/'db',999)
  expect_refused(lambda:search(s,0,'restart-retry'))
  results.append({'case':'bounded_plan_and_recovery','N':n,'attempts':3*n,'remote_submissions':sends,'upper_submission_bound':3*n,'evidence_count':len(dump['evidence']),'persisted_policy_survives_restart':s.dump()['policy'][0]['n']==n,'pass':True});s.close()
for behavior in ['timeout',429,500,432,'redirect','oversize','missing_usage','bad_query','bad_url','overcharge']:
 with tempfile.TemporaryDirectory() as td:
  s=Store(Path(td)/'db',2,{'queries':['query 0','query 1']})
  search(s,0,'prior-success');r=search(s,1,'uncertain',behavior)
  assert r['state']=='unknown' and len(r['sends'])==1
  s.close();s=Store(Path(td)/'db',2)
  expect_refused(lambda:search(s,1,'blind-retry'))
  d=s.dump();u=d['attempts'][1];assert u['held']==SEARCH_RATE*(2 if behavior=='overcharge' else 1) and u['credits']==(2 if behavior=='overcharge' else 1) and len(d['evidence'])>=3
  results.append({'case':'uncertain_no_retry','behavior':behavior,'submissions':1,'held_microUSD':u['held'],'held_credit':u['credits'],'previous_evidence_preserved':True,'pass':True});s.close()
with tempfile.TemporaryDirectory() as td:
 s=Store(Path(td)/'db',2,{'queries':['q']},quota=0);expect_refused(lambda:search(s,0,'quota'));assert not s.dump()['attempts'];s.close()
results.append({'case':'quota_admission','submissions':0,'pass':True})
script='Original approved script words.'
expect_refused(lambda:validate_check({'warnings':[{'evidence_ids':['invented-id']}]},['retrieved-id'],script))
expect_refused(lambda:validate_check({'script':'rewritten'},[],script))
r=validate_check({'warnings':[{'evidence_ids':['retrieved-id'],'text':'Claim needs review'}],'proposed_changes':['Suggestion only']},['retrieved-id'],script)
assert r['original_script']==script and r['requires_creator_approval']
results.append({'case':'citation_link_and_script_preservation','result':r,'pass':True})
# Integer examples: full serving input fallback vs tighter independently validated budgets.
def text_cost(i,o):return int((Decimal(i)*Decimal('.3')+Decimal(o)*Decimal('2.5')).to_integral_value(rounding=ROUND_CEILING))
economics=[]
for n in [2,4,8]:
 planning=text_cost(1048576,1024);synthesis=text_cost(1048576,4096)
 tight_plan=text_cost(8192,1024);tight_synth=text_cost(16384,4096)
 economics.append({'N':n,'search_initial_microUSD':n*8000,'search_three_attempt_microUSD':3*n*8000,'total_full_input_fallback_three_attempt_microUSD':3*planning+3*synthesis+3*n*8000,'total_tighter_validated_input_three_attempt_microUSD':3*tight_plan+3*tight_synth+3*n*8000,'free_1000_credit_projects_initial':1000//n,'free_1000_credit_projects_worst_search':1000//(3*n),'tighter_budget_is_conditional_not_tokenization_verified':True})
source=Path(httpx.__file__).parent/'_transports/default.py'
assert 'retries: int = 0' in source.read_text()
evidence={'scope':'Synthetic research only; no quality/provider/account evidence','python':sys.version,'httpx':importlib.metadata.version('httpx'),'httpx_transport_source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'cases':results,'economics':economics,'pass':all(x['pass'] for x in results),'live_calls':0}
OUT.mkdir(parents=True,exist_ok=True);(OUT/'witness.json').write_text(json.dumps(evidence,indent=2)+'\n')
print(json.dumps({'pass':evidence['pass'],'cases':len(results),'economic_examples':economics}))
assert evidence['pass']
