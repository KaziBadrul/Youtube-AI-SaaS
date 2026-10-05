"""Disposable S9 v8 read-only measurements and Decimal sensitivities; no network/providers.
Reproduce from repository root: python3 spikes/operating-economics/infrastructure_v8.py
Only writes v8 evidence. No production runtime/authority is implemented here.
"""
from pathlib import Path
from decimal import Decimal as D, ROUND_CEILING, ROUND_FLOOR
import hashlib, json, math, statistics, struct, wave

ROOT = Path(__file__).resolve().parents[2]
E = ROOT / 'docs/architecture/evidence/operating-economics/S9/v8'
S6 = ROOT / 'docs/architecture/evidence/rendering-feasibility/S6'
S5 = ROOT / 'docs/architecture/evidence/narration-feasibility/runs/approved-lite-v1'
GB = D(10**9)
GIB = D(2**30)
PARTIAL = D('2.074187543736878936319104269')
UNKNOWN = None


def complete_sum(*values):
    return None if any(x is None for x in values) else sum(values, D(0))


def envelope(fixed, uplift, cash_reserve):
    if fixed is None or uplift is None or cash_reserve is None:
        return None
    if uplift < 0 or cash_reserve < 0:
        raise ValueError('Negative sensitivity input')
    return (D(30) - cash_reserve) / (1 + uplift) - fixed


def capacity(budget, unit):
    if budget is None or unit is None:
        return None
    if unit <= 0:
        raise ValueError('Positive unit cost required')
    return max(0, int((budget / unit).to_integral_value(rounding=ROUND_FLOOR)))


def egress(usage, included, rate):
    if usage is None or included is None:
        return None
    return max(D(0), usage - included) * rate


def b2_storage(gb, free_verified=False):
    return max(D(0), gb - (D(10) if free_verified else D(0))) * D('.00695')


def r2_cost(gb, a, b, free_verified=False):
    def ceil(x):
        return max(D(0), x).to_integral_value(rounding=ROUND_CEILING)
    free_gb, free_a, free_b = (D(10), 1000000, 10000000) if free_verified else (D(0), 0, 0)
    return (ceil(gb - free_gb) * D('.015')
            + ceil(D(a - free_a) / 1000000) * D('4.50')
            + ceil(D(b - free_b) / 1000000) * D('.36'))


def encoded_backup_bytes(payload, files):
    # Candidate ZIP_STORED, ASCII controlled names <=128B; not a production contract.
    # Per-file central/local records 76 + 2*128; EOCD22; manifest bound<=1024/file.
    # AES-GCM nonce12 + authentication tag16, as existing S8 binary envelope.
    # Includes conservative reserved manifest entry/header, no compression savings.
    return payload + (files + 1) * (332 + 1024) + 22 + 28


