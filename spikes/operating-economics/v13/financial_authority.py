"""Disposable S9 V13. SQLite fake-provider authority; no production/network imports.
All fake USD receipts, authority limits and certificates are synthetic test data.
"""
from pathlib import Path
from decimal import Decimal as D, ROUND_CEILING
import hashlib, json, sqlite3, socket, tempfile, threading, sys
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'docs/architecture/evidence/operating-economics/S9/v13'
sys.path.insert(0,str(ROOT/'spikes/operating-economics'))
from sentence_scope_v5 import sentences

def deny(*a,**kw): raise RuntimeError('NO NETWORK IN V13')
socket.socket=deny; socket.create_connection=deny; socket.getaddrinfo=deny
checks=[]; scenarios=[]
def check(n,v):
    checks.append({'name':n,'result':'PASS' if v else 'FAIL'})
    if not v: raise AssertionError(n)
def rejects(fn):
    try: fn()
    except (ValueError,sqlite3.IntegrityError): return True
    return False

def usd(i): return str(D(i)/1000000)
def micro(x): return int((D(x)*1000000).to_integral_value(rounding=ROUND_CEILING))
def complete(values): return None if any(v is None for v in values) else sum(values,D(0))

class Ledger:
    """Single-host disposable SQLite ledger, persist before fake remote acceptance.
    Future project hold -> attempt hold -> spent, never all three for same charge.
    Fencing + compare-and-set before network. SENT ambiguity blocks takeover.
    No TTL releases; lease expiry alone is not cessation evidence.
    """
    def __init__(self,path):
        self.path=path; self.db=sqlite3.connect(path,timeout=10,isolation_level=None)
        self.db.row_factory=sqlite3.Row
    def initialize(self,shared=40000000,fixed=24000000,reserve=1000000,creator=10000000,project=4000000):
        self.db.executescript('''
        PRAGMA journal_mode=WAL;
        CREATE TABLE authority(id INTEGER PRIMARY KEY, ceiling INTEGER, fixed INTEGER, reserve INTEGER, creator INTEGER, project INTEGER, epoch INTEGER, cancelled INTEGER, reconciled INTEGER);
        CREATE TABLE future(id INTEGER PRIMARY KEY, shared INTEGER, allowance INTEGER);
        CREATE TABLE operation(id TEXT PRIMARY KEY, cap INTEGER, enabled INTEGER, max_attempts INTEGER, signature TEXT);
        CREATE TABLE attempt(id TEXT PRIMARY KEY, op TEXT, number INTEGER, status TEXT, bound INTEGER, hold INTEGER, allowance_hold INTEGER, cost INTEGER, consumed INTEGER, artifact TEXT, current INTEGER, receipt_valid INTEGER, receipt_cost INTEGER, UNIQUE(op,number));
        CREATE TABLE event(id INTEGER PRIMARY KEY, attempt TEXT, kind TEXT, payload TEXT, UNIQUE(attempt,kind));
        ''')
        self.db.execute('INSERT INTO authority VALUES(1,?,?,?,?,?,1,0,1)',(shared,fixed,reserve,creator,project))
        self.db.execute('INSERT INTO future VALUES(1,0,0)')
    def transaction(self,fn):
        self.db.execute('BEGIN IMMEDIATE')
        try: result=fn(); self.db.execute('COMMIT'); return result
        except BaseException: self.db.execute('ROLLBACK'); raise
    def row(self): return self.db.execute('SELECT * FROM authority').fetchone()
    def exposure(self):
        return self.db.execute('SELECT coalesce(sum(cost+hold),0) FROM attempt').fetchone()[0]+self.db.execute('SELECT shared FROM future').fetchone()[0]
    def allowance(self):
        return self.db.execute('SELECT coalesce(sum(consumed+allowance_hold),0) FROM attempt').fetchone()[0]+self.db.execute('SELECT allowance FROM future').fetchone()[0]
    def totals(self):
        a=self.row(); return {'shared':a['fixed']+a['reserve']+self.exposure(),'creator':self.allowance(),'project':self.exposure(),'ceiling':a['ceiling']}
    def audit(self):
        a=self.row()
        if any(a[k] is None for k in ['ceiling','fixed','reserve','creator','project']): raise ValueError('UNKNOWN_CASH_AUTHORITY')
        t=self.totals()
        assert t['shared']<=a['ceiling'] and t['creator']<=a['creator'] and t['project']<=a['project']
        assert not self.db.execute('SELECT 1 FROM attempt WHERE hold<0 OR cost<0 OR allowance_hold<0 OR consumed<0 OR cost+hold>bound OR consumed+allowance_hold>bound').fetchone()
        for r in self.db.execute('SELECT a.op,count(*) n,max(o.max_attempts) m FROM attempt a JOIN operation o ON o.id=a.op GROUP BY a.op'): assert r['n']<=r['m']
    def op(self,name,cap=100000,enabled=True,attempts=3,signature='fixture-v1'):
        if not 1<=attempts<=3: raise ValueError('ATTEMPT_POLICY')
        self.db.execute('INSERT INTO operation VALUES(?,?,?,?,?)',(name,cap,int(enabled),attempts,signature))
    def plan(self,amount):
        def work():
            if amount is None or amount<0: raise ValueError('UNKNOWN_BOUND')
            if self.db.execute("SELECT 1 FROM attempt WHERE status IN ('SENT','UNKNOWN')").fetchone(): raise ValueError('UNKNOWN_LANE')
            self.db.execute('UPDATE future SET shared=?,allowance=?',(amount,amount))
            a=self.row()
            if a['cancelled'] or not a['reconciled']: raise ValueError('NOT_ADMISSIBLE')
            try:self.audit()
            except AssertionError:raise ValueError('REAUTHORIZATION_OR_BUDGET_REQUIRED')
        return self.transaction(work)
    def begin(self,op,aid,epoch=1,signature='fixture-v1'):
        def work():
            a=self.row();o=self.db.execute('SELECT * FROM operation WHERE id=?',(op,)).fetchone()
            if not o or not o['enabled'] or o['cap'] is None: raise ValueError('BOUND_OR_CAPABILITY_UNVALIDATED')
            if epoch!=a['epoch'] or a['cancelled'] or not a['reconciled'] or signature!=o['signature']: raise ValueError('FENCED_OR_STALE')
            if self.db.execute("SELECT 1 FROM attempt WHERE status IN ('RESERVED','SENT','UNKNOWN')").fetchone(): raise ValueError('ACTIVE_OR_UNKNOWN')
            prior=list(self.db.execute('SELECT * FROM attempt WHERE op=? ORDER BY number',(op,)))
            if len(prior)>=o['max_attempts'] or any(r['status'] not in ('SAFE_FAILURE','PAID_FAILURE') for r in prior): raise ValueError('NO_SAFE_RETRY')
            f=self.db.execute('SELECT * FROM future').fetchone()
            if min(f['shared'],f['allowance'])<o['cap']: raise ValueError('NO_RESERVATION')
            self.db.execute('UPDATE future SET shared=shared-?,allowance=allowance-?',(o['cap'],o['cap']))
            self.db.execute('INSERT INTO attempt VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',(aid,op,len(prior)+1,'RESERVED',o['cap'],o['cap'],o['cap'],0,0,None,0,None,None))
            self.db.execute('INSERT INTO event(attempt,kind,payload) VALUES(?,?,?)',(aid,'reservation',json.dumps({'maximum':o['cap'],'epoch':epoch,'signature':signature})))
            self.audit()
        return self.transaction(work)
    def send(self,aid,epoch=1):
        def work():
            a=self.row();r=self.db.execute('SELECT * FROM attempt WHERE id=?',(aid,)).fetchone()
            if not r or r['status']!='RESERVED' or r['hold']!=r['bound']: raise ValueError('NO_COMMITTED_RESERVATION_OR_REPLAY')
            if epoch!=a['epoch'] or a['cancelled'] or not a['reconciled']: raise ValueError('FENCED_OR_CANCELLED')
            self.db.execute("UPDATE attempt SET status='SENT' WHERE id=?",(aid,))
            self.db.execute('INSERT INTO event(attempt,kind,payload) VALUES(?,?,?)',(aid,'submission','one fake transport send'))
            self.audit()
        return self.transaction(work)
    def safe_before_send(self,aid):
        def work():
            r=self.db.execute('SELECT * FROM attempt WHERE id=?',(aid,)).fetchone()
            if r['status']!='RESERVED': raise ValueError('SUBMISSION_POSSIBLE')
            self.db.execute("UPDATE attempt SET status='SAFE_FAILURE',hold=0,allowance_hold=0 WHERE id=?",(aid,))
        self.transaction(work)
    def unknown(self,aid):
        self.db.execute("UPDATE attempt SET status='UNKNOWN' WHERE id=? AND status='SENT'",(aid,)); self.audit()
    def receipt(self,aid,cost,valid):
        def work():
            r=self.db.execute('SELECT * FROM attempt WHERE id=?',(aid,)).fetchone()
            if r['status'] not in ('SENT','UNKNOWN'): raise ValueError('INVALID_RECEIPT_STATE')
            if cost is not None and not 0<=cost<=r['bound']: raise ValueError('BOUND_BREACH_HALT')
            self.db.execute('UPDATE attempt SET receipt_valid=?,receipt_cost=? WHERE id=?',(int(valid),cost,aid))
            self.db.execute('INSERT INTO event(attempt,kind,payload) VALUES(?,?,?)',(aid,'receipt',json.dumps({'valid':valid,'synthetic_known_cost':cost})))
        self.transaction(work)
    def register(self,aid):
        def work():
            r=self.db.execute('SELECT * FROM attempt WHERE id=?',(aid,)).fetchone()
            if r['status'] in ('SUCCESS','PAID_FAILURE','SAFE_FAILURE','INVALID_PENDING'): return
            if r['receipt_valid'] is None: raise ValueError('NO_VALIDATION')
            valid=bool(r['receipt_valid']);c=r['receipt_cost'];unknown=c is None
            self.db.execute('UPDATE attempt SET status=?,hold=?,allowance_hold=?,cost=?,consumed=?,artifact=?,current=? WHERE id=?',
              ('SUCCESS' if valid else ('INVALID_PENDING' if unknown else ('PAID_FAILURE' if c else 'SAFE_FAILURE')),
               r['bound'] if unknown else 0,r['bound'] if unknown and valid else 0,0 if unknown else c,c if valid and not unknown else 0,
               'history/'+aid if valid else None,int(valid and not self.row()['cancelled']),aid))
            self.db.execute('INSERT INTO event(attempt,kind,payload) VALUES(?,?,?)',(aid,'registration','valid delivered history' if valid else 'unusable rejected'))
            self.audit()
        self.transaction(work)
    def cancel(self):
        def work():
            self.db.execute('UPDATE authority SET cancelled=1,epoch=epoch+1')
            self.db.execute('UPDATE future SET shared=0,allowance=0')
            self.db.execute("UPDATE attempt SET status='SAFE_FAILURE',hold=0,allowance_hold=0 WHERE status='RESERVED'")
        self.transaction(work)
    def restart(self):
        self.db.close(); self.db=sqlite3.connect(self.path,timeout=10,isolation_level=None);self.db.row_factory=sqlite3.Row
    def attempt(self,aid): return dict(self.db.execute('SELECT * FROM attempt WHERE id=?',(aid,)).fetchone())

