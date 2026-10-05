"""Read-only documentation/preservation checks; no imports of application/spike code."""
from pathlib import Path
from decimal import Decimal
import hashlib,json,re,sys
ROOT=Path(__file__).resolve().parents[4]
BUNDLE=Path(__file__).resolve().parent
checks=[]
def check(name, condition): checks.append({'name':name,'result':'PASS' if condition else 'FAIL'})
def text(name):return (ROOT/name).read_text()
def has(name,*parts):return all(s in text(name) for s in parts)
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
current=['AGENTS.md','README.md','GLOSSARY.md']+['docs/'+n+'.md' for n in ['README','ALPHA_PRODUCT_SPEC','ARCHITECTURE','ARTIFACT_MODEL','JOB_EXECUTION_MODEL','COST_MODEL','DESIGN','UX_FLOWS','VALIDATION_PLAN','ARCHITECTURE_SPIKES']]+['docs/architecture/ARCHITECTURE_FREEZE.md']
F='docs/architecture/ARCHITECTURE_FREEZE.md';A='docs/ARCHITECTURE.md';P='docs/ALPHA_PRODUCT_SPEC.md';M='docs/ARTIFACT_MODEL.md';J='docs/JOB_EXECUTION_MODEL.md';C='docs/COST_MODEL.md';U='docs/UX_FLOWS.md';D='docs/DESIGN.md'
check('freeze_exact_pass_and_version',has(F,'ARCHITECTURE FREEZE: PASS','v1','2026-10-05'))
check('hierarchy_explicit_and_scoped',has('AGENTS.md','Explicit current-session owner','Accepted current ADR','Existing code','SPEC_BLOCKED'))
check('current_ceiling_40_calendar',has(C,'$40 USD per Asia/Dhaka calendar month'))
check('current_docs_no_active_30',all(re.search(r'\$30(?![\d.])',text(p)) is None for p in current if p not in ['AGENTS.md','docs/README.md']) and has('docs/README.md','old pending-status/$30 statements applicable then'))
check('agents_30_only_history',has('AGENTS.md','Historical reports, including their earlier $30 ceiling'))
check('current_s9_pass_v14',has('docs/ARCHITECTURE_SPIKES.md','PASS FOR PRIVATE-ALPHA ARCHITECTURE FEASIBILITY','CREDITS-v14.md'))
check('no_current_pending_spike_status',all('NOT_YET_PASS' not in text(p) for p in current))
check('no_v15_report_or_bundle',not (ROOT/'docs/architecture/evidence/operating-economics/S9/CREDITS-v15.md').exists() and not (ROOT/'docs/architecture/evidence/operating-economics/S9/v15').exists())
check('qualified_host_sizing_closed',has(A,'2 vCPU / 4 GiB','host sizing is closed'))
check('sqlite_wal_short_integer_no_external_transaction',has(A,'WAL','foreign keys','short','integer','SQLite') and has(C,'no database transaction spans the network call'))
check('postgres_fallback_not_mandatory',has(A,'PostgreSQL','reconsideration'))
check('django_worker_same_host',has(A,'Django web and API','Single Python production worker','one persistent host'))
check('global_lane_and_no_http_execution',has(J,'One active production request globally','no long-running HTTP execution'))
check('serialized_heavy_maintenance',has(A,'Memory-heavy backup/maintenance must be serialized'))
check('typed_domain_no_universal_json',has(M,'typed','Original Input','Research Result','Factual Warning','Final Export','universal arbitrary JSON'))
check('version_axes_separate',has(M,'Selected','Compatible/outdated','Review needed','Last generation outcome'))
check('pinned_versions_fenced_selection',has(M,'current inputs/selection intent','worker ownership','history'))
check('b_initial_b_whole_correction',has(M,'Initial generation','Corrections regenerate the entire affected coherent segment','No C1'))
check('continuous_narration_not_visual_cuts',has(P,'Scene Audio Mappings drive visuals/captions while narration remains continuous','Visual changes are not audio cuts'))
check('no_fixed_segment_constant',has(M,'historical 500-word/3,000-byte exploration is not a final constant'))
check('next_scene_start_visuals',has(M,'image i remains visible until the mapped narration start of scene i+1'))
check('acoustic_restore_prerequisite_not_claimed',has(F,'not establish arbitrary acoustic extraction','BLOCKING BEFORE IMPLEMENTING A PARTICULAR CAPABILITY') if 'not establish arbitrary acoustic extraction' in text(F) else has(F,'S7 silent WAVs','validate ranges/coverage/joins'))
check('compound_restore_and_scoped_config',has(M,'different words','compound text/audio approval','scene only','project defaults'))
check('accepted_variations_separate',has(P,'Keep approved script text, recognized transcript and accepted spoken variations separate'))
check('invalidation_matrix_preserved',has(M,'Scene narration text','Visual description/image prompt','Caption text edit','Scene reorder/delete','Music choice/volume'))
check('disabled_captions_do_not_bypass_audio',has(M,'Disabled captions','required audio/scene-timing validity'))
check('creator_images_review_not_automatic_regeneration',has(M,'keep or replace','automatically pay for replacement'))
check('exact_entitlement_matrix',has(P,'| Research | No | Yes | Yes |','| Topic Suggestions | No | Yes | Yes |','| Custom Topic Suggestions | No | Yes | Yes |','| Expert Topic Suggestions | No | No | Yes |'))
check('suggestions_distinct_custom_model_no_alpha_promotion',has(P,'gemini-3.8-flash','No per-click LLM','not required first Private Alpha deliverables','Model selection and any bounded permitted'))
check('research_app_bounded',has(A,'bounded Gemini planner','application-controlled Tavily Basic','tool-free bounded synthesis/checking','model output cannot expand searches'))
check('pasted_preserved_explicit_translation',has(P,'Preserve pasted script wording','Translation requires approval'))
check('scope_sentence_heuristic_separate',has(C,'~12 images/minute','deterministic sentence count','retaining incurred research/script work'))
check('financial_no_free_quota_no_credit_override',has(C,'No free/provider promotional capacity is assumed','credits never authorize USD spending'))
check('unknown_liability_durable_not_blind_retry',has(C,'Unknown costs are never released','no automatic paid retry','Restored backup: pause paid work'))
check('finite_attempts_conditional_reservations',has(C,'at most two automatic retries','Each paid attempt','shared budget','before every paid submission'))
check('integer_money_rounding',has(C,'integer USD subunits','conservative rounding','binary floating-point'))
check('fixed_and_reference_cash_arithmetic',sum(map(Decimal,['24.000000','0.017182','6.598836','9.383982']))==Decimal('40.000000'))
check('5_min_conditional_cash',Decimal('40')-Decimal('24.017182')-Decimal('9.941172')==Decimal('6.041646'))
check('10_min_over_envelope',Decimal('24.017182')+Decimal('18.297012')-Decimal('40')==Decimal('2.314194') and has(P,'ten-minute fallback exceeds'))
check('unknown_cash_blocks_commitment_no_reserve_percent_policy',has(C,'UNKNOWN coverage blocks commitment','not a generation allowance','reserve-percentage decision'))
check('optional_cost_review_dual_display',has(U,'both','estimated credits and estimated USD','no mandatory financial acknowledgement') and has(D,'no mandatory estimate screen'))
check('explicit_input_mode_no_postclick_classification',has(U,'Paste opens options but does not select a mode','no post-click classification'))
check('simple_auto_manual_optional',has(U,'default off','Later corrections do not silently trigger another render'))
check('render_manifest_lock_and_previous_export',has(M,'manifest pins','render lock','earlier exports remain'))
check('render_cancel_confirmed_cessation',has(A,'bounded escalation','unlock only after confirmed cessation'))
check('render_full_validation_not_exit_shortest',has(A,'1080p/30 fps MP4','complete narration','scene order/coverage','`-shortest`'))
check('captions_shaped_local_path',has(A,'HarfBuzz','FreeType','Pillow','FFmpeg overlays'))
check('session_invite_ownership_range',has(A,'Django identity/session','operator-provisioned invited accounts','range requests','No direct public media mount'))
check('opaque_paths_image_only_upload',has(A,'opaque logical keys','image replacement is the only current media-upload scope','Never pass user filenames/paths into FFmpeg'))
check('delete_active_unknown_prohibited',has(U,'Active generation/rendering or uncertain outstanding execution prohibits deletion','never-started queued request'))
check('7day_backup24_and_end14',has(F,'7 days','≤24 additional hours','14-day download window','≤24h catastrophic-loss objective'))
check('purge_cannot_resurrect',has(A,'independently recoverable non-content deletion/purge journal','Missing or incomplete deletion history fails closed'))
check('storage_block_no_prune',has(F,'Overflow blocks creation, not silent deletion','versions','retained deleted content','scratch'))
check('design_warm_and_mobile_accessible',has(D,'Warm','forest','olive','near-black','prefers-reduced-motion','mobile supports the complete scene-correction workflow'))
check('composer_exact_owner_copy',has(D,'Tell us what you want to make.','We’ll handle the visuals, narration and captions.'))
check('english_gate_experimental_separate',has(P,'ten real English','eight','15 minutes','experimental','Before enabling each'))
check('deferred_major_features_and_followups',has(F,'Director/timeline','public signup','commercial credit','9:16 and Emphasis Text are follow-up','shipping unassigned'))
check('open_decisions_correctly_classified',has(F,'BLOCKING BEFORE TASKS.md: none found','BLOCKING BEFORE IMPLEMENTING A PARTICULAR CAPABILITY','BLOCKING BEFORE PRIVATE ALPHA INVITATIONS','DEFERRED PRODUCT DECISION','NON-BLOCKING IMPLEMENTATION DETAIL'))
check('empirical_calibration_deferred',has(F,'failure/retry/regeneration/corrections','unknown outcomes','later allowances/credits/pricing'))
check('pipeline_all_four_reuse_classes',has('docs/PIPELINE_INVESTIGATION.md','A — reusable substantially as-is','B — reusable after extraction/refactoring','C — incompatible','D — prototype/historical only'))
check('history_current_doc_originals_archived',all((BUNDLE/'before'/p).exists() for p in current if p not in ['README.md',F]))
# Links: local files only; no network is used.
missing=[]
for name in current+['docs/FEATURE_ROADMAP.md','docs/PRODUCT_DECISIONS.md','docs/PIPELINE_INVESTIGATION.md']:
 p=ROOT/name
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  target=target.strip('<>').split('#')[0]
  if not target or target.startswith(('http:','https:','app:','plugin:')):continue
  target=re.sub(r':\d+$','',target)
  resolved=Path(target) if target.startswith('/') else p.parent/target
  if not resolved.exists():missing.append({'file':name,'target':target})
check('current_local_document_links_resolve',not missing)
original=json.loads((BUNDLE/'preservation-before.json').read_text()); changed=[]
for name,item in original.items():
 p=Path(name) if name.startswith('/') else ROOT/name
 if not p.is_file() or digest(p)!=item['sha256']:changed.append(name)
check('historical_evidence_media_scripts_all_preserved',not changed)
check('tasks_not_created',not any(p.name=='TASKS.md' for p in ROOT.rglob('TASKS.md')))
result={'scope':'Read-only local documentation verification; no spike or provider execution','checks_count':len(checks),'passed':sum(c['result']=='PASS' for c in checks),'checks':checks,'missing_links':missing,'preservation':{'files_checked':len(original),'changed':changed}}
if '--record' in sys.argv:
 (BUNDLE/'verification-results.json').write_text(json.dumps(result,indent=2)+'\n')
 (BUNDLE/'preservation-result.json').write_text(json.dumps(result['preservation'],indent=2)+'\n')
print(json.dumps(result,indent=2))
raise SystemExit(0 if all(c['result']=='PASS' for c in checks) else 1)