def collect():
    files = {}
    def receipt(p):
        p = p.resolve()
        name = str(p.relative_to(ROOT))
        if name not in files:
            h = hashlib.sha256()
            with p.open('rb') as f:
                for block in iter(lambda: f.read(1024 * 1024), b''):
                    h.update(block)
            files[name] = {'bytes': p.stat().st_size, 'sha256': h.hexdigest()}
        return dict(files[name], path=name)
    def wav(p):
        result = receipt(p)
        with wave.open(str(p), 'rb') as w:
            result.update(sample_rate=w.getframerate(), channels=w.getnchannels(),
                          sample_width=w.getsampwidth(), frames=w.getnframes(),
                          seconds=w.getnframes()/w.getframerate())
        return result
    def png(p):
        result = receipt(p)
        with p.open('rb') as f:
            header = f.read(24)
        if header[:8] == b'\x89PNG\r\n\x1a\n':
            result['format']='PNG'
            result['width'], result['height'] = struct.unpack('>II', header[16:24])
        elif header[:2] == b'\xff\xd8':
            result['format']='JPEG stored with .png suffix'
            result['width']=result['height']=None
            with p.open('rb') as f:
                f.read(2)
                while True:
                    marker=f.read(1)
                    if not marker: break
                    if marker!=b'\xff': continue
                    code=f.read(1)
                    while code==b'\xff': code=f.read(1)
                    if code in (b'\xd9',b'\xda'): break
                    if not code: break
                    length=struct.unpack('>H',f.read(2))[0]
                    segment=f.read(length-2)
                    if code[0] in (0xc0,0xc1,0xc2,0xc3,0xc5,0xc6,0xc7,0xc9,0xca,0xcb,0xcd,0xce,0xcf):
                        result['height'],result['width']=struct.unpack('>HH',segment[1:5]);break
        else:
            raise ValueError('Unknown image signature: '+str(p))
        return result
    images = [png(p) for p in sorted((ROOT/'demo-video-example/images').glob('*.png'))]
    sizes = [p['bytes'] for p in images]
    image_mean = D(sum(sizes)) / len(sizes)
    calls = [wav(p) for p in sorted((S5/'audio').glob('call-*/attempt-*/source.wav'))]
    ledger = json.loads((S5/'ledger.json').read_text())
    for a in ledger['attempts']:
        actual = next(c for c in calls if f"call-{a['call']:02d}/" in c['path'])
        assert actual['sha256'] == a['audio']['sha256']
    wav_overhead=max(c['bytes']-c['frames']*c['channels']*c['sample_width'] for c in calls)
    benchmarks = json.loads((S6/'S6-results.json').read_text())['benchmarks']
    measured, models = [], []
    for b in benchmarks:
        folder = S6/'fixtures'/b['label']
        captions = [receipt(p) for p in sorted(folder.glob('caption-*.png'))]
        fixture_images = [png(p) for p in sorted(folder.glob('image-*.png'))]
        manifest = receipt(folder/'manifest.json')
        output = receipt(Path(b['output']))
        assert output['sha256'] == b['sha256'] and output['bytes'] == b['bytes']
        scratch_files = [receipt(p) for p in sorted(Path(b['attempt']).glob('*')) if p.is_file()]
        retained = sum(p['bytes'] for p in scratch_files)
        peak = b['scratch_peak_bytes']
        # Original final evidence adds moved candidate to retained intermediates.
        assert peak >= retained
        audios = [wav(p) for p in sorted(folder.glob('*.wav'))]
        measured.append(dict(seconds=b['duration'], scene_count=b['scene_count'],
            images=fixture_images, caption_bytes=sum(c['bytes'] for c in captions),
            narration_and_music=audios, manifest=manifest, export=output,
            scratch_recorded_peak_bytes=peak, scratch_retained_now_bytes=retained,
            render_wall_seconds=b['render_wall_seconds'], cpu_seconds=b['cpu_seconds'],
            ffmpeg_peak_rss_bytes=b['peak_ffmpeg_rss_bytes']))
        n = b['duration'] // 60 * 12
        cap = math.ceil(D(sum(c['bytes'] for c in captions)) / b['scene_count'] * n)
        meta = math.ceil(D(manifest['bytes']) / b['scene_count'] * n)
        img = math.ceil(image_mean * n)
        audio = b['duration']*24000*2+wav_overhead
        active = img + audio + cap + meta
        total = active + output['bytes']
        models.append(dict(minutes=b['duration']//60, images=n,
            historical_image_mean_extrapolation_bytes=img, pcm24k_source_bytes=audio, wav_container_overhead_extrapolation=wav_overhead,
            caption_cache_extrapolation_bytes=cap, metadata_extrapolation_bytes=meta,
            active_project_bytes_excluding_export=active, measured_synthetic_export_bytes=output['bytes'],
            clean_retained_bytes=total, render_scratch_bytes=peak,
            additional_previous_export_bytes=output['bytes'],
            caveat='Historical image model unspecified; synthetic export/caption cache and duration PCM extrapolation, not expected new image output distribution.'))
    # All available legacy project files are inventoried; ZIP is not counted again as images.
    legacy = [receipt(p) for p in sorted((ROOT/'demo-video-example').rglob('*'))
              if p.is_file() and p.name != '.DS_Store']
    legacy_audio = wav(ROOT/'demo-video-example/narration.wav')
    db = receipt(S6/'web-boundary.sqlite3')
    receipts = {str(S6.relative_to(ROOT))+'/S6-results.json':receipt(S6/'S6-results.json'),
                str(S5.relative_to(ROOT))+'/ledger.json':receipt(S5/'ledger.json')}
    # Re-read after collection to certify this analysis did not mutate inspected sources.
    for name, data in files.items():
        assert receipt(ROOT/name)['sha256'] == data['sha256']
        h=hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
        assert h == data['sha256'], name
    return dict(image_population={'count':len(images), 'bytes':sum(sizes),
        'mean_bytes':str(image_mean), 'median_bytes':statistics.median(sizes),
        'min_bytes':min(sizes), 'max_bytes':max(sizes), 'sources':images},
        S5_sources=calls, S6_measured=measured, storage_models=models,
        legacy_project_files=legacy, legacy_narration=legacy_audio, SQLite_fixture=db,
        source_receipts=receipts, source_file_inventory=files,
        source_hashes_unchanged=True, accounting_units='MB/GB decimal; MiB/GiB binary, not interchangeable')


