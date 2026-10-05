"""Disposable S9 v5 witness. Stdlib only; never imports provider/application code."""
from __future__ import annotations

import hashlib
import json
import re
from copy import deepcopy
from decimal import Decimal
from pathlib import Path

D = Decimal
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/architecture/evidence/operating-economics/S9'
COUNTER_VERSION = 's9-local-terminal-punctuation-v1'
RATE_SOURCE = OUT / 'analysis.json'
RATE_EVIDENCE = json.loads(RATE_SOURCE.read_text())
IMAGE_RATE = D(RATE_EVIDENCE['owner_fixed_image_output_tariff_USD'])
HISTORICAL_IMAGE_BOUND = D(RATE_EVIDENCE['conservative_image_attempt_max_USD_before_fees'])
# Preserve original text, terminal punctuation and closing quotes/brackets.
TERMINAL = re.compile(r'''[.!?।॥]+["'”’»)\]}]*(?=\s|$)''')
MISSING_COSTS = ['research/script real project usage', 'factual checking where applicable',
                 'image input/text/thinking', 'TTS request usage', 'justified retry distribution',
                 'render/compute', 'retained storage/backups/egress', 'tax/fees/FX']


def sentences(text: str) -> dict:
    if not isinstance(text, str):
        raise ValueError('script must be text')
    spans, cursor = [], 0

    def append(left: int, right: int) -> None:
        while left < right and text[left].isspace():
            left += 1
        while right > left and text[right - 1].isspace():
            right -= 1
        if any(c.isalnum() for c in text[left:right]):
            spans.append({'start': left, 'end': right, 'text': text[left:right]})

    for match in TERMINAL.finditer(text):
        append(cursor, match.end())
        cursor = match.end()
    append(cursor, len(text))
    concerns = []
    patterns = {
        'abbreviation_or_initial': r'\b(?:Dr|Mr|Mrs|Ms|Prof|Sr|Jr|etc|vs|e\.g|i\.e)\.|\b[A-Z]\.',
        'decimal_or_numeric_punctuation': r'\d[.,]\d',
        'ellipses': r'\.{2,}|…',
        'quotation_or_bracket': r'''["“”‘’«»()\[\]]''',
        'no_whitespace_after_terminal': r'[.!?।॥][A-Za-z]',
        'line_or_list_structure': r'\n\s*(?:[-*#]|\d+[.)])',
    }
    for name, pattern in patterns.items():
        if re.search(pattern, text):
            concerns.append(name)
    if spans and not TERMINAL.search(spans[-1]['text']):
        concerns.append('unterminated_tail_counted_as_one_fragment')
    return {'counter_version': COUNTER_VERSION,
            'script_sha256': hashlib.sha256(text.encode('utf-8')).hexdigest(),
            'sentence_count': len(spans), 'predicted_image_count': len(spans), 'spans': spans,
            'review_flags': concerns,
            'segmentation_status': 'REVIEW_REQUIRED' if concerns else ('INVALID_EMPTY' if not spans else 'LOCAL_FIXTURE_VALID')}


def credit_estimate(minutes=None) -> D:
    minutes = D(5) if minutes is None else D(str(minutes))
    if not minutes.is_finite() or minutes <= 0:
        raise ValueError('positive finite duration required')
    return minutes / D(5)


def estimate(count: int, credits: D | None, phase: str) -> dict:
    return {'phase': phase, 'predicted_images': count,
            'credit_estimate': None if credits is None else str(credits),
            'credit_state': 'UNRESOLVED_POST_SCRIPT_POLICY' if credits is None else 'PRELIMINARY_DURATION_ESTIMATE',
            'image_output_expected_USD': str(D(count) * IMAGE_RATE),
            'image_output_rate': {'model': 'gemini-3.1-flash-lite-image', 'USD_per_1K_image': '.0336',
                                  'source': 'Owner-fixed S9 tariff; prior README.md / analysis.json, 2026-10-05'},
            'complete_expected_USD': None, 'unresolved_components': MISSING_COSTS,
            'qualification': 'Known image-output subtotal only, not complete cost or financial authority'}


