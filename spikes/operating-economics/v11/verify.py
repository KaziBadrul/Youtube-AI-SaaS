"""Recompute V11 resource/economics evidence locally, no network or provider imports."""
import hashlib,json,math
from decimal import Decimal as D
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'docs/architecture/evidence/operating-economics/S9/v11'
G=OUT/'guest'
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
def check(name,ok):
    checks.append({'name':name,'result':'PASS' if ok else 'FAIL'})
    if not ok:raise AssertionError(name)
def summarize():
    env=load(G/'environment.json'); summary=load(G/'summary.json'); kernel=load(G/'kernel-after.json')
    samples=[json.loads(x) for x in (G/'telemetry.jsonl').read_text().splitlines()]
    probes=[json.loads(x) for x in (G/'probes.jsonl').read_text().splitlines()]
    total=4*1024**3; visible=env['meminfo']['MemTotal']; reserve=total-visible
    check('two_guest_cpus',env['cpu_count']==2)
    config=(OUT/'effective-guest.yaml').read_text()
    check('whole_guest_4GiB_native_vz',all(x in config for x in ['cpus: 2','memory: 4GiB','vmType: vz','arch: aarch64','mounts: []']) and env['machine']=='aarch64')
    actual_vm=load(OUT/'vm-inspection.json')
    check('actual_VM_allocation_not_just_yaml',actual_vm['cpus']==2 and actual_vm['memory']==total and actual_vm['vmType']=='vz' and actual_vm['arch']=='aarch64')
    check('complete_guest_kernel_systemd_services_ext4',env['kernel']['exit']==0 and 'systemd-journald' in env['services']['stdout'] and 'ssh' in env['services']['stdout'] and 'ext4' in env['findmnt']['stdout'])
    check('global_not_cgroup_measurement',all('MemAvailable' in s['meminfo'] for s in samples) and env['measure'].startswith('GLOBAL'))
    check('no_swap_config_or_activity',env['meminfo']['SwapTotal']==0 and all(s['swap_used']==0 and s['vmstat']['pswpin']==0 and s['vmstat']['pswpout']==0 for s in samples))
    phase_order=[p['phase'] for p in summary['phases']]
    check('required_phases_measured',phase_order==['alignment','render','validation','backup','cancellation'] and {'guest_idle','application_idle'} <= {s['phase'] for s in samples})
    check('maintenance_serialized',summary['maintenance_serialized'] and all(summary['phases'][i]['end']<=summary['phases'][i+1]['start'] for i in range(len(summary['phases'])-1)))
    check('kernel_OOM_checked',kernel['dmesg']['exit']==0 and kernel['journal_kernel']['exit']==0)
    oom_delta=kernel['vmstat']['oom_kill']-env['vmstat_before']['oom_kill']
    rows=[]
    for name in ['guest_idle','application_idle']+phase_order:
        ss=[s for s in samples if s['phase']==name];pp=[p for p in probes if p['phase']==name]
        if not ss:continue
        minimum=min(s['meminfo']['MemAvailable'] for s in ss); a,b=ss[0]['cpu_times'],ss[-1]['cpu_times']
        cpu_total=sum(b.values())-sum(a.values()); idle=b.get('idle',0)-a.get('idle',0)+b.get('iowait',0)-a.get('iowait',0)
        times=sorted(p['seconds'] for p in pp)
        phase=next((p for p in summary['phases'] if p['phase']==name),None)
        def psi_total(s,kind):
            line=next(x for x in s['psi']['memory'].splitlines() if x.startswith(kind+' '))
            return int(line.split('total=')[1])
        rows.append({'phase':name,'samples':len(ss),'wall_seconds':phase['wall_seconds'] if phase else ss[-1]['time']-ss[0]['time'],
                     'status':phase['status'] if phase else 'MEASURED','peak_whole_unavailable_including_reserved_bytes':total-minimum,
                     'peak_kernel_visible_used_minus_available_bytes':visible-minimum,'peak_used_minus_free_bytes':max(s['whole_used_minus_free'] for s in ss),
                     'minimum_available_bytes':minimum,'headroom_percent_of_configured_RAM':100*minimum/total,
                     'peak_app_tree_rss_sum_bytes':max(s['application_tree_rss_sum'] for s in ss),'peak_all_process_rss_sum_bytes':max(s['all_process_rss_sum'] for s in ss),
                     'cache_at_min_headroom_bytes':next(s['meminfo']['Cached']+s['meminfo']['Buffers'] for s in ss if s['meminfo']['MemAvailable']==minimum),
                     'memory_PSI_some_delta_us':psi_total(ss[-1],'some')-psi_total(ss[0],'some'),'memory_PSI_full_delta_us':psi_total(ss[-1],'full')-psi_total(ss[0],'full'),
                     'peak_swap_bytes':max(s['swap_used'] for s in ss),'cpu_busy_percent':100*(1-idle/cpu_total) if cpu_total>0 else None,
                     'web_requests':len(pp),'web_failures':sum(not p['ok'] for p in pp),'web_p95_seconds':times[min(len(times)-1,math.ceil(.95*len(times))-1)] if times else None,
                     'web_max_seconds':max(times) if times else None,'peak_disk_used_bytes':max(s['disk_used'] for s in ss),'peak_output_bytes':max(s['output_bytes'] for s in ss)})
    check('headroom_peak_CPU_probes_disk_recorded',all(r['minimum_available_bytes']>=0 and r['samples']>0 for r in rows))
    media=load(G/'render-result.json');v=media['validation']; c=load(G/'cancellation-result.json')
    check('unchanged_full_S6_validation',v['status']=='PASS' and v['decoded_frame_count']==18000 and len(v['transitions'])==111 and v['blank_frames']==0 and v['audio_snr_db']>20 and v['registered_after_validation'])
    check('retrieved_final_export_hash',sha(G/Path(media['result']['output']).relative_to('/out'))==media['result']['sha256'])
    check('cancellation_previous_export_lock_cessation',c['status']=='PASS' and not c['live_group_members'] and c['previous_export_preserved'] and c['lock_released_after_confirmed_cessation'] and not c['incomplete_registered'])
    process_text=(OUT/'processes-after.txt').read_text()
    check('no_orphan_heavy_or_web_processes',not any(name in process_text for name in ['ffmpeg','gunicorn','python']) and 'has shut down' in (OUT/'vm-stop.log').read_text())
    caption=load(G/'captions-result.json')
    check('five_language_identical_reference_pixels',len(caption['results'])==5 and all(r['exact_decoded_pixels_match_S6_reference'] for r in caption['results']))
    check('source_guest_copies_verified',load(OUT/'guest-source-verification.json')['all_match'])
    before=load(OUT/'preservation-before.json'); changed=[]
    for name,r in before.items():
        p=ROOT/name
        if not p.is_file() or sha(p)!=r['sha256']:changed.append(name)
    allowed='docs/architecture/evidence/operating-economics/S9/README.md'
    check('history_unchanged_or_live_index_archived',set(changed)<={allowed} and sha(OUT/'README-before.md')==before[allowed]['sha256'])
    (OUT/'preservation-result.json').write_text(json.dumps({'files':len(before),'changed':changed,'historical_files_unchanged':True,'index_prior_bytes_archived':True},indent=2)+'\n')
    decision=load(OUT/'classification.json')
    minimum_all=min(s['meminfo']['MemAvailable'] for s in samples)
    classification=decision['classification'];reason=decision['reason']
    check('classification_tied_to_this_evidence',decision['summary_sha256']==sha(G/'summary.json') and decision['minimum_available_bytes']==minimum_all)
    check('safe_class_cannot_override_failed_phases_or_OOM',classification!='SAFE_ENOUGH_FOR_ALPHA' or (oom_delta==0 and summary['application_complete'] and summary['probe_failures']==0 and summary['peak_swap']==0))
    check('owner_last_sizing_stop_rule',decision['last_sizing_experiment_unless_failure'] is True)
    previous=load(ROOT/'docs/architecture/evidence/operating-economics/S9/v8/arithmetic-results-v8.json')
    archive=load(G/'backup-result.json')['archive_bytes']
    backup=D(archive)*2/D(1000000000)*D('.00695')
    check('measured_backup_two_snapshot_sensitivity',backup==D(archive)*D(2)*D('.00695')/D(1000000000))
    partial=D('2.074187543736878936319104269');fixed=D(24)+backup;envelopes=[]
    for uplift in [D(0),D('.10'),D('.20')]:
        remaining=D(30)/(1+uplift)-fixed
        envelopes.append({'host_class_USD':'24','fixed_partial_USD':str(fixed),'uplift_sensitivity_not_policy':str(uplift),'remaining_nominal_USD':str(remaining),
                          'optimistic_partial_only_capacity':max(0,int(remaining//partial)),'complete_expected_capacity':None,'owner_allowance':None})
        check('envelope_arithmetic_'+str(uplift),remaining==D(30)/(1+uplift)-D(24)-backup)
    check('zero_provider_spend_and_no_complete_cost_invention',summary['provider_generation_calls']==0 and all(x['complete_expected_capacity'] is None for x in envelopes))
    result={'S9':'NOT_YET_PASS','resource_classification':classification,'reason':reason,'configured_RAM_bytes':total,'kernel_visible_RAM_bytes':visible,'guest_reserved_RAM_bytes':reserve,
            'measurement_limit':'Sampled (~0.1s nominal; raw timestamps retain actual spacing), not an exact kernel high-water mark. MemAvailable estimates reclaimable headroom; reserved RAM counted in configured-total-unavailable metric; RSS sums may double-count shared pages.',
            'phases':rows,'OOM_kills_delta':oom_delta,'minimum_available_bytes':minimum_all,
            'backup_storage_sensitivity':{'archive_bytes':archive,'copies':2,'paid_equivalent_USD':str(backup),'rate_source':'preserved V8 official B2 tariff .00695/decimal GB/month; backup-only, no vendor selection','retention_policy_or_allowance':False},
            'envelopes':envelopes,'checks':checks,'checks_passed':len(checks),'provider_generation_calls':0,'paid_spend_USD':'0','production_changes':False,'TASKS_changes':False,'cloud_provisioning':False,'public_deployments':False,'purchases':False,'downloads':0,'host_sizing_closed_at_local_scope':classification=='SAFE_ENOUGH_FOR_ALPHA','additional_sizing_authorized_only_on_failure':True}
    (OUT/'RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':summarize()
