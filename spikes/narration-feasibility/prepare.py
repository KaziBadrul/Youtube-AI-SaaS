"""S5 offline preparation. Standard library only; never imports a provider client."""
import hashlib,json,math,re,socket,wave,array
from score_alignment import score
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/architecture/evidence/narration-feasibility'
def sha(data): return hashlib.sha256(data).hexdigest()
def words(t): return re.findall(r"\b[\w’'-]+\b",t)
def metrics(t):
 return {'words':len(words(t)),'characters':len(t),'utf8_bytes':len(t.encode()),'token_proxy_ceil_chars_div4':math.ceil(len(t)/4),'sha256':sha(t.encode())}
def groups(scenes,byte_cap):
 result=[]; batch=[]
 for s in scenes:
  if len(s['text'].encode())>byte_cap: raise ValueError('explicit oversized-scene plan required')
  proposed='\n\n'.join(x['text'] for x in batch+[s])
  if len(proposed.encode())>byte_cap and batch: result.append(batch);batch=[]
  batch.append(s)
 if batch: result.append(batch)
 return result

def run():
 socket.socket.connect=lambda *a,**k: (_ for _ in ()).throw(AssertionError('network forbidden'))
 socket.getaddrinfo=lambda *a,**k: (_ for _ in ()).throw(AssertionError('DNS forbidden'))
 src=ROOT/'demo-video-example/script.txt'
 lines=[s.strip() for s in src.read_text().splitlines() if s.strip()]
 scenes=[{'id':i,'text':s,'metrics':metrics(s)} for i,s in enumerate(lines,1)]
 original=scenes[19]['text']; assert 'three weeks' in original
 edited=original.replace('three weeks','a month',1)
 block='\n\n'.join(s['text'] for s in scenes[:32])
 changed='\n\n'.join(edited if s['id']==20 else s['text'] for s in scenes[:32])
 context='\n\n'.join(edited if s['id']==20 else s['text'] for s in scenes[18:21])
 style='Natural, engaging, conversational documentary-style YouTube narration.'
 alternate='Calm, reflective documentary-style narration, with measured delivery.'
 fixture={'version':'s5-fixture-1','source':str(src.relative_to(ROOT)),'source_sha256':sha(src.read_bytes()),'scenes':scenes,'initial_block_scene_ids':list(range(1,33)),'comparison_scene_ids':[19,20,21],'edit':{'scene_id':20,'original':original,'edited':edited,'edited_metrics':metrics(edited)},'delivery_style':style,'alternate_delivery_style':alternate,'derived_texts':{'block_original':block,'block_edited':changed,'context_edited':context}}
 with wave.open(str(ROOT/'demo-video-example/narration.wav')) as w:
  duration=w.getnframes()/w.getframerate(); audio={'sha256':sha((ROOT/'demo-video-example/narration.wav').read_bytes()),'seconds':duration,'rate':w.getframerate(),'channels':w.getnchannels(),'width':w.getsampwidth()}
 fixture['historical_audio']=audio
 fixture['other_source_hashes']={p:sha((ROOT/p).read_bytes()) for p in ['demo-video-example/03_scenes.json','demo-video-example/output/timestamps.json']}
 fixture['inspected_pipeline_source_hashes']={str(p):sha(p.read_bytes()) for p in [ROOT.parent/'YoutubeAI/python-scripts/create_tts.py',ROOT.parent/'YoutubeAI/python-scripts/make_timestamps.py']}
 fixture['tts_provenance']='Historical model/voice/segment membership unverified; not a controlled quality baseline.'
 manifest=[]
 calls=[('A','Initial scene 19',scenes[18]['text'],style),('A','Initial scene 20',original,style),('A','Initial scene 21',scenes[20]['text'],style),('B/C','Shared initial source, scenes 1–32',block,style),('A/C-isolated','Edited scene 20; reused as isolated surgical replacement',edited,style),('B','Edited containing segment, scenes 1–32',changed,style),('C-context','Edited scene 20 with spoken context scenes 19 and 21',context,style),('Restoration','Original scene 20, alternate delivery only',original,alternate)]
 for i,(strategy,purpose,text,delivery) in enumerate(calls,1):
  m=metrics(text)
  manifest.append({'call':i,'strategy':strategy,'purpose':purpose,'text':text,'input':m,'delivery_style':delivery,'delivery_utf8_bytes':len(delivery.encode()),'model':'gemini-3.8-flash-lite-tts','voice':'Charon','response_modalities':['AUDIO'],'candidates':1,'serving_input_token_ceiling':8192,'serving_output_token_ceiling':16384,'requested_max_output_tokens':16384,'one_send_per_attempt':True,'max_microUSD':102400,'live_execution_authorized':False})
 fixture['block_metrics']=metrics(block)
 rates={'words_per_minute':len(words(' '.join(lines)))/duration*60,'scenes_per_minute':len(lines)/duration*60}
 counts=[]
 for minutes in [3,5,10]:
  n=math.ceil(rates['scenes_per_minute']*minutes); w=math.ceil(rates['words_per_minute']*minutes)
  # Repeat the measured scene distribution, not a claim these are independent approved scripts.
  projected=[dict(s,id=j+1) for j,s in enumerate((scenes*3)[:n])]
  for cap in [2000,3000,4000]:
   b=len(groups(projected,cap))
   counts.append({'minutes':minutes,'estimated_words':w,'projected_scene_count':n,'byte_cap':cap,'A_initial':n,'B_C_initial':b,'A_one_edit_plus_two_safe_retries':n+3,'B_one_edit_plus_two_safe_retries':b+3,'C_one_edit_plus_two_safe_retries':b+3,'C_with_one_failed_correction_then_B_fallback_plus_two_safe_retries':b+4,'projection_words_actual':sum(len(words(s['text'])) for s in projected)})
 checks=[]
 def check(name,condition):
  assert condition,name;checks.append({'name':name,'pass':True})
 fixture['scene_json_text_mismatches']=[s['id'] for s,j in zip(scenes,json.loads((ROOT/'demo-video-example/03_scenes.json').read_text())['scenes']) if s['text']!=j['narration'].strip()]
 check('script.txt chosen explicitly; JSON not substituted',fixture['source']=='demo-video-example/script.txt')
 for cap in [2000,3000,4000]:
  g=groups(scenes,cap)
  check('exact once ordered scene membership '+str(cap),[s['id'] for b in g for s in b]==list(range(1,50)))
  check('exact approved words/punctuation '+str(cap),'\n\n'.join(s['text'] for b in g for s in b)=='\n\n'.join(lines))
  check('byte ceiling '+str(cap),all(len('\n\n'.join(s['text'] for s in b).encode())<=cap for b in g))
 try: groups([{'id':1,'text':'x'*4001}],4000)
 except ValueError: check('oversized scene blocked, not truncated',True)
 else: raise AssertionError('oversized scene admitted')
 # Sample-exact synthetic replacement: source and mappings, no ASR/quality claim.
 pcm=array.array('h',range(3000)).tobytes(); replacement=array.array('h',[7]*1200).tobytes()
 assembled=pcm[:2000]+replacement+pcm[4000:]
 check('surgical untouched prefix byte identical',assembled[:2000]==pcm[:2000])
 check('surgical untouched suffix byte identical',assembled[4400:]==pcm[4000:])
 check('later offset shifts 200 samples without source mutation',len(assembled)//2==3200 and sha(pcm)==sha(array.array('h',range(3000)).tobytes()))
 reordered=pcm[4000:]+pcm[:2000];check('reorder/delete uses ranges only',len(reordered)==4000)
 truth={'words':[{'word':'One','start':0,'end':.1},{'word':'two','start':.1,'end':.2}], 'duration':.3, 'boundaries':[{'observed':.1,'reference':.12}]}
 check('exact word coverage accepted for review',score('One two',truth)['export_candidate'])
 check('missing word rejected',not score('One two three',truth)['export_candidate'])
 check('repeated word rejected',not score('One',truth)['export_candidate'])
 truth['words'][1]['start']=.05
 check('overlapping word ranges rejected',not score('One two',truth)['export_candidate'])
 check('were not falsely normalized to we are',score('were',{'words':[{'word':"we're",'start':0,'end':.1}], 'duration':.2})['edit_distance']==1)
 timestamps=json.loads((ROOT/'demo-video-example/output/timestamps.json').read_text())
 outputs={'fixture-manifest.json':fixture,'real-call-manifest.json':{'status':'PROPOSED_NOT_AUTHORIZED','base_submissions':8,'experiment_max_submissions_including_retries':10,'base_microUSD':8*102400,'total_microUSD':10*102400,'price_date':'2026-10-04','tax_account_fees':'Must be established and reserved separately before authorization; otherwise do not submit.','calls':manifest},'request-counts.json':{'basis':rates,'assumptions':'Extrapolation/repeated measured scene distribution, not independently measured 3/5/10 scripts. UTF-8 bytes exact; chars/4 token proxy not a certified tokenizer or cost bound.','rows':counts},'local-results.json':{'status':'LOCAL_PREPARATION_ONLY','checks':checks,'provider_calls':0,'quality_evidence':False,'asr_executed':False,'alignment_runtime':'faster_whisper and rapidfuzz unavailable in current python3; no model downloaded','historical_audio':audio,'historical_timestamp_statuses':[r.get('status') for r in timestamps.get('results',[])],'sample_rate_synthetic':24000}}
 for name,value in outputs.items(): (OUT/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
 print(json.dumps({'checks':len(checks),'block':metrics(block),'calls':[{k:r[k] for k in ['call','purpose','input']} for r in manifest],'counts':counts},indent=2))
if __name__=='__main__':run()
