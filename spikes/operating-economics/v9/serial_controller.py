"""Local Linux resource harness. No provider clients, no production authority."""
import hashlib,json,os,platform,signal,sqlite3,subprocess,sys,threading,time,urllib.request
from pathlib import Path
import psutil
O=Path('/out');O.mkdir(exist_ok=True);C=Path('/sys/fs/cgroup');R=Path('/repo/spikes/operating-economics/v9')
samples=[];latencies=[];errors=[];stage='startup';done=threading.Event()

def dump(name,obj):(O/name).write_text(json.dumps(obj,indent=2)+'\n')
def read(name):
    p=C/name
    return p.read_text().strip() if p.exists() else None

def counters(name):
    data=read(name)
    return {} if data is None else {line.split()[0]:int(line.split()[1]) for line in data.splitlines()}

def usage():
    size=0
    for p in O.rglob('*'):
        try:
            if p.is_file() and not p.is_symlink():size+=p.stat().st_size
        except FileNotFoundError:pass
    return size

def sampler():
    while not done.is_set():
        try:
            rss=0
            for p in psutil.process_iter(['memory_info']):
                try:rss+=p.info['memory_info'].rss
                except (psutil.NoSuchProcess,psutil.AccessDenied):pass
            samples.append({'time':time.monotonic(),'phase':stage,'memory_current':int(read('memory.current')),
                'memory_peak':int(read('memory.peak')) if read('memory.peak') else None,'cpu_stat':counters('cpu.stat'),
                'memory_events':counters('memory.events'),'process_rss_sum':rss,'output_disk_bytes':usage()})
        except Exception as e:errors.append('sampler '+repr(e))
        done.wait(.5)

def probe():
    while not done.is_set():
        started=time.monotonic()
        try:
            with urllib.request.urlopen('http://127.0.0.1:8080/status',timeout=5) as f:
                body=json.load(f);assert f.status==200 and 'job' in body
            latencies.append({'phase':stage,'seconds':time.monotonic()-started,'ok':True})
        except Exception as e:latencies.append({'phase':stage,'seconds':time.monotonic()-started,'ok':False,'error':repr(e)})
        done.wait(.25)

def state(phase,status):
    global stage
    stage=phase
    with sqlite3.connect('/out/state.sqlite3',timeout=5) as db:db.execute('INSERT INTO job(phase,status) VALUES(?,?)',(phase,status))

def launch(phase):
    log=(O/(phase+'.log')).open('wb')
    p=subprocess.Popen([sys.executable,str(R/'serial_phase.py'),phase],stdout=log,stderr=log,start_new_session=True)
    log.close();return p

def phase_result(name,p,start):
    return {'phase':name,'pid':p.pid,'exit':p.returncode,'wall_seconds':time.monotonic()-start,
        'status':'PASS' if p.returncode==0 else 'FAIL','log':name+'.log'}

