"""S9 scenario witness; projections only, no provider/network/runtime changes."""
import hashlib
import json
from decimal import Decimal as D, ROUND_CEILING
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/architecture/evidence/operating-economics/S9'
baseline = json.loads((OUT / 'analysis.json').read_text())
if not (OUT / 'baseline-v1.json').exists():
    (OUT / 'baseline-v1.json').write_text(json.dumps(baseline, indent=2) + '\n')

def ceil(x):
    return int(x.to_integral_value(rounding=ROUND_CEILING))

tts_initial = baseline['historical_B_initial_and_correction'][0]
tts_edit = baseline['historical_B_initial_and_correction'][1]
rows, storage, monthly = [], [], []
source_inventory = []
ledger = json.loads((ROOT / 'docs/architecture/evidence/narration-feasibility/runs/approved-lite-v1/ledger.json').read_text())
for attempt in ledger['attempts']:
    p = ROOT / f"docs/architecture/evidence/narration-feasibility/runs/approved-lite-v1/audio/call-{attempt['call']:02d}/attempt-{attempt['id']:02d}/source.wav"
    actual_hash = hashlib.sha256(p.read_bytes()).hexdigest()
    assert actual_hash == attempt['audio']['sha256'], 'Historical source changed'
    source_inventory.append({'call': attempt['call'], 'path': str(p.relative_to(ROOT)), 'bytes': p.stat().st_size,
                             'sha256': actual_hash, 'matches_historical_receipt': True})
for b in baseline['projection_rows']:
    seconds = D(b['minutes'] * 60)
    n = b['synthetic_scene_count']
    initial_tts = D(tts_initial['usage_derived_USD_historical_rate']) * seconds / D(str(tts_initial['duration_seconds']))
    for extra_fraction in ['0', '.1', '.25']:
        edits = ceil(D(n) * D(extra_fraction))
        image = D(n + edits) * D('.0336')
        # Explicit sensitivity, not production text-model selection or token measurements.
        text = (D(20000) * D('.3') + D(10000) * D('2.5')) / D(1000000)
        search = D(4) * D('.008')
        tts = initial_tts + D(tts_edit['usage_derived_USD_historical_rate'])
        subtotal = image + tts + text + search
        row = {'minutes': b['minutes'], 'initial_images': n, 'extra_attempt_fraction_assumed': extra_fraction,
               'additional_image_outputs_assumed': edits, 'total_image_output_cost_USD': str(image),
               'TTS_initial_scaled_historical_USD': str(initial_tts),
               'one_171_second_B_segment_correction_historical_USD': tts_edit['usage_derived_USD_historical_rate'],
               'illustrative_text_USD': str(text), 'four_basic_search_paid_equivalent_USD': str(search),
               'illustrative_variable_subtotal_USD': str(subtotal),
               'not_in_subtotal': ['image input/thinking', 'tax/fees', 'paid failures without an image', 'alignment/VM performance differences', 'infrastructure', 'other account spend'],
               'certainty': 'Scenario; observed only historical TTS basis, no measured complete project'}
        rows.append(row)
        if extra_fraction != '.1':
            continue
        # Two full narration source versions, two exports; hypothetical image bytes.
        # No deduplication/compression savings are assumed for snapshots.
        for image_mb in [1, 3, 8]:
            sources = int(seconds) * 24000 * 2 * 2 + 88
            retained = (n + edits) * image_mb * 1000000 + sources + 2 * b['output_bytes_measured_synthetic']
            storage.append({'minutes': b['minutes'], 'image_MB_assumed': image_mb,
                            'retained_project_bytes_scenario': retained,
                            'one_attempt_scratch_bytes_S6_synthetic': b['scratch_peak_bytes_measured_synthetic'],
                            'qualifications': 'Unmeasured image size; two PCM source versions and two synthetic exports; metadata/OS/models excluded.'})
        for projects in [3, 5, 10, 20]:
            for host in [12, 18, 24]:
                fixed_and_initial_images = D(host) + D(projects * n) * D('.0336')
                # All projects resident all month is deliberately conservative relative
                # to rolling 7-day purge. Eight full snapshot copies model an upper
                # daily-snapshot count, not a certified provider purge schedule.
                per_project = next(s['retained_project_bytes_scenario'] for s in storage if s['minutes'] == b['minutes'] and s['image_MB_assumed'] == 3)
                backup_bytes = per_project * projects * 8
                backup = D(backup_bytes) / D(10**12) * D('6.95')
                subtotal_month = D(host) + subtotal * projects + backup
                monthly.append({'minutes': b['minutes'], 'projects_per_month_scenario': projects,
                                'host_USD_public_base': host, 'host_plus_initial_images_only_USD': str(fixed_and_initial_images),
                                'lower_bound_exceeds_30': fixed_and_initial_images > D(30),
                                'backup_bytes_monthlong_sensitivity': backup_bytes, 'backup_storage_USD_sensitivity': str(backup),
                                'illustrative_monthly_subtotal_USD': str(subtotal_month),
                                'remaining_for_excluded_costs_USD': str(D(30) - subtotal_month),
                                'affordability_established': False,
                                'monthly_full_snapshot_upload_bytes_sensitivity': per_project * projects * 30,
                                'exports_one_download_bytes_synthetic': projects * b['output_bytes_measured_synthetic'],
                                'local_render_CPU_seconds_S6_total': str(D(str(next(x['cpu_seconds'] for x in json.loads((ROOT / 'docs/architecture/evidence/rendering-feasibility/S6/S6-results.json').read_text())['benchmarks'] if x['duration'] == int(seconds)))) * projects),
                                'status': 'INFEASIBLE_FROM_LOWER_BOUND' if fixed_and_initial_images > D(30) else 'UNPROVEN_REMAINDER_AVAILABLE'})

