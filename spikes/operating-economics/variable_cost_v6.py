"""Disposable S9 v6 arithmetic, evidence only. No network/provider/application imports."""
from decimal import Decimal as D
import hashlib
import json
from pathlib import Path
from sentence_scope_v5 import sentences

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/architecture/evidence/operating-economics/S9'
S5 = ROOT / 'docs/architecture/evidence/narration-feasibility'
MILLION = D(1000000)
IMAGE = D('.0336')  # Owner-fixed 1K-resolution image output, not per thousand images.
IMAGE_BOUND = D('.139264')  # Historical S4 serving-cap fallback, conditional before fees.

def tokens(i, o, ir, ore):
    vals = [D(str(x)) for x in (i,o,ir,ore)]
    if any(not x.is_finite() or x < 0 for x in vals):
        raise ValueError('finite nonnegative quantities required')
    return (vals[0]*vals[2]+vals[1]*vals[3])/MILLION

def total(parts):
    return None if any(x is None for x in parts) else sum(parts, D(0))

def attempt_exposure(bound, attempts):
    if attempts not in (1,2,3):
        raise ValueError('initial plus at most two retries')
    return bound * attempts

def cash(paid, verified_free_units, required_units, active=True):
    if not active:
        return {'status':'BLOCKED_NO_SERVICE_QUOTA','USD':None,'paid_equivalent_USD':paid}
    if verified_free_units is None:
        return {'status':'UNKNOWN_ENTITLEMENT','USD':None,'paid_equivalent_USD':paid}
    if required_units <= verified_free_units:
        return {'status':'VERIFIED_FREE_FIXTURE_ONLY','USD':D(0),'paid_equivalent_USD':paid}
    return {'status':'PAID_OVERAGE_FIXTURE','USD':paid*D(required_units-verified_free_units)/D(required_units),'paid_equivalent_USD':paid}

