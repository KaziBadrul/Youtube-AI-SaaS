"""Synthetic AUDIO response/usage/config capture; no quality experiment."""
import os,socket,json,base64
from pathlib import Path
os.environ.clear()
def deny(*a,**k): raise AssertionError('NETWORK FORBIDDEN')
socket.create_connection=deny;socket.getaddrinfo=deny;socket.socket.connect=deny
import httpx
from google import genai
from google.genai import types
wire=[]
def transport(r):
 wire.append(json.loads(r.content))
 return httpx.Response(200,json={'responseId':'fake-audio-response','candidates':[{'finishReason':'STOP','content':{'parts':[{'inlineData':{'mimeType':'audio/wav','data':base64.b64encode(b'NOT-REAL-AUDIO').decode()}}]}}],'usageMetadata':{'promptTokenCount':12,'candidatesTokenCount':25,'totalTokenCount':37,'candidatesTokensDetails':[{'modality':'AUDIO','tokenCount':25}]}},headers={'x-request-id':'fake-audio-request'})
h=httpx.Client(transport=httpx.MockTransport(transport),trust_env=False,follow_redirects=False)
c=genai.Client(vertexai=False,api_key='S4-DUMMY',http_options=types.HttpOptions(httpx_client=h,retry_options=types.HttpRetryOptions(attempts=1),timeout=1000))
r=c.models.generate_content(model='gemini-3.8-flash-tts',contents='Synthetic words',config=types.GenerateContentConfig(response_modalities=['AUDIO'],max_output_tokens=128,candidate_count=1,speech_config=types.SpeechConfig(voice_config=types.VoiceConfig(prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name='Charon'))),automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)))
assert len(wire)==1 and wire[0]['generationConfig']['maxOutputTokens']==128
assert r.usage_metadata.candidates_tokens_details[0].token_count==25
assert r.candidates[0].content.parts[0].inline_data.data==b'NOT-REAL-AUDIO'
Path('docs/architecture/evidence/provider-feasibility/tts-wire.json').write_text(json.dumps({'pass':True,'scope':'Synthetic SDK schema only; no server cap compliance/audio validation/quality evidence','requests':wire,'response':r.model_dump(mode='json',exclude_none=True)},indent=2)+'\n')
c.close();print('Synthetic TTS wire/usage capture PASS')
