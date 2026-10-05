"""Local process-group witness with boot/start identity; not deployment supervision."""
import hashlib,json,os,signal,subprocess,sys,time
from pathlib import Path
from core import durable

def boot_identity():
 p=Path('/proc/sys/kernel/random/boot_id')
 if p.exists():return p.read_text().strip()
 return hashlib.sha256(subprocess.check_output(['/usr/sbin/sysctl','-n','kern.boottime'])).hexdigest()
def start_identity(pid):
 return subprocess.check_output(['/bin/ps','-p',str(pid),'-o','lstart='],text=True).strip()
def running(pid):
 r=subprocess.run(['/bin/ps','-p',str(pid),'-o','stat='],capture_output=True,text=True)
 return r.returncode==0 and bool(r.stdout.strip()) and not r.stdout.strip().startswith('Z')
def stop_verified(record):
 if record['boot']!=boot_identity() or (running(record['pid']) and record['start']!=start_identity(record['pid'])):return False
 if running(record['pid']):
  os.killpg(record['pgid'],signal.SIGTERM)
  deadline=time.monotonic()+.2
  while running(record['pid']) and time.monotonic()<deadline:time.sleep(.01)
  if running(record['pid']):os.killpg(record['pgid'],signal.SIGKILL)
 deadline=time.monotonic()+3
 while any(running(pid) for pid in record['members']) and time.monotonic()<deadline:time.sleep(.02)
 return not any(running(pid) for pid in record['members'])
if __name__=='__main__':
 if sys.argv[1]=='child':
  signal.signal(signal.SIGTERM,signal.SIG_IGN)
  nested=subprocess.Popen([sys.executable,'-c','import signal,time;signal.signal(signal.SIGTERM,signal.SIG_IGN);time.sleep(60)'])
  record={'pid':os.getpid(),'pgid':os.getpgrp(),'members':[os.getpid(),nested.pid],'boot':boot_identity(),'start':start_identity(os.getpid())}
  durable(sys.argv[2],json.dumps(record).encode());time.sleep(60)
 else:
  subprocess.Popen([sys.executable,__file__,'child',sys.argv[2]],start_new_session=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  deadline=time.monotonic()+5
  while not Path(sys.argv[2]).exists():
   if time.monotonic()>deadline:raise RuntimeError('child identity unavailable; check process-inspection permission')
   time.sleep(.01)
  os._exit(92)