def run():
    pricing_path = OUT/'pricing-v6.json'
    pricing = json.loads(pricing_path.read_text())
    assert pricing['retrieved_on'] == '2026-10-05'
    assert D(pricing['image']['owner_fixed_output_USD_per_1K_resolution_image']) == IMAGE
    assert pricing['TTS']['input_USD_per_M'] == '0.50' and pricing['TTS']['audio_USD_per_M'] == '6'
    ledger_path = S5/'runs/approved-lite-v1/ledger.json'
    ledger = json.loads(ledger_path.read_text())
    calls = {a['call']:a for a in ledger['attempts']}
    receipts = {}
    for n,a in calls.items():
        u=a['usage_metadata']
        receipts[n]={'input_tokens':u['promptTokenCount'],'audio_tokens':u['candidatesTokenCount'],
                     'seconds':D(str(a['audio']['seconds'])),
                     'paid_equivalent_USD':tokens(u['promptTokenCount'],u['candidatesTokenCount'],'.5','6'),
                     'source_sha256':a['audio']['sha256']}
    initial = receipts[4]
    rows=[]
    for minutes in (3,5,10):
        images=minutes*12
        image_out=D(images)*IMAGE
        tts_proxy=initial['paid_equivalent_USD']*D(minutes*60)/initial['seconds']
        rows.append({'minutes':minutes,'preliminary_images':images,'preliminary_credits':D(minutes)/D(5),
                     'operations':{'research_search':None,'research_planner_synthesis':None,
                                   'script_generation':None,'pasted_script_factual_check':'NOT_APPLICABLE_TOPIC',
                                   'scene_visual_prompt_planning':None,'image_output':image_out,
                                   'image_input_text_thinking':None,'TTS_duration_proxy':tts_proxy,
                                   'expected_paid_failure_retry_reserve':None,'render_compute_allocation':None,
                                   'storage_backup_egress_allocation':None,'tax_fee_FX':None},
                     'image_plus_TTS_proxy_subtotal':image_out+tts_proxy,
                     'complete_expected_variable_USD':None,
                     'conditional_image_initial_max_USD':D(images)*IMAGE_BOUND,
                     'conditional_image_three_attempt_max_USD':D(images)*attempt_exposure(IMAGE_BOUND,3),
                     'complete_authorized_variable_max_USD':None,'possible_actual_cash_USD':None})
    fixture_path=S5/'fixture-manifest.json'
    fixture=json.loads(fixture_path.read_text())
    scope=sentences(fixture['derived_texts']['block_original'])
    known={'source':'S5 Call 4 exact approved block_original, 498 words, 32 historical scene memberships',
           'sentence_scope':scope,'image_output_USD':D(scope['sentence_count'])*IMAGE,
           'measured_TTS_USD':initial['paid_equivalent_USD'],
           'image_output_plus_measured_TTS_subtotal':D(scope['sentence_count'])*IMAGE+initial['paid_equivalent_USD'],
           'pasted_script_generation_USD':D(0),'pasted_script_generation_status':'NOT_APPLICABLE_PRESERVE_WORDS',
           'pasted_factual_check_USD':None,'planning_USD':None,'complete_expected_variable_USD':None,
           'warning':'Sentence-parser REVIEW_REQUIRED is explicit; count is local economics evidence, not production parser certification. No new images generated.'}
    correction={'one_image_output_USD':IMAGE,'one_image_complete_expected_USD':None,
                'one_image_conditional_max_one_attempt_USD':IMAGE_BOUND,
                'one_image_conditional_max_three_attempts_USD':attempt_exposure(IMAGE_BOUND,3),
                'B_segment_measured_call6_USD':receipts[6]['paid_equivalent_USD'],
                'B_segment_seconds':receipts[6]['seconds'],'B_segment_words':498,
                'B_segment_conditional_max_one_attempt_USD':tokens(8192,16384,'.5','6'),
                'B_segment_conditional_max_three_attempts_USD':attempt_exposure(tokens(8192,16384,'.5','6'),3),
                'final_correction_credits':None}
    tests=[]
    def check(name, ok):
        tests.append({'name':name,'PASS':bool(ok)})
        if not ok: raise AssertionError(name)
    for row,cost in zip(rows,('1.2096','2.016','4.032')):
        check(f"image_{row['minutes']}_min",row['operations']['image_output']==D(cost))
        check(f"scope_{row['minutes']}_min",row['preliminary_images']==row['minutes']*12)
        check(f"proxy_sum_{row['minutes']}_min",row['image_plus_TTS_proxy_subtotal']==total([row['operations']['image_output'],row['operations']['TTS_duration_proxy']]))
        check(f"unknown_total_{row['minutes']}_min",total([row['image_plus_TTS_proxy_subtotal'],None]) is None and row['complete_expected_variable_USD'] is None)
        check(f"retry_not_expected_{row['minutes']}_min",row['conditional_image_three_attempt_max_USD']>row['operations']['image_output'] and row['operations']['expected_paid_failure_retry_reserve'] is None)
    check('call4_cost',receipts[4]['paid_equivalent_USD']==D('.033260'))
    check('call6_correction_cost',receipts[6]['paid_equivalent_USD']==D('.033128'))
    check('eight_call_total',total([x['paid_equivalent_USD'] for x in receipts.values()])==D('.078970'))
    check('text_token_arithmetic_synthetic',tokens(1000,2000,'.3','2.5')==D('.0053'))
    check('search_arithmetic_synthetic_not_normal_query_count',D(4)*D('.008')==D('.032'))
    check('complete_known_expected_fixture_sum',total([D('.0053'),D('.032')])==D('.0373'))
    check('complete_known_max_fixture_sum',total([attempt_exposure(D('.139264'),3),attempt_exposure(D('.1024'),3)])==D('.724992'))
    check('unknown_expected_not_zero',total([D(2),None]) is None)
    check('unknown_max_not_zero',total([D('.724992'),None]) is None)
    check('known_pasted_no_topic_heuristic',known['image_output_USD']==D(scope['sentence_count'])*IMAGE and known['pasted_script_generation_USD']==0)
    check('pasted_check_unknown_not_free',known['pasted_factual_check_USD'] is None)
    check('same_script_deterministic',scope==sentences(fixture['derived_texts']['block_original']))
    check('correction_image_output',correction['one_image_output_USD']==D('.0336'))
    check('correction_image_retry_max',correction['one_image_conditional_max_three_attempts_USD']==D('.417792'))
    check('correction_TTS_retry_max',correction['B_segment_conditional_max_three_attempts_USD']==D('.307200'))
    free=cash(D('.008'),1,1)
    check('free_does_not_erase_paid_equivalent',free['USD']==0 and free['paid_equivalent_USD']==D('.008'))
    check('unverified_free_not_zero',cash(D('.008'),None,1)['USD'] is None)
    check('zero_image_quota_blocks_not_zero_cost',cash(IMAGE,0,1,False)['status']=='BLOCKED_NO_SERVICE_QUOTA' and cash(IMAGE,0,1,False)['USD'] is None)
    check('partial_verified_free_arithmetic',cash(D('.032'),2,4)['USD']==D('.016'))
    for a in (0,4):
        try: attempt_exposure(IMAGE_BOUND,a)
        except ValueError: check(f'invalid_attempts_{a}_rejected',True)
        else: check(f'invalid_attempts_{a}_rejected',False)
    check('new_credits_unresolved',correction['final_correction_credits'] is None)
    result={'S9':'NOT_YET_PASS','date':'2026-10-05','paid_equivalent_receipts':receipts,
            'topic_projects':rows,'known_script':known,'corrections':correction,
            'conditional_text_full_cap_attempt_USD':tokens(1048576,65536,'.3','2.5'),
            'TTS_audio_tokens_per_second_call4':D(5488)/D('171.48'),
            'tests':tests,'test_count':len(tests),'provider_API_generation_calls':0,'paid_spend_USD':D(0),
            'final_credit_formula':None,'prelaunch_monthly_ceiling_USD':D(30),
            'source_hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (ledger_path,fixture_path,OUT/'analysis.json',pricing_path)},
            'cash_view':'UNKNOWN complete cash total; images BLOCKED on owner Free tier zero quotas. Published text/TTS free and Tavily 1000 monthly need verified unused account entitlement; no account activation assumed.',
            'precision':'Decimal arithmetic; values unrounded in JSON; displayed proxies rounded separately. No empirical retry probability available.'}
    (OUT/'credits-v6.json').write_text(json.dumps(result,indent=2,ensure_ascii=False,default=str)+'\n')
    print(json.dumps({'tests':len(tests),'PASS':True,'S9':result['S9'],'sentence_count_call4':scope['sentence_count'],'sentence_review_flags':scope['review_flags'],'topic_subtotals':[str(x['image_plus_TTS_proxy_subtotal']) for x in rows]}))

if __name__=='__main__': run()
