"""Disposable S5 bounded runner. Default dry-run; never imports legacy pipeline."""
import argparse,base64,fcntl,hashlib,io,json,os,re,time,wave
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
EVIDENCE=ROOT/'docs/architecture/evidence/narration-feasibility'
MANIFEST=EVIDENCE/'real-call-manifest.json'
MODEL='gemini-3.8-flash-lite-tts';VOICE='Charon';COST=102400;CEILING=1024000
ENDPOINT=f'https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent'
RUNROOT=EVIDENCE/'runs/approved-lite-v1'
PIN='b65cc790d372bfd7d73f7d77fcbd429df089d5515bb60414b7db0a6cf2d92d63'
FIXTURE_PIN='63f667db388b1b9d9e71e807001b0c8d48ca8c1d53cbeaaf1d7cafe47f773d11'
class GuardError(Exception):pass
class Interruption(BaseException):pass

def sha(data):return hashlib.sha256(data).hexdigest()
def atomic(path,data):
 path.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
 if path.is_symlink() or path.parent.is_symlink():raise GuardError('unsafe storage path')
 tmp=path.with_suffix(path.suffix+'.tmp')
 with open(tmp,'wb') as f:os.chmod(tmp,0o600);f.write(data);f.flush();os.fsync(f.fileno())
 os.replace(tmp,path)
 fd=os.open(path.parent,os.O_RDONLY);os.fsync(fd);os.close(fd)
def dump(path,value):atomic(path,(json.dumps(value,indent=2)+'\n').encode())
def validate_manifest(path=MANIFEST):
 raw=path.read_bytes()
 if sha(raw)!=PIN:raise GuardError('approved manifest changed')
 m=json.loads(raw)
 if len(m['calls'])!=8 or [c['call'] for c in m['calls']]!=list(range(1,9)):raise GuardError('call set changed')
 if (m['base_submissions'],m['experiment_max_submissions_including_retries'],m['base_microUSD'],m['total_microUSD'])!=(8,10,819200,CEILING):raise GuardError('financial/request bound changed')
 fixture_raw=(EVIDENCE/'fixture-manifest.json').read_bytes()
 if sha(fixture_raw)!=FIXTURE_PIN:raise GuardError('fixture inventory changed')
 f=json.loads(fixture_raw)
 if sha((ROOT/f['source']).read_bytes())!=f['source_sha256']:raise GuardError('source changed')
 for p,h in f['other_source_hashes'].items():
  if sha((ROOT/p).read_bytes())!=h:raise GuardError('source changed')
 if sha((ROOT/'demo-video-example/narration.wav').read_bytes())!=f['historical_audio']['sha256']:raise GuardError('audio fixture changed')
 lines=[s.strip() for s in (ROOT/f['source']).read_text().splitlines() if s.strip()]
 edit=lines[19].replace('three weeks','a month',1)
 expected=[lines[18],lines[19],lines[20],'\n\n'.join(lines[:32]),edit,'\n\n'.join(edit if i==19 else t for i,t in enumerate(lines[:32])),'\n\n'.join([lines[18],edit,lines[20]]),lines[19]]
 for c,t in zip(m['calls'],expected):
  if c['text']!=t or sha(t.encode())!=c['input']['sha256'] or len(t.encode())!=c['input']['utf8_bytes']:raise GuardError('fixture changed')
  if c['model']!=MODEL or c['voice']!=VOICE:raise GuardError('model/voice substitution')
  if c['delivery_style']!=f['alternate_delivery_style' if c['call']==8 else 'delivery_style']:raise GuardError('delivery changed')
  if (c['serving_input_token_ceiling'],c['serving_output_token_ceiling'],c['requested_max_output_tokens'],c['max_microUSD'])!=(8192,16384,16384,COST):raise GuardError('bounds changed')
  if c['response_modalities']!=['AUDIO'] or c['candidates']!=1:raise GuardError('configuration changed')
 return m

def body(c):
 return {'contents':[{'role':'user','parts':[{'text':c['text'],'speechMetadata':{'style':c['delivery_style']}}]}], 'generationConfig':{'responseModalities':['AUDIO'],'candidateCount':1,'maxOutputTokens':16384,'speechConfig':{'voiceConfig':{'prebuiltVoiceConfig':{'voiceName':VOICE}}}}}

