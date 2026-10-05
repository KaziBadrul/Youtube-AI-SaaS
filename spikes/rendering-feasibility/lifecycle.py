"""S6 real FFmpeg cancellation/recovery witness over disposable persisted state."""
import argparse,json,os,signal,subprocess,sys,time,uuid
from pathlib import Path
import psutil
from s6 import OUT,EXPORTS,SCRATCH,FFMPEG,sha,dump,output_basic

STATE=OUT/'lifecycle-state';STATE.mkdir(exist_ok=True)

def durable(path,record):
    temporary=path.with_suffix('.tmp')
    with temporary.open('w') as f:json.dump(record,f,indent=2);f.flush();os.fsync(f.fileno())
    os.replace(temporary,path)

def live(pid):
    try:return psutil.Process(pid).is_running() and psutil.Process(pid).status()!=psutil.STATUS_ZOMBIE
    except psutil.NoSuchProcess:return False

def identity(pid):return psutil.Process(pid).create_time()

def launch(state_path,crash=False,ignore_term=False):
    boot=psutil.boot_time()  # Inspect identity capability before creating a child.
    attempt=STATE/uuid.uuid4().hex;attempt.mkdir()
    previous=(EXPORTS/'project-300.mp4').resolve()
    record=dict(state='RENDERING',lock=True,previous_export=str(previous),previous_hash=sha(previous),output=str(attempt/'incomplete.mp4'),registered_success=False)
    durable(state_path,record)
    cmd=[FFMPEG,'-y','-v','error','-re','-stream_loop','-1','-i',str(previous),'-t','600','-c:v','libx264','-preset','ultrafast','-threads','2','-c:a','aac',record['output']]
    with (attempt/'ffmpeg.log').open('wb') as log:
        p=subprocess.Popen(cmd,start_new_session=True,stdout=log,stderr=log)
    record.update(pid=p.pid,pgid=os.getpgid(p.pid),process_start=identity(p.pid),boot=boot,argv=cmd)
    durable(state_path,record)
    time.sleep(.5)
    if crash:os._exit(91)
    return p,record

def stop(record,grace=.5):
    trace=[]
    assert record['boot']==psutil.boot_time(),'boot_identity_changed'
    if live(record['pid']):assert abs(identity(record['pid'])-record['process_start'])<.0001,'pid_identity_mismatch'
    tracked=[record['pid']]
    if live(record['pid']):tracked+=[x.pid for x in psutil.Process(record['pid']).children(recursive=True)]
    if live(record['pid']):
        os.killpg(record['pgid'],signal.SIGTERM);trace.append('SIGTERM')
        end=time.monotonic()+grace
        while any(live(p) for p in tracked) and time.monotonic()<end:time.sleep(.02)
        if any(live(p) for p in tracked):os.killpg(record['pgid'],signal.SIGKILL);trace.append('SIGKILL')
    end=time.monotonic()+3
    while any(live(p) for p in tracked) and time.monotonic()<end:time.sleep(.02)
    stopped=not any(live(p) for p in tracked)
    return dict(signals=trace,tracked_members=tracked,confirmed_stopped=stopped)

