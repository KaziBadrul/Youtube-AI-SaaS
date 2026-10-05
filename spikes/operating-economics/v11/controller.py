"""Disposable whole-guest resource witness; no production/provider authority."""
import hashlib,json,os,platform,signal,sqlite3,subprocess,sys,threading,time,urllib.request
from pathlib import Path
import psutil
O=Path('/out'); O.mkdir(exist_ok=True)
R=Path('/work'); stage='guest_idle'; done=threading.Event(); samples=[]; probes=[]; results=[]
def dump(name,value): (O/name).write_text(json.dumps(value,indent=2)+'\n')
def text(path): return Path(path).read_text()
def cmd(args):
    p=subprocess.run(args,capture_output=True,text=True)
    return {'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
def meminfo():
    return {x.split(':')[0]:int(x.split()[1])*1024 for x in text('/proc/meminfo').splitlines()}
def vmstat(): return {x.split()[0]:int(x.split()[1]) for x in text('/proc/vmstat').splitlines()}
def diskbytes():
    size=0
    for p in O.rglob('*'):
        try:
            if p.is_file() and not p.is_symlink():size+=p.stat().st_size
        except FileNotFoundError: pass
    return size
def sample():
    while not done.is_set():
        m=meminfo(); v=vmstat(); d=psutil.disk_usage('/'); rss=0; apps=0
        own=psutil.Process().children(recursive=True)
        for p in psutil.process_iter(['memory_info']):
            try:rss+=p.info['memory_info'].rss
            except (psutil.NoSuchProcess,psutil.AccessDenied):pass
        for p in own:
            try:apps+=p.memory_info().rss
            except (psutil.NoSuchProcess,psutil.AccessDenied):pass
        apps+=psutil.Process().memory_info().rss
        x={'time':time.monotonic(),'phase':stage,'meminfo':m,'whole_used_minus_available':m['MemTotal']-m['MemAvailable'],
           'whole_used_minus_free':m['MemTotal']-m['MemFree'],'available_percent':100*m['MemAvailable']/m['MemTotal'],
           'swap_used':m['SwapTotal']-m['SwapFree'],'vmstat':{k:v[k] for k in ['pswpin','pswpout','oom_kill','pgmajfault']},
           'psi':{k:text('/proc/pressure/'+k) for k in ['memory','cpu','io']},'all_process_rss_sum':rss,'application_tree_rss_sum':apps,
           'disk_used':d.used,'disk_free':d.free,'output_bytes':diskbytes(),'cpu_times':psutil.cpu_times()._asdict()}
        samples.append(x)
        with (O/'telemetry.jsonl').open('a') as f:f.write(json.dumps(x)+'\n')
        done.wait(.1)
def probe():
    while not done.is_set():
        start=time.monotonic()
        try:
            with urllib.request.urlopen('http://127.0.0.1:8080/status',timeout=5) as f:
                body=json.load(f); assert f.status==200 and 'job' in body
            p={'time':start,'phase':stage,'seconds':time.monotonic()-start,'ok':True}
        except Exception as e:p={'time':start,'phase':stage,'seconds':time.monotonic()-start,'ok':False,'error':repr(e)}
        probes.append(p)
        with (O/'probes.jsonl').open('a') as f:f.write(json.dumps(p)+'\n')
        done.wait(.25)
def state(name,status='running'):
    global stage
    stage=name
    with sqlite3.connect('/out/state.sqlite3') as db:db.execute('INSERT INTO job(phase,status) VALUES(?,?)',(name,status))
def phase(name,timeout=3600):
    state(name); start=time.monotonic()
    with (O/(name+'.log')).open('wb') as log:
        p=subprocess.Popen([sys.executable,str(R/'phase.py'),name],stdout=log,stderr=log,start_new_session=True)
        try:p.wait(timeout=timeout)
        except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);p.wait()
    result={'phase':name,'pid':p.pid,'exit':p.returncode,'start':start,'end':time.monotonic(),'wall_seconds':time.monotonic()-start,'status':'PASS' if p.returncode==0 else 'FAIL'}
    results.append(result);dump('phases.json',results); return result
def cancel():
    state('cancellation'); start=time.monotonic()
    previous=json.loads((O/'render-result.json').read_text()) if (O/'render-result.json').exists() else None
    with sqlite3.connect('/out/state.sqlite3') as db:db.execute('UPDATE render_lane SET locked=1 WHERE id=1')
    with (O/'cancel.log').open('wb') as log:
        p=subprocess.Popen(['ffmpeg','-v','error','-y','-re','-f','lavfi','-i','testsrc2=size=1920x1080:rate=30','-t','600','-c:v','libx264','-threads','2','-preset','ultrafast',str(O/'cancelled-incomplete.mp4')],stdout=log,stderr=log,start_new_session=True)
    time.sleep(2); pgid=os.getpgid(p.pid); identity=psutil.Process(p.pid).create_time()
    with urllib.request.urlopen('http://127.0.0.1:8080/status',timeout=5) as response:assert response.status==200
    requested=time.monotonic(); os.killpg(pgid,signal.SIGTERM); escalated=False
    try:p.wait(timeout=3)
    except subprocess.TimeoutExpired:escalated=True;os.killpg(pgid,signal.SIGKILL);p.wait(timeout=3)
    live=[]
    for q in psutil.process_iter(['status']):
        try:
            if os.getpgid(q.pid)==pgid and q.info['status']!='zombie':live.append(q.pid)
        except (ProcessLookupError,psutil.NoSuchProcess):pass
    assert not live
    with sqlite3.connect('/out/state.sqlite3') as db:
        assert db.execute('SELECT locked FROM render_lane').fetchone()[0]==1
        db.execute('UPDATE render_lane SET locked=0 WHERE id=1')
    preserved=previous is not None and hashlib.sha256(Path(previous['result']['output']).read_bytes()).hexdigest()==previous['result']['sha256']
    registry=json.loads((O/'s6/export-registrations.json').read_text()) if (O/'s6/export-registrations.json').exists() else {}
    assert preserved and len(registry)==1
    receipt={'status':'PASS','pid':p.pid,'start_identity':identity,'pgid':pgid,'exit':p.returncode,'cessation_seconds':time.monotonic()-requested,
             'escalated':escalated,'live_group_members':live,'lock_released_after_confirmed_cessation':True,'incomplete_registered':False,'previous_export_preserved':preserved,'status_request_during_render_succeeded':True}
    dump('cancellation-result.json',receipt);results.append({'phase':'cancellation','start':start,'end':time.monotonic(),'wall_seconds':time.monotonic()-start,**receipt})
