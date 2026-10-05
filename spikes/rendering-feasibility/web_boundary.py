"""S6: Django command/status remain short while separate worker renders 10 min."""
import json,sqlite3,subprocess,time,sys,os,signal
from pathlib import Path
import django
sys.path.append('/private/tmp/s6-render-venv/lib/python3.12/site-packages')
import psutil
from django.conf import settings
from django.http import JsonResponse
from django.test import Client
from django.urls import path

ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'docs/architecture/evidence/rendering-feasibility/S6'
DB=OUT/'web-boundary.sqlite3'
settings.configure(SECRET_KEY='local-disposable-s6-not-production',ROOT_URLCONF=__name__,ALLOWED_HOSTS=['testserver'],MIDDLEWARE=[],INSTALLED_APPS=[])
django.setup()
with sqlite3.connect(DB) as db:
    db.execute('CREATE TABLE IF NOT EXISTS jobs (id INTEGER PRIMARY KEY,state TEXT)')
def command(request):
    with sqlite3.connect(DB) as db:db.execute("INSERT INTO jobs VALUES (1,'QUEUED') ON CONFLICT(id) DO NOTHING")
    return JsonResponse({'job':1,'state':'QUEUED'},status=202)
def status(request):
    with sqlite3.connect(DB) as db:row=db.execute('SELECT state FROM jobs WHERE id=1').fetchone()
    return JsonResponse({'state':row[0]})
urlpatterns=[path('command',command),path('status',status)]
def main():
    # Recover an observer crash before replacing durable queue state. Exact
    # internal worker argv identifies this spike's child, not arbitrary processes.
    expected=['/private/tmp/s6-render-venv/bin/python',str(ROOT/'spikes/rendering-feasibility/s6.py'),'benchmark','--duration','600']
    recovered=[]
    for proc in psutil.process_iter(['pid','cmdline']):
        try:
            if proc.info['cmdline']==expected:
                members=proc.children(recursive=True)+[proc]
                for member in members:
                    try:os.killpg(os.getpgid(member.pid),signal.SIGTERM)
                    except ProcessLookupError:pass
                gone,alive=psutil.wait_procs(members,timeout=2)
                for member in alive:
                    if member.status()!=psutil.STATUS_ZOMBIE:os.killpg(os.getpgid(member.pid),signal.SIGKILL)
                assert not any(p.is_running() and p.status()!=psutil.STATUS_ZOMBIE for p in alive)
                recovered.append(proc.pid)
        except (psutil.NoSuchProcess,psutil.AccessDenied):continue
    with sqlite3.connect(DB) as db:db.execute('DELETE FROM jobs')
    client=Client();start=time.monotonic();response=client.post('/command');admission=time.monotonic()-start
    assert response.status_code==202
    # Dispatcher/worker launch is explicitly outside command(request).
    with sqlite3.connect(DB) as db:db.execute("UPDATE jobs SET state='RUNNING'")
    cmd=['/private/tmp/s6-render-venv/bin/python',str(ROOT/'spikes/rendering-feasibility/s6.py'),'benchmark','--duration','600']
    with (OUT/'worker-600.log').open('w') as log:
        worker=subprocess.Popen(cmd,stdout=log,stderr=log,start_new_session=True)
        (OUT/'worker-identity.json').write_text(json.dumps(dict(pid=worker.pid,process_start=psutil.Process(worker.pid).create_time(),pgid=os.getpgid(worker.pid),argv=cmd))+'\n')
        timings=[];resources=[]
        while worker.poll() is None:
            begin=time.monotonic();r=client.get('/status');timings.append(time.monotonic()-begin)
            assert r.status_code==200 and r.json()['state']=='RUNNING'
            try:
                proc=psutil.Process(worker.pid);members=[proc]+proc.children(recursive=True)
                resources.append(dict(worker_rss=proc.memory_info().rss,process_tree_rss=sum(p.memory_info().rss for p in members)))
            except (psutil.NoSuchProcess,psutil.AccessDenied,PermissionError):pass
            time.sleep(.25)
    with sqlite3.connect(DB) as db:db.execute("UPDATE jobs SET state=?",('COMPLETED' if worker.returncode==0 else 'FAILED',))
    result=dict(status='PASS' if worker.returncode==0 else 'FAIL',django_version=django.get_version(),admission_seconds=admission,status_requests=len(timings),max_status_seconds=max(timings),average_status_seconds=sum(timings)/len(timings),worker_pid=worker.pid,worker_exit=worker.returncode,argv=cmd,http_request_held_open=False,recovered_observer_crash_workers=recovered,resource_samples=len(resources),peak_worker_rss_bytes=max((x['worker_rss'] for x in resources),default=None),peak_process_tree_rss_bytes=max((x['process_tree_rss'] for x in resources),default=None),limits='Django test client, no browser/load/network isolation proof; SQLite queue witness only')
    (OUT/'web-boundary-results.json').write_text(json.dumps(result,indent=2)+'\n')
    assert worker.returncode==0,(OUT/'worker-600.log').read_text()[-2000:]
    print(json.dumps(result))
if __name__=='__main__':main()
