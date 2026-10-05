"""Disposable S6 worker/media witness. No production code, providers or shell commands."""
import argparse,array,copy,hashlib,json,math,os,signal,subprocess,sys,time,uuid,wave
from pathlib import Path
import numpy as np
import psutil
from PIL import Image,ImageDraw,features
import uharfbuzz as hb
import freetype
from fontTools.ttLib import TTFont

ROOT=Path('/repo')
OUT=Path('/out/s6')
ASSETS=ROOT/'docs/architecture/evidence/rendering-feasibility/S6/fixtures';EXPORTS=OUT/'exports';SCRATCH=OUT/'scratch';FRAMES=OUT/'frames'
for p in (ASSETS,EXPORTS,SCRATCH,FRAMES):p.mkdir(parents=True,exist_ok=True)
FFMPEG='/usr/bin/ffmpeg';FFPROBE='/usr/bin/ffprobe'
W,H,FPS,SR=1920,1080,30,48000
FONT_RECORDS=json.loads((OUT/'fonts.json').read_text())
FONTS={x['family']:x['path'] for x in FONT_RECORDS}

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,x):Path(p).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def run(args,log=None):
    p=subprocess.run(args,capture_output=True)
    if log:Path(log).write_bytes(p.stdout+p.stderr)
    if p.returncode:raise RuntimeError((p.returncode,args,p.stderr.decode(errors='replace')[-1500:]))
    return p.stdout
def probe(p):return json.loads(run([FFPROBE,'-v','error','-show_streams','-show_format','-of','json',str(p)]))

def shaped(text,fontpath,size,language):
    face=hb.Face(Path(fontpath).read_bytes());font=hb.Font(face);font.scale=(size*64,size*64);hb.ot_font_set_funcs(font)
    buf=hb.Buffer();buf.add_str(text);buf.guess_segment_properties();buf.language=language
    hb.shape(font,buf)
    assert all(i.codepoint!=0 for i in buf.glyph_infos),'missing_glyph'
    return buf.glyph_infos,buf.glyph_positions

def text_width(text,font,size,language):return sum(p.x_advance for p in shaped(text,font,size,language)[1])/64

def caption(text,fontpath,language,path,size=54,maxwidth=1500):
    assert Path(fontpath).is_file(),'invalid_font'
    assert any(r['path']==fontpath and sha(fontpath)==r['sha256'] for r in FONT_RECORDS),'font_provenance_changed'
    cmap=TTFont(fontpath).getBestCmap()
    assert all(ord(c) in cmap for c in text if not c.isspace()),'font_fallback_or_missing_glyph'
    lines=[];line=''
    for word in text.split():
        candidate=(line+' '+word).strip()
        if text_width(candidate,fontpath,size,language)>maxwidth:
            assert line,'unwrappable_caption';lines.append(line);line=word
        else:line=candidate
    if line:lines.append(line)
    assert len(lines)<=2,'caption_exceeds_safe_box'
    im=Image.new('RGBA',(1600,180),(0,0,0,0));draw=ImageDraw.Draw(im)
    draw.rounded_rectangle((8,4,1592,176),radius=16,fill=(0,0,0,215))
    face=freetype.Face(fontpath);face.set_pixel_sizes(0,size)
    glyphs=[]
    for lineno,line in enumerate(lines):
        infos,positions=shaped(line,fontpath,size,language)
        pen=(1600-sum(p.x_advance for p in positions)/64)/2
        baseline=68+lineno*70 if len(lines)==2 else 112
        for info,pos in zip(infos,positions):
            face.load_glyph(info.codepoint,freetype.FT_LOAD_RENDER)
            slot=face.glyph;bm=slot.bitmap
            if bm.width and bm.rows:
                pix=np.array(bm.buffer,dtype=np.uint8).reshape(bm.rows,abs(bm.pitch))[:,:bm.width]
                mask=Image.fromarray(pix,'L');glyph=Image.new('RGBA',(bm.width,bm.rows),(255,255,255,255));glyph.putalpha(mask)
                x=round(pen+pos.x_offset/64+slot.bitmap_left);y=round(baseline-pos.y_offset/64-slot.bitmap_top)
                assert 0<=x and x+bm.width<=1600 and 0<=y and y+bm.rows<=180,'glyph_clipping'
                im.alpha_composite(glyph,(x,y))
            glyphs.append(dict(glyph_id=info.codepoint,cluster=info.cluster,x_advance=pos.x_advance))
            pen+=pos.x_advance/64
    im.save(path)
    return dict(text=text,font=fontpath,language=language,lines=lines,glyphs=glyphs,notdef_count=0,fallback=False,clipped=False,mechanism='HarfBuzz OpenType shaping + FreeType raster + Pillow composition',sha256=sha(path))

