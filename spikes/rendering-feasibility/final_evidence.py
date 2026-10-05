"""Aggregate required S6 evidence and pin original S5 source integrity."""
import hashlib,json,struct
from pathlib import Path
from s6 import ROOT,OUT,EXPORTS,ASSETS,sha,dump

def main():
    benchmarks=[]
    for t in (180,300,600):
        b=json.loads((OUT/f'project-{t}-benchmark.json').read_text());v=json.loads((OUT/f'project-{t}-validation.json').read_text())
        assert v['status']=='PASS' and sha(b['output'])==b['sha256']
        assert v.get('registered_after_validation'), 'export_not_registered_after_validation'
        # Scratch is monotonically growing until candidate publication; its retained
        # size plus installed candidate bytes provides exact prepublication peak.
        retained=sum(p.stat().st_size for p in Path(b['attempt']).glob('*') if p.is_file())
        candidate=Path(b['attempt'])/'candidate.mp4'
        # A byte-identical export can reuse an already installed immutable file;
        # in that case the retained scratch already includes the candidate.
        b['scratch_peak_bytes']=max(b['scratch_peak_bytes'],retained+(0 if candidate.exists() else b['bytes']))
        b['representative_cpu_percent']=100*b['cpu_seconds']/b['render_wall_seconds']
        b['max_scene_transition_error_seconds']=max(x['error_seconds'] for x in v['transitions'])
        # Read container atom ordering to verify faststart, alongside actual seeks.
        atoms=[]
        with Path(b['output']).open('rb') as f:
            while f.tell()<Path(b['output']).stat().st_size:
                pos=f.tell();header=f.read(8)
                if len(header)<8:break
                size,kind=struct.unpack('>I4s',header)
                if size==1:size=struct.unpack('>Q',f.read(8))[0]
                if size==0:break
                atoms.append(kind.decode(errors='replace'));f.seek(pos+size)
        assert atoms.index('moov')<atoms.index('mdat'),'not_faststart'
        b['container_atoms']=atoms;benchmarks.append(b)
    controls=json.loads((OUT/'control-results.json').read_text());assert controls['status']=='PASS'
    failures=json.loads((OUT/'failure-results.json').read_text());assert len(failures)>=18
    lifecycle=json.loads((OUT/'lifecycle-results.json').read_text());assert all(x['result']=='PASS' for x in lifecycle)
    web=json.loads((OUT/'web-boundary-results.json').read_text());assert web['status']=='PASS'
    real=json.loads((OUT/'real-narration-results.json').read_text());assert real['status']=='PASS'
    languages=json.loads((OUT/'multilingual-results.json').read_text());assert all(x['visual_shaping']=='PASS' for x in languages)
    sources=json.loads((ROOT/'docs/architecture/evidence/narration-feasibility/S5-GENERATION-RESULTS.json').read_text())['calls']
    integrity=[]
    for s in sources:
        assert sha(ROOT/s['audio'])==s['hash'];integrity.append(dict(call=s['call'],sha256=s['hash'],unchanged=True))
    dump(OUT/'S6-results.json',dict(verdict='PASS',scope='local fixture feasibility, not production implementation/host economics',benchmarks=benchmarks,
        languages=[dict(language=x['name'],font=x['font_family'],shaping=x['visual_shaping'],fallback=x['fallback'],clipped=x['clipped'],frame=x['decoded_frame']) for x in languages],
        failure_checks=len(failures),lifecycle=lifecycle,web_boundary=web,real_narration=real,source_integrity=integrity,
        model_downloads=0,provider_calls=0,paid_services=0,S9_executed=False,production_implementation=False))
    # Evidence hashes excluding SQLite transient state, aliases and this inventory.
    hashes={str(p.relative_to(OUT)):sha(p) for p in OUT.rglob('*') if p.is_file() and not p.is_symlink() and p.name not in ('hashes.json',) and p.suffix in ('.json','.png','.mp4','.wav','.txt','.log','.lock')}
    dump(OUT/'hashes.json',hashes)
    print(json.dumps([dict(minutes=b['duration']/60,seconds=round(b['render_wall_seconds'],2),MB=round(b['bytes']/1e6,2),scratch_MB=round(b['scratch_peak_bytes']/1e6,2),ffmpeg_rss_MB=round(b['peak_ffmpeg_rss_bytes']/1e6,2),cpu_percent=round(b['representative_cpu_percent'],1)) for b in benchmarks]))
if __name__=='__main__':main()