def consumption(events: list[dict]) -> dict:
    known_credits = sum((D(e['credits']) for e in events if e['credits'] is not None), D(0))
    pending = [e['attempt_id'] for e in events if e['credits'] is None]
    return {'events': deepcopy(events), 'recorded_USD': str(sum((D(e['USD']) for e in events), D(0))),
            'known_consumed_credits': str(known_credits),
            'total_consumed_credits': None if pending else str(known_credits),
            'pending_credit_policy_attempts': pending,
            'qualification': 'All event amounts are synthetic accounting fixtures, not real spend/rates'}


def update(text: str, prior: dict, events: list[dict]) -> dict:
    mapping = sentences(text)
    remaining = estimate(mapping['sentence_count'], None, 'SCRIPT_KNOWN')
    spent = consumption(events)
    return {'prior_preliminary_estimate': deepcopy(prior), 'script_scope': mapping,
            'consumed': spent, 'remaining_estimate': remaining,
            'projected_total': {'known_recorded_plus_image_output_USD': str(D(spent['recorded_USD']) + D(remaining['image_output_expected_USD'])),
                                'complete_expected_USD': None, 'credits': None},
            'old_estimate_is_not_added_to_total': True,
            'provider_calls': 0}


def admission(plan: dict, authority: dict, events: list[dict]) -> dict:
    # Authority is separate deterministic input, never taken from script/model output.
    # This .139264 bound is CONDITIONAL historical S4 evidence, not live certification.
    count = plan['script_scope']['sentence_count']
    liability = D(count) * HISTORICAL_IMAGE_BOUND
    spent = D(consumption(events)['recorded_USD'])
    reasons = []
    if plan['script_scope']['segmentation_status'] != 'LOCAL_FIXTURE_VALID':
        reasons.append('SEGMENTATION_REVIEW_OR_INVALID_INPUT')
    if count > authority['fixture_authorized_image_count']:
        reasons.append('REVISED_SCOPE_REQUIRES_SUFFICIENT_AUTHORIZATION')
    if liability > D(authority['image_liability_ceiling_USD']):
        reasons.append('IMAGE_EXPOSURE_EXCEEDS_OPERATION_AUTHORITY')
    if spent + liability > D(authority['whole_request_ceiling_USD']):
        reasons.append('WHOLE_REQUEST_EXPOSURE_EXCEEDED')
    available = D(30) - D(authority['recurring_obligations_USD']) - D(authority['other_spend_USD']) - D(authority['unknown_liabilities_USD']) - spent
    if liability > available:
        reasons.append('SHARED_BUDGET_INSUFFICIENT')
    if count > authority['available_image_requests']:
        reasons.append('PROVIDER_QUOTA_INSUFFICIENT')
    return {'state': 'ADDITIONAL_AUTHORIZATION_OR_BUDGET_HANDLING_REQUIRED' if reasons else 'WITHIN_SYNTHETIC_IMAGE_AUTHORITY_ONLY',
            'reasons': reasons, 'conditional_image_liability_USD': str(liability),
            'available_shared_USD_after_consumed_and_holds': str(available),
            'consumed_retained': consumption(events), 'authority_unchanged': deepcopy(authority),
            'maximum_complete_project_exposure': None,
            'can_submit_provider_request': False, 'provider_calls': 0,
            'qualification': 'Financial fixture only. Final scope thresholds/full-project caps, endpoint, taxes and real quotas unestablished; no live authority.'}


def fixture_script(n: int) -> str:
    return ' '.join(f'Sentence number {i} explains a simple idea.' for i in range(1, n + 1))


