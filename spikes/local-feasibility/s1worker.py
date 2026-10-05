import sys,time
from core import Store
s=Store(sys.argv[1]);claim=s.claim()
if claim:
 job,fence=claim
 for stage in ['Planning scenes','Creating narration','Preparing timing']:
  s.progress(job,stage);time.sleep(.12)
 s.finish(job,fence,confirmed=True)
