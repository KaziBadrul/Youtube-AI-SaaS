"""Disposable S4 SDK wire witness. All HTTP is synthetic; sockets forbidden."""
import os, socket, json, hashlib, sys, time, tempfile
from pathlib import Path
from unittest.mock import patch
os.environ.clear()
def forbidden(*a, **k): raise AssertionError('NETWORK FORBIDDEN')
socket.create_connection = forbidden
socket.getaddrinfo = forbidden
socket.socket.connect = forbidden
import httpx
from google import genai
from google.genai import types
import importlib.metadata
OUT = Path('docs/architecture/evidence/provider-feasibility')
rows=[]
interaction={'id':'synthetic-id','created':'2026-10-04T00:00:00Z','updated':'2026-10-04T00:00:00Z','status':'completed','steps':[], 'usage':{'total_input_tokens':12,'total_output_tokens':25,'total_thought_tokens':3,'output_tokens_by_modality':[{'modality':'image','tokens':25}]}}
generated={'responseId':'synthetic-response','modelVersion':'synthetic-model','candidates':[{'content':{'parts':[{'text':'fixture'}]},'finishReason':'STOP'}], 'usageMetadata':{'promptTokenCount':12,'candidatesTokenCount':25,'thoughtsTokenCount':3,'totalTokenCount':40}}
def run(api, attempts, behavior, expected, timeout=None, guard=False):
    seen=[]; blocked=[]
    with tempfile.TemporaryDirectory() as td:
        receipt=Path(td)/'attempt.json'
        def handle(req):
            if guard and req.method=='POST' and receipt.exists():
                blocked.append(True); raise RuntimeError('Attempt submission already reserved; outcome retained as unknown')
            if guard and req.method=='POST':
                with receipt.open('w') as f:
                    json.dump({'submission_started':True,'liability':'held'},f); f.flush(); os.fsync(f.fileno())
            seen.append({'method':req.method,'path':req.url.path,'timeout':req.extensions.get('timeout'), 'idempotency_header':req.headers.get('idempotency-key'),'body':json.loads(req.content) if req.content else None})
            if behavior=='read_timeout': raise httpx.ReadTimeout('synthetic after possible receipt',request=req)
            if isinstance(behavior,int): return httpx.Response(behavior,json={'error':{'code':behavior,'message':'synthetic','status':'RESOURCE_EXHAUSTED'}},headers={'retry-after':'0.001','x-request-id':'synthetic-request'})
            return httpx.Response(200,json=interaction if api=='interactions' else generated,headers={'x-request-id':'synthetic-request'})
        hc=httpx.Client(transport=httpx.MockTransport(handle),trust_env=False,follow_redirects=False)
        opts={'httpx_client':hc,'timeout':timeout}
        if attempts is not None: opts['retry_options']=types.HttpRetryOptions(attempts=attempts)
        c=genai.Client(vertexai=False,api_key='S4-DUMMY-NOT-A-CREDENTIAL',http_options=types.HttpOptions(**opts))
        result=None; error=None
        with patch('time.sleep',lambda _:None):
            try:
                if api=='interactions': result=c.interactions.create(model='gemini-3.1-flash-image',input='synthetic',response_format={'type':'image','image_size':'1K'},generation_config={'max_output_tokens':128})
                else: result=c.models.generate_content(model='gemini-3.8-flash',contents='synthetic',config=types.GenerateContentConfig(max_output_tokens=128,candidate_count=1,automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)))
            except Exception as e: error=type(e).__name__
        row={'api':api,'configured_attempts':attempts,'behavior':behavior,'timeout_ms':timeout,'guard':guard,'submissions':len(seen),'blocked_reentries':len(blocked),'requests':seen,'error':error,'response':result.model_dump(mode='json',exclude_none=True) if result else None,'expected_submissions':expected,'pass':len(seen)==expected}
        rows.append(row); c.close()
for api, attempts, expected in [('generate',None,1),('generate',1,1),('generate',0,1),('interactions',None,4),('interactions',1,2),('interactions',0,2)]:
    run(api,attempts,429,expected)
for api, expected in [('generate',1),('interactions',2)]:
    run(api,1,'read_timeout',expected,1234)
    run(api,1,400,1)
    run(api,1,'success',1,1234)
    run(api,1,'success',1)
run('interactions',1,'read_timeout',1,1234,True)
run('interactions',1,429,1,1234,True)
# Known result ID: public retrieval path, raw headers. Not proof of real server persistence.
seen=[]
def retrieval(req):
    seen.append({'method':req.method,'path':req.url.path}); return httpx.Response(200,json=interaction,headers={'x-request-id':'synthetic-retrieval'})
hc=httpx.Client(transport=httpx.MockTransport(retrieval),trust_env=False)
c=genai.Client(vertexai=False,api_key='S4-DUMMY',http_options=types.HttpOptions(httpx_client=hc,retry_options=types.HttpRetryOptions(attempts=1)))
raw=c.interactions.with_raw_response.get('synthetic-id'); parsed=raw.parse()
rows.append({'case':'known_id_retrieval','requests':seen,'id':parsed.id,'status':parsed.status,'request_id':raw.headers.get('x-request-id'),'pass':len(seen)==1 and parsed.id=='synthetic-id'})
c.close()
root=Path(genai.__file__).parent
sources={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [root/'client.py',root/'_api_client.py',root/'_interactions/_base_client.py']}
evidence={'scope':'No real network; synthetic SDK transport only','python':sys.version,'versions':{p:importlib.metadata.version(p) for p in ['google-genai','httpx','httpcore','tenacity']},'source_sha256':sources,'cases':rows,'pass':all(r['pass'] for r in rows)}
OUT.mkdir(parents=True,exist_ok=True)
(OUT/'witness.json').write_text(json.dumps(evidence,indent=2)+'\n')
print(json.dumps({'cases':len(rows),'pass':evidence['pass'],'submissions':[r.get('submissions') for r in rows]}))
assert evidence['pass']