def test():
    events=[]
    # Recover the retained first-run sandbox-denied launch, if it still executes.
    # Match the exact private attempt output, not a process name or untrusted PID.
    prior=STATE/'cancel.json'
    if prior.exists():
        saved=json.loads(prior.read_text())
        for proc in psutil.process_iter(['pid','cmdline']):
            try:
                argv=proc.info['cmdline'] or []
                if saved['output'] in argv and argv[0]==FFMPEG:
                    stale=dict(pid=proc.pid,pgid=os.getpgid(proc.pid),process_start=identity(proc.pid),boot=psutil.boot_time())
                    termination=stop(stale);assert termination['confirmed_stopped']
                    events.append(dict(case='initial_sandbox_denial_orphan_recovery',result='PASS',termination=termination))
            except (psutil.NoSuchProcess,psutil.AccessDenied):continue
    state_path=STATE/'cancel.json';p,record=launch(state_path)
    assert live(record['pid']) and record['lock'];record['state']='CANCELLING';durable(state_path,record)
    outcome=stop(record);p.wait(timeout=3);assert outcome['confirmed_stopped']
    record.update(lock=False,state='CANCELLED');durable(state_path,record)
    assert sha(record['previous_export'])==record['previous_hash'] and not record['registered_success']
    incomplete=Path(record['output'])
    if incomplete.exists():os.replace(incomplete,incomplete.with_suffix('.quarantined.mp4'))
    events.append(dict(case='cancel',result='PASS',termination=outcome,lock_release='after confirmed cessation',previous_export_preserved=True))
    crash_state=STATE/'recovery.json'
    worker=subprocess.Popen([sys.executable,__file__,'launch-crash','--state',str(crash_state)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    assert worker.wait(timeout=10)==91
    record=json.loads(crash_state.read_text());assert live(record['pid']) and record['lock']
    # Expired heartbeat is insufficient. Persist recovery-required with lock retained.
    record.update(state='RECOVERY_REQUIRED',stale_heartbeat=True);durable(crash_state,record)
    assert record['lock'] and live(record['pid'])
    wrong=dict(record,process_start=record['process_start']-10)
    try:stop(wrong)
    except AssertionError:pass
    else:raise AssertionError('wrong process identity was accepted')
    outcome=stop(record);assert outcome['confirmed_stopped']
    record.update(lock=False,state='INTERRUPTED_SAFE_TO_RETRY');durable(crash_state,record)
    assert sha(record['previous_export'])==record['previous_hash'] and not record['registered_success']
    incomplete=Path(record['output'])
    if incomplete.exists():os.replace(incomplete,incomplete.with_suffix('.quarantined.mp4'))
    events.append(dict(case='worker_crash_recovery',result='PASS',old_child_observed_alive=True,stale_lock_retained=True,pid_reuse_guard=True,termination=outcome,previous_export_preserved=True))
    # Exercise bounded escalation with a stubborn two-member local media group.
    stubborn_state=STATE/('stubborn-'+uuid.uuid4().hex+'.json')
    child=subprocess.Popen([sys.executable,__file__,'stubborn','--state',str(stubborn_state)],start_new_session=True)
    deadline=time.monotonic()+5
    while not stubborn_state.exists() and time.monotonic()<deadline:time.sleep(.02)
    stubborn=json.loads(stubborn_state.read_text());outcome=stop(stubborn);child.wait(timeout=3)
    assert outcome['confirmed_stopped'] and 'SIGKILL' in outcome['signals']
    events.append(dict(case='bounded_escalation',result='PASS',termination=outcome))
    # Retry uses existing immutable source manifest, with no fixture generation.
    from s6 import render,validate_output
    manifest=json.loads((OUT/'fixtures/project-12/manifest.json').read_text())
    before={x:sha(x) for x in [manifest['narration']]+[s['image'] for s in manifest['scenes']]}
    result=render(manifest,'recovery-retry',False,False,False);validate_output(manifest,result)
    assert all(sha(x)==h for x,h in before.items())
    events.append(dict(case='retry_reuses_assets',result='PASS',source_hashes_preserved=True,provider_calls=0,output=result['output']))
    dump(OUT/'lifecycle-results.json',events)
    print('Cancellation, interrupted worker recovery, escalation and local retry passed',flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('mode');ap.add_argument('--state',type=Path);args=ap.parse_args()
    if args.mode=='launch-crash':launch(args.state,True)
    elif args.mode=='stubborn':
        signal.signal(signal.SIGTERM,signal.SIG_IGN)
        nested=subprocess.Popen([sys.executable,'-c','import signal,time;signal.signal(signal.SIGTERM,signal.SIG_IGN);time.sleep(30)'])
        time.sleep(.1)
        durable(args.state,dict(pid=os.getpid(),pgid=os.getpgrp(),process_start=identity(os.getpid()),boot=psutil.boot_time()))
        time.sleep(30)
    else:test()