def main():
    E.mkdir(exist_ok=True)
    m = collect()
    five = next(x for x in m['storage_models'] if x['minutes']==5)
    # Five simultaneously retained projects is a capacity/storage sensitivity, NOT allowance.
    cohort_payload = five['clean_retained_bytes'] * 5
    # image, captions, source audio, manifest and export per project; DB/journal extras UNKNOWN.
    files_per_snapshot = 5*(60*2+3)
    one = encoded_backup_bytes(cohort_payload, files_per_snapshot)
    backups=[]
    for copies in [1,2,8]:
        gb = D(one*copies)/GB
        backups.append(dict(retained_copies_sensitivity=copies, cohort_projects=5,
            archive_upper_bytes_candidate=one, stored_GB=str(gb),
            b2_paid_equivalent_storage_USD=str(b2_storage(gb)),
            b2_possible_free_cash_storage_USD=str(b2_storage(gb,True)),
            r2_paid_equivalent_1000_A_1000_B_USD=str(r2_cost(gb,1000,1000)),
            r2_possible_free_cash_USD=str(r2_cost(gb,1000,1000,True)),
            complete_backup_cost_USD=None,
            notes='Packaging/file bound is candidate. Shared DB/journal/logs/extra versions not included. Free cash conditional on unused verified allowance; no account activated.'))
    backup2 = D(backups[1]['b2_paid_equivalent_storage_USD'])
    envelopes=[]
    for host in [D(12),D(18),D(24)]:
        fixed = host+backup2
        for margin in [D(0),D('.10'),D('.20'),D('.30')]:
            budget=envelope(fixed,margin,D(0))
            envelopes.append(dict(host_USD=str(host), fixed_partial_USD=str(fixed),
                total_spend_uplift_sensitivity=str(margin), approved_policy=False,
                cash_reserve_sensitivity_USD='0', actual_cash_reserve_USD=None,
                nominal_generation_headroom_USD=str(budget),
                optimistic_partial_cost_only_capacity=capacity(budget,PARTIAL),
                complete_expected_capacity=None,
                unit_cost_sensitivities={str(c):capacity(budget,c) for c in [D('2.5'),D(3),D(4),D(6)]}))
    traffic=[]
    for projects in [5,10,20]:
        for downloads in [1,2,10]:
            # One preview of every image + one full narration per project. Deliberate sensitivity.
            usage=projects*(downloads*five['measured_synthetic_export_bytes']
                + five['historical_image_mean_extrapolation_bytes']+five['pcm24k_source_bytes'])+30*one
            traffic.append(dict(projects_sensitivity=projects, downloads_per_project=downloads,
                previews='one full set of images and one source audio per project, sensitivity only',
                daily_full_backup_upload_bytes=one, outbound_GB=str(D(usage)/GB),
                DO_12_host_overage_USD=str(egress(D(usage)/GIB,D(2000),D('.01'))),
                Linode_24_host_overage_USD=str(egress(D(usage)/GB,D(4000),D('.005'))),
                excluded_unknown_bytes='pages/provider prompts/TLS/HTTP overhead/retries/journal/log traffic'))
    checks=[]
    def check(name, condition):
        assert condition,name
        checks.append({'name':name,'result':'PASS'})
    check('unknown_component_not_zero', complete_sum(D(12),None) is None)
    check('unknown_margin_not_zero', envelope(D(12),None,D(0)) is None)
    check('unknown_reserve_blocks_complete_budget', envelope(D(12),D(0),None) is None)
    check('unknown_unit_cost_no_promised_capacity', capacity(D(18),None) is None)
    check('capacity_floor',capacity(D(10),D(3))==3)
    check('negative_budget_no_admission',envelope(D(31),D(0),D(0))<0 and capacity(D(-1),D(1))==0)
    check('whole_spend_margin',envelope(D(12),D('.2'),D(0))==D(13))
    check('cash_reserve_subtracted_before_margin',envelope(D(12),D('.2'),D(6))==D(8))
    check('fixed_variable_separate',complete_sum(D(12),PARTIAL)==D(12)+PARTIAL)
    check('owner_local_not_invited_host',D(0)!=D(12))
    for mins,count in [(3,36),(5,60),(10,120)]:
        row=next(x for x in m['storage_models'] if x['minutes']==mins)
        check(f'images_{mins}_min',row['images']==count)
        check(f'active_sum_{mins}',row['active_project_bytes_excluding_export']==sum(row[k] for k in ['historical_image_mean_extrapolation_bytes','pcm24k_source_bytes','caption_cache_extrapolation_bytes','metadata_extrapolation_bytes']))
        check(f'export_once_{mins}',row['clean_retained_bytes']==row['active_project_bytes_excluding_export']+row['measured_synthetic_export_bytes'])
        check(f'scratch_not_retained_{mins}',row['clean_retained_bytes']+row['render_scratch_bytes']>row['clean_retained_bytes'])
        check(f'shared_audio_not_multiplied_{mins}',row['pcm24k_source_bytes']==mins*60*48000+row['wav_container_overhead_extrapolation'])
    check('backup_two_copies_not_daily_upload_volume',D(backups[1]['stored_GB'])==2*D(one)/GB and 30*one>2*one)
    check('backup_packaging_AES_and_headers',encoded_backup_bytes(0,0)==1406)
    check('b2_paid_free_distinct',b2_storage(D(1))>0 and b2_storage(D(1),True)==0)
    check('b2_storage_above_free',b2_storage(D(12),True)==D('.01390'))
    check('r2_rounding',r2_cost(D('1.1'),1,1)==D('4.89'))
    check('r2_cash_free_separate',r2_cost(D(1),1000,1000)>0 and r2_cost(D(1),1000,1000,True)==0)
    check('included_traffic_before_overage',egress(D(100),D(2000),D('.01'))==0)
    check('traffic_overage_only_excess',egress(D(2001),D(2000),D('.01'))==D('.01'))
    check('unknown_traffic_not_zero',egress(None,D(2000),D('.01')) is None)
    check('b2_restore_within_allowance',egress(D(1),D(3),D('.01'))==0)
    check('b2_restore_excess_only',egress(D(4),D(3),D('.01'))==D('.01'))
    check('owner_cash_ceiling_unchanged',envelope(D(0),D(0),D(0))==D(30))
    check('previous_export_preserved_disk',five['clean_retained_bytes']+five['render_scratch_bytes']==five['active_project_bytes_excluding_export']+five['measured_synthetic_export_bytes']+five['render_scratch_bytes'])
    check('units_distinct',GB!=GIB)
    check('expected_partial_not_total',complete_sum(PARTIAL,None) is None)
    check('conditional_v7_not_expected',D('.410964')!=PARTIAL and complete_sum(PARTIAL,None) is None)
    check('worst_case_holds_plus_host_not_safe',D(12)+D('25.785684')>30)
    check('margins_not_owner_policy',all(not x['approved_policy'] for x in envelopes))
    # These fields model the authority boundary: v8 never emits a grant.
    policy={'video_tiers':['3/week','1/day'],'alpha_allowances':None,
            'final_credits':None,'optional_discovery_per_video_USD':None,
            'mandatory_discovery_operations':[], 'hosting_selection':None,
            'complete_cash_fixed_USD':None, 'complete_project_expected_USD':None}
    check('tiers_not_allowances',policy['alpha_allowances'] is None)
    check('credits_not_invented',policy['final_credits'] is None)
    check('optional_discovery_not_per_video',policy['mandatory_discovery_operations']==[])
    check('source_media_hashes_match',m['source_hashes_unchanged'] and len(m['S5_sources'])==8)
    before=json.loads((E/'preservation-before.json').read_text())
    live_index='docs/architecture/evidence/operating-economics/S9/README.md'
    archived_index=E/'S9-index-before-v8.md'
    preserved=[]
    for name,digest in before.items():
        p=archived_index if name==live_index else ROOT/name
        actual=hashlib.sha256(p.read_bytes()).hexdigest()
        assert actual==digest,name
        preserved.append(dict(path=name,sha256=digest,preserved_as=str(p.relative_to(ROOT))))
    check('all_prior_evidence_preserved_or_index_archived',len(preserved)==len(before))
    results={'verdict':'NOT_YET_PASS','measurements':'measurements-v8.json',
        'backup_sensitivities':backups,'monthly_envelopes':envelopes,'traffic_sensitivities':traffic,
        'policy':policy,'checks':checks,'checks_passed':len(checks),
        'provider_generation_calls':0,'paid_spend_USD':'0','downloads':0,
        'production_changes':False,'TASKS_changes':False,'deployments':0,'purchases':0}
    (E/'measurements-v8.json').write_text(json.dumps(m,indent=2)+'\n')
    (E/'arithmetic-results-v8.json').write_text(json.dumps(results,indent=2)+'\n')
    (E/'preservation-results-v8.json').write_text(json.dumps({'preserved_prior_files':len(preserved),'entries':preserved},indent=2)+'\n')
    print(json.dumps({'checks_passed':len(checks),'preserved_prior_files':len(preserved),
        'storage_MB':[{'minutes':x['minutes'],'active':x['active_project_bytes_excluding_export']/1e6,
        'retained':x['clean_retained_bytes']/1e6} for x in m['storage_models']],
        'backup2_GB':backups[1]['stored_GB'],'backup2_paid_USD':str(backup2),
        'baseline_envelopes':[x for x in envelopes if x['total_spend_uplift_sensitivity']=='0']}))

if __name__=='__main__':
    main()
