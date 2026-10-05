"""Disposable invariant witness. Not a production schema/service or provider adapter."""
import contextlib, hashlib, io, json, os, sqlite3, time, uuid, wave
from pathlib import Path

SCHEMA = '''
CREATE TABLE meta(key TEXT PRIMARY KEY,value TEXT NOT NULL);
CREATE TABLE account(id INTEGER PRIMARY KEY,cap INTEGER NOT NULL,held INTEGER NOT NULL DEFAULT 0,spent INTEGER NOT NULL DEFAULT 0,allowance INTEGER NOT NULL,allowheld INTEGER NOT NULL DEFAULT 0,consumed INTEGER NOT NULL DEFAULT 0);
CREATE TABLE projects(id INTEGER PRIMARY KEY,owner INTEGER NOT NULL,deleted INTEGER,purged INTEGER NOT NULL DEFAULT 0,render_job TEXT);
CREATE TABLE scenes(id INTEGER PRIMARY KEY,project INTEGER NOT NULL REFERENCES projects(id),words TEXT NOT NULL,rev INTEGER NOT NULL DEFAULT 0,voice TEXT NOT NULL DEFAULT 'default',delivery TEXT NOT NULL DEFAULT 'calm',selected TEXT,timing TEXT,caption TEXT,manual_timing TEXT,manual_caption TEXT,outdated INTEGER NOT NULL DEFAULT 0);
CREATE TABLE jobs(id TEXT PRIMARY KEY,project INTEGER NOT NULL REFERENCES projects(id),command TEXT NOT NULL UNIQUE,state TEXT NOT NULL,kind TEXT NOT NULL,scene INTEGER REFERENCES scenes(id),input_rev INTEGER NOT NULL,cancel INTEGER NOT NULL DEFAULT 0,fence INTEGER NOT NULL DEFAULT 0,maximum INTEGER NOT NULL DEFAULT 100);
CREATE TABLE lane(id INTEGER PRIMARY KEY CHECK(id=1),job TEXT REFERENCES jobs(id),fence INTEGER NOT NULL DEFAULT 0,guard TEXT NOT NULL DEFAULT 'clear',child INTEGER);
CREATE TABLE attempts(id TEXT PRIMARY KEY,job TEXT NOT NULL REFERENCES jobs(id),state TEXT NOT NULL,cost INTEGER NOT NULL DEFAULT 100,registered INTEGER NOT NULL DEFAULT 0);
CREATE TABLE artifacts(id TEXT PRIMARY KEY,project INTEGER NOT NULL REFERENCES projects(id),scene INTEGER REFERENCES scenes(id),attempt TEXT UNIQUE REFERENCES attempts(id),kind TEXT NOT NULL,key TEXT NOT NULL UNIQUE,hash TEXT NOT NULL,words TEXT,voice TEXT,delivery TEXT,source TEXT,range_start INTEGER,range_end INTEGER,valid INTEGER NOT NULL CHECK(valid=1),input_rev INTEGER NOT NULL);
CREATE TABLE selections(project INTEGER NOT NULL REFERENCES projects(id),slot TEXT NOT NULL,artifact TEXT NOT NULL REFERENCES artifacts(id),PRIMARY KEY(project,slot));
CREATE TABLE ledger(event TEXT PRIMARY KEY,kind TEXT NOT NULL,amount INTEGER NOT NULL);
CREATE TABLE progress(seq INTEGER PRIMARY KEY,job TEXT NOT NULL REFERENCES jobs(id),stage TEXT NOT NULL);
'''

def durable(path, data):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + '.tmp')
    with open(tmp, 'wb') as f:
        f.write(data); f.flush(); os.fsync(f.fileno())
    os.replace(tmp, path)
    fd = os.open(path.parent, os.O_RDONLY)
    try: os.fsync(fd)
    finally: os.close(fd)

def wav_bytes():
    out = io.BytesIO()
    with wave.open(out, 'wb') as w:
        w.setparams((1, 2, 8000, 8000, 'NONE', 'not compressed')); w.writeframes(b'\x00\x00' * 8000)
    return out.getvalue()

