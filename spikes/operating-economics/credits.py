"""Disposable credit estimate / spending-scope witness. No application code."""
import json
from decimal import Decimal as D, ROUND_CEILING
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/architecture/evidence/operating-economics/S9'

def estimate(minutes=None):
    duration = D(5) if minutes is None else D(str(minutes))
    if not duration.is_finite() or duration <= 0:
        raise ValueError('duration_invalid')
    return duration / D(5)

def scope_check(credits, scenes, images_per_credit_fixture, already_spent, max_image_scope):
    # The numeric density is a disposable test parameter, not adopted policy.
    limit = int((credits * D(images_per_credit_fixture)).to_integral_value(rounding=ROUND_CEILING))
    if scenes < 1 or scenes > limit:
        return 'BLOCKED_SCENE_SCOPE'
    if already_spent + D(scenes) * D('.0336') > max_image_scope:
        return 'BLOCKED_IMAGE_OUTPUT_COST_SCOPE'
    return 'WITHIN_LOCAL_FIXTURE_SCOPE_NOT_PROVIDER_AUTHORIZATION'

assert estimate() == 1
assert estimate(6) == D('1.2')
assert estimate(10) == 2
assert estimate(3) == D('.6')
bad = []
for duration in [0, -1, 'NaN', 'Infinity']:
    try:
        estimate(duration)
    except ValueError:
        bad.append(str(duration))
assert len(bad) == 4
assert scope_check(D(1), 500, 40, D(0), D('1.344')) == 'BLOCKED_SCENE_SCOPE'
assert scope_check(D(1), 40, 40, D('.0336'), D('1.344')) == 'BLOCKED_IMAGE_OUTPUT_COST_SCOPE'
assert scope_check(D(1), 40, 40, D(0), D('1.344')) == 'WITHIN_LOCAL_FIXTURE_SCOPE_NOT_PROVIDER_AUTHORIZATION'

density = []
for images in [30, 40, 56, 80]:
    unit_cost = D(images) * D('.0336')
    density.append({'images_per_five_minutes_scenario': images, 'initial_output_USD_per_credit': str(unit_cost),
                    'one_weekly_plan_average_month_output_USD': str(unit_cost * D(52) / D(12)),
                    'three_weekly_plan_average_month_output_USD': str(unit_cost * D(13)),
                    'one_daily_plan_average_month_output_USD': str(unit_cost * D(365) / D(12))})
envelopes = []
capacity_ranges = []
for host in [0, 12, 18, 24]:
    for other_cost_reserve in [0, 5, 10]:
        for images in [30, 40, 56, 80]:
            available = max(D(0), D(30 - host - other_cost_reserve))
            unit_cost = D(images) * D('.0336')
            capacity_ranges.append({'host_USD_scenario': host, 'other_cost_reserve_USD_assumed': other_cost_reserve,
                                    'images_per_credit_scenario': images,
                                    'complete_initial_image_sets_upper_bound': int(available // unit_cost),
                                    'available_for_initial_images_USD': str(available),
                                    'qualification': 'Sensitivity only; other reserve not measured or approved, excludes additional image outputs if reserve insufficient. Not an allowance or S9 PASS.'})
for host in [0, 12, 18, 24]:
    for credits in [3, 5, 10]:
        for images in [30, 40, 56, 80]:
            output = D(credits * images) * D('.0336')
            remaining = D(30 - host) - output
            envelopes.append({'host_monthly_USD_scenario': host, 'monthly_credits_scenario': credits,
                              'images_per_credit_scenario': images, 'initial_image_output_USD': str(output),
                              'remaining_for_ALL_other_costs_USD': str(remaining),
                              'verdict': 'INFEASIBLE_FROM_IMAGE_HOST_ALONE' if remaining < 0 else 'UNPROVEN_HEADROOM',
                              'qualifications': 'Host=0 is owner-local incremental rental scenario, not zero electricity/backup/compute cost. Prior host quote scenarios only. No free cash entitlement or production affordability proven.'})

result = {'status': 'NOT_YET_PASS', 'creator_display': 'Estimated credits only; no dollar amounts',
          'conversion': 'requested topic duration in minutes / 5, default 5; final debit basis undecided',
          'examples': [{'requested_minutes': d, 'estimated_credits': str(estimate(d))} for d in [None, 3, 5, 6, 10]],
          'density_sensitivity': density, 'private_alpha_envelopes': envelopes,
          'owner_alpha_capacity_direction': 'Derive from cost; owner reply Depends on the cost',
          'cost_derived_capacity_ranges': capacity_ranges,
          'pathological_plan_test': {'sentences_or_words_input_count': 500, 'proposed_scene_count': 500,
              'disposable_images_per_credit_limit': 40, 'result': 'BLOCKED_SCENE_SCOPE',
              'provider_calls': 0, 'scope': 'Synthetic returned-plan financial rejection, not semantic narration/planner quality test or implemented input validator'},
          'tests': ['default duration', 'fractional credits', 'invalid duration rejection', '500-scene plan blocked',
                    'spent amount preserved before additional scope', 'bounded positive fixture'],
          'production_parameters_selected': False, 'production_implementation': False, 'provider_calls': 0,
          'unresolved': ['image density/maximum scope policy', 'cost-grounded Alpha allowance after obligations/uncertainty established', 'actual vs requested final debit',
                         'correction credits/included scope', 'reset/carryover', 'full internal cost and host/backup evidence']}
(OUT / 'credits-v4.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'status': result['status'], 'density': density, 'tests': result['tests'], 'provider_calls': 0}, indent=2))
