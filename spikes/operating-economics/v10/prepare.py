"""Prepare a fresh local VM input bundle from existing assets only. No network."""
import argparse,hashlib,json,tarfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--bundle',required=True);ap.add_argument('--receipt',required=True);a=ap.parse_args()
 bundle=Path(a.bundle);receipt=Path(a.receipt)
 assert not bundle.exists() and not receipt.exists(),'preserve existing evidence; supply fresh output paths'
 items=[]
 for folder in ['docs/architecture/evidence/rendering-feasibility/S6/fixtures','demo-video-example/images']:
  items.extend((f,'repo/'+str(f.relative_to(ROOT))) for f in (ROOT/folder).rglob('*') if f.is_file())
 for name in ['spikes/rendering-feasibility/s6.py','docs/architecture/evidence/rendering-feasibility/S6/fonts.json','docs/architecture/evidence/narration-feasibility/runs/approved-lite-v1/audio/call-04/attempt-04/source.wav']:
  items.append((ROOT/name,'repo/'+name))
 p=next((ROOT/'docs/architecture/evidence/rendering-feasibility/S6/exports').glob('project-300-*.mp4'));items.append((p,'repo/'+str(p.relative_to(ROOT))))
 for p in Path('/private/tmp/s9-v9-model').iterdir():items.append((p,'model/'+p.name))
 for p in Path('/private/tmp/s6-render-fonts').glob('*.ttf'):items.append((p,'fonts/'+p.name))
 records=[]
 with tarfile.open(bundle,'w') as t:
  for p,name in items:
   t.add(p,arcname=name,recursive=False)
   records.append({'host_path':str(p),'guest_path':'/'+name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
 receipt.write_text(json.dumps(records,indent=2)+'\n')
 print('files',len(records),'bundle bytes',bundle.stat().st_size)
if __name__=='__main__':main()
