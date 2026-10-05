"""Owner budget amendment: deterministic arithmetic/docs/history checks, no providers."""
from decimal import Decimal as D
from pathlib import Path
import hashlib,json,math,socket
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'docs/architecture/evidence/operating-economics/S9/v12'
def deny(*a,**k):raise AssertionError('network forbidden in local budget witness')
socket.socket=deny;socket.create_connection=deny;socket.getaddrinfo=deny
checks=[]
def check(name,ok):
 checks.append({'name':name,'result':'PASS' if ok else 'FAIL'})
 assert ok,name
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def complete_sum(*values):return None if any(v is None for v in values) else sum(values,D(0))
def headroom(cap,fixed,spent,holds,reserve):
 return None if any(v is None for v in [fixed,spent,holds,reserve]) else cap-fixed-spent-holds-reserve
def request_fits(free,request_remaining,attempt_max,unknown_outcome=False):
 return free is not None and not unknown_outcome and attempt_max<=free and attempt_max<=request_remaining
old=json.loads((ROOT/'docs/architecture/evidence/operating-economics/S9/v11/RESULTS.json').read_text())
archive=old['backup_storage_sensitivity']['archive_bytes'];backup=D(archive)*D(2)/D(10**9)*D('.00695');host=D(24);fixed=host+backup;ceiling=D(40);nominal=ceiling-fixed
partial=D('2.074187543736878936319104269');prior=D(old['envelopes'][0]['remaining_nominal_USD']);optimistic=max(0,math.floor(nominal/partial))
check('explicit_active_owner_ceiling',ceiling==D(40))
check('qualified_host_local_scope_preserved',old['resource_classification']=='SAFE_ENOUGH_FOR_ALPHA' and old['host_sizing_closed_at_local_scope'])
check('measured_backup_arithmetic',backup==D('.0059323133070'))
check('nominal_fixed_arithmetic',fixed==D('24.0059323133070'))
check('new_nominal_remainder',nominal==D('15.9940676866930'))
check('change_is_exactly_ten_USD',nominal-prior==D(10))
check('complete_fixed_unknown_not_zero',complete_sum(host,backup,None) is None)
check('unknown_reserve_prevents_actual_headroom_claim',headroom(ceiling,fixed,D(0),D(0),None) is None)
check('unknown_current_spending_prevents_actual_headroom_claim',headroom(ceiling,fixed,None,D(0),D(0)) is None)
check('unknown_liability_prevents_actual_headroom_claim',headroom(ceiling,fixed,D(0),None,D(0)) is None)
check('existing_spend_and_holds_preserved_in_budget_revision',headroom(D(40),D(24),D(9),D(3),D(0))==D(4) and headroom(D(30),D(24),D(9),D(3),D(0))==D(-6))
check('higher_monthly_cap_does_not_raise_request_authority',not request_fits(nominal,D(1),D(2)))
check('unknown_outcome_still_blocks_blind_duplicate',not request_fits(nominal,D(5),D(1),True))
check('known_holds_consumed_once',headroom(ceiling,fixed,D(1),D(2),D(3))==nominal-D(6))
check('negative_balance_denies_admission',not request_fits(D(-1),D(3),D(1)))
check('unknown_admission_denied',not request_fits(None,D(3),D(1)))
check('unknown_project_expected_not_replaced_by_partial',complete_sum(partial,None) is None)
check('optimistic_partial_floor_not_allowance',optimistic==7 and int(nominal/partial)==optimistic)
check('image_and_TTS_partial_preserved',D('2.016')+D('.058187543736878936319104269')==partial)
check('conditional_text_cap_not_expected_or_usable_max',complete_sum(D('.410964'),None) is None)
active_files=['docs/README.md','docs/ALPHA_PRODUCT_SPEC.md','docs/ARCHITECTURE.md','docs/COST_MODEL.md','docs/ARCHITECTURE_SPIKES.md','docs/VALIDATION_PLAN.md','docs/FEATURE_ROADMAP.md','docs/PRODUCT_DECISIONS.md','docs/ARCHITECTURE_DISCOVERY.md','docs/architecture/evidence/operating-economics/S9/README.md']
check('current_docs_have_explicit_40_authority',all('40/month' in (ROOT/p).read_text() for p in active_files))
check('cost_authority_table_updated','currently US$40/month' in (ROOT/'docs/COST_MODEL.md').read_text())
check('product_requirement_updated','current strict total prelaunch Alpha operating ceiling is US$40/month' in (ROOT/'docs/ALPHA_PRODUCT_SPEC.md').read_text())
check('validation_constraint_updated','shared US$40/month ceiling' in (ROOT/'docs/VALIDATION_PLAN.md').read_text())
check('current_S9_monthly_invariant_updated','unreconciled liabilities <= $40' in (ROOT/'docs/architecture/evidence/operating-economics/S9/README.md').read_text())
check('owner_last_sizing_rule_preserved','no further host-sizing experiments unless failure' in (ROOT/'docs/ARCHITECTURE_SPIKES.md').read_text())
manifest=json.loads((OUT/'preservation-before.json').read_text());changed=[name for name,r in manifest.items() if not (ROOT/name).is_file() or sha(ROOT/name)!=r['sha256']]
allowed='docs/architecture/evidence/operating-economics/S9/README.md'
check('all_prior_evidence_and_spike_files_unchanged',set(changed)<={allowed})
check('prior_live_index_bytes_archived',sha(OUT/'before'/allowed.replace('/','__'))==manifest[allowed]['sha256'])
check('V1_V11_reports_preserved',all(sha(ROOT/name)==r['sha256'] for name,r in manifest.items() if 'CREDITS-v' in name))
(OUT/'preservation-result.json').write_text(json.dumps({'files_checked':len(manifest),'changed':changed,'historical_evidence_unchanged':True,'prior_index_archived':True},indent=2)+'\n')
result={'S9':'NOT_YET_PASS','active_total_monthly_ceiling_USD':str(ceiling),'previous_ceiling_USD':'30','host_nominal_USD':str(host),
 'measured_archive_bytes':archive,'snapshot_copies_sensitivity_not_retention_policy':2,'backup_storage_only_paid_equivalent_USD':str(backup),
 'partial_fixed_USD':str(fixed),'complete_fixed_cash_USD':None,'nominal_remainder_before_reserves_spend_holds_USD':str(nominal),'increase_USD':str(nominal-prior),
 'actual_admittable_generation_budget_USD':None,'safety_fees_FX_reserve_USD':None,'current_settled_spend_USD':None,'current_liabilities_reservations_USD':None,
 'five_minute_partial_image_TTS_proxy_USD':str(partial),'complete_expected_project_USD':None,'usable_whole_project_maximum_USD':None,
 'optimistic_partial_only_floor_not_capacity_or_allowance':optimistic,'guaranteed_capacity':None,'creator_allowances':None,'final_credit_conversion':None,
 'expected_versus_maximum':'Existing partial projections and conditional caps stay qualified; no new expected usage/retry probabilities invented.',
 'pricing_provenance':'Preserved V8 official-price capture and V11 measured archive; nominal sensitivities, not refreshed account quotes or provider selection.',
 'host_sizing_closed':True,'further_sizing_only_on_failure':True,'checks':checks,'checks_passed':len(checks),'provider_API_calls':0,'paid_spend_USD':'0',
 'production_changes':False,'TASKS_changes':False,'hosting_selected':False,'deployments':False,'purchases':False,'new_experiments':False,'architecture_frozen':False}
(OUT/'RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