def multilingual():
    tests=[('en','English','Noto Sans','A clear caption: “It’s ready!” 1, 2, 3.'),
           ('es','Spanish','Noto Sans','¿Qué ocurrió? El niño tomó café; acción y corazón.'),
           ('fr','French','Noto Sans','L’été à Montréal : « déjà prêt », cœur et français.'),
           ('bn','Bangla','Noto Sans Bengali','বাংলা ভাষায় শিক্ষা: ক্ষুদ্র প্রশ্ন, শ্রদ্ধা ও বিজ্ঞান।'),
           ('hi','Hindi','Noto Sans Devanagari','हिन्दी में शिक्षा: क्षत्रिय, श्रद्धा और विज्ञान।')]
    results=[]
    for code,name,font,text in tests:
        cap=ASSETS/f'caption-{code}.png';info=caption(text,FONTS[font],code,cap)
        canvas=Image.new('RGB',(W,H),(38,52,72));canvas.paste(Image.open(cap),(160,880),Image.open(cap))
        canvas.save(FRAMES/f'language-{code}.png')
        path=EXPORTS/f'language-{code}.mp4'
        cmd=[FFMPEG,'-y','-v','error','-loop','1','-i',str(FRAMES/f'language-{code}.png'),'-f','lavfi','-i','anullsrc=r=48000:cl=mono','-t','3','-r','30','-c:v','libx264','-preset','ultrafast','-threads','2','-pix_fmt','yuv420p','-c:a','aac','-movflags','+faststart',str(path)]
        run(cmd,OUT/f'language-{code}-ffmpeg.log')
        info.update(name=name,font_family=font,frame=f'frames/language-{code}.png',output=f'exports/language-{code}.mp4',visual_shaping='PENDING_INSPECTION',codec=probe(path)['streams'][0]['codec_name'])
        results.append(info)
    dump(OUT/'multilingual-results.json',results)
    print('Multilingual fixtures ready',flush=True)