def run_scenarios(tmp):
    def new(name,**kw):
        l=Ledger(tmp/(name+'.sqlite')); l.initialize(**kw);l.op('image'); l.plan(300000); return l
    def success(l,aid='a',valid=True,cost=60000):
        l.begin('image',aid);l.send(aid);l.receipt(aid,cost,valid);l.register(aid);l.audit()
    def record(name,l):
        l.audit(); scenarios.append({'scenario':name,'totals_microUSD':l.totals(),'attempts':[dict(r) for r in l.db.execute('SELECT * FROM attempt')],'events':[dict(r) for r in l.db.execute('SELECT * FROM event')],'result':'PASS'})
    l=new('normal');success(l);check('valid_delivery_consumes_once',l.allowance()==260000 and l.attempt('a')['consumed']==60000);l.register('a');check('registration_idempotent',l.attempt('a')['consumed']==60000);record('normal success',l)
    for name in ['failure before submission','timeout before submission']:
        l=new(name);l.begin('image','a');l.safe_before_send('a');check(name,l.attempt('a')['hold']==0);record(name,l)
    for name in ['timeout after possible acceptance','HTTP 429 equivalent','provider 5xx equivalent','unknown billing outcome','restart while unknown liability exists']:
        l=new(name);l.begin('image','a');l.send('a');l.unknown('a');before=l.totals();l.restart()
        check(name+' retains full liability across restart',before==l.totals() and l.attempt('a')['hold']==100000)
        check(name+' blocks blind retry',rejects(lambda:l.begin('image','b')))
        record(name,l)
    for name in ['corrupt output','invalid image output']:
        l=new(name);success(l,valid=False);r=l.attempt('a');check(name+' records paid failure without allowance or artifact',r['cost']==60000 and r['consumed']==0 and r['artifact'] is None);record(name,l)
    l=new('crash_before_receipt');l.begin('image','a');l.send('a');l.restart();check('success_remote_crash_before_durable_receipt retains hold',l.attempt('a')['hold']==100000 and rejects(lambda:l.begin('image','b')));record('successful response lost before local durable receipt',l)
    l=new('crash_before_registration');l.begin('image','a');l.send('a');l.receipt('a',60000,True);l.restart();l.register('a');check('durable_response_recovered_without_new_send',l.attempt('a')['cost']==60000 and l.db.execute("SELECT count(*) FROM event WHERE kind='submission'").fetchone()[0]==1);record('successful response then crash before registration',l)
    l=new('crash_after_registration');success(l);l.restart();l.register('a');check('worker_crash_after_registration_no_recharge_or_resend',l.attempt('a')['consumed']==60000 and rejects(lambda:l.begin('image','b')));record('artifact registration then worker crash',l)
    l=new('safe_retry');l.begin('image','a');l.send('a');l.receipt('a',0,False);l.register('a');success(l,'b');check('confirmed_nonbillable_retry_counted',l.attempt('b')['number']==2);record('retry after confirmed non-billable failure',l)
    l=new('max_attempts')
    for i in range(3):l.begin('image',str(i));l.send(str(i));l.receipt(str(i),0,False);l.register(str(i));l.restart()
    check('maximum_retry_count_persistent',rejects(lambda:l.begin('image','fourth')));record('maximum retry count reached',l)
    l=Ledger(tmp/'shared.sqlite');l.initialize(fixed=39950000,reserve=0);l.op('image');check('shared_ceiling_exhausted_blocks_plan',rejects(lambda:l.plan(100000)));record('shared monthly ceiling nearly exhausted',l)
    l=Ledger(tmp/'creator.sqlite');l.initialize(creator=50000);l.op('image');check('creator_ceiling_exhausted_blocks_plan',rejects(lambda:l.plan(100000)));record('creator authorization nearly exhausted',l)
    l=new('expanded',project=10000000);l.op('script');l.plan(6100000)
    l.begin('script','script-a');l.send('script-a');l.receipt('script-a',60000,True);l.register('script-a')
    old=l.totals();count=sentences(' '.join('Word.' for _ in range(214)))['sentence_count']
    check('214_sentence_count_measured',count==214)
    check('expanded_scope_blocks_unauthorized_plan',rejects(lambda:l.plan(count*100000)))
    check('scope_rejection_preserves_spent_and_original_holds',l.totals()==old and l.attempt('script-a')['cost']==60000)
    record('60 preliminary images expands to 214 after valid script work',l)
    l.plan(47*100000)
    check('47_sentence_replan_replaces_60_without_erasing_prior_script',l.exposure()==4760000 and l.attempt('script-a')['consumed']==60000)
    record('known 47 sentence scope replaces estimate with prior consumption preserved',l)
    l=new('stale');l.db.execute('UPDATE authority SET epoch=2');check('stale_worker_fenced_before_reserve',rejects(lambda:l.begin('image','a',epoch=1)));l.begin('image','a',epoch=2);check('stale_worker_fenced_before_send',rejects(lambda:l.send('a',epoch=1)));l.send('a',epoch=2);check('one_send_only',rejects(lambda:l.send('a',epoch=2)));record('stale worker duplicate submission',l)
    l=new('concurrent');l.db.close();barrier=threading.Barrier(2);results=[]
    def compete(aid):
        x=Ledger(l.path);barrier.wait()
        try:x.begin('image',aid);results.append('admitted')
        except ValueError:results.append('rejected')
        finally:x.db.close()
    ts=[threading.Thread(target=compete,args=(str(i),)) for i in range(2)]
    for t in ts:t.start()
    for t in ts:t.join()
    l=Ledger(l.path);check('concurrent_workers_transactionally_one_attempt',sorted(results)==['admitted','rejected']);record('concurrent workers competing for one operation',l)
    l=new('cancel');l.begin('image','a');l.send('a');l.cancel();check('cancel_after_submission_keeps_liability',l.attempt('a')['hold']==100000);check('cancel_blocks_new_work',rejects(lambda:l.begin('image','b',epoch=2)));record('cancellation after paid submission',l)
    l.receipt('a',60000,True);l.register('a');check('late_paid_valid_delivery_history_only_and_allowance',l.attempt('a')['current']==0 and l.attempt('a')['consumed']==60000);record('valid canceled output arriving late',l)
    l=new('unknown_success');l.begin('image','a');l.send('a');l.receipt('a',None,True);l.register('a');check('valid_delivery_unknown_cost_stays_pending_not_fake_actual',l.attempt('a')['hold']==100000 and l.attempt('a')['cost']==0 and l.attempt('a')['allowance_hold']==100000);record('valid delivery with unknown actual billing',l)
    l=new('invalid_unknown');l.begin('image','a');l.send('a');l.receipt('a',None,False);l.register('a');check('invalid_unknown_cost_holds_money_releases_success_allowance',l.attempt('a')['hold']==100000 and l.attempt('a')['allowance_hold']==0);check('invalid_unknown_cost_no_retry',rejects(lambda:l.begin('image','b')));record('invalid output with unknown charge',l)
    l=new('disabled');l.op('unbounded',cap=None,enabled=False);check('unbounded_paid_operation_disabled',rejects(lambda:l.begin('unbounded','a')));check('send_without_reservation_denied',rejects(lambda:l.send('never_reserved')));record('unknown bound fails closed',l)
    l=new('changed_request');check('changed_payload_signature_fails_closed',rejects(lambda:l.begin('image','a',signature='changed')));record('request/config/version signature changed',l)
    l=new('restore');l.db.execute('UPDATE authority SET reconciled=0');check('restored_snapshot_blocks_unreconciled_admission',rejects(lambda:l.begin('image','a')));record('restored database pending external reconciliation',l)
    l=new('fixed_unknown');l.db.execute('UPDATE authority SET reserve=NULL');check('unknown_reserve_does_not_become_zero',l.row()['reserve'] is None)
    # Validate UNKNOWN before arithmetic, rather than interpreting NULL as a zero balance.
    check('ledger_unknown_reserve_blocks_paid_plan',rejects(lambda:l.plan(100000)))
    check('unknown_cash_envelope_requires_explicit_admission_gate',admit_cash(40000000,24000000,None,0,0,100000) is False)
    l.db.close()
    l=new('paid_failure_retry');success(l,'a',valid=False,cost=60000);success(l,'b',cost=50000)
    check('paid_failed_attempt_stays_in_owner_spend_after_retry',l.db.execute('SELECT sum(cost) FROM attempt').fetchone()[0]==110000)
    check('only_valid_retry_delivery_consumes_allowance',l.db.execute('SELECT sum(consumed) FROM attempt').fetchone()[0]==50000);record('known paid failure then safe retry',l)
    l=new('boundary');l.begin('image','a');l.send('a');l.unknown('a');l.restart()
    dt=datetime(2026,10,31,18,0,tzinfo=timezone.utc).astimezone(ZoneInfo('Asia/Dhaka'))
    check('Asia_Dhaka_calendar_cutover',dt.strftime('%Y-%m')=='2026-11')
    check('period_rollover_is_not_liability_release',l.attempt('a')['hold']==100000 and rejects(lambda:l.begin('image','b')));record('calendar rollover retains old unknown obligation',l)
    l=new('rollback');l.begin('image','a')
    try:
        def uncommitted():
            l.db.execute("UPDATE attempt SET hold=0 WHERE id='a'")
            raise ValueError('synthetic worker crash inside transaction')
        l.transaction(uncommitted)
    except ValueError:pass
    l.restart();check('transaction_crash_rolls_back_reservation_mutation',l.attempt('a')['hold']==100000);record('transaction rollback on synthetic crash',l)
    l=new('bound_breach');check('more_than_three_attempts_cannot_be_configured',rejects(lambda:l.op('four',attempts=4)));l.begin('image','a');l.send('a')
    check('receipt_above_bound_raises_incident_and_retains_exclusion',rejects(lambda:l.receipt('a',100001,True)) and rejects(lambda:l.begin('image','b')));record('simulated provider bound breach halts paid lane',l)

