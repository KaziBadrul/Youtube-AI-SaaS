"""Isolated Linux media/ASR/full-volume backup phases; existing assets read-only."""
import hashlib,importlib.util,io,json,os,sqlite3,subprocess,sys,time,zipfile
from pathlib import Path
R=Path('/repo');O=Path('/out');O.mkdir(exist_ok=True)
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
def dump(name,obj):(O/name).write_text(json.dumps(obj,indent=2)+'\n')
def renderer():
    origin=R/'spikes/rendering-feasibility/s6.py'
    text=origin.read_text().replace("ROOT=Path(__file__).resolve().parents[2]","ROOT=Path('/repo')")
    text=text.replace("OUT=ROOT/'docs/architecture/evidence/rendering-feasibility/S6'","OUT=Path('/out/s6')")
    text=text.replace("ASSETS=OUT/'fixtures'","ASSETS=ROOT/'docs/architecture/evidence/rendering-feasibility/S6/fixtures'")
    text=text.replace("'/opt/homebrew/bin/ffmpeg'","'/usr/bin/ffmpeg'").replace("'/opt/homebrew/bin/ffprobe'","'/usr/bin/ffprobe'")
    text=text.replace("cmd+=['-c:v','copy','-c:a'","cmd+=['-bsf:v','setts=pts=N/(30*TB):dts=N/(30*TB):duration=1/(30*TB)','-c:v','copy','-c:a'")
    folder=O/'s6';folder.mkdir(exist_ok=True)
    records=json.loads((R/'docs/architecture/evidence/rendering-feasibility/S6/fonts.json').read_text())
    for f in records:f['path']='/fonts/'+Path(f['path']).name
    (folder/'fonts.json').write_text(json.dumps(records))
    local=O/'adapted-s6.py';local.write_text(text)
    spec=importlib.util.spec_from_file_location('disposable_s6',local);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    dump('renderer-adaptation.json',{'source_sha256':sha(origin),'adapted_sha256':sha(local),'changes':['source/output and font paths only','FFmpeg/ffprobe Linux paths','explicit 30fps packet timestamp grid at stream-copy final mux'],'render_parameters_changed':'timestamp metadata only; frames/audio unchanged'})
    return mod

def remap(value):
    if isinstance(value,str):return value.replace('/Users/kazibadrul/Python Codes/YoutubeAISaaSFinal','/repo')
    if isinstance(value,list):return [remap(x) for x in value]
    if isinstance(value,dict):return {k:remap(v) for k,v in value.items()}
    return value

def render():
    mod=renderer();m=remap(json.loads((R/'docs/architecture/evidence/rendering-feasibility/S6/fixtures/project-600/manifest.json').read_text()))
    result=mod.render(m,label='linux-600');dump('render-generated.json',result)
    validation=mod.validate_output(m,result)
    dump('render-result.json',{'result':result,'validation':validation})

def alignment():
    import av
    original=av.open
    def compat(*a,**kw):kw.pop('metadata_errors',None);return original(*a,**kw)
    av.open=compat
    from faster_whisper import WhisperModel
    path=R/'docs/architecture/evidence/narration-feasibility/runs/approved-lite-v1/audio/call-04/attempt-04/source.wav'
    start=time.monotonic();model=WhisperModel('/model',device='cpu',compute_type='int8',cpu_threads=2,num_workers=1,local_files_only=True)
    loaded=time.monotonic();segs,info=model.transcribe(str(path),word_timestamps=True,vad_filter=True,beam_size=5,temperature=0,condition_on_previous_text=True)
    words=[]
    for seg in segs:
        for w in seg.words or []:words.append({'word':w.word,'start':w.start,'end':w.end,'probability':w.probability})
    assert words and all(w['start']<=w['end'] for w in words)
    dump('alignment-result.json',{'source_sha256':sha(path),'model':'existing local faster-whisper-base','load_seconds':loaded-start,'total_seconds':time.monotonic()-start,'words':words,'duration':info.duration,'coverage_verdict':'RESOURCE_TEST_ONLY; no replacement of accepted S5 mappings/fidelity review'})