def fixture(duration):
    directory=ASSETS/f'project-{duration}';directory.mkdir(exist_ok=True)
    mapping=json.loads((ROOT/'docs/architecture/evidence/narration-feasibility/runs/approved-lite-v1/b-mapping-final-v1/call-04-reviewed-mapping.json').read_text())
    base=mapping['scene_mappings'];n=math.ceil(32*duration/171.48)
    weights=[m['visual_end']-m['visual_start'] for m in base]
    durations=np.array([weights[i%32] for i in range(n)]);starts=np.r_[0,np.cumsum(durations)]*duration/durations.sum()
    starts[-1]=float(duration)  # Exact terminal boundary; no floating-point overshoot.
    text_variants=['A clear caption follows continuous narration.', 'Ready!',
        'This long caption wraps onto a second readable line while narration continues through every visual change.',
        '“It’s ready,” she said. Numbers: 12, 24 and 1080.']
    scene_records=[];cues=[]
    for i in range(n):
        color=(45+(i*37)%155,50+(i*61)%150,55+(i*83)%145)
        im=Image.new('RGB',(3840,2160),color);draw=ImageDraw.Draw(im)
        draw.rectangle((200,200,3640,1700),outline=(235,240,245),width=16)
        draw.ellipse((1750,650,2150,1050),fill=(245,220,130))
        # Scene ID is encoded both by hue and a binary marker; render analysis uses hue.
        for bit in range(8):draw.rectangle((300+bit*100,350,360+bit*100,410),fill=(250,250,250) if i&(1<<bit) else (25,25,25))
        image=directory/f'image-{i+1:03}.png';im.save(image)
        text=text_variants[i%len(text_variants)];cap=directory/f'caption-{i+1:03}.png'
        layout=caption(text,FONTS['Noto Sans'],'en',cap)
        frame_start=math.ceil((starts[i]-1e-8)*FPS);frame_end=math.ceil((starts[i+1]-1e-8)*FPS)
        cue_start=frame_start/FPS;cue_end=min(frame_end/FPS,cue_start+max(.4,(frame_end-frame_start)/FPS-.2))
        scene_records.append(dict(scene_id=i+1,image_id=f'image-{i+1:03}',image=str(image),image_sha256=sha(image),
            mapped_narration_start=float(starts[i]),visual_start=0. if i==0 else float(starts[i]),visual_end=float(starts[i+1]),
            frame_start=frame_start,frame_end=frame_end,color=color,caption_image=str(cap),caption_sha256=sha(cap),caption_lines=layout['lines']))
        cues.append(dict(scene_id=i+1,start=cue_start,end=cue_end,text=text,font='Noto Sans'))
    # Continuous deterministic non-speech signal. No per-scene narration slicing.
    narration=directory/'narration.wav';music=directory/'music.wav'
    with wave.open(str(narration),'wb') as w, wave.open(str(music),'wb') as m:
        for target in (w,m):target.setnchannels(1);target.setsampwidth(2);target.setframerate(SR)
        for sec in range(duration):
            t=(sec+np.arange(SR)/SR)
            x=.16*np.sin(2*np.pi*(220*t+8*np.sin(2*np.pi*.3*t)))+.035*np.sin(2*np.pi*440*t)
            bg=.12*np.sin(2*np.pi*110*t)+.06*np.sin(2*np.pi*165*t)
            w.writeframes((x*32767).astype('<i2').tobytes());m.writeframes((bg*32767).astype('<i2').tobytes())
    manifest=dict(duration=duration,scene_count=n,source_s5_mapping_sha256=sha(ROOT/'docs/architecture/evidence/narration-feasibility/runs/approved-lite-v1/b-mapping-final-v1/call-04-reviewed-mapping.json'),
        fixture_kind='deterministic synthetic, S5-density and duration pattern; no speech quality claim',
        scenes=scene_records,captions=cues,narration=str(narration),narration_sha256=sha(narration),music=str(music),music_sha256=sha(music),
        config=dict(width=W,height=H,fps=FPS,captions=True,motion=True,music=True,font='Noto Sans',music_gain=.12),
        registry={s['image_id']:s['image'] for s in scene_records})
    dump(directory/'manifest.json',manifest)
    return manifest

def validate_input(m,captions=True,music=True):
    duration=m['duration'];assert duration>0
    for key in ('narration',)+(('music',) if music else ()):
        assert Path(m[key]).resolve().is_relative_to(ASSETS.resolve()),'unsafe_audio_path'
    with wave.open(m['narration'],'rb') as w:
        assert w.getnframes()/w.getframerate()==duration,'narration_duration'
        assert len(w.readframes(w.getnframes()))==w.getnframes()*w.getnchannels()*w.getsampwidth(),'corrupt_narration'
    assert sha(m['narration'])==m['narration_sha256'],'narration_hash'
    if music:
        assert sha(m['music'])==m['music_sha256'],'music_hash'
        with wave.open(m['music'],'rb') as w:assert w.getnframes()/w.getframerate()==duration,'music_duration'
    assert [s['scene_id'] for s in m['scenes']]==list(range(1,len(m['scenes'])+1)),'scene_order'
    assert m['scenes'][0]['frame_start']==0 and m['scenes'][-1]['frame_end']==duration*FPS,'coverage'
    for i,s in enumerate(m['scenes']):
        path=Path(m['registry'][s['image_id']]).resolve()
        assert path==Path(s['image']).resolve() and path.is_relative_to(ASSETS.resolve()),'unsafe_path'
        assert path.is_file(),'missing_image'
        with Image.open(path) as im:im.verify()
        assert sha(path)==s['image_sha256'],'image_hash'
        assert s['frame_end']>s['frame_start'],'invalid_mapping'
        assert math.isfinite(s['visual_start']) and math.isfinite(s['visual_end']) and 0<=s['visual_start']<s['visual_end']<=duration,'invalid_visual_mapping'
        assert s['visual_start']==s['mapped_narration_start'],'visual_not_next_start'
        assert s['frame_start']==math.ceil((s['mapped_narration_start']-1e-8)*FPS),'mapping_frame_mismatch'
        if i:
            assert m['scenes'][i-1]['frame_end']==s['frame_start'],'mapping_gap'
            assert m['scenes'][i-1]['visual_end']==s['visual_start'],'visual_gap'
        if captions:
            cap=Path(s['caption_image']).resolve();assert cap.is_relative_to(ASSETS.resolve()),'unsafe_caption_path'
            assert sha(cap)==s['caption_sha256'],'caption_hash'
    prev=0.
    for c in m['captions'] if captions else []:
        assert prev<=c['start']<c['end']<=duration,'invalid_caption_timing';prev=c['end']
        assert c['font'] in FONTS and Path(FONTS[c['font']]).is_file(),'invalid_caption_font'
    return True