def run() -> None:
    tests = []

    def check(name: str, condition: bool) -> None:
        if not condition:
            raise AssertionError(name)
        tests.append({'case': name, 'result': 'PASS'})

    fixture_dir = OUT / 'fixtures-v5'
    fixture_dir.mkdir(parents=True, exist_ok=True)
    fixtures = {f'script-{n}.txt': fixture_script(n) for n in [7, 47, 214, 500]}
    for name, text in fixtures.items():
        (fixture_dir / name).write_text(text + '\n')
    topic = []
    for minutes, count, credits in [(3, 36, '.6'), (5, 60, '1'), (10, 120, '2')]:
        e = estimate(minutes * 12, credit_estimate(minutes), 'TOPIC_PRELIMINARY')
        check(f'topic_{minutes}_minutes', e['predicted_images'] == count and D(e['credit_estimate']) == D(credits))
        topic.append(e)
    check('default_5_minutes_and_1_credit', credit_estimate() == D(1))
    check('fractional_6_minutes', credit_estimate(6) == D('1.2'))
    for value in [0, -1, 'NaN', 'Infinity']:
        try:
            credit_estimate(value)
        except ValueError:
            check(f'invalid_duration_{value}', True)
        else:
            check(f'invalid_duration_{value}', False)
    events = [{'attempt_id': 'fixture-research-1', 'kind': 'valid_research', 'USD': '.008', 'credits': None},
              {'attempt_id': 'fixture-script-1', 'kind': 'valid_script', 'USD': '.012', 'credits': None}]
    initial = topic[1]
    small = update(fixtures['script-47.txt'], initial, events)
    check('generated_47_replaces_60', small['remaining_estimate']['predicted_images'] == 47)
    check('prior_valid_USD_preserved', D(small['consumed']['recorded_USD']) == D('.020') and small['consumed']['events'] == events)
    check('projected_total_not_reset_or_double_counted', D(small['projected_total']['known_recorded_plus_image_output_USD']) == D('1.5992'))
    check('unknown_consumed_credits_not_invented', small['consumed']['total_consumed_credits'] is None and len(small['consumed']['pending_credit_policy_attempts']) == 2)
    check('post_script_credit_formula_not_images_div_60', small['remaining_estimate']['credit_estimate'] is None)
    pasted = update(fixtures['script-7.txt'], {'phase': 'PASTED_SCRIPT_NO_IMAGE_HEURISTIC'}, [])
    check('pasted_known_scope_7_not_60', pasted['remaining_estimate']['predicted_images'] == 7)
    check('pasted_script_does_not_fake_script_generation_spend', D(pasted['consumed']['recorded_USD']) == 0)
    check('sentence_count_deterministic_with_exact_spans', all(sentences(fixtures['script-47.txt']) == sentences(fixtures['script-47.txt']) for _ in range(20)))
    quoted = sentences('She said "Ready?" Then we left.')
    check('closing_quote_preserved', quoted['sentence_count'] == 2 and quoted['spans'][0]['text'].endswith('"'))
    cases = [{'text': 'A fact. A question? Yes!', 'count': 3},
             {'text': 'Price is 3.14 units. Next.', 'count': 2},
             {'text': 'Dr. Smith arrived. Next.', 'count': 3},
             {'text': 'Wait... then continue.', 'count': 2},
             {'text': 'প্রথম বাক্য। দ্বিতীয় বাক্য।', 'count': 2},
             {'text': 'पहला वाक्य। दूसरा वाक्य।', 'count': 2},
             {'text': 'Unpunctuated fragment', 'count': 1},
             {'text': 'Word. ' * 500, 'count': 500}, {'text': '... !!', 'count': 0}]
    punctuation = []
    for i, c in enumerate(cases):
        parsed = sentences(c['text'])
        check(f'sentence_case_{i}', parsed['sentence_count'] == c['count'])
        punctuation.append({'fixture': c, 'output': parsed})
    check('abbreviation_flags_review_not_linguistic_certification', 'abbreviation_or_initial' in punctuation[2]['output']['review_flags'])
    authority = {'fixture_authorized_image_count': 60, 'image_liability_ceiling_USD': '8.355840',
                 'whole_request_ceiling_USD': '8.50', 'recurring_obligations_USD': '12',
                 'other_spend_USD': '0', 'unknown_liabilities_USD': '.5', 'available_image_requests': 60}
    old_authority, old_events = deepcopy(authority), deepcopy(events)
    large = update(fixtures['script-214.txt'], initial, events)
    decision = admission(large, authority, events)
    small_decision = admission(small, authority, events)
    check('large_script_scope_measured_214', large['remaining_estimate']['predicted_images'] == 214)
    check('large_script_output_cost_recomputed', D(large['remaining_estimate']['image_output_expected_USD']) == D('7.1904'))
    check('large_script_prior_work_retained', large['consumed']['events'] == old_events)
    check('large_scope_blocked_despite_expected_output_fitting_8_50', D('7.2104') < D('8.50') and 'REVISED_SCOPE_REQUIRES_SUFFICIENT_AUTHORIZATION' in decision['reasons'])
    check('model_output_cannot_modify_authority', authority == old_authority and events == old_events)
    check('expected_not_maximum_exposure', D(decision['conditional_image_liability_USD']) == D('29.802496') and D(decision['conditional_image_liability_USD']) > D('7.1904'))
    check('47_within_fixture_authority_is_not_live_permission', small_decision['state'] == 'WITHIN_SYNTHETIC_IMAGE_AUTHORITY_ONLY' and not small_decision['can_submit_provider_request'])
    poor_budget = deepcopy(authority)
    poor_budget['unknown_liabilities_USD'] = '17'
    check('unknown_hold_blocks_otherwise_valid_47', 'SHARED_BUDGET_INSUFFICIENT' in admission(small, poor_budget, events)['reasons'])
    zero_quota = deepcopy(authority)
    zero_quota['available_image_requests'] = 0
    check('free_zero_quota_blocks_47', 'PROVIDER_QUOTA_INSUFFICIENT' in admission(small, zero_quota, events)['reasons'])
    altered_credit = deepcopy(small)
    altered_credit['remaining_estimate']['credit_estimate'] = '0.0001'
    check('display_credits_do_not_change_USD_admission', admission(altered_credit, authority, events) == small_decision)
    partial = deepcopy(events)
    partial[0]['credits'] = '.1'
    check('known_credit_usage_retained_while_other_usage_pending', consumption(partial)['known_consumed_credits'] == '0.1' and consumption(partial)['total_consumed_credits'] is None)
    partial[1]['credits'] = '.2'
    check('explicit_fixture_credit_usage_preserved_without_debit_formula', D(consumption(partial)['total_consumed_credits']) == D('.3'))
    result = {'S9': 'NOT_YET_PASS', 'local_witness_result': 'PASS', 'counter_version': COUNTER_VERSION,
              'rate_provenance': {'file': str(RATE_SOURCE.relative_to(ROOT)),
                                  'sha256': hashlib.sha256(RATE_SOURCE.read_bytes()).hexdigest(),
                                  'expected_image_output_USD_per_image': str(IMAGE_RATE),
                                  'conditional_historical_attempt_bound_USD': str(HISTORICAL_IMAGE_BOUND),
                                  'bound_scope': 'S4 full-serving-cap bound before fees, historical conditional evidence; not refreshed or certified for live execution'},
              'topic_preliminary': topic, 'generated_47': small, 'pasted_7': pasted,
              'future_tier_topic_heuristic_only': [
                  {'tier': 'one_per_week', 'average_month_images': str(D(60) * D(52) / D(12)), 'image_output_USD_average_month': str(D(60) * IMAGE_RATE * D(52) / D(12))},
                  {'tier': 'three_per_week', 'average_month_images': str(D(60) * D(13)), 'image_output_USD_average_month': str(D(60) * IMAGE_RATE * D(13))},
                  {'tier': 'one_per_day', 'average_month_images': str(D(60) * D(365) / D(12)), 'image_output_USD_average_month': str(D(60) * IMAGE_RATE * D(365) / D(12))}],
              'generated_214': large, 'large_scope_admission': decision, 'small_scope_admission': small_decision,
              'sentence_edge_cases': punctuation, 'tests': tests, 'test_count': len(tests),
              'financial_fixtures': 'Synthetic consumed operations and authority only, not actual spending/credit policy. 60-authorized-image fixture is explicit test scope, not preliminary heuristic conferring authority.',
              'prelaunch_ceiling_USD': '30', 'provider_API_calls': 0, 'paid_spend_USD': '0',
              'dependencies_added': [], 'production_implementation_touched': False}
    (OUT / 'credits-v5.json').write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({'result': result['local_witness_result'], 'tests': len(tests), 'S9': result['S9'], 'provider_calls': 0}))


if __name__ == '__main__':
    run()