def main():
    global stage
    requested=int(os.environ['EXPECTED_MEMORY_BYTES']); actual=int(read('memory.max'))
    assert 0<=requested-actual<os.sysconf('SC_PAGE_SIZE'),(requested,actual)
    assert read('memory.swap.max')=='0'
    assert read('cpu.max')==os.environ['EXPECTED_CPU_MAX']
    with sqlite3.connect('/out/state.sqlite3') as db:
        assert db.execute('PRAGMA journal_mode=WAL').fetchone()[0]=='wal'
        db.execute('CREATE TABLE IF NOT EXISTS job(id INTEGER PRIMARY KEY,phase TEXT,status TEXT)')
    env={'platform':platform.platform(),'machine':platform.machine(),'python':sys.version,'cpu.max':read('cpu.max'),
        'memory.max':read('memory.max'),'memory.swap.max':read('memory.swap.max'),'pids.max':read('pids.max'),
        'cgroup_start_cpu':counters('cpu.stat'),'cgroup_start_memory_events':counters('memory.events'),
        'ffmpeg':Path('/runtime-ffmpeg.txt').read_text(),'python_packages':Path('/runtime-python.txt').read_text(),
        'database_bytes':Path('/out/state.sqlite3').stat().st_size,
        'model_files':[{'name':p.name,'bytes':p.stat().st_size} for p in Path('/model').iterdir() if p.is_file()],
        'network':'none; loopback only','limitations':['application cgroup excludes Linux VM kernel/daemon','x86_64 emulation on arm64 Mac','no native host performance certification']}
    dump('environment.json',env)
    web=subprocess.Popen(['gunicorn','--chdir',str(R),'--workers','1','--threads','2','--bind','127.0.0.1:8080','web:application'],stdout=(O/'web.log').open('wb'),stderr=subprocess.STDOUT,start_new_session=True)
    for attempt in range(100):
        try:
            urllib.request.urlopen('http://127.0.0.1:8080/status',timeout=.2).close();break
        except Exception:time.sleep(.1)
    else:raise RuntimeError('web failed to become ready')
    sample=threading.Thread(target=sampler,daemon=True);sample.start()
    probes=threading.Thread(target=probe,daemon=True);probes.start()
    results=[]
    try:
        state('backup_standalone','running');started=time.monotonic();b=launch('backup');b.wait()
        result=phase_result('backup_standalone',b,started);results.append(result)
        if (O/'backup-result.json').exists():dump('backup-standalone-result.json',json.loads((O/'backup-result.json').read_text()))
        state('render','running');started=time.monotonic();p=launch('render');overlap=None;overlap_started=None
        while p.poll() is None:
            if False:  # serialized maintenance resource mode, no overlap admitted
                state('render_backup_overlap','running');overlap_started=time.monotonic();overlap=launch('backup')
            if overlap is not None and overlap.poll() is not None and stage=='render_backup_overlap':
                results.append(phase_result('backup_overlap',overlap,overlap_started));state('render','running')
                if overlap.returncode==0 and (O/'backup-result.json').exists():dump('backup-overlap-result.json',json.loads((O/'backup-result.json').read_text()))
            if time.monotonic()-started>3600:os.killpg(p.pid,signal.SIGTERM);p.wait(timeout=10);break
            time.sleep(.25)
        if overlap is not None and overlap.poll() is None:
            overlap.wait();results.append(phase_result('backup_overlap',overlap,overlap_started))
        results.append(phase_result('render',p,started))
        state('alignment','running');started=time.monotonic();p=launch('alignment');p.wait(timeout=1800);results.append(phase_result('alignment',p,started))
        state('cancellation','running')
        previous=json.loads((O/'render-result.json').read_text())['result']['sha256'] if (O/'render-result.json').exists() else None
        cancel=O/'cancelled-incomplete.mp4';log=(O/'cancel.log').open('wb')
        q=subprocess.Popen(['ffmpeg','-v','error','-y','-re','-f','lavfi','-i','testsrc2=size=1920x1080:rate=30','-t','600','-c:v','libx264','-preset','ultrafast',str(cancel)],stdout=log,stderr=log,start_new_session=True)
        time.sleep(2);start=time.monotonic();pgid=os.getpgid(q.pid);os.killpg(pgid,signal.SIGTERM);escalated=False
        try:q.wait(timeout=3)
        except subprocess.TimeoutExpired:escalated=True;os.killpg(pgid,signal.SIGKILL);q.wait(timeout=3)
        live=[]
        for proc in psutil.process_iter(['pid','status']):
            try:
                if os.getpgid(proc.pid)==pgid and proc.info['status']!='zombie':live.append(proc.pid)
            except (ProcessLookupError,psutil.NoSuchProcess):pass
        assert not live
        preserved=True
        if previous:
            path=Path(json.loads((O/'render-result.json').read_text())['result']['output']);preserved=hashlib.sha256(path.read_bytes()).hexdigest()==previous
        assert preserved
        cancel_record={'pid':q.pid,'pgid':pgid,'exit':q.returncode,'cessation_seconds':time.monotonic()-start,
            'escalated':escalated,'live_group_members':live,'incomplete_registered':False,'previous_export_preserved':preserved,'previous_export_available':previous is not None}
        dump('cancellation-result.json',cancel_record);results.append({'phase':'cancellation','status':'PASS','details':cancel_record})
        state('complete','done')
        with sqlite3.connect('/out/state.sqlite3') as db:integrity=db.execute('PRAGMA integrity_check').fetchone()[0]
        assert integrity=='ok'
    except Exception as e:
        errors.append(repr(e));state('error','failed')
    finally:
        done.set();sample.join(timeout=5);probes.join(timeout=5)
        if web.poll() is None:
            os.killpg(web.pid,signal.SIGTERM)
            try:web.wait(timeout=5)
            except subprocess.TimeoutExpired:os.killpg(web.pid,signal.SIGKILL);web.wait()
        dump('samples.json',samples);dump('web-probes.json',latencies)
        dump('summary.json',{'phases':results,'errors':errors,'application_phases_complete':all(x['status']=='PASS' for x in results) and len(results)>=4 and not errors,
            'memory_peak_bytes':int(read('memory.peak')) if read('memory.peak') else None,
            'memory_events':counters('memory.events'),'cpu_stat':counters('cpu.stat'),
            'sample_peak_disk_bytes':max((x['output_disk_bytes'] for x in samples),default=0),
            'web_requests':len(latencies),'web_failures':sum(not x['ok'] for x in latencies),
            'web_latency_max_seconds':max((x['seconds'] for x in latencies),default=0),
            'provider_calls':0,'model_downloads':0,'synthetic_resource_scope_only':True})
        print(json.dumps(json.loads((O/'summary.json').read_text())),flush=True)

if __name__=='__main__':main()