def capacity(cap, settled, unknown, planned, recurring):
    return cap - settled - unknown - planned - recurring

assert capacity(D(30), D(2), D(3), D(4), D(12)) == D(9)
assert capacity(D(30), D(5), D(0), D(4), D(12)) == D(9), 'settlement must replace hold, not double-count it'
assert D(56) * D('.0336') == D('1.8816')
assert 56 * 20 * D('.0336') > D(30), '20 five-minute initial image sets alone exceed budget'
assert all(not x['affordability_established'] for x in monthly)
assert all(D(rows[i + 1]['total_image_output_cost_USD']) >= D(rows[i]['total_image_output_cost_USD']) for i in [0, 1, 3, 4, 6, 7])
result = {'status': 'NOT_YET_PASS', 'scenario_revision': 2, 'fixed_image_tariff_USD': '.0336',
          'original_source_inventory': source_inventory,
          'project_scenarios': rows, 'storage_sensitivities': storage, 'monthly_scenarios': monthly,
          'sources': {'digitalocean': 'https://www.digitalocean.com/pricing/droplets', 'backup': 'https://www.backblaze.com/cloud-storage/pricing',
                      'text_reference_only': 'https://ai.google.dev/gemini-api/docs/pricing', 'search_reference': 'https://docs.tavily.com/documentation/api-credits'},
          'assumptions': '10% extras rounded up in monthly scenarios; one historical-sized coherent TTS correction; illustrative 20K text input/10K output at S4-R reference model, not selected; four paid-equivalent Basic searches; no free-tier credit assumed; 3MB images and 8 full snapshot copies; all scenarios unmeasured.',
          'tests': ['fixed-tariff arithmetic', 'edit-cost monotonicity', 'image-only infeasibility', 'unknown holds preserved', 'settlement no double counting', 'unknown full costs prevent affordability PASS'],
          'provider_calls': 0, 'purchases': 0}
(OUT / 'forecast-v2.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps([x for x in monthly if x['minutes'] == 5 and x['host_USD_public_base'] == 12], indent=2))
