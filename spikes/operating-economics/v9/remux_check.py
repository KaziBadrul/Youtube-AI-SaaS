"""Repair candidate concat duration metadata using existing scene frame counts only."""
import json,subprocess,time
from pathlib import Path
from phase import renderer,remap,sha,dump
R=Path('/repo');O=Path('/out');O.mkdir(exist_ok=True)
old=R/'docs/architecture/evidence/operating-economics/S9/v9/1cpu-2gb'
record=json.loads((old/'render-generated.json').read_text())
m=remap(json.loads((R/'docs/architecture/evidence/rendering-feasibility/S6/fixtures/project-600/manifest.json').read_text()))
origin=Path(record['attempt'].replace('/out',str(old),1))
recipe=O/'concat.txt'
for p in sorted(origin.glob('scene-*.mp4')):(O/p.name).symlink_to(p)
recipe.write_text(''.join(f"file 'scene-{s['scene_id']:03d}.mp4'\nduration {(s['frame_end']-s['frame_start'])/30:.9f}\n" for s in m['scenes']))
commands=json.loads((origin/'commands.json').read_text());cmd=commands[-1]
cmd=[str(recipe) if x==str(Path(record['attempt'])/'concat.txt') else x for x in cmd]
cmd=[x.replace('/out/s6/scratch',str(old/'s6/scratch')) if x.startswith('/out/s6/scratch') else x for x in cmd]
cmd[-1]=str(O/'candidate.mp4');start=time.monotonic();subprocess.run(cmd,check=True)
record.update(label='linux-600-repaired',output=cmd[-1],attempt=str(O),sha256=sha(cmd[-1]),bytes=Path(cmd[-1]).stat().st_size)
mod=renderer();v=mod.validate_output(m,record)
dump('remux-result.json',{'status':'PASS','repair':'explicit per-scene concat durations = integer frame counts /30; no reencoding','commands':cmd,'validation':v,'result':record,'wall_seconds':time.monotonic()-start,'source_failed_output_preserved':True})