def command(m,s,output,motion=True,captions=True):
    count=s['frame_end']-s['frame_start']
    args=[FFMPEG,'-y','-v','error','-threads','2','-i',s['image']]
    if captions:args+=['-loop','1','-framerate','30','-i',s['caption_image']]
    z=f"1+0.025*on/{max(1,count-1)}" if motion else '1'
    filt=f"[0:v]format=yuv444p,zoompan=z='{z}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d={count}:s=1920x1080:fps=30,format=yuv420p[v]"
    if captions:
        cue=m['captions'][s['scene_id']-1];end=cue['end']-s['frame_start']/FPS
        filt+=f";[v][1:v]overlay=160:880:enable='lt(t,{end:.9f})':shortest=1[out]"
    else:filt=filt.replace('[v]','[out]')
    args+=['-filter_complex_threads','1','-filter_complex',filt,'-map','[out]','-an','-frames:v',str(count),'-c:v','libx264','-preset','ultrafast','-crf','23','-threads','2','-pix_fmt','yuv420p','-r','30',str(output)]
    return args

def spawn_measured(args,log,scratch):
    start=time.monotonic();stats=[]
    with Path(log).open('wb') as f:
        p=subprocess.Popen(args,stdout=f,stderr=f,start_new_session=True)
        proc=psutil.Process(p.pid)
        while p.poll() is None:
            try:
                cpu=proc.cpu_times();rss=proc.memory_info().rss
                stats.append(dict(elapsed=time.monotonic()-start,rss=rss,cpu_seconds=cpu.user+cpu.system,scratch_bytes=sum(x.stat().st_size for x in scratch.glob('*') if x.is_file())))
            except (psutil.NoSuchProcess,psutil.AccessDenied):pass
            time.sleep(.1)
    assert p.returncode==0,(args,p.returncode,Path(log).read_text()[-1000:])
    scratch_final=sum(x.stat().st_size for x in scratch.glob('*') if x.is_file())
    return dict(wall_seconds=time.monotonic()-start,peak_rss_bytes=max((s['rss'] for s in stats),default=0),cpu_seconds=max((s['cpu_seconds'] for s in stats),default=0),scratch_peak_bytes=max([scratch_final]+[s['scratch_bytes'] for s in stats]))

def render(m,label=None,captions=True,motion=True,music=True):
    validate_input(m,captions,music);label=label or f'project-{m["duration"]}'
    import re
    assert re.fullmatch(r'[a-z0-9-]+',label),'unsafe_output_label'
    attempt=SCRATCH/(label+'-'+uuid.uuid4().hex[:8]);attempt.mkdir()
    start=time.monotonic();stats=[];commands=[]
    for s in m['scenes']:
        cancel_file=os.environ.get('S6_CANCEL_FILE')
        if cancel_file and Path(cancel_file).exists():raise RuntimeError('cancelled_before_next_media_step')
        output=attempt/f'scene-{s["scene_id"]:03}.mp4';cmd=command(m,s,output,motion,captions)
        commands.append(cmd);stats.append(spawn_measured(cmd,attempt/f'scene-{s["scene_id"]:03}.log',attempt))
        if s['scene_id']%10==0:print(label,'scene',s['scene_id'],'/',len(m['scenes']),flush=True)
    concat=attempt/'concat.txt';concat.write_text(''.join(f"file '{p.name}'\n" for p in sorted(attempt.glob('scene-*.mp4'))))
    cancel_file=os.environ.get('S6_CANCEL_FILE')
    if cancel_file and Path(cancel_file).exists():raise RuntimeError('cancelled_before_mux')
    output=attempt/'candidate.mp4'  # Private, unregistered until full validation.
    cmd=[FFMPEG,'-y','-v','error','-f','concat','-safe','1','-i',str(concat),'-i',m['narration']]
    if music:cmd+=['-i',m['music'],'-filter_complex','[2:a]volume=0.12[bg];[1:a][bg]amix=inputs=2:duration=first:normalize=0[a]','-map','0:v','-map','[a]']
    else:cmd+=['-map','0:v','-map','1:a']
    cmd+=['-bsf:v','setts=pts=N/(30*TB):dts=N/(30*TB):duration=1/(30*TB)','-c:v','copy','-c:a','aac','-b:a','160k','-ar','48000','-ac','1','-movflags','+faststart',str(output)]
    commands.append(cmd);stats.append(spawn_measured(cmd,attempt/'mux.log',attempt))
    result=dict(label=label,duration=m['duration'],scene_count=len(m['scenes']),output=str(output),sha256=sha(output),bytes=output.stat().st_size,
        render_wall_seconds=time.monotonic()-start,peak_ffmpeg_rss_bytes=max(s['peak_rss_bytes'] for s in stats),
        cpu_seconds=sum(s['cpu_seconds'] for s in stats),scratch_peak_bytes=max(s['scratch_peak_bytes'] for s in stats),
        config=dict(captions=captions,motion=motion,music=music),attempt=str(attempt))
    dump(attempt/'commands.json',commands);dump(OUT/(label+'-benchmark.json'),result)
    return result

