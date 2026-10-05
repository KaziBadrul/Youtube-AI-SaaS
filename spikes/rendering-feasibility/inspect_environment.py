"""S6 environment inventory; no dependency installation or media changes."""
import json
import platform
import shutil
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/architecture/evidence/rendering-feasibility/S6'
OUT.mkdir(parents=True,exist_ok=True)
commands={'macos':['sw_vers'],'architecture':['uname','-m'],
 'hardware':['system_profiler','SPHardwareDataType','-detailLevel','mini'],
 'sysctl':['/usr/sbin/sysctl','machdep.cpu.brand_string','hw.memsize','hw.ncpu'],
 'disk':['df','-h',str(ROOT)],'ffmpeg-version':['ffmpeg','-version'],
 'ffmpeg-buildconf':['ffmpeg','-buildconf'],'ffmpeg-filters':['ffmpeg','-filters'],
 'ffmpeg-encoders':['ffmpeg','-encoders'],'ffprobe-version':['ffprobe','-version']}
report={'python':sys.version,'platform':platform.platform(),'ffmpeg_path':shutil.which('ffmpeg'),
 'ffmpeg_realpath':str(Path(shutil.which('ffmpeg')).resolve()),'commands':{}}
for name,cmd in commands.items():
 p=subprocess.run(cmd,capture_output=True,text=True)
 text=p.stdout+p.stderr
 (OUT/f'{name}.txt').write_text(text)
 report['commands'][name]={'argv':cmd,'exit_code':p.returncode,'output_file':f'{name}.txt'}
report['fonts']=[str(p) for base in ('/System/Library/Fonts','/Library/Fonts',str(Path.home()/'Library/Fonts'))
 for p in Path(base).rglob('*') if p.suffix.lower() in ('.ttf','.ttc','.otf')]
filters=(OUT/'ffmpeg-filters.txt').read_text();encoders=(OUT/'ffmpeg-encoders.txt').read_text()
report['capabilities']={f:bool(__import__('re').search(r'\s'+f+r'\s',filters)) for f in ('subtitles','ass','drawtext','zoompan','scale','overlay','concat','amix')}
report['capabilities'].update({e:bool(__import__('re').search(r'\s'+e+r'\s',encoders)) for e in ('libx264','aac','h264_videotoolbox')})
(OUT/'environment.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'capabilities':report['capabilities'],'environment':'environment.json'}))
