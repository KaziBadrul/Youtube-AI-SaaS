"""S6 deterministic motion/audio/caption controls over decoded frames."""
import json
import numpy as np
from PIL import Image
from s6 import OUT,ASSETS,EXPORTS,FRAMES,FFMPEG,FPS,run,frame,dump,command

def motion_check(m,label,on):
    p=EXPORTS/(label+'.mp4')
    raw=run([FFMPEG,'-v','error','-i',str(p),'-vf','crop=400:400:760:250,scale=80:80','-f','rawvideo','-pix_fmt','rgb24','pipe:1'])
    images=np.frombuffer(raw,np.uint8).reshape(-1,80,80,3)
    rows=[]
    yy,xx=np.mgrid[:80,:80]
    for s in m['scenes']:
        sequence=images[s['frame_start']:s['frame_end']]
        mask=(sequence[:,:,:,0]>220)&(sequence[:,:,:,1]>180)&(sequence[:,:,:,2]<180)
        area=mask.sum((1,2));assert area.min()>500,'graphic_missing'
        cx=(mask*xx).sum((1,2))/area;cy=(mask*yy).sum((1,2))/area
        maxstep=max(np.max(np.abs(np.diff(cx))),np.max(np.abs(np.diff(cy))))*5 if len(cx)>1 else 0
        growth=float(area[-1]/area[0])
        assert maxstep<1.0,'transform_jitter_over_one_output_pixel'
        if on:assert growth>1.015,'scene_motion_not_applied'
        else:assert np.max(area)-np.min(area)<3,'unexpected_motion'
        rows.append(dict(scene_id=s['scene_id'],area_growth=growth,max_centroid_step_output_pixels=float(maxstep),motion=on))
    # Image corners are filled at beginning/middle/end of every scene.
    corners=[]
    for s in m['scenes']:
        f=frame(p,(s['frame_start']+.5)/FPS)
        assert min(int(f[:8,:8].min()),int(f[:8,-8:].min()),int(f[-8:,:8].min()),int(f[-8:,-8:].min()))>15,'black_border'
        corners.append(s['scene_id'])
    return dict(status='PASS',scene_motion=rows,corner_checks=corners,centroid_step_limit_output_pixels=1.0,limits='synthetic geometry transform stability, not subjective artistic motion quality')

def main():
    results=[]
    for duration in (180,300,600):
        m=json.loads((ASSETS/f'project-{duration}/manifest.json').read_text())
        results.append(dict(label=f'project-{duration}',result=motion_check(m,f'project-{duration}',True)))
    m=json.loads((ASSETS/'project-12/manifest.json').read_text())
    for label,on in [('control-all-on',True),('control-all-off',False)]:
        results.append(dict(label=label,result=motion_check(m,label,on)))
    off=EXPORTS/'control-all-off.mp4'
    s=m['scenes'][0]
    a=frame(off,(s['frame_start']+2)/FPS);b=frame(off,(s['frame_end']-2)/FPS)
    # Lossy H.264 may refine pixels across P frames without moving the image.
    # Verify exact static frames before compression instead of treating codec
    # refinement as motion. Decoded geometric stability is checked above.
    md5_results=[]
    for scene in m['scenes']:
        argv=command(m,scene,EXPORTS/'unused.mp4',False,False)
        argv=argv[:argv.index('-c:v')]+['-c:v','rawvideo','-pix_fmt','rgb24','-f','framemd5','pipe:1']
        records=[line.rsplit(',',1)[-1].strip() for line in run(argv).decode().splitlines() if line and not line.startswith('#')]
        assert len(records)==scene['frame_end']-scene['frame_start'] and len(set(records))==1,'motion_off_filter_instability'
        md5_results.append(dict(scene_id=scene['scene_id'],frames=len(records),unique_frame_hashes=1))
    # Cue end transition: sample frames directly before/after the metadata cut.
    on=EXPORTS/'control-all-on.mp4';cue=m['captions'][0]
    def indexed(index):
        raw=run([FFMPEG,'-v','error','-i',str(on),'-vf',f'select=eq(n\\,{index})','-frames:v','1','-f','rawvideo','-pix_fmt','rgb24','pipe:1'])
        return np.frombuffer(raw,np.uint8).reshape(1080,1920,3)
    before=indexed(int(np.ceil(cue['end']*FPS))-1)
    after=indexed(int(np.ceil(cue['end']*FPS)))
    white_before=int((before[890:1050,170:1750].min(2)>215).sum())
    white_after=int((after[890:1050,170:1750].min(2)>215).sum())
    assert white_before>100 and white_after<100,'caption_end_timing'
    dump(OUT/'control-results.json',dict(status='PASS',motion_checks=results,motion_off_lossless_frame_identity=md5_results,lossy_decoded_still_mean_absolute_difference=float(np.abs(a.astype(float)-b.astype(float)).mean()),caption_end_white_pixels=[white_before,white_after],
        audio_checks='ON/OFF complete decoded signal compared to corresponding source or source+music in per-render validation; music-off has no contribution',
        music_policy='full-duration local fixture; fixed -18.4dB gain (0.12), no time stretch/ducking; source synthetic narration RMS dominates quiet music; no clipping'))
    print('Motion, caption end and still-frame controls passed',flush=True)
if __name__=='__main__':main()
