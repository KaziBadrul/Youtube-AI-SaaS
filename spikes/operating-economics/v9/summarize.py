"""Aggregate local resource evidence and fail closed on stale/incomplete receipts."""
from pathlib import Path
import hashlib,json,statistics
R=Path(__file__).resolve().parents[3]
E=R/'docs/architecture/evidence/operating-economics/S9/v9'

def main():
    rows=[];checks=[]
    for name in ['1cpu-2gb','2cpu-4gb','1cpu-2gb-serial']:
        folder=E/name
        if not (folder/'summary.json').exists():
            rows.append({'envelope':name,'status':'INCOMPLETE'});continue
        s=json.loads((folder/'summary.json').read_text());samples=json.loads((folder/'samples.json').read_text());web=json.loads((folder/'web-probes.json').read_text());env=json.loads((folder/'environment.json').read_text())
        phases=[]
        for p in s['phases']:
            subset=[x for x in samples if x['phase']==p['phase'] or (p['phase']=='backup_standalone' and x['phase']=='backup_standalone') or (p['phase']=='backup_overlap' and x['phase']=='render_backup_overlap')]
            w=[x for x in web if x['phase']==p['phase'] or (p['phase']=='backup_overlap' and x['phase']=='render_backup_overlap')]
            valid=[x['seconds'] for x in w if x['ok']]
            q=sorted(valid)
            phases.append(dict(p, sample_current_peak_bytes=max((x['memory_current'] for x in subset),default=0),
                sample_rss_peak_bytes=max((x['process_rss_sum'] for x in subset),default=0),
                web_requests=len(w),web_failures=sum(not x['ok'] for x in w),
                web_p95_seconds=q[max(0,int(len(q)*.95)-1)] if q else None))
        overlap=next((p for p in phases if p['phase']=='backup_overlap'),None)
        if overlap and overlap['status']!='PASS' and (folder/'backup-overlap-result.json').exists():
            # First controller iteration copied an older successful receipt after child failure.
            # Never permit the file to override process exit/OOM evidence. Preserve raw history.
            marker={'validation':'INVALID_STALE_RECEIPT','ignored':True,'reason':'backup overlap child did not exit successfully; copied prior receipt is not evidence for this attempt','phase_exit':overlap.get('exit')}
            (folder/'backup-overlap-receipt-invalid.json').write_text(json.dumps(marker,indent=2)+'\n')
            checks.append({'name':name+'_failed_child_cannot_publish_old_receipt','PASS':True})
        row={'envelope':name,'application_status':'PASS' if s['application_phases_complete'] and s['memory_events'].get('oom_kill',0)==0 else 'FAIL_OR_PARTIAL',
             'whole_host_qualification':'NOT_ESTABLISHED','environment':env,'memory_peak_bytes':s['memory_peak_bytes'],'memory_events':s['memory_events'],
             'sample_disk_peak_bytes':s['sample_peak_disk_bytes'],'web_failures':s['web_failures'],'phases':phases,'errors':s['errors']}
        for result in ['render-result.json','alignment-result.json','backup-standalone-result.json','backup-overlap-result.json','cancellation-result.json']:
            if (folder/result).exists() and not (result=='backup-overlap-result.json' and overlap and overlap['status']!='PASS'):
                record=json.loads((folder/result).read_text())
                if result=='alignment-result.json':record={k:v for k,v in record.items() if k!='words'}|{'word_count':len(record['words'])}
                if result=='render-result.json':record={'render':record['result'],'validation':{k:v for k,v in record['validation'].items() if k not in ['ffprobe','transitions']},'transition_count':len(record['validation']['transitions'])}
                row[result]=record
        assert env['memory.swap.max']=='0'
        checks.append({'name':name+'_no_swap','PASS':True})
        assert env['cpu.max'] in ['100000 100000','200000 100000']
        checks.append({'name':name+'_hard_CPU_quota','PASS':True})
        rows.append(row)
    before=json.loads((E/'preservation-before.json').read_text());index='docs/architecture/evidence/operating-economics/S9/README.md'
    failures=[]
    for name,digest in before.items():
        path=E/'S9-index-before-v9.md' if name==index else R/name
        if hashlib.sha256(path.read_bytes()).hexdigest()!=digest:failures.append(name)
    assert not failures,failures
    checks.append({'name':'all_prior_evidence_unchanged_or_exact_index_archived','PASS':True})
    indexed={row['envelope']:row for row in rows}
    def verify(name,condition):
        assert condition,name
        checks.append({'name':name,'PASS':True})
    verify('overlap_2GB_OOM_is_not_a_pass',indexed['1cpu-2gb']['application_status']!='PASS' and indexed['1cpu-2gb']['memory_events']['oom_kill']>0)
    for name in ['2cpu-4gb','1cpu-2gb-serial']:
        row=indexed[name]
        if row.get('application_status')!='PASS': continue
        video=row['render-result.json'];v=video['validation']
        verify(name+'_18000_frames',v['decoded_frame_count']==18000)
        verify(name+'_111_transitions',video['transition_count']==111)
        verify(name+'_no_blank_frames',v['blank_frames']==0)
        verify(name+'_continuous_audio',v['source_narration_samples']==600*48000 and v['audio_snr_db']>20)
        verify(name+'_no_clipping',v['audio_peak']<.95)
        verify(name+'_three_caption_samples',len(v['caption_samples'])==3 and all(x['white_text_pixels']>100 for x in v['caption_samples']))
        verify(name+'_no_oom',row['memory_events']['oom_kill']==0)
        verify(name+'_web_no_failures',row['web_failures']==0)
        c=row['cancellation-result.json']
        verify(name+'_bounded_cancel_no_child',c['cessation_seconds']<6 and not c['live_group_members'])
        verify(name+'_previous_export_preserved',c['previous_export_available'] and c['previous_export_preserved'] and not c['incomplete_registered'])
    cap_path=E/'captions/captions-result.json'
    if cap_path.exists():
        cap=json.loads(cap_path.read_text())
        for x in cap['results']:verify('Linux_'+x['language']+'_exact_reference_RGBA',x['exact_decoded_pixels_match_S6_reference'] and not x['layout']['fallback'] and not x['layout']['clipped'])
    for receipt in json.loads((E/'local-model-receipt.json').read_text()):
        verify('original_model_'+receipt['name']+'_unchanged',hashlib.sha256(Path(receipt['original']).read_bytes()).hexdigest()==receipt['sha256'])
    body={'S9':'NOT_YET_PASS','envelopes':rows,'checks':checks,'preserved_prior_files':len(before),
        'provider_calls':0,'paid_spend_USD':0,'separate_Whisper_model_downloads':0,'bundled_VAD_asset':'included in downloaded faster-whisper package; no separate model-fetch','dependency_downloads':'yes, disposable Debian/PyPI image only',
        'production_touched':False,'TASKS_touched':False,'deployment':False,'purchase':False,
        'global_limitations':['Shared Docker VM kernel/daemon outside application cgroup','x86_64 emulation on Apple Silicon','synthetic render/backup sensitivity, not production workload distribution','no off-machine backup or hosting purchase','V7 token-preflight not exercised']}
    (E/'RESULTS.json').write_text(json.dumps(body,indent=2)+'\n')
    print(json.dumps({'envelopes':[{'name':x['envelope'],'status':x.get('application_status',x.get('status')),'peak':x.get('memory_peak_bytes'),'phases':[{k:p[k] for k in ['phase','status','wall_seconds'] if k in p} for p in x.get('phases',[])]} for x in rows],'preserved':len(before)}))

if __name__=='__main__':main()