def main():
    assert os.cpu_count()==2
    m=meminfo(); assert 3.8*1024**3 < m['MemTotal'] <= 4*1024**3
    assert m['SwapTotal']==0 and len(text('/proc/swaps').splitlines())==1
    env={'machine':platform.machine(),'platform':platform.platform(),'python':sys.version,'cpu_count':os.cpu_count(),'meminfo':m,
         'os_release':text('/etc/os-release'),'kernel':cmd(['uname','-a']),'lscpu':cmd(['lscpu']),'findmnt':cmd(['findmnt','-T','/out']),
         'swaps':text('/proc/swaps'),'services':cmd(['systemctl','list-units','--type=service','--state=running','--no-pager']),
         'disk':psutil.disk_usage('/')._asdict(),'ffmpeg':cmd(['ffmpeg','-version']),'packages':cmd([sys.executable,'-m','pip','freeze']),
         'kernel_log_before':cmd(['dmesg']),'vmstat_before':vmstat(),'network':'private VM; web loopback; no provider SDK/keys; models offline',
         'measure':'GLOBAL /proc/meminfo includes guest kernel/services/cache; not container cgroup','sample_interval_seconds':.1}
    dump('environment.json',env)
    with sqlite3.connect('/out/state.sqlite3') as db:
        assert db.execute('PRAGMA journal_mode=WAL').fetchone()[0]=='wal'
        db.execute('CREATE TABLE job(id INTEGER PRIMARY KEY,phase TEXT,status TEXT)')
        db.execute('CREATE TABLE render_lane(id INTEGER PRIMARY KEY,locked INTEGER)');db.execute('INSERT INTO render_lane VALUES(1,0)')
    sampler=threading.Thread(target=sample,daemon=True);sampler.start()
    time.sleep(10);state('application_idle')
    log=(O/'web.log').open('wb')
    web=subprocess.Popen([str(Path(sys.executable).parent/'gunicorn'),'--chdir',str(R),'--workers','1','--threads','2','--bind','127.0.0.1:8080','web:application'],stdout=log,stderr=log,start_new_session=True)
    for _ in range(100):
        try:urllib.request.urlopen('http://127.0.0.1:8080/status',timeout=.2).close();break
        except Exception:time.sleep(.1)
    else:raise RuntimeError('web did not start')
    prober=threading.Thread(target=probe,daemon=True);prober.start();time.sleep(10)
    errors=[]
    try:
        phase('alignment',1800)
        phase('render')
        if results[-1]['status']=='PASS':phase('validation')
        # Child wait is confirmed before maintenance: no overlapping heavy work.
        phase('backup',300)
        cancel()
        state('captions');p=subprocess.run([sys.executable,'-c','import sys;sys.path.insert(0,"/work");import phase;phase.captions()']);assert p.returncode==0
        state('complete','done')
        with sqlite3.connect('/out/state.sqlite3') as db:assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
    except Exception as e:errors.append(repr(e));state('error','failed')
    finally:
        done.set();sampler.join(5);prober.join(5)
        os.killpg(web.pid,signal.SIGTERM);web.wait(timeout=5)
        dump('kernel-after.json',{'dmesg':cmd(['dmesg']),'journal_kernel':cmd(['journalctl','-k','--no-pager']),'vmstat':vmstat()})
        dump('summary.json',{'phases':results,'errors':errors,'global_samples':len(samples),'probe_count':len(probes),'probe_failures':sum(not p['ok'] for p in probes),
                             'memory_total':m['MemTotal'],'whole_peak_used_minus_available':max(x['whole_used_minus_available'] for x in samples),
                             'minimum_available':min(x['meminfo']['MemAvailable'] for x in samples),'peak_swap':max(x['swap_used'] for x in samples),
                             'peak_disk_used':max(x['disk_used'] for x in samples),'disk_after':psutil.disk_usage('/')._asdict(),
                             'provider_generation_calls':0,'maintenance_serialized':True,'application_complete':all(p['status']=='PASS' for p in results) and len(results)==5 and not errors})
        print(json.dumps(json.loads((O/'summary.json').read_text())),flush=True)
if __name__=='__main__':main()
