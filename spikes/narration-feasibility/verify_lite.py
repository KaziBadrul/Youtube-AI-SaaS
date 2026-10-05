"""Local-only manifest and SDK wire witness; no live executor or credential loading."""
import os,socket,json,hashlib
from pathlib import Path
os.environ.clear()
def deny(*a,**k):raise AssertionError('NETWORK FORBIDDEN')
socket.create_connection=deny;socket.getaddrinfo=deny;socket.socket.connect=deny
import httpx
from google import genai
from google.genai import types
ROOT=Path(__file__).resolve().parents[2]; evidence=ROOT/'docs/architecture/evidence/narration-feasibility'
m=json.loads((evidence/'real-call-manifest.json').read_text());f=json.loads((evidence/'fixture-manifest.json').read_text());sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha((ROOT/f['source']).read_bytes())==f['source_sha256']
for p,h in f['other_source_hashes'].items():assert sha((ROOT/p).read_bytes())==h
assert sha((ROOT/'demo-video-example/narration.wav').read_bytes())==f['historical_audio']['sha256']
assert len(m['calls'])==8 and m['base_submissions']==8 and m['experiment_max_submissions_including_retries']==10
assert m['base_microUSD']==819200 and m['total_microUSD']==1024000
checks=[]
for call in m['calls']:
 assert call['model']=='gemini-3.8-flash-lite-tts' and call['voice']=='Charon' and not call['live_execution_authorized']
 assert sha(call['text'].encode())==call['input']['sha256'] and len(call['text'].encode())==call['input']['utf8_bytes']
 assert call['delivery_style']==f['alternate_delivery_style' if call['call']==8 else 'delivery_style']
 sends=[]
 def transport(req):
  body=json.loads(req.content);sends.append(body)
  assert req.url.path.endswith('/models/gemini-3.8-flash-lite-tts:generateContent')
  assert body['contents'][0]['parts'][0]['text']==call['text']
  assert body['contents'][0]['parts'][0]['speechMetadata']['style']==call['delivery_style']
  conf=body['generationConfig'];assert conf['maxOutputTokens']==16384 and conf['candidateCount']==1
  assert conf['speechConfig']=={'voice_config':{'prebuilt_voice_config':{'voice_name':'Charon'}}}
  return httpx.Response(429,json={'error':{'code':429,'message':'Synthetic quota error','status':'RESOURCE_EXHAUSTED'}})
 h=httpx.Client(transport=httpx.MockTransport(transport),trust_env=False,follow_redirects=False)
 client=genai.Client(vertexai=False,api_key='S5-DUMMY',http_options=types.HttpOptions(httpx_client=h,retry_options=types.HttpRetryOptions(attempts=1),timeout=1000,extra_body={'contents':[{'role':'user','parts':[{'text':call['text'],'speechMetadata':{'style':call['delivery_style']}}]}]}))
 try:
  client.models.generate_content(model=call['model'],contents=call['text'],config=types.GenerateContentConfig(response_modalities=['AUDIO'],max_output_tokens=16384,candidate_count=1,speech_config=types.SpeechConfig(voice_config=types.VoiceConfig(prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name='Charon'))),automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)))
 except genai.errors.APIError:pass
 else:raise AssertionError('synthetic error missing')
 assert len(sends)==1;client.close();checks.append({'call':call['call'],'fixture_hash_matches':True,'wire_config_matches':True,'synthetic_429_submissions':1})
(evidence/'flash-lite-verification.json').write_text(json.dumps({'status':'PASS_LOCAL_MANIFEST_AND_WIRE_ONLY','checks':checks,'provider_requests':0,'mock_transport_requests':8,'sdk':'google-genai 2.3.0','initial_failure':'Typed Part rejects speech_metadata before submission; retained finding. Public HttpOptions.extra_body carries exact structured metadata in local wire witness; no live schema acceptance proven.','hard_cap_pacing_unknown_outcome_runner_enforcement':'NOT_VERIFIED_NO_LIVE_RUNNER'},indent=2)+'\n')
print('PASS: eight immutable fixture/config checks; eight synthetic 429 cases each exactly one send; zero provider requests.')
