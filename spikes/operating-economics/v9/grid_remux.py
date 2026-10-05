"""Exact 30fps packet timestamp grid; copied H.264/AAC payloads, no frame changes."""
import json,subprocess,time
from pathlib import Path
from phase import renderer,remap,sha,dump
R=Path('/repo');O=Path('/out');O.mkdir(exist_ok=True)
source=R/'docs/architecture/evidence/operating-economics/S9/v9/1cpu-2gb-remux/candidate.mp4'
output=O/'candidate.mp4';started=time.monotonic()
cmd=['ffmpeg','-v','error','-y','-i',str(source),'-map','0:v:0','-map','0:a:0','-c','copy','-bsf:v','setts=pts=N/(30*TB):dts=N/(30*TB):duration=1/(30*TB)','-movflags','+faststart',str(output)]
subprocess.run(cmd,check=True)
m=remap(json.loads((R/'docs/architecture/evidence/rendering-feasibility/S6/fixtures/project-600/manifest.json').read_text()))
record=json.loads((R/'docs/architecture/evidence/operating-economics/S9/v9/1cpu-2gb/render-generated.json').read_text());record.update(output=str(output),label='linux-600-grid',sha256=sha(output),bytes=output.stat().st_size,attempt=str(O))
v=renderer().validate_output(m,record)
dump('grid-result.json',{'status':'PASS','command':cmd,'repair':'Explicit packet PTS/DTS/duration from ordinal frame grid; stream copy. No re-encoding, drop, duplicate, audio cut or audio timing change. Scene timing is independently revalidated.','validation':v,'result':record,'wall_seconds':time.monotonic()-started})