def audio_from_response(r):
 if len(r.get('candidates',[]))!=1:raise GuardError('missing/multiple audio candidate')
 candidate=r['candidates'][0]
 if candidate.get('finishReason')!='STOP':raise GuardError('incomplete audio response')
 parts=candidate.get('content',{}).get('parts',[])
 audio=[p['inlineData'] for p in parts if 'inlineData' in p and p['inlineData'].get('mimeType') in ('audio/wav','audio/x-wav')]
 if len(audio)!=1:raise GuardError('expected one WAV output')
 data=base64.b64decode(audio[0]['data'],validate=True)
 if len(data)>40_000_000:raise GuardError('audio exceeds bounded storage')
 with wave.open(io.BytesIO(data)) as w:
  frames=w.getnframes();rate=w.getframerate();width=w.getsampwidth();channels=w.getnchannels()
  if w.getcomptype()!='NONE' or not frames or rate<=0 or channels not in (1,2) or width not in (1,2,3,4):raise GuardError('invalid PCM WAV')
  if frames/rate>655.36:raise GuardError('audio exceeds serving-duration envelope')
  if len(w.readframes(frames))!=frames*width*channels:raise GuardError('truncated audio')
 return data,{'frames':frames,'sample_rate':rate,'channels':channels,'sample_width':width,'seconds':frames/rate,'sha256':sha(data)}

class RealTransport:
 """Exactly one POST, no SDK/redirect/retry/tool loop. Construct only after explicit auth."""
 def __init__(self,key):
  import httpx
  if httpx.__version__!='0.28.1':raise GuardError('unverified HTTPX version')
  self.key=key;self.httpx=httpx
 def __call__(self,payload):
  self.last_ids={}
  # Exceptions/messages/bodies/headers are never logged verbatim.
  with self.httpx.Client(transport=self.httpx.HTTPTransport(retries=0),trust_env=False,follow_redirects=False,timeout=self.httpx.Timeout(120,connect=15)) as c:
   with c.stream('POST',ENDPOINT,headers={'x-goog-api-key':self.key,'Content-Type':'application/json'},json=payload) as r:
    self.last_ids={k:v for k,v in r.headers.items() if k.lower() in ('x-request-id','x-goog-request-id','retry-after')}
    pieces=[];size=0;deadline=time.monotonic()+900
    for chunk in r.iter_bytes():
     if time.monotonic()>deadline:raise GuardError('whole-response deadline exceeded')
     size+=len(chunk)
     if size>55_000_000:raise GuardError('response too large')
     pieces.append(chunk)
    raw=b''.join(pieces)
    try:parsed=json.loads(raw)
    except Exception:parsed={}
    headers={k:v for k,v in r.headers.items() if k.lower() in ('x-request-id','x-goog-request-id','retry-after')}
    # Schema rejection stops; 429/transient status is NOT assumed safely unbilled.
    return {'status':r.status_code,'body':parsed,'ids':headers,'safe_failure':False}

def clean(value,secret):
 if isinstance(value,str):return value.replace(secret,'[REDACTED]') if secret else value
 if isinstance(value,list):return [clean(v,secret) for v in value]
 if isinstance(value,dict):return {clean(str(k),secret):clean(v,secret) for k,v in value.items() if str(k).lower() not in ('api_key','apikey','x-goog-api-key','authorization')}
 return value

