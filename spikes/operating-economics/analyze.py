"""Disposable S9 analysis. Standard library only; no network/provider calls."""
import hashlib
import json
from decimal import Decimal as D
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/architecture/evidence/operating-economics/S9'
render_path = ROOT / 'docs/architecture/evidence/rendering-feasibility/S6/S6-results.json'
ledger_path = ROOT / 'docs/architecture/evidence/narration-feasibility/runs/approved-lite-v1/ledger.json'
render = json.loads(render_path.read_text())
ledger = json.loads(ledger_path.read_text())
rows = []
for b in render['benchmarks']:
    n = b['scene_count']
    rows.append({
        'minutes': b['duration'] // 60, 'synthetic_scene_count': n,
        'standard_image_output_only_USD': str(D(n) * D('.0336')),
        'standard_output_with_10_percent_additional_attempts_USD': str(D(n) * D('1.1') * D('.0336')),
        'qualification': 'Owner-fixed Standard image-output tariff; projected S6 counts, not measured production. Other billing components tracked separately; no Batch assumption.',
        'tier1_RPD_only_full_initial_projects_upper_bound': 1000 // n,
        'tier1_evenly_paced_dispatch_span_seconds': str(D(max(0, n - 1)) * D(60) / D(150)),
        'quota_projection_limits': 'One request per image assumed, no edits/retries/other account use. Input TPM and latency unmeasured; dispatch span is not completion time.',
        'render_wall_seconds_measured_local': b['render_wall_seconds'],
        'output_bytes_measured_synthetic': b['bytes'],
        'scratch_peak_bytes_measured_synthetic': b['scratch_peak_bytes'],
    })
tts = []
for a in ledger['attempts']:
    if a['call'] in (4, 6):
        u = a['usage_metadata']
        tts.append({'call': a['call'], 'usage_derived_USD_historical_rate': str((D(u['promptTokenCount']) * D('.5') + D(u['candidatesTokenCount']) * D('6')) / D(1000000)),
                    'source_bytes': a['audio']['frames'] * a['audio']['channels'] * a['audio']['sample_width'] + 44,
                    'duration_seconds': a['audio']['seconds'], 'certainty': 'Historical usage tariff, not invoice or production distribution'})
maximum = (D(65536) * D('.25') + D(4096) * D('30')) / D(1000000)
assert maximum == D('.139264')
assert D(56) * D('.0336') == D('1.8816')
styles = ['Minimal Illustration', 'Storybook', 'Documentary Illustration']
subjects = ['A ceramic mug beside a window with morning sunlight; no lettering.', 'A cutaway diagram-like illustration of a rain cloud above mountains and a river; no lettering.']
calls = [{'call': i + 1, 'kind': 'initial', 'prompt': f'{style}. Educational video still, coherent composition, 16:9. {subject}'}
         for i, (style, subject) in enumerate((s, t) for s in styles for t in subjects)]
calls += [
    {'call': 7, 'kind': 'independent_scene_regeneration', 'prompt': 'Minimal Illustration. Educational video still, 16:9. A blue ceramic mug beside a window with warm evening sunlight; no lettering.'},
    {'call': 8, 'kind': 'independent_scene_regeneration', 'prompt': 'Documentary Illustration. Educational video still, 16:9. A cutaway diagram-like illustration of a rain cloud above mountains, a winding river and a forest; no lettering.'},
]
result = {'status': 'NOT_YET_PASS', 'scope': 'Local analysis and public documentation only', 'model': 'gemini-3.1-flash-lite-image',
          'projection_rows': rows, 'historical_B_initial_and_correction': tts,
          'conservative_image_attempt_max_USD_before_fees': str(maximum),
          'source_hashes': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in [render_path, ledger_path]},
          'provider_calls': 0, 'settled_image_cost': None, 'image_acceptance_rate': None,
          'owner_fixed_image_output_tariff_USD': '0.0336',
          'image_RPM_TPM_RPD': {'source': 'Owner supplied 2026-10-05; not independently authenticated', 'active_tier': 'Free',
                               'Free': {'RPM': 0, 'input_TPM': 0, 'RPD': 0},
                               'Tier_1_conditional_not_active': {'RPM': 150, 'input_TPM': 100000, 'RPD': 1000}},
          'live_image_pilot': 'DEFERRED_FREE_TIER_ZERO_CAPACITY; no approval requested or upgrade authorized',
          'monthly_formula': 'fixed host + backup/storage/egress + tax/fees + all project stages + corrections + paid failures + unreconciled liabilities <= 30 USD',
          'tests': ['Decimal cost arithmetic PASS', 'full-cap bound PASS'],
          'unknowns': ['actual image usage/bytes/quality', 'text/research project usage', 'tax/billing and future active Tier 1 verification', 'target-host CPU and alignment cost', 'off-host purge/storage/traffic', 'meaningful intended monthly project volume']}
manifest = {'status': 'PROPOSED_NOT_AUTHORIZED', 'model': result['model'], 'aspect_ratio': '16:9', 'resolution': '1K',
            'service': 'standard', 'calls': calls, 'retries': 0, 'grounding': False, 'references': False,
            'maximum_before_fees_USD': str(maximum * 8), 'proposed_all_in_authorization_USD': '1.50',
            'preflight': 'No submission until owner authorizes, exact endpoint/configuration bounds and account fees/quotas are validated, and ceiling fits remaining monthly budget. Unknown outcome halts experiment. No extra/fallback requests.',
            'review': 'Owner marks each image usable/unusable and notes prompt adherence, style, defects and readability at 1080p. Measure usage, latency, decoded dimensions, bytes, hashes, and output count; small pilot is not a production reliability distribution.'}
OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'analysis.json').write_text(json.dumps(result, indent=2) + '\n')
if not (OUT / 'proposed-image-pilot.json').exists():
    (OUT / 'proposed-image-pilot.json').write_text(json.dumps(manifest, indent=2) + '\n')
print(json.dumps({'status': result['status'], 'projections': rows, 'live_pilot': result['live_image_pilot'], 'provider_calls': 0}, indent=2))
