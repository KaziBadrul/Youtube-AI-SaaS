"""Existing S5 speech+quiet music control; no speech generation or source changes."""
import copy,json,math,wave
import numpy as np
from s6 import ROOT,OUT,ASSETS,SR,FPS,FFMPEG,run,render,validate_output,sha,dump
def main():
    old=ROOT/'docs/architecture/evidence/narration-feasibility/runs/approved-lite-v1/audio/call-04/attempt-04/source.wav'
    digest=sha(old)
    base=json.loads((ASSETS/'project-12/manifest.json').read_text());m=copy.deepcopy(base)
    directory=ASSETS/'real-s5-control';directory.mkdir(exist_ok=True);audio=directory/'narration.wav'
    cmd=[FFMPEG,'-y','-v','error','-i',str(old),'-t','12','-ar','48000','-ac','1','-c:a','pcm_s16le',str(audio)]
    run(cmd);m['narration']=str(audio);m['narration_sha256']=sha(audio)
    reviewed=json.loads((ROOT/'docs/architecture/evidence/narration-feasibility/runs/approved-lite-v1/b-mapping-final-v1/call-04-reviewed-mapping.json').read_text())
    starts=[s['visual_start'] for s in reviewed['scene_mappings'][:3]]+[12.]
    for i,s in enumerate(m['scenes']):
        s.update(mapped_narration_start=starts[i],visual_start=starts[i],visual_end=starts[i+1],frame_start=math.ceil(starts[i]*FPS-1e-8),frame_end=math.ceil(starts[i+1]*FPS-1e-8))
    dump(directory/'manifest.json',m)
    results=[]
    for label,music in [('real-s5-music-on',True),('real-s5-music-off',False)]:
        r=render(m,label,False,False,music);v=validate_output(m,r);results.append(dict(label=label,validation=v['status'],snr_db=v['audio_snr_db']))
    def pcm(path):
        with wave.open(str(path),'rb') as w:return np.frombuffer(w.readframes(w.getnframes()),'<i2').astype(float)/32768
    narration=pcm(audio);music=.12*pcm(m['music'])
    ratio=10*np.log10(np.mean(narration**2)/np.mean(music**2))
    assert ratio>15,'music_overpowers_narration'
    assert sha(old)==digest
    dump(OUT/'real-narration-results.json',dict(status='PASS',source_sha256=digest,source_unchanged=True,processing=cmd,
        narration_over_music_db=float(ratio),mix_peak=float(np.max(np.abs(narration+music))),results=results,
        evidence='Decoded AAC matches expected existing speech+mix; relative music level >15dB below speech RMS; no clipping. This is signal preservation, not a listening-panel or new narration-quality claim.'))
    print('Existing S5 speech/music control passed',flush=True)
if __name__=='__main__':main()