def backup():
    # Five clean-project payloads using actual existing legacy images/source and S6 output.
    # Distinct versions/projects consume bytes; no compression benefit assumed. Not production parser.
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    images=sorted((R/'demo-video-example/images').glob('*.png'))
    source=R/'docs/architecture/evidence/rendering-feasibility/S6/fixtures/project-300/narration.wav'
    export=next((R/'docs/architecture/evidence/rendering-feasibility/S6/exports').glob('project-300-*.mp4'))
    files=[]
    for project in range(5):
        files += [(f'p{project}/image-{i:03d}',images[i%len(images)]) for i in range(60)]
        files += [(f'p{project}/narration.wav',source),(f'p{project}/export.mp4',export)]
    snap=O/'backup-db.sqlite3'
    with sqlite3.connect('/out/state.sqlite3') as live,sqlite3.connect(snap) as db:live.backup(db)
    files.append(('state.sqlite3',snap));raw=io.BytesIO();manifest={};start=time.monotonic()
    with zipfile.ZipFile(raw,'w',zipfile.ZIP_STORED) as z:
        for name,path in files:
            data=path.read_bytes();manifest[name]={'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)};z.writestr(name,data)
        z.writestr('manifest.json',json.dumps(manifest))
    key=AESGCM.generate_key(bit_length=256);nonce=os.urandom(12)
    encrypted=nonce+AESGCM(key).encrypt(nonce,raw.getvalue(),b'v9-resource-backup')
    file=O/'backup.enc';file.write_bytes(encrypted)
    # Full authenticated decrypt/hash verification; no remote storage and no insecure key output.
    decoded=AESGCM(key).decrypt(encrypted[:12],encrypted[12:],b'v9-resource-backup')
    with zipfile.ZipFile(io.BytesIO(decoded)) as z:
        for name,item in manifest.items():assert hashlib.sha256(z.read(name)).hexdigest()==item['sha256']
    dump('backup-result.json',{'wall_seconds':time.monotonic()-start,'file_count':len(files),'uncompressed_payload_bytes':sum(x['bytes'] for x in manifest.values()),'archive_bytes':len(encrypted),'sha256':sha(file),'restore_hashes_verified':True,'implementation':'in-memory full archive + AES-GCM stress, ZIP_STORED avoids hiding cost through compression','remote_proof':False,'key_retained':False})
    # Disposable archive cannot be recovered later; clean after verified local restore.
    file.unlink();snap.unlink()

if __name__=='__main__':
    {'render':render,'alignment':alignment,'backup':backup}[sys.argv[1]]()

# Optional independent platform-portability check; not run as a resource pipeline phase.
def captions():
    mod=renderer();tests=[('en','Noto Sans','A clear caption: “It’s ready!” 1, 2, 3.'),('es','Noto Sans','¿Qué ocurrió? El niño tomó café; acción y corazón.'),('fr','Noto Sans','L’été à Montréal : « déjà prêt », cœur et français.'),('bn','Noto Sans Bengali','বাংলা ভাষায় শিক্ষা: ক্ষুদ্র প্রশ্ন, শ্রদ্ধা ও বিজ্ঞান।'),('hi','Noto Sans Devanagari','हिन्दी में शिक्षा: क्षत्रिय, श्रद्धा और विज्ञान।')]
    from PIL import Image,ImageChops
    results=[]
    for language,family,text in tests:
        path=O/f'caption-{language}.png';layout=mod.caption(text,mod.FONTS[family],language,path)
        reference=R/'docs/architecture/evidence/rendering-feasibility/S6/fixtures'/f'caption-{language}.png'
        equal=False
        if reference.exists():
            a=Image.open(path).convert('RGBA');b=Image.open(reference).convert('RGBA')
            equal=a.size==b.size and a.tobytes()==b.tobytes()
        results.append({'language':language,'text':text,'font':family,'layout':layout,'exact_decoded_pixels_match_S6_reference':equal,'reference_available':reference.exists(),'sha256':sha(path)})
    dump('captions-result.json',{'results':results,'new_visual_review_required':[x['language'] for x in results if not x['exact_decoded_pixels_match_S6_reference']]})
