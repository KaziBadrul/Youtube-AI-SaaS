"""S9 tier workload projections; no subscription implementation or provider calls."""
import json
from decimal import Decimal as D
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/architecture/evidence/operating-economics/S9'
forecast = json.loads((OUT / 'forecast-v2.json').read_text())
variable = D(next(x['illustrative_variable_subtotal_USD'] for x in forecast['project_scenarios']
                  if x['minutes'] == 5 and x['extra_attempt_fraction_assumed'] == '.1'))
image = D(56) * D('.0336')
tiers = [
    ('one_per_week', 4, D(52) / D(12), '52 weekly units per illustrative year'),
    ('three_per_week', 12, D(156) / D(12), '156 weekly units per illustrative year'),
    ('one_per_day', 28, D(365) / D(12), '365 daily units per non-leap illustrative year'),
]
rows, cohorts = [], []
for label, four_week, monthly_avg, year_basis in tiers:
    rows.append({'tier': label, 'five_minute_equivalents_28_days': four_week,
                 'five_minute_equivalents_average_month': str(monthly_avg), 'average_basis': year_basis,
                 'initial_image_output_USD_28_days': str(image * four_week),
                 'initial_image_output_USD_average_month': str(image * monthly_avg),
                 'illustrative_variable_USD_average_month': str(variable * monthly_avg),
                 'image_plus_12_USD_host_average_month': str(image * monthly_avg + D(12))})
    for creators in [1, 3, 5]:
        units = monthly_avg * creators
        lower = image * units + D(12)
        cohorts.append({'tier': label, 'creators': creators, 'average_month_equivalents': str(units),
                        'initial_image_output_USD': str(image * units),
                        'shared_12_USD_host_plus_initial_images': str(lower),
                        'exceeds_30_from_image_host_alone': lower > D(30),
                        'illustrative_variable_plus_shared_host_USD': str(variable * units + D(12)),
                        'proven_full_budget_fit': False})
assert 112 * D('.0336') == 2 * image
assert rows[1]['five_minute_equivalents_28_days'] == 3 * rows[0]['five_minute_equivalents_28_days']
assert D(cohorts[1]['shared_12_USD_host_plus_initial_images']) == D('36.4608')
assert all(not c['proven_full_budget_fit'] for c in cohorts)
result = {'status': 'NOT_YET_PASS', 'owner_direction': {'default_script_target_minutes': 5,
          'one_video_credit_approximate_minutes': 5, 'ten_minute_video_credits': 2,
          'six_minute_video_credits': '1.2', 'duration_conversion': 'minutes / 5',
          'plan_purpose': 'Future paid subscriptions; not private Alpha allowance amendment',
          'tiers': ['1 five-minute equivalent/week', '3 five-minute equivalents/week', '1 five-minute equivalent/day']},
          'tier_projections': rows, 'cohort_projections': cohorts,
          'scene_density_sensitivity_per_five_minutes': [{'images_assumed': n, 'initial_image_output_USD': str(D(n) * D('.0336'))} for n in [30, 56, 80]],
          'open_product_decisions': ['weekly/daily reset and carryover', 'authoritative duration measurement and precision',
                                     'charging/reservation point and edits treatment if credit system adopted', 'subscription prices and margin target'],
          'qualification': 'Workload equivalent only; not a monetary exchange rate, subscription price, actual bill, month-reset policy or implemented entitlement. Existing USD liability accounting retained.',
          'tests': ['10-minute output equivalence', 'weekly tier ratios', 'shared host charged once', 'no unknown full-budget PASS'],
          'provider_calls': 0, 'production_implementation': False}
assert D(6) / D(5) == D('1.2')
assert D(10) / D(5) == D(2)
(OUT / 'tiers-v3.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(rows, indent=2))
