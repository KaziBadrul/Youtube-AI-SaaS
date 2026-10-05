"""Crashable fake worker/publication protocol, never a live provider integration."""
import hashlib,io,json,os,sqlite3,sys,time,wave
from pathlib import Path
from core import Store,durable,wav_bytes

PHASES=['prepared','before_submission','submission_started','response_received','staged','validated','installed','metadata_registered','financial_registered','selected','export_published']

def checkpoint(phase,stop):
 if phase==stop:os._exit(91)

class FakeProvider:
 def __init__(self,root):
  self.path=Path(root)/'provider.sqlite3'
  with self.connection() as c:c.execute('CREATE TABLE IF NOT EXISTS calls(seq INTEGER PRIMARY KEY,attempt TEXT,state TEXT,payload BLOB,cost INTEGER)')
 def connection(self):return sqlite3.connect(self.path,timeout=5)
 def begin(self,attempt):
  with self.connection() as c:c.execute("INSERT INTO calls(attempt,state,cost) VALUES(?,'in_flight',100)",(attempt,))
 def complete(self,attempt,kind='audio'):
  data=wav_bytes() if kind=='audio' else b'EXPORT-FIXTURE:new fully validated synthetic export'
  with self.connection() as c:c.execute("UPDATE calls SET state='complete',payload=? WHERE attempt=?",(data,attempt))
  return data
 def fail(self,attempt):
  with self.connection() as c:c.execute("UPDATE calls SET state='failed',cost=40 WHERE attempt=?",(attempt,))
 def lookup(self,attempt):
  with self.connection() as c:
   c.row_factory=sqlite3.Row;r=c.execute('SELECT * FROM calls WHERE attempt=? ORDER BY seq LIMIT 1',(attempt,)).fetchone();return dict(r) if r else None
 def count(self,attempt):
  with self.connection() as c:return c.execute('SELECT count(*) FROM calls WHERE attempt=?',(attempt,)).fetchone()[0]

def install(store,attempt,data,kind,stop=None):
 job=store.read('SELECT j.* FROM jobs j JOIN attempts a ON a.job=j.id WHERE a.id=?',(attempt,))[0]
 scene=store.read('SELECT * FROM scenes WHERE id=?',(job['scene'],))[0]
 # Pin original words/configuration once; never rebuild provenance from edited scene.
 manifest_path=store.root/'spool'/f'{attempt}.json'
 if manifest_path.exists():manifest=json.loads(manifest_path.read_text())
 else:
  manifest={'key':attempt+'.'+('wav' if kind=='audio' else 'bin'),'hash':hashlib.sha256(data).hexdigest(),'words':scene['words'],'voice':scene['voice'],'source':'shared-source','start':0,'end':4000}
  durable(manifest_path,json.dumps(manifest).encode())
 checkpoint('response_received',stop)
 stage=store.root/'spool'/f'{attempt}.bytes';durable(stage,data);checkpoint('staged',stop)
 if kind=='audio':
  with wave.open(io.BytesIO(data)) as w:
   if w.getnframes()!=8000:raise ValueError('fixture decode/frames failed')
 elif not data.startswith(b'EXPORT-FIXTURE:'):raise ValueError('invalid synthetic export')
 if hashlib.sha256(data).hexdigest()!=manifest['hash']:raise ValueError('immutable response mismatch')
 checkpoint('validated',stop)
 durable(store.media/manifest['key'],data);checkpoint('installed',stop)
 store.register(attempt,kind,crash_inside=stop=='inside_registration');checkpoint('metadata_registered',stop);checkpoint('financial_registered',stop)
 return job

def settle_known_failure(store,attempt,cost):
 with store.tx() as c:
  a=c.execute('SELECT * FROM attempts WHERE id=?',(attempt,)).fetchone();j=c.execute('SELECT * FROM jobs WHERE id=?',(a['job'],)).fetchone()
  inserted=c.execute('INSERT OR IGNORE INTO ledger VALUES(?,?,?)',('failure:'+attempt,'failure',cost)).rowcount
  if inserted:
   c.execute('UPDATE account SET spent=spent+?,held=held-?,allowheld=allowheld-? WHERE id=1',(cost,j['maximum'],j['maximum']))
   c.execute("UPDATE attempts SET state='failed' WHERE id=?",(attempt,));c.execute("UPDATE jobs SET state='failed' WHERE id=?",(j['id'],));c.execute("UPDATE lane SET job=NULL,guard='clear' WHERE job=?",(j['id'],))

def execute(root,job,fence,attempt,stop=None,kind='audio',behavior='success'):
 store=Store(root);provider=FakeProvider(root);store.prepare(job,fence,attempt)
 # Pin provenance before external execution, not from current text on recovery.
 scene=store.read('SELECT s.* FROM scenes s JOIN jobs j ON j.scene=s.id WHERE j.id=?',(job,))[0]
 durable(store.root/'spool'/f'{attempt}.json',json.dumps({'key':attempt+'.'+('wav' if kind=='audio' else 'bin'),'hash':hashlib.sha256(wav_bytes() if kind=='audio' else b'EXPORT-FIXTURE:new fully validated synthetic export').hexdigest(),'words':scene['words'],'voice':scene['voice'],'source':'shared-source','start':0,'end':4000}).encode())
 checkpoint('prepared',stop)
 # Submission intent committed first. A crash here is ambiguous without independent evidence.
 store.attempt_state(attempt,'submitting');checkpoint('before_submission',stop)
 if behavior=='timeout_before':settle_known_failure(store,attempt,0);return 'definite_zero_submission'
 with store.tx() as c:
  if not store.owns(c,job,fence):raise PermissionError('lost authority before external call')
 provider.begin(attempt);checkpoint('submission_started',stop)
 if behavior in ['timeout_after','delayed']:
  store.uncertainty(job);return 'unknown'
 if behavior=='definite_failure':provider.fail(attempt);settle_known_failure(store,attempt,40);return 'known_failure'
 data=provider.complete(attempt,kind);install(store,attempt,data,kind,stop)
 store.select(attempt,fence);checkpoint('selected',stop)
 if kind=='export':checkpoint('export_published',stop)
 store.finish(job,fence,confirmed=True);return 'complete'

def recover(root,attempt,fence,kind='audio'):
 store=Store(root);provider=FakeProvider(root);a=store.read('SELECT * FROM attempts WHERE id=?',(attempt,))[0]
 receipt=provider.lookup(attempt);stage=store.root/'spool'/f'{attempt}.bytes'
 if receipt and receipt['state']=='failed':settle_known_failure(store,attempt,receipt['cost']);return 'known_failure'
 if not (receipt and receipt['state']=='complete') and not stage.exists():
  store.uncertainty(a['job']);return 'unknown'
 data=stage.read_bytes() if stage.exists() else receipt['payload']
 install(store,attempt,data,kind)
 with store.tx() as c:
  # A completed authoritative fake outcome proves no remote execution still exists.
  c.execute("UPDATE lane SET guard='active' WHERE job=? AND fence=?",(a['job'],fence))
 selected=store.select(attempt,fence);store.finish(a['job'],fence,confirmed=True)
 return 'selected' if selected else 'history'

if __name__=='__main__':
 args=sys.argv[1:];print(execute(args[0],args[1],int(args[2]),args[3],args[4] if len(args)>4 else None,args[5] if len(args)>5 else 'audio',args[6] if len(args)>6 else 'success'))