class Store:
    def __init__(self, root):
        self.root = Path(root); self.db = self.root / 'state.sqlite3'; self.media = self.root / 'media'
    def connection(self):
        c = sqlite3.connect(self.db, timeout=5, isolation_level=None)
        c.row_factory = sqlite3.Row
        c.execute('PRAGMA foreign_keys=ON'); c.execute('PRAGMA synchronous=FULL'); c.execute('PRAGMA busy_timeout=5000')
        return c
    @contextlib.contextmanager
    def tx(self):
        c = self.connection()
        try:
            c.execute('BEGIN IMMEDIATE'); yield c; c.commit()
        except BaseException:
            c.rollback(); raise
        finally: c.close()
    def initialize(self):
        self.root.mkdir(parents=True, exist_ok=True); self.media.mkdir(exist_ok=True)
        c = self.connection(); c.execute('PRAGMA journal_mode=WAL'); c.executescript(SCHEMA)
        c.execute("INSERT INTO meta VALUES('reconciled','1')")
        c.execute('INSERT INTO account(id,cap,allowance) VALUES(1,10000,10000)')
        c.executemany('INSERT INTO projects(id,owner) VALUES(?,?)', [(1,1),(2,2)])
        c.executemany('INSERT INTO scenes(id,project,words) VALUES(?,?,?)',[(1,1,'First approved words.'),(2,1,'Sibling approved words.'),(3,2,'Other private project.')])
        c.execute('INSERT INTO lane(id) VALUES(1)'); c.close()
    def read(self, sql, args=()):
        with contextlib.closing(self.connection()) as c:
            return [dict(r) for r in c.execute(sql,args)]
    def project(self, c, project, owner=None):
        p = c.execute('SELECT * FROM projects WHERE id=?',(project,)).fetchone()
        if not p or p['deleted'] is not None or p['purged'] or (owner is not None and p['owner'] != owner): raise PermissionError('private/deleted project')
        return p
    def edit(self, scene, revision, words, owner=1):
        with self.tx() as c:
            s = c.execute('SELECT * FROM scenes WHERE id=?',(scene,)).fetchone()
            if not s: raise PermissionError('unknown scene')
            p = self.project(c,s['project'],owner)
            if p['render_job']: return 'locked'
            changed = c.execute('UPDATE scenes SET words=?,rev=rev+1,outdated=1 WHERE id=? AND rev=?',(words,scene,revision)).rowcount
            return 'saved' if changed else 'conflict'
    def admit(self, command, scene=1, owner=1, kind='generate', maximum=100):
        with self.tx() as c:
            if c.execute("SELECT value FROM meta WHERE key='reconciled'").fetchone()[0] != '1': return 'reconciliation_required'
            s = c.execute('SELECT * FROM scenes WHERE id=?',(scene,)).fetchone(); self.project(c,s['project'],owner)
            old = c.execute('SELECT id FROM jobs WHERE command=?',(f'{owner}:{s["project"]}:{command}',)).fetchone()
            if old: return old[0]
            a = c.execute('SELECT * FROM account WHERE id=1').fetchone()
            if a['spent']+a['held']+maximum>a['cap'] or a['consumed']+a['allowheld']+maximum>a['allowance']:return 'budget_blocked'
            job = uuid.uuid4().hex
            c.execute('INSERT INTO jobs(id,project,command,state,kind,scene,input_rev,maximum) VALUES(?,?,?,?,?,?,?,?)',(job,s['project'],f'{owner}:{s["project"]}:{command}','queued',kind,scene,s['rev'],maximum))
            c.execute('UPDATE account SET held=held+?,allowheld=allowheld+? WHERE id=1',(maximum,maximum))
            c.execute('INSERT INTO ledger VALUES(?,?,?)',('reserve:'+job,'reserve',maximum)); return job
    def claim(self):
        with self.tx() as c:
            lane = c.execute('SELECT * FROM lane WHERE id=1').fetchone()
            if lane['job'] or lane['guard']!='clear':return None
            job = c.execute("SELECT j.* FROM jobs j JOIN projects p ON p.id=j.project JOIN scenes s ON s.id=j.scene WHERE j.state='queued' AND j.cancel=0 AND p.deleted IS NULL AND p.purged=0 AND s.rev=j.input_rev ORDER BY j.rowid LIMIT 1").fetchone()
            if not job:return None
            fence=lane['fence']+1
            c.execute("UPDATE lane SET job=?,fence=?,guard='active' WHERE id=1",(job['id'],fence))
            c.execute("UPDATE jobs SET state='running',fence=? WHERE id=?",(fence,job['id']))
            if job['kind']=='render':c.execute('UPDATE projects SET render_job=? WHERE id=?',(job['id'],job['project']))
            return job['id'],fence
    def owns(self,c,job,fence):
        lane=c.execute('SELECT * FROM lane WHERE id=1').fetchone();j=c.execute('SELECT * FROM jobs WHERE id=?',(job,)).fetchone()
        return bool(j and lane['job']==job and lane['fence']==fence and not j['cancel'] and lane['guard']=='active')
    def prepare(self,job,fence,attempt):
        with self.tx() as c:
            if not self.owns(c,job,fence):raise PermissionError('fenced/canceled')
            c.execute("INSERT OR IGNORE INTO attempts(id,job,state) VALUES(?,?,'prepared')",(attempt,job))
    def attempt_state(self,attempt,state):
        with self.tx() as c:c.execute('UPDATE attempts SET state=? WHERE id=?',(state,attempt))
    def progress(self,job,stage):
        with self.tx() as c:c.execute('INSERT INTO progress(job,stage) VALUES(?,?)',(job,stage))
    def cancel(self,job):
        with self.tx() as c:c.execute("UPDATE jobs SET cancel=1,state='cancelling' WHERE id=? AND state IN ('running','queued','recovery_required')",(job,))
    def finish(self,job,fence,confirmed=False):
        with self.tx() as c:
            lane=c.execute('SELECT * FROM lane WHERE id=1').fetchone()
            if lane['job']!=job or lane['fence']!=fence:return False
            if not confirmed:return False
            c.execute("UPDATE jobs SET state=CASE WHEN cancel=1 THEN 'cancelled' ELSE 'completed' END WHERE id=?",(job,))
            c.execute('UPDATE projects SET render_job=NULL WHERE render_job=?',(job,))
            c.execute("UPDATE lane SET job=NULL,guard='clear',child=NULL WHERE id=1")
            return True
    def uncertainty(self,job):
        with self.tx() as c:
            c.execute("UPDATE lane SET guard='unknown' WHERE job=?",(job,))
            c.execute("UPDATE jobs SET state='recovery_required' WHERE id=?",(job,))
    def delete(self,project,now,owner=1):
        with self.tx() as c:
            p=self.project(c,project,owner)
            busy=c.execute("SELECT 1 FROM jobs WHERE project=? AND state IN ('running','cancelling','recovery_required')",(project,)).fetchone()
            if p['render_job'] or busy:return 'busy'
            c.execute('UPDATE projects SET deleted=? WHERE id=?',(now,project))
            queued=c.execute("SELECT * FROM jobs WHERE project=? AND state='queued'",(project,)).fetchall()
            for j in queued:
                c.execute("UPDATE jobs SET cancel=1,state='cancelled' WHERE id=?",(j['id'],))
                c.execute('UPDATE account SET held=held-?,allowheld=allowheld-? WHERE id=1',(j['maximum'],j['maximum']))
            return 'deleted'
    def register(self,attempt,kind='audio',crash_inside=False):
        """Metadata and financial delivery atomically registered; selection separate."""
        manifest=json.loads((self.root/'spool'/f'{attempt}.json').read_text());path=self.media/manifest['key']
        payload=path.read_bytes()
        if hashlib.sha256(payload).hexdigest()!=manifest['hash']:raise ValueError('bytes changed')
        if kind=='audio':
            with wave.open(io.BytesIO(payload)) as w:
                if w.getnframes()==0:raise ValueError('empty audio')
        elif not payload.startswith(b'EXPORT-FIXTURE:'):raise ValueError('invalid synthetic export')
        with self.tx() as c:
            a=c.execute('SELECT * FROM attempts WHERE id=?',(attempt,)).fetchone();j=c.execute('SELECT * FROM jobs WHERE id=?',(a['job'],)).fetchone()
            if a['registered']:return attempt
            c.execute('INSERT INTO artifacts VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(attempt,j['project'],j['scene'],attempt,kind,manifest['key'],manifest['hash'],manifest['words'],manifest['voice'],'calm',manifest.get('source'),manifest.get('start',0),manifest.get('end',8000),1,j['input_rev']))
            if crash_inside:os._exit(91)
            # Known fake charge = 100 integer cents, not a provider price.
            c.execute('INSERT INTO ledger VALUES(?,?,?)',('delivery:'+attempt,'delivered',a['cost']))
            c.execute('UPDATE account SET spent=spent+?,consumed=consumed+?,held=held-?,allowheld=allowheld-? WHERE id=1',(a['cost'],a['cost'],j['maximum'],j['maximum']))
            c.execute("UPDATE attempts SET registered=1,state='registered' WHERE id=?",(attempt,));return attempt
    def select(self,attempt,fence):
        rows=self.read('SELECT * FROM artifacts WHERE id=?',(attempt,))
        if not rows:return False
        asset=rows[0]
        try:
            if hashlib.sha256((self.media/asset['key']).read_bytes()).hexdigest()!=asset['hash']:return False
        except OSError:return False
        manifest=json.loads((self.root/'spool'/f'{attempt}.json').read_text())
        with self.tx() as c:
            a=c.execute('SELECT * FROM artifacts WHERE id=?',(attempt,)).fetchone();j=c.execute('SELECT j.* FROM jobs j JOIN attempts t ON t.job=j.id WHERE t.id=?',(attempt,)).fetchone()
            if not a or not self.owns(c,j['id'],fence):return False
            p=c.execute('SELECT * FROM projects WHERE id=?',(a['project'],)).fetchone();scene=c.execute('SELECT * FROM scenes WHERE id=?',(a['scene'],)).fetchone()
            if p['deleted'] is not None or p['purged'] or scene['project']!=a['project'] or scene['rev']!=a['input_rev']:return False
            for member in manifest.get('members',[]):
                current=c.execute('SELECT project,rev FROM scenes WHERE id=?',(member['id'],)).fetchone()
                if not current or current['project']!=a['project'] or current['rev']!=member['rev']:return False
            slot='export' if a['kind']=='export' else 'audio:'+str(a['scene'])
            c.execute('INSERT INTO selections VALUES(?,?,?) ON CONFLICT(project,slot) DO UPDATE SET artifact=excluded.artifact',(a['project'],slot,a['id']))
            if a['kind']=='audio':c.execute('UPDATE scenes SET selected=?,outdated=0 WHERE id=?',(a['id'],a['scene']))
            return True
    def audit(self):
        with contextlib.closing(self.connection()) as c:
            assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
            assert not c.execute('PRAGMA foreign_key_check').fetchall()
            a=dict(c.execute('SELECT * FROM account WHERE id=1').fetchone())
            assert min(a['held'],a['allowheld'],a['spent'],a['consumed'])>=0
            assert a['held']+a['spent']<=a['cap'] and a['allowheld']+a['consumed']<=a['allowance']
            for r in c.execute('SELECT * FROM artifacts'):
                assert hashlib.sha256((self.media/r['key']).read_bytes()).hexdigest()==r['hash']
            assert c.execute("SELECT count(*) FROM jobs WHERE state='running'").fetchone()[0]<=1
            return a