def admit_cash(ceiling,fixed,reserve,spent,holds,request):
    return all(v is not None for v in (ceiling,fixed,reserve,spent,holds,request)) and all(v>=0 for v in (fixed,reserve,spent,holds,request)) and fixed+reserve+spent+holds+request<=ceiling

def bounded_scope(proposed,authorized):
    if type(proposed)!=int or type(authorized)!=int or proposed<0 or proposed>authorized:raise ValueError('SCOPE_AUTHORITY_EXCEEDED')
    return proposed

def model():
    base=ROOT/'docs/architecture/evidence/operating-economics/S9'
    prices=json.loads((base/'pricing-v6.json').read_text()); caps=json.loads((ROOT/'docs/architecture/evidence/provider-feasibility/capabilities.json').read_text())['capabilities']
    v7=json.loads((base/'text-research-manifest-v7.json').read_text())
    ops=v7['operations'] if 'operations' in v7 else v7['topic']['operations']
    # Inspect actual top-level structure without assigning undocumented constants.
    rates=prices['text_reference']; textcap=next(c for c in caps if c['model']==rates['model'])
    text=[]
    for op in ops:
        if op['kind']=='text':
            c=D(textcap['maximum_input_tokens'])*D(rates['input_USD_per_M'])/1000000+D(op['max_output_tokens_including_thinking'])*D(rates['output_thinking_USD_per_M'])/1000000
            text.append({'name':op['name'],'model':op['model'],'input_cap':op['max_input_tokens'],'output_including_thinking_cap':op['max_output_tokens_including_thinking'],'max_requests':1,'max_attempts':3,'billing_unit':'input and total output/thinking tokens','thinking_cap':'shares configured total output; no unbounded extra reasoning','maximum_input_proof_status':'UNKNOWN','artifact':op['result_artifact'],'depends_on':op['depends_on'],'price_source':'pricing-v6.json and S4 capabilities.json','v7_candidate_attempt_USD':op['candidate_max_USD_per_attempt'],'serving_input_fallback_attempt_USD':usd(micro(c)),'expected_USD':None,'enabled':False,'bound_evidence':'V7 candidate narrow input unvalidated; S4 serving fallback conditional; output total/transport/rate/account proof required','usable_max_USD':None})
    search=D(prices['search']['PAYGO_USD_per_credit'])*6
    one=sum((D(o['serving_input_fallback_attempt_USD']) for o in text),D(0))+search
    writing=next(D(o['serving_input_fallback_attempt_USD']) for o in text if o['name']=='script_generation')
    ic=next(c for c in caps if c['model']==prices['image']['model']);tc=next(c for c in caps if c['model']==prices['TTS']['model'])
    image_full=(D(ic['maximum_input_tokens'])*D(prices['image']['input_USD_per_M'])+D(ic['maximum_output_tokens'])*D(prices['image']['image_output_USD_per_M']))/1000000
    tts_full=(D(tc['maximum_input_tokens'])*D(prices['TTS']['input_USD_per_M'])+D(tc['maximum_output_tokens'])*D(prices['TTS']['audio_USD_per_M']))/1000000
    projects=[]
    for minutes in [3,5,10]:
        n=12*minutes; rate=D(prices['image']['owner_fixed_output_USD_per_1K_resolution_image'])
        projects.append({'kind':'topic','requested_minutes':minutes,'preliminary_images':n,'preliminary_credits':str(D(minutes)/5),'actual_images':None,'B_segment_count':None,'expected_total_USD':None,'usable_whole_project_max_USD':None,'image_output_only_first_attempt_USD':str(n*rate),'image_output_only_three_attempt_USD':str(n*rate*3),'conditional_provider_max_formula':'A_text*T_text + A_image*N*I + A_TTS*K*T; actual N/K re-admitted; excludes unknown cash extras','conditional_IF_preliminary_N_and_one_B_segment_single_attempt_USD':str(one+n*image_full+tts_full),'conditional_IF_preliminary_N_and_one_B_segment_three_attempt_USD':str(3*(one+n*image_full+tts_full)),'enabled':False})
    pasted='The sky appears blue. Tiny particles scatter light. We see that scattered light.'
    n=sentences(pasted)['sentence_count'];projects.append({'kind':'pasted','fixture_text':pasted,'actual_images':n,'sentence_review_status':'local limited parser unambiguous fixture only','script_generation_required':False,'B_segment_count':None,'conditional_check_search_one_attempt_USD':str(one-writing),'usable_whole_project_max_USD':None,'expected_total_USD':None,'conditional_IF_one_B_segment_single_attempt_USD':str(one-writing+n*image_full+tts_full),'conditional_IF_one_B_segment_three_attempt_USD':str(3*(one-writing+n*image_full+tts_full)),'enabled':False})
    for minutes,images in [(3,36),(5,60),(10,120)]:check(f'image_scope_{minutes}_minutes',12*minutes==images)
    check('image_output_baselines',[D(p['image_output_only_first_attempt_USD']) for p in projects[:3]]==[D('1.2096'),D('2.016'),D('4.032')])
    check('three_attempt_output_only_exposure',[D(p['image_output_only_three_attempt_USD']) for p in projects[:3]]==[D('3.6288'),D('6.048'),D('12.096')])
    check('full_conditional_image_dimensions',image_full==D('.139264'))
    check('full_conditional_TTS_dimensions',tts_full==D('.1024'))
    check('model_output_cannot_widen_query_authority',rejects(lambda:bounded_scope(50,6)))
    check('model_output_cannot_widen_total_output_cap',rejects(lambda:bounded_scope(16385,16384)))
    check('UNKNOWN_not_zero',complete([D(1),None]) is None)
    check('pasted_no_script_generation_and_sentence_count',n==3 and writing>0)
    check('expected_not_retry_maximum',all(p['expected_total_USD'] is None for p in projects))
    check('unvalidated_provider_operations_not_enabled',all(not p['enabled'] and p['usable_whole_project_max_USD'] is None for p in projects))
    check('free_capacity_not_assumed',prices['image']['free']=='Unavailable; owner active quota zero')
    fixed=D('24.005932313307');sens=[]
    for pct in [0,10,20,30]:
        nominal=D(40)/(1+D(pct)/100)-fixed
        sens.append({'total_cash_uplift_percent_sensitivity_NOT_POLICY':pct,'nominal_pre_uplift_provider_headroom_USD':str(nominal),'complete_authorized_generation_budget_USD':None})
    check('fixed_envelope_40',D(40)-fixed==D('15.994067686693'))
    check('reserve_sensitive_block',not admit_cash(40000000,24000000,None,0,0,1))
    check('negative_free_capacity_denies',not admit_cash(40000000,41000000,0,0,0,1))
    check('creator_credit_UI_not_authority',not admit_cash(40000000,39000000,0,0,0,2000000))
    historical=ROOT/'demo-video-example/02_script_humanized.txt';hs=sentences(historical.read_text());hn=hs['sentence_count']
    check('same_script_deterministic_scope',hs==sentences(historical.read_text()))
    projects.append({'kind':'pasted_existing_representative','source':str(historical.relative_to(ROOT)),'source_sha256':hashlib.sha256(historical.read_bytes()).hexdigest(),'actual_local_count':hn,'segmentation_review_required':True,'reason':'V7 ellipsis/quote flags; local count is not reviewed production sentence scope','B_segment_count':None,'script_generation_required':False,'expected_total_USD':None,'usable_whole_project_max_USD':None,'conditional_IF_count_accepted_and_one_B_segment_single_attempt_USD':str(one-writing+hn*image_full+tts_full),'conditional_IF_count_accepted_and_one_B_segment_three_attempt_USD':str(3*(one-writing+hn*image_full+tts_full)),'enabled':False})
    # Synthetic byte/traffic caps test semantics, not owner-selected operating caps.
    def storage_fits(cap,active,versions,deleted,scratch,backup_stage,new_bytes):
        vals=[cap,active,versions,deleted,scratch,backup_stage,new_bytes]
        return all(v is not None and v>=0 for v in vals) and sum(vals[1:])<=cap
    check('deleted_and_previous_versions_count_against_storage_cap',not storage_fits(100,30,30,30,5,5,1))
    check('storage_cap_blocks_creation_not_silent_version_deletion',storage_fits(100,30,30,30,5,5,0) and not storage_fits(100,30,30,30,5,5,1))
    check('unknown_staging_or_storage_cap_blocks_creation',not storage_fits(None,1,1,1,1,1,1) and not storage_fits(100,1,1,1,1,None,1))
    def transfer_cost(bytes_used,included_bytes,usd_per_byte):
        return None if any(v is None for v in (bytes_used,included_bytes,usd_per_byte)) else max(0,bytes_used-included_bytes)*usd_per_byte
    check('included_traffic_precedes_paid_egress',transfer_cost(90,100,D('.01'))==0 and transfer_cost(120,100,D('.01'))==D('.20'))
    check('unknown_traffic_contract_not_zero',transfer_cost(120,None,D('.01')) is None)
    return {'text_operations':text,'search':{'provider':'Tavily Basic','queries_max':6,'attempts_max_per_query':3,'unit':'one credit per pinned Basic request','one_attempt_query_batch_USD':str(search),'three_attempt_query_batch_USD':str(search*3),'enabled':False,'reason':'account/terms/rate/transport proof before enablement; no verified free credits'},'image':{'model':prices['image']['model'],'output_tariff_USD':'.0336','tariff_status':'Owner-fixed 1K-resolution output sensitivity, V6 dated evidence; not permanent or complete','input_serving_fallback_tokens':ic['maximum_input_tokens'],'all_output_serving_fallback_tokens':ic['maximum_output_tokens'],'conditional_attempt_full_modal_worst_rate_USD':str(image_full),'enabled':False,'usable_attempt_bound_USD':None,'reason':'exact endpoint/output/thinking/single-send/billing rate proof unresolved'},'TTS':{'model':prices['TTS']['model'],'B_initial_and_B_corrections':True,'conditional_attempt_serving_USD':str(tts_full),'input_tokens_max':tc['maximum_input_tokens'],'audio_output_tokens_max':tc['maximum_output_tokens'],'enabled':False,'usable_attempt_bound_USD':None,'rate_valid_through':prices['TTS']['valid_through'],'segment_count':'derive deterministic scope; not frozen','empirical_S5_eight_call_paid_equivalent_USD':'.07897'},'projects':projects,'text_search_conditional_serving_fallback_single_attempt_USD':str(one),'text_search_conditional_serving_fallback_three_attempt_USD':str(one*3),'v7_text_search_narrow_three_attempt_USD':'.410964','fixed_partial_USD':str(fixed),'ceiling_USD':'40','nominal_remainder_USD':str(D(40)-fixed),'sensitivities':sens,'complete_fixed_cash_envelope_USD':None,'owner_reserve_policy':None,'current_account_spend_and_liabilities':None,'pricing_provenance':'Reused dated S4/V6/V7/V8/V11/V12 captures; no public price refresh/current provider assertion; quotes invalidate before enablement','local_operations':['sentence counting and membership','alignment','captions','FFmpeg render','validation'],'local_generation_allowance_debit':0,'local_infrastructure_cost_is_not_zero':True,'optional_discovery_operations':'excluded from normal video; disabled until separately bounded/entitled','credit_formula':None,'Alpha_allowances':None}