class Runner:
 def __init__(self,root=RUNROOT,clock=time.time,wait=time.sleep,transport=None,secret='',hook=lambda p:None):
  self.root=Path(root);self.clock=clock;self.wait=wait;self.transport=transport;self.secret=secret;self.hook=hook
  self.m=validate_manifest();self.path=self.root/'ledger.json';self.lock=None
 def __enter__(self):
  if any(p.is_symlink() for p in [self.root,*self.root.parents]):raise GuardError('symlink output ancestry')
  self.root.mkdir(parents=True,exist_ok=True,mode=0o700)
  if self.root.is_symlink():raise GuardError('unsafe storage root')
  self.lock=open(self.root/'runner.lock','a');os.chmod(self.root/'runner.lock',0o600)
  try:fcntl.flock(self.lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
  except BlockingIOError:self.lock.close();raise GuardError('experiment already running')
  if self.path.exists():self.l=json.loads(self.path.read_bytes())
  else:
   if (self.root/'attempts').exists() or (self.root/'audio').exists():raise GuardError('ledger missing beside execution evidence')
   self.l={'manifest_sha256':PIN,'attempts':[],'events':[],'halt':None,'clock_highwater':0}
  if self.l.get('manifest_sha256')!=PIN:raise GuardError('ledger manifest mismatch')
  self.integrity()
  for a in self.l['attempts']:
   if a['state']=='submitting':a['state']='unknown_outcome'
   if a['state']=='unknown_outcome':self.l['halt']='reconciliation_required'
   if a['state']=='succeeded':
    audio=self.root/f"audio/call-{a['call']:02d}/attempt-{a['id']:02d}/source.wav"
    if not audio.exists() or sha(audio.read_bytes())!=a['audio']['sha256']:self.l['halt']='saved_audio_missing_or_changed_no_resubmission'
  self.save();return self
 def __exit__(self,*exc):
  if self.lock:fcntl.flock(self.lock,fcntl.LOCK_UN);self.lock.close()
 def save(self):dump(self.path,clean(self.l,self.secret))
 def integrity(self):
  a=self.l['attempts'];n=len(a);retry=sum(x['kind']=='retry' for x in a);primary=n-retry
  if n>10 or primary>8 or retry>2 or any(x['call'] not in range(1,9) or x['max_microUSD']!=COST for x in a):raise GuardError('ledger limits violated')
  if n*COST>CEILING:raise GuardError('financial ceiling exceeded')
  if len({x['id'] for x in a})!=n:raise GuardError('duplicate attempt identity')
  if len({x['call'] for x in a if x['kind']=='primary'})!=primary:raise GuardError('duplicate primary')
  return n,primary,retry
 def eligible(self):
  now=self.clock()
  if now<self.l['clock_highwater']:raise GuardError('clock moved backward; wait/reconcile')
  # Reserve full 8192 input tokens; one per >=61s respects 10K input TPM and 3 RPM.
  stamps=[a['submitted_at'] for a in self.l['attempts']]
  return max(now,max(stamps,default=now-61)+61)
 def dry(self,stage=1):
  n,p,r=self.integrity();schedule=[];next_at=self.eligible()
  for c in self.m['calls'][:1] if stage==1 else self.m['calls'][1:]:
   if any(a['call']==c['call'] and a['state']=='succeeded' for a in self.l['attempts']):continue
   schedule.append({'call':c['call'],'model':MODEL,'voice':VOICE,'input_bytes':c['input']['utf8_bytes'],'style_bytes':c['delivery_utf8_bytes'],'fixture_sha256':c['input']['sha256'],'eligible_at':next_at,'output':str(self.root/f"audio/call-{c['call']:02d}")});next_at+=61
  result={'mode':'DRY_RUN','provider_submissions':0,'stage':stage,'calls':schedule,'persisted_submission_count':n,'remaining_primary_slots':8-p,'remaining_retry_slots':2-r,'remaining_total_slots':10-n,'maximum_remaining_tariff_microUSD':CEILING-n*COST,'halt':self.l['halt'],'stage2_requires_separate_authorization':True,'output_root':str(self.root)}
  dump(self.root/'dry-run.json',result);return result
 def execute(self,stage,authorization,fee_microUSD=0):
  try:return self._execute(stage,authorization,fee_microUSD)
  except GuardError:
   self.l['events'].append({'state':'rejected_locally','at':self.clock(),'stage':stage});self.save();raise
 def _execute(self,stage,authorization,fee_microUSD=0):
  if stage not in (1,2):raise GuardError('invalid stage')
  if authorization!=('AUTHORIZE_S5_LITE_CALL_1' if stage==1 else 'AUTHORIZE_S5_LITE_CALLS_2_8'):raise GuardError('explicit stage authorization required')
  if fee_microUSD!=0:raise GuardError('fees need separate reservation/owner decision')
  if not self.transport:raise GuardError('no transport')
  if stage==2 and not any(a['call']==1 and a['state']=='succeeded' for a in self.l['attempts']):raise GuardError('Call 1 not validated')
  if self.l['halt']:raise GuardError('experiment halted; reconciliation/owner decision required')
  for c in self.m['calls'][:1] if stage==1 else self.m['calls'][1:]:
   previous=[a for a in self.l['attempts'] if a['call']==c['call']]
   if any(a['state']=='succeeded' for a in previous):continue
   if previous and (previous[-1]['state']!='definite_failure' or not previous[-1]['safe_retry']):raise GuardError('call not safely retryable')
   validate_manifest();self.integrity()
   kind='retry' if previous else 'primary'
   n,p,r=self.integrity()
   if n>=10 or (kind=='primary' and p>=8) or (kind=='retry' and r>=2):raise GuardError('submission limit reached')
   if (n+1)*COST>CEILING:raise GuardError('financial limit reached')
   at=self.eligible();self.wait(max(0,at-self.clock()))
   if self.clock()<at:raise GuardError('pacing violation')
   self.l['events'].append({'state':'prepared','call':c['call'],'at':self.clock()});self.save();self.hook('before_intent')
   a={'id':n+1,'call':c['call'],'kind':kind,'state':'submitting','submitted_at':self.clock(),'max_microUSD':COST,'safe_retry':False,'fixture_sha256':c['input']['sha256']}
   self.l['attempts'].append(a);self.l['clock_highwater']=self.clock();self.save();self.hook('after_intent')
   try:
    response=self.transport(body(c));self.hook('after_response')
    status=response['status'];data=response.get('body',{})
    a['http_status']=status;a['provider_ids']=clean(response.get('ids',{}),self.secret)
    if isinstance(data,dict):
     a['response_id']=clean(data.get('responseId'),self.secret);a['usage_metadata']=clean(data.get('usageMetadata'),self.secret)
    dump(self.root/f"attempts/attempt-{a['id']:02d}-receipt.json",clean(response,self.secret))
    if status!=200:
     if status in (400,404,405,422):
      a['state']='definite_failure';a['category']='schema_model_endpoint_rejection';self.l['halt']='schema_rejection_no_variation_retry'
     elif response.get('safe_failure') and not isinstance(self.transport,RealTransport):
      # Fixture simulates independently confirmed non-execution, not a live 429 policy.
      a['state']='definite_failure';a['safe_retry']=True;a['category']='confirmed_safe_fixture_failure'
     else:a['state']='unknown_outcome';self.l['halt']='reconciliation_required'
     self.save();return {'stopped':True,'state':a['state'],'attempt':a['id']}
    try:
     audio,meta=audio_from_response(data)
     atomic(self.root/f"audio/call-{c['call']:02d}/attempt-{a['id']:02d}/source.wav",audio)
     a['audio']=meta;a['state']='succeeded'
    except Exception:
     a['state']='definite_failure';a['category']='received_but_invalid_audio';self.l['halt']='audio_validation_failed_reuse_receipt_no_retry'
    self.save()
    if self.l['halt']:return {'stopped':True,'state':a['state']}
   except Exception:
    a['provider_ids']=clean(getattr(self.transport,'last_ids',{}),self.secret)
    a['state']='unknown_outcome';a['category']='transport_or_local_persistence_uncertainty';self.l['halt']='reconciliation_required';self.save();return {'stopped':True,'state':'unknown_outcome'}
  return {'stage':stage,'complete':True,'next':'STOP; separate stage-2 authorization required' if stage==1 else 'STOP; human evaluation required'}

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--stage',type=int,choices=(1,2),default=1);parser.add_argument('--live-authorization');parser.add_argument('--applicable-fee-microusd',type=int,default=0);args=parser.parse_args()
 try:
  with Runner() as r:
   if not args.live_authorization:print(json.dumps(r.dry(args.stage),indent=2));return
   expected='AUTHORIZE_S5_LITE_CALL_1' if args.stage==1 else 'AUTHORIZE_S5_LITE_CALLS_2_8'
   if args.live_authorization!=expected:raise GuardError('wrong stage authorization')
   # Key is read ONLY here, after explicit token, never exported or logged.
   entries=[line.split('=',1)[1].strip().strip('\"\'') for line in (ROOT/'.env').read_text().splitlines() if line.strip().startswith('GEMINI_API_KEY=')]
   if len(entries)!=1 or not entries[0]:raise GuardError('key unavailable')
   r.secret=entries[0];r.transport=RealTransport(r.secret)
   print(json.dumps(r.execute(args.stage,args.live_authorization,args.applicable_fee_microusd)))
 except Exception:
  if not any(p.is_symlink() for p in [RUNROOT,*RUNROOT.parents]):dump(RUNROOT/'rejected-locally.json',{'state':'rejected_locally','message':'Guard/setup failure; inspect approved local evidence. No secret exception details retained.'})
  print('S5 stopped: local guard/setup failure; no exception details logged.');raise SystemExit(1)
if __name__=='__main__':main()
