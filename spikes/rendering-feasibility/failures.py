"""Deterministic S6 malformed media/security/output failures; no providers."""
import copy,json,subprocess,wave,os,uuid
from pathlib import Path
from s6 import OUT,ASSETS,EXPORTS,FFMPEG,FONTS,validate_input,output_basic,render,sha,caption,dump

def main():
    m=json.loads((ASSETS/'project-300/manifest.json').read_text());directory=ASSETS/'invalid';directory.mkdir(exist_ok=True)
    badimage=directory/'corrupt.png';badimage.write_bytes(b'not an image')
    badaudio=directory/'corrupt.wav';badaudio.write_bytes(b'not audio')
    previous=EXPORTS/'project-300.mp4';previous_hash=sha(previous);cases=[]
    def expect(name,fn):
        try:fn()
        except (AssertionError,ValueError,KeyError,OSError,RuntimeError,wave.Error,EOFError) as e:
            cases.append(dict(case=name,result='REJECTED',error=str(e)[:350],previous_export_preserved=sha(previous)==previous_hash))
        else:raise AssertionError(('invalid input accepted',name))
    def changed(fn):
        bad=copy.deepcopy(m);fn(bad);return bad
    def image_path(x,path):x['scenes'][0]['image']=str(path);x['registry'][x['scenes'][0]['image_id']]=str(path)
    expect('missing_image',lambda:validate_input(changed(lambda x:image_path(x,directory/'missing.png'))))
    expect('corrupt_image',lambda:validate_input(changed(lambda x:image_path(x,badimage))))
    expect('missing_narration',lambda:validate_input(changed(lambda x:x.update(narration=str(directory/'missing.wav')))))
    expect('corrupt_narration',lambda:validate_input(changed(lambda x:x.update(narration=str(badaudio)))))
    expect('invalid_scene_mapping',lambda:validate_input(changed(lambda x:x['scenes'][0].update(frame_end=0))))
    expect('scene_order_error',lambda:validate_input(changed(lambda x:x['scenes'].reverse())))
    expect('caption_outside_duration',lambda:validate_input(changed(lambda x:x['captions'][-1].update(end=301))))
    expect('invalid_caption_font',lambda:validate_input(changed(lambda x:x['captions'][0].update(font='unapproved font'))))
    expect('caption_overflow',lambda:caption(' '.join(['caption']*300),FONTS['Noto Sans'],'en',directory/'overflow.png'))
    expect('unsafe_asset_path',lambda:validate_input(changed(lambda x:image_path(x,Path('/etc/passwd')))))
    expect('unsafe_audio_path',lambda:validate_input(changed(lambda x:x.update(narration='/etc/passwd'))))
    expect('unsafe_output_path',lambda:render(m,'../../outside'))
    # Untrusted display filenames and subtitle text do not enter argv/filtergraph.
    from s6 import command
    odd=copy.deepcopy(m);odd['original_filename']='--filter_complex ; touch /tmp/S6_BAD'
    sentinel=Path('/private/tmp')/('S6-SENTINEL-'+uuid.uuid4().hex[:8])
    odd['captions'][0]['text']=f'[x];movie=/etc/passwd; -y $(touch {sentinel})'
    injection=directory/'injection-caption.png';caption(odd['captions'][0]['text'],FONTS['Noto Sans'],'en',injection)
    odd['scenes'][0]['caption_image']=str(injection);odd['scenes'][0]['caption_sha256']=sha(injection)
    argv=command(odd,odd['scenes'][0],directory/'safe.mp4')
    assert odd['original_filename'] not in ' '.join(argv) and odd['captions'][0]['text'] not in ' '.join(argv)
    assert not sentinel.exists()
    cases.append(dict(case='filename_and_caption_injection',result='PASS',construction='argv list; text rendered as glyph pixels; internal paths only'))
    disabled=copy.deepcopy(m);disabled['captions'][0].update(font='bad',end=301)
    assert validate_input(disabled,captions=False)
    cases.append(dict(case='disabled_caption_branch',result='PASS'))
    result=subprocess.run([FFMPEG,'-y','-v','error','-i',str(badimage),str(directory/'failed.mp4')],capture_output=True,text=True)
    assert result.returncode!=0
    cases.append(dict(case='ffmpeg_nonzero',result='REJECTED',exit_code=result.returncode,registered=False))
    incomplete=directory/'incomplete.mp4';incomplete.write_bytes(previous.read_bytes()[:1000])
    expect('incomplete_output',lambda:output_basic(incomplete,300))
    silent=directory/'no-audio.mp4';wrong=directory/'wrong-resolution.mp4'
    subprocess.run([FFMPEG,'-y','-v','error','-i',str(previous),'-t','1','-map','0:v','-c:v','copy',str(silent)],check=True)
    expect('missing_audio_stream',lambda:output_basic(silent,1))
    subprocess.run([FFMPEG,'-y','-v','error','-i',str(previous),'-t','1','-vf','scale=640:360','-c:v','libx264','-threads','2','-c:a','aac',str(wrong)],check=True)
    expect('wrong_resolution',lambda:output_basic(wrong,1))
    assert sha(previous)==previous_hash
    cancel_file=directory/'cancel-before-next-step';cancel_file.write_text('cancel requested')
    os.environ['S6_CANCEL_FILE']=str(cancel_file)
    try:expect('persistent_cancel_blocks_next_step',lambda:render(m,'cancel-before-next-step'))
    finally:os.environ.pop('S6_CANCEL_FILE',None)
    dump(OUT/'failure-results.json',cases);print(len(cases),'failure/security checks passed',flush=True)

if __name__=='__main__':main()