def run():
    OUT.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='s9-v13-') as t:run_scenarios(Path(t))
    m=model()
    before=json.loads((OUT/'preservation-before.json').read_text());changed=[p for p,r in before.items() if not (ROOT/p).is_file() or hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=r['sha256']]
    index='docs/architecture/evidence/operating-economics/S9/README.md'
    check('historical_V1_V12_files_and_prior_spikes_unchanged',set(changed)<={index})
    if index in changed:check('original_live_index_archived',hashlib.sha256((OUT/'before'/index.replace('/','__')).read_bytes()).hexdigest()==before[index]['sha256'])
    check('calendar_ceiling_authority_40',m['ceiling_USD']=='40')
    check('current_documents_link_V13_and_keep_40',all('CREDITS-v13.md' in (ROOT/f).read_text() and 'US$40' in (ROOT/f).read_text() for f in ['docs/README.md','docs/ALPHA_PRODUCT_SPEC.md','docs/ARCHITECTURE.md','docs/COST_MODEL.md','docs/ARCHITECTURE_SPIKES.md','docs/architecture/evidence/operating-economics/S9/README.md']))
    check('local_transforms_not_provider_allowance',m['local_generation_allowance_debit']==0 and m['local_infrastructure_cost_is_not_zero'])
    result={'S9':'NOT_YET_PASS','checks_passed':len(checks),'checks':checks,'scenarios':scenarios,'scenario_count':len(scenarios),'model':m,'provider_API_calls':0,'fake_transport_submissions':'SQLite events only, not HTTP','paid_spend_USD':'0','downloads':0,'production_changes':False,'TASKS_changes':False,'hosting_selected_or_provisioned':False,'deployment':False,'purchases':False,'empirical_provider_behavior_validated':False,'architecture_frozen':False}
    (OUT/'RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    (OUT/'financial-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
    (OUT/'preservation-result.json').write_text(json.dumps({'files_checked':len(before),'changed_current_index':changed,'historical_V1_V12_unchanged':True,'previous_live_index_archived':True},indent=2)+'\n')
    print(json.dumps({'verdict':result['S9'],'checks':len(checks),'scenarios':len(scenarios),'conditional_text_search_single':m['text_search_conditional_serving_fallback_single_attempt_USD'],'projects':m['projects'],'history_checked':len(before)},indent=2))
if __name__=='__main__':run()