def frame(p,t):
    raw=run([FFMPEG,'-v','error','-ss',f'{t:.9f}','-i',str(p),'-frames:v','1','-f','rawvideo','-pix_fmt','rgb24','pipe:1'])
    assert len(raw)==W*H*3,'missing_frame'
    return np.frombuffer(raw,dtype=np.uint8).reshape(H,W,3)

def output_basic(p,duration):
    assert Path(p).is_file(),'missing_output';info=probe(p)
    assert 'mp4' in info['format']['format_name'],'wrong_container'
    video=next((s for s in info['streams'] if s['codec_type']=='video'),None)
    audio=next((s for s in info['streams'] if s['codec_type']=='audio'),None)
    assert video and audio,'missing_stream'
    assert (video['width'],video['height'])==(W,H),'wrong_resolution'
    assert video['codec_name']=='h264' and audio['codec_name']=='aac','wrong_codec'
    a,b=map(int,video['avg_frame_rate'].split('/'));assert abs(a/b-FPS)<1e-6,'wrong_fps'
    tolerance=1/FPS+1024/SR
    assert abs(float(info['format']['duration'])-duration)<=tolerance,'wrong_duration'
    run([FFMPEG,'-v','error','-i',str(p),'-f','null','-'],OUT/(Path(p).stem+'-decode.log'))
    return info

