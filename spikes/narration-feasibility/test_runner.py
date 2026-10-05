"""Deterministic local-only S5 safety witnesses. No credentials or provider requests."""
import base64,io,json,socket,tempfile,wave
from pathlib import Path
from unittest.mock import patch
import runner as s

def deny(*a,**k):raise AssertionError('NETWORK FORBIDDEN')
socket.getaddrinfo=deny;socket.socket.connect=deny;socket.create_connection=deny
class Clock:
 def __init__(self):self.t=1000
 def now(self):return self.t
 def wait(self,n):self.t+=n

def response():
 b=io.BytesIO()
 with wave.open(b,'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(24000);w.writeframes(b'\0\0'*2400)
 return {'status':200,'body':{'responseId':'fake-response','candidates':[{'finishReason':'STOP','content':{'parts':[{'inlineData':{'mimeType':'audio/wav','data':base64.b64encode(b.getvalue()).decode()}}]}}],'usageMetadata':{'promptTokenCount':12,'candidatesTokenCount':3}},'ids':{'x-request-id':'fake-request'}}
class Fake:
 def __init__(self,sequence=()):self.sequence=list(sequence);self.calls=[]
 def __call__(self,body):
  self.calls.append(body)
  if not self.sequence:return response()
  r=self.sequence.pop(0)
  if isinstance(r,Exception):raise r
  return r
safe={'status':429,'body':{'error':{'message':'fixture independently confirms no execution'}},'ids':{'x-request-id':'fake-429'},'safe_failure':True}
A1='AUTHORIZE_S5_LITE_CALL_1';A2='AUTHORIZE_S5_LITE_CALLS_2_8'
results=[]
def run_case(name,test):
 with tempfile.TemporaryDirectory(prefix='s5-witness-') as tmp:
  c=Clock();f=Fake();root=Path(tmp).resolve()/'run'
  def make(**kwargs):return s.Runner(root,c.now,c.wait,kwargs.pop('transport',f),**kwargs)
  test(root,c,f,make)
  if (root/'ledger.json').exists():
   ledger=json.loads((root/'ledger.json').read_text());assert len(ledger['attempts'])<=10
  assert len(f.calls)<=10
  results.append({'case':name,'PASS':True,'fake_submissions':len(f.calls)})
def all_success(root,c,f,make):
 with make() as r:
  assert r.dry()['provider_submissions']==0 and not f.calls
  assert r.execute(1,A1)['complete'];assert len(f.calls)==1
 with make() as r:assert r.execute(2,A2)['complete'];assert len(f.calls)==8
 with make() as r:r.execute(1,A1);r.execute(2,A2);assert len(f.calls)==8
run_case('eight successes; default dry-run; staged continuation; duplicate invocation idempotent',all_success)
def retries(root,c,f,make):
 f.sequence=[safe,safe,response()]
 for _ in range(3):
  with make() as r:r.execute(1,A1)
 with make() as r:r.execute(2,A2);assert r.integrity()==(10,8,2)
 with make() as r:r.execute(2,A2);assert len(f.calls)==10
 with make() as r:
  r.l['attempts'][-1]['state']='definite_failure';r.l['attempts'][-1]['safe_retry']=True;r.save()
 with make() as r:
  try:r.execute(2,A2)
  except s.GuardError:pass
  else:raise AssertionError('eleventh submission allowed')
 assert len(f.calls)==10
run_case('confirmed safe fixture 429 retries; absolute ten submissions; resume preserves counters',retries)
def exhaustion(root,c,f,make):
 f.sequence=[safe,safe,safe]
 for _ in range(3):
  with make() as r:r.execute(1,A1)
 with make() as r:
  try:r.execute(1,A1)
  except s.GuardError:pass
  else:raise AssertionError('retry cap absent')
 assert len(f.calls)==3
run_case('two-retry budget exhausted stops third retry',exhaustion)
def unknown(root,c,f,make):
 f.sequence=[TimeoutError('secret-in-exception')];f.last_ids={'x-request-id':'known-before-timeout'}
 with make() as r:assert r.execute(1,A1)['state']=='unknown_outcome';assert r.l['attempts'][0]['max_microUSD']==s.COST;assert r.l['attempts'][0]['provider_ids']['x-request-id']=='known-before-timeout'
 with make() as r:
  try:r.execute(1,A1)
  except s.GuardError:pass
  else:raise AssertionError('unknown retry admitted')
 assert len(f.calls)==1
run_case('timeout unknown holds liability and halts restart',unknown)
def interrupt(root,c,f,make,point):
 def hook(p):
  if p==point:raise s.Interruption()
 try:
  with make(hook=hook) as r:r.execute(1,A1)
 except s.Interruption:pass
 with make() as r:
  if point=='before_intent':r.execute(1,A1);assert len(f.calls)==1
  else:
   assert r.l['halt']=='reconciliation_required'
   try:r.execute(1,A1)
   except s.GuardError:pass
   else:raise AssertionError('interrupted request retried')
for point in ['before_intent','after_intent','after_response']:
 run_case('interruption '+point,lambda *a,p=point:interrupt(*a,p))
def concurrent(root,c,f,make):
 with make() as r:
  try:
   with make():pass
  except s.GuardError:pass
  else:raise AssertionError('duplicate runner lock absent')
run_case('concurrent runner denied by process lock',concurrent)
def partial(root,c,f,make):
 f.sequence=[response(),response(),safe]
 with make() as r:r.execute(1,A1)
 with make() as r:r.execute(2,A2)
 with make() as r:r.execute(2,A2)
 assert len(f.calls)==9
 assert [a['call'] for a in json.loads((root/'ledger.json').read_text())['attempts']]==[1,2,3,3,4,5,6,7,8]
run_case('resume partial success skips completed audio',partial)
def mutated(root,c,f,make,kind):
 m=json.loads(s.MANIFEST.read_text())
 if kind=='text':m['calls'][0]['text']='Changed'
 if kind=='model':m['calls'][0]['model']='gemini-other'
 if kind=='voice':m['calls'][0]['voice']='Puck'
 if kind=='money':m['total_microUSD']=s.CEILING+1
 p=root.parent/'changed.json';p.write_text(json.dumps(m))
 try:s.validate_manifest(p)
 except s.GuardError:pass
 else:raise AssertionError('tamper accepted')
 assert not f.calls
for kind in ['text','model','voice','money']:run_case('sealed manifest rejects '+kind,lambda *a,k=kind:mutated(*a,k))
def invalid(root,c,f,make):
 f.sequence=[{'status':200,'body':{'candidates':[]},'ids':{}}]
 with make() as r:r.execute(1,A1);assert r.l['halt'];assert r.l['attempts'][0]['state']!='succeeded'
 with make() as r:
  try:r.execute(1,A1)
  except s.GuardError:pass
  else:raise AssertionError('invalid audio retried')
run_case('missing audio stops; receipt retained; no technical success',invalid)
def badwav(root,c,f,make):
 r=response();r['body']['candidates'][0]['content']['parts'][0]['inlineData']['data']=base64.b64encode(b'bad WAV').decode();f.sequence=[r]
 with make() as r:r.execute(1,A1);assert r.l['halt']
run_case('undecodable audio stops',badwav)
def schema(root,c,f,make):
 f.sequence=[{'status':400,'body':{'error':{'message':'schema rejected'}},'ids':{'x-request-id':'schema-id'}}]
 with make() as r:r.execute(1,A1);assert r.l['halt']=='schema_rejection_no_variation_retry'
 with make() as r:
  try:r.execute(2,A2)
  except s.GuardError:pass
  else:raise AssertionError('schema rejection continued')
 assert len(f.calls)==1
run_case('Call 1 schema rejection prevents further calls and schema variants',schema)
def raw429(root,c,f,make):
 f.sequence=[{'status':429,'body':{},'ids':{}}]
 with make() as r:r.execute(1,A1);assert r.l['halt']=='reconciliation_required'
run_case('unconfirmed live-style 429 is not assumed unbilled',raw429)
def redact(root,c,f,make):
 secret='SYNTHETIC-SECRET';r=response();r['ids']={'x-request-id':secret,'authorization':secret};r['body']['responseId']=secret;f.sequence=[r]
 with make(secret=secret) as r:r.execute(1,A1)
 for p in root.rglob('*.json'):assert secret not in p.read_text()
run_case('secret redaction in receipts and ledger',redact)
def pace(root,c,f,make):
 with make() as r:r.execute(1,A1)
 with make() as r:r.execute(2,A2);times=[a['submitted_at'] for a in r.l['attempts']];assert all(b-a>=61 for a,b in zip(times,times[1:]));assert all(sum(t>=x and t<x+60 for t in times)<=1 for x in times)
run_case('fake clock enforces RPM and conservative 8192-token TPM reserve',pace)
def fee(root,c,f,make):
 with make() as r:
  try:r.execute(1,A1,fee_microUSD=1)
  except s.GuardError:pass
  else:raise AssertionError('fees enlarged authority')
 assert not f.calls
run_case('fees cannot silently enlarge reservation',fee)
def stage(root,c,f,make):
 with make() as r:
  for stage,token in [(2,A2),(1,A2),(1,'')]:
   try:r.execute(stage,token)
   except s.GuardError:pass
   else:raise AssertionError('stage authority bypass')
 assert not f.calls
run_case('stage2 prerequisite and distinct authorization enforced',stage)
def transport_wire(root,c,f,make):
 import httpx
 wire=[]
 def endpoint(request):
  wire.append(json.loads(request.content));f.calls.append(wire[-1])
  assert str(request.url)==s.ENDPOINT
  assert request.headers['x-goog-api-key']=='SYNTHETIC-ONLY'
  assert wire[-1]['generationConfig']['speechConfig']=={'voiceConfig':{'prebuiltVoiceConfig':{'voiceName':'Charon'}}}
  return httpx.Response(429,json={'error':{'code':429,'message':'synthetic'}})
 def no_retry_transport(**kwargs):
  assert kwargs=={'retries':0};return httpx.MockTransport(endpoint)
 with patch('httpx.HTTPTransport',no_retry_transport):
  t=s.RealTransport('SYNTHETIC-ONLY')
  with make(transport=t,secret='SYNTHETIC-ONLY') as r:r.execute(1,A1);assert r.l['halt']=='reconciliation_required'
 assert len(wire)==1
run_case('actual HTTPX public transport path: one POST, camelCase REST schema, synthetic 429 no retry',transport_wire)
def financial_independent(root,c,f,make):
 with make() as r:
  with patch.object(s,'CEILING',0):
   try:r.execute(1,A1)
   except s.GuardError:pass
   else:raise AssertionError('ceiling not checked')
 assert not f.calls
run_case('independent financial admission check before submission',financial_independent)
def lost_audio(root,c,f,make):
 with make() as r:r.execute(1,A1)
 next(root.rglob('source.wav')).unlink()
 with make() as r:
  assert r.l['halt']=='saved_audio_missing_or_changed_no_resubmission'
  try:r.execute(1,A1)
  except s.GuardError:pass
  else:raise AssertionError('missing saved audio caused resend')
 assert len(f.calls)==1
run_case('saved audio missing on restart halts without repeat generation',lost_audio)
def backwards(root,c,f,make):
 with make() as r:r.execute(1,A1)
 c.t-=1
 with make() as r:
  try:r.execute(2,A2)
  except s.GuardError:pass
  else:raise AssertionError('backward clock bypass')
 assert len(f.calls)==1
run_case('clock rollback cannot bypass persisted pacing',backwards)
def no_day_reset(root,c,f,make):
 f.sequence=[safe,safe,response()]
 for _ in range(3):
  with make() as r:r.execute(1,A1)
 with make() as r:r.execute(2,A2)
 c.t+=86400
 with make() as r:
  assert r.integrity()==(10,8,2);assert r.dry()['remaining_total_slots']==0
 assert len(f.calls)==10
run_case('new calendar day never resets experiment budget or quota counters',no_day_reset)
def ledger_deleted(root,c,f,make):
 with make() as r:r.execute(1,A1)
 (root/'ledger.json').unlink()
 try:
  with make():pass
 except s.GuardError:pass
 else:raise AssertionError('lost ledger restarted experiment')
 assert len(f.calls)==1
run_case('missing ledger with execution evidence blocks reset/resubmit',ledger_deleted)
s.dump(s.EVIDENCE/'runner-verification.json',{'status':'PASS_LOCAL_ONLY','cases':results,'real_provider_requests':0,'max_fake_submissions_any_case':max(x['fake_submissions'] for x in results),'server_acceptance':'UNPROVEN'})
print(json.dumps({'PASS_cases':len(results),'real_requests':0,'maximum_fake_submissions':max(x['fake_submissions'] for x in results)},indent=2))