def validate_output(m,result):
    p=Path(result['output']);info=output_basic(p,m['duration']);transitions=[]
    colors=np.array([s['color'] for s in m['scenes']])
    # Decode a small protected color patch for every frame, establishing coverage/order.
    raw=run([FFMPEG,'-v','error','-i',str(p),'-vf','crop=8:8:40:40','-pix_fmt','rgb24','-f','rawvideo','pipe:1'])
    patch=np.frombuffer(raw,np.uint8).reshape(-1,8,8,3).mean(axis=(1,2))
    assert len(patch)==m['duration']*FPS,'incomplete_video_frames'
    ids=np.argmin(((patch[:,None,:]-colors[None,:,:])**2).sum(axis=2),axis=1)
    expected=np.empty(len(patch),dtype=np.int32)
    for i,s in enumerate(m['scenes']):expected[s['frame_start']:s['frame_end']]=i
    assert np.array_equal(ids,expected),'scene_order_or_transition_mismatch'
    assert patch.min()>15,'blank_visual'
    for i,s in enumerate(m['scenes']):
        if i:
            actual=float(np.flatnonzero(ids==i)[0]/FPS);err=actual-s['mapped_narration_start']
            assert -.000001<=err<=1/FPS+.000001,'transition_tolerance'
            transitions.append(dict(scene_id=s['scene_id'],expected=s['mapped_narration_start'],rendered=actual,error_seconds=err))
    # Decode the full AAC output and compare with expected continuous PCM mix.
    audio=np.frombuffer(run([FFMPEG,'-v','error','-i',str(p),'-map','0:a','-ac','1','-ar',str(SR),'-f','f32le','pipe:1']),dtype='<f4')
    def readwav(path):
        with wave.open(path,'rb') as w:return np.frombuffer(w.readframes(w.getnframes()),'<i2').astype(np.float32)/32768
    reference=readwav(m['narration'])
    if result['config']['music']:reference+=.12*readwav(m['music'])
    assert len(audio)>=len(reference),'truncated_narration'
    assert len(audio)-len(reference)<=1024,'unexpected_audio_tail'
    audio=audio[:len(reference)]
    error=audio-reference;snr=10*np.log10(np.mean(reference**2)/max(1e-12,np.mean(error**2)))
    rms=np.sqrt(np.mean(audio[:len(audio)//480*480].reshape(-1,480)**2,axis=1))
    reference_rms=np.sqrt(np.mean(reference[:len(reference)//480*480].reshape(-1,480)**2,axis=1))
    active=reference_rms>.005
    assert snr>20,'narration_mix_mismatch'
    assert np.all(rms[active]>.2*reference_rms[active]),'unintended_audio_gap'
    assert np.abs(audio).max()<.95,'clipping'
    caption_samples=[]
    for index in [0,len(m['scenes'])//2,len(m['scenes'])-1]:
        s=m['scenes'][index];cue=m['captions'][index];t=cue['start']+min(.25,(cue['end']-cue['start'])/2)
        f=frame(p,t);Image.fromarray(f).save(FRAMES/f'{result["label"]}-scene-{s["scene_id"]}.png')
        bright=int((f[890:1050,170:1750].min(axis=2)>215).sum())
        if result['config']['captions']:assert bright>100,'missing_caption'
        else:assert bright<100,'unexpected_caption'
        caption_samples.append(dict(scene_id=s['scene_id'],white_text_pixels=bright,enabled=result['config']['captions']))
    validation=dict(status='PASS',ffprobe=info,transition_tolerance_seconds=1/FPS,transitions=transitions,
        decoded_frame_count=len(patch),blank_frames=0,source_narration_samples=len(reference),decoded_audio_samples=len(audio),
        audio_snr_db=float(snr),audio_min_10ms_rms=float(rms.min()),audio_peak=float(np.abs(audio).max()),caption_samples=caption_samples,
        limits='synthetic audio proves rendering continuity, not speech intelligibility or narration quality')
    # Only validated output enters this disposable export registry. Filenames and
    # benchmark receipts alone are never proof of successful export.
    final=EXPORTS/(result['label']+'-'+sha(p)[:12]+'.mp4')
    if final.exists():assert sha(final)==sha(p),'immutable_export_collision'
    else:os.replace(p,final)
    p=final;result['output']=str(final)
    # A local convenience alias is switched only after validation. Registry pins
    # the immutable file/hash rather than this alias.
    alias=EXPORTS/(result['label']+'.mp4');temporary_alias=EXPORTS/(result['label']+'.link-tmp')
    if temporary_alias.exists() or temporary_alias.is_symlink():temporary_alias.unlink()
    temporary_alias.symlink_to(final.name);os.replace(temporary_alias,alias)
    registry_path=OUT/'export-registrations.json'
    registry=json.loads(registry_path.read_text()) if registry_path.exists() else {}
    registry[result['label']]=dict(path=str(p),sha256=sha(p),validation='PASS',source_narration_sha256=m['narration_sha256'])
    temporary=registry_path.with_suffix('.tmp')
    with temporary.open('w') as f:json.dump(registry,f,indent=2);f.flush();os.fsync(f.fileno())
    os.replace(temporary,registry_path)
    validation['registered_after_validation']=True
    dump(OUT/(result['label']+'-benchmark.json'),result)
    dump(OUT/(result['label']+'-validation.json'),validation)
    print(result['label'],'validated',flush=True)
    return validation

def main():
    ap=argparse.ArgumentParser();ap.add_argument('action',choices=['languages','benchmark','control']);ap.add_argument('--duration',type=int,default=300)
    args=ap.parse_args()
    if args.action=='languages':multilingual();return
    if args.action=='benchmark':
        m=fixture(args.duration);r=render(m);validate_output(m,r)
    else:
        m=fixture(12)
        for label,captions,motion,music in [('control-all-on',True,True,True),('control-all-off',False,False,False)]:
            r=render(m,label,captions,motion,music);validate_output(m,r)

if __name__=='__main__':main()
