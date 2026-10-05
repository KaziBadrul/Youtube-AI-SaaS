"""Publication crash matrix and explicit scoped restoration invariant witness."""
import hashlib,io,json,tempfile,wave
from pathlib import Path
from core import Store,durable,wav_bytes
from publication import FakeProvider,execute,recover
from s3 import killed
from evidence import run

def seed_export(s):
 data=b'EXPORT-FIXTURE:previous valid export';durable(s.media/'old.bin',data)
 with s.tx() as c:
  c.execute('INSERT INTO artifacts VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',('old',1,1,None,'export','old.bin',hashlib.sha256(data).hexdigest(),'First approved words.','default','calm',None,0,0,1,0))
  c.execute("INSERT INTO selections VALUES(1,'export','old')")

def restore(s,asset,approved=False):
 a=s.read('SELECT * FROM artifacts WHERE id=?',(asset,))[0]
 # Decode and validate immutable source range before transactional selection.
 raw=(s.media/a['key']).read_bytes();assert hashlib.sha256(raw).hexdigest()==a['hash']
 with wave.open(io.BytesIO(raw)) as w:
  assert 0<=a['range_start']<a['range_end']<=w.getnframes()
  w.setpos(a['range_start']);assert len(w.readframes(a['range_end']-a['range_start']))==(a['range_end']-a['range_start'])*2
 with s.tx() as c:
  scene=c.execute('SELECT * FROM scenes WHERE id=?',(a['scene'],)).fetchone();s.project(c,a['project'])
  if c.execute('SELECT render_job FROM projects WHERE id=?',(a['project'],)).fetchone()[0]:raise PermissionError('render locked')
  changed=any(scene[k]!=a[k] for k in ['words','voice','delivery'])
  if changed and not approved:return 'approval_required'
  basis_rows=c.execute('SELECT value FROM meta WHERE key=?',('manual_basis:'+str(a['scene']),)).fetchone()
  basis=json.loads(basis_rows[0]) if basis_rows else {}
  compatible=all(basis.get(k)==a[k] for k in ['words','voice','delivery','hash'])
  bundle_rows=c.execute('SELECT value FROM meta WHERE key=?',('restore_bundle:'+asset,)).fetchone()
  bundle=json.loads(bundle_rows[0]) if bundle_rows else {}
  bundle_valid=all(bundle.get(k)==a[k] for k in ['hash','words','range_start','range_end'])
  timing=bundle.get('timing') if bundle_valid else None;caption=bundle.get('caption') if bundle_valid else None
  c.execute('UPDATE scenes SET words=?,voice=?,delivery=?,rev=rev+?,selected=?,outdated=?,timing=?,caption=? WHERE id=?',(a['words'],a['voice'],a['delivery'],int(changed),asset,int(not bundle_valid),timing,caption,a['scene']))
  if changed:
   script=' '.join(r[0] for r in c.execute('SELECT words FROM scenes WHERE project=? ORDER BY id',(a['project'],)))
   c.execute('INSERT OR REPLACE INTO meta VALUES(?,?)',('current_script:'+str(a['project']),script))
  # New validated automatic versions selected; incompatible manual history retained.
  c.execute('INSERT INTO selections VALUES(?,?,?) ON CONFLICT(project,slot) DO UPDATE SET artifact=excluded.artifact',(a['project'],'audio:'+str(a['scene']),asset))
  c.execute('INSERT OR REPLACE INTO meta VALUES(?,?)',('manual_status:'+str(a['scene']),'compatible' if compatible else 'outdated'))
 return 'restored'

def experiment():
 cases=[];phases=['response_received','staged','validated','installed','inside_registration','metadata_registered','financial_registered','selected','export_published']
 for repeat in range(3):
  for phase in phases:
   with tempfile.TemporaryDirectory(prefix='alpha-s7-') as tmp:
    s=Store(tmp);s.initialize();seed_export(s);job=s.admit('replace',kind='render');_,f=s.claim();killed(tmp,job,f,phase,'export')
    selected=s.read("SELECT artifact FROM selections WHERE slot='export'")[0]['artifact']
    assert selected==('a' if phase in ['selected','export_published'] else 'old')
    assert (s.media/'old.bin').read_bytes().endswith(b'previous valid export')
    if phase in ['response_received','staged','validated','installed','inside_registration']:
     assert not s.read("SELECT * FROM artifacts WHERE id='a'");assert not s.read("SELECT * FROM ledger WHERE kind='delivered'")
    recover(tmp,'a',f,'export');assert s.read("SELECT artifact FROM selections WHERE slot='export'")[0]['artifact']=='a'
    recover(tmp,'a',f,'export');assert FakeProvider(tmp).count('a')==1
    assert len(s.read("SELECT * FROM ledger WHERE kind='delivered'"))==1;s.audit()
    cases.append({'repeat':repeat,'crash':phase,'selected_before_recovery':selected,'recovered_without_resubmission':True})
 invalid=[]
 for defect in ['missing','corrupt']:
  with tempfile.TemporaryDirectory(prefix='alpha-s7-invalid-') as tmp:
   s=Store(tmp);s.initialize();seed_export(s);job=s.admit('replace',kind='render');_,f=s.claim();killed(tmp,job,f,'installed','export')
   if defect=='missing':(s.media/'a.bin').unlink()
   else:durable(s.media/'a.bin',b'invalid bytes')
   try:s.register('a','export');raise AssertionError('invalid registration accepted')
   except (FileNotFoundError,ValueError):pass
   assert not s.select('a',f);assert s.read("SELECT artifact FROM selections WHERE slot='export'")[0]['artifact']=='old'
   recover(tmp,'a',f,'export');assert FakeProvider(tmp).count('a')==1;s.audit();invalid.append(defect)
 # Complete shared response becomes history if any pinned member changed.
 shared=[]
 for changed in [1,2,3]:
  with tempfile.TemporaryDirectory(prefix='alpha-s7-shared-') as tmp:
   s=Store(tmp);s.initialize();job=s.admit('shared');_,f=s.claim();execute(tmp,job,f,'a',behavior='delayed')
   mp=Path(tmp)/'spool/a.json';m=json.loads(mp.read_text());m['members']=[{'id':1,'rev':0},{'id':2,'rev':0}];durable(mp,json.dumps(m).encode())
   s.edit(changed,0,'Changed words.',owner=2 if changed==3 else 1);FakeProvider(tmp).complete('a');outcome=recover(tmp,'a',f)
   assert outcome==('selected' if changed==3 else 'history');assert not s.read("SELECT * FROM selections WHERE slot='audio:2'");s.audit();shared.append({'edited_scene':changed,'result':outcome})
 with tempfile.TemporaryDirectory(prefix='alpha-s7-restore-') as tmp:
  s=Store(tmp);s.initialize();job=s.admit('source');_,f=s.claim();execute(tmp,job,f,'source')
  sibling=s.read('SELECT * FROM scenes WHERE id=2')[0]
  with s.tx() as c:c.execute("INSERT INTO meta VALUES('original_input:1','Exact immutable original script')")
  with s.tx() as c:
   c.execute("UPDATE scenes SET manual_timing='manual-t-v1',manual_caption='manual-c-v1' WHERE id=1")
   c.execute("UPDATE artifacts SET voice='recorded-voice',delivery='recorded-delivery' WHERE id='source'")
  original=s.read("SELECT * FROM artifacts WHERE id='source'")[0];before=s.audit()
  with s.tx() as c:
   c.execute('INSERT INTO meta VALUES(?,?)',('manual_basis:1',json.dumps({'words':original['words'],'voice':'default','delivery':'calm','hash':original['hash']})))
   c.execute('INSERT INTO meta VALUES(?,?)',('restore_bundle:source',json.dumps({**{k:original[k] for k in ['hash','words','range_start','range_end']},'timing':'timing:source','caption':'captions:source'})))
  assert restore(s,'source')=='approval_required';assert s.read('SELECT voice FROM scenes WHERE id=1')[0]['voice']=='default'
  assert restore(s,'source',True)=='restored';assert s.read('SELECT * FROM scenes WHERE id=2')[0]==sibling
  assert s.read("SELECT value FROM meta WHERE key='manual_status:1'")[0]['value']=='outdated'
  assert restore(s,'source')=='restored';assert s.read("SELECT value FROM meta WHERE key='manual_status:1'")[0]['value']=='outdated'
  # Independently compatible manual-version fixture remains current on matching restore.
  with s.tx() as c:c.execute('UPDATE meta SET value=? WHERE key=?',(json.dumps({k:original[k] for k in ['words','voice','delivery','hash']}),'manual_basis:1'))
  assert restore(s,'source')=='restored';assert s.read("SELECT value FROM meta WHERE key='manual_status:1'")[0]['value']=='compatible'
  s.edit(1,s.read('SELECT rev FROM scenes WHERE id=1')[0]['rev'],'Different current words.')
  assert restore(s,'source')=='approval_required';assert s.read('SELECT words FROM scenes WHERE id=1')[0]['words']=='Different current words.'
  assert restore(s,'source',True)=='restored';scene=s.read('SELECT * FROM scenes WHERE id=1')[0]
  assert s.read("SELECT value FROM meta WHERE key='current_script:1'")[0]['value']==original['words']+' '+sibling['words']
  assert s.read("SELECT value FROM meta WHERE key='original_input:1'")[0]['value']=='Exact immutable original script'
  assert scene['words']==original['words'] and scene['manual_timing']=='manual-t-v1' and scene['manual_caption']=='manual-c-v1'
  assert scene['timing']=='timing:source' and scene['caption']=='captions:source';assert s.read('SELECT * FROM scenes WHERE id=2')[0]==sibling
  assert s.read("SELECT * FROM artifacts WHERE id='source'")[0]==original;assert s.audit()==before
  with s.tx() as c:c.execute("DELETE FROM meta WHERE key='restore_bundle:source'")
  assert restore(s,'source')=='restored';assert s.read('SELECT outdated,timing,caption FROM scenes WHERE id=1')[0]=={'outdated':1,'timing':None,'caption':None}
 return {'publication_crashes':cases,'invalid_files_rejected_and_recovered':invalid,'shared_member_staleness':shared,'restoration_checks':['same_words_voice_delivery_requires_approval','different_words_compound_approval','current_script_updated_original_input_preserved','scene_only_config_adoption','source_range_decoded','compatible_local_timing_captions_selected','missing_compatible_bundle_remains_outdated','incompatible_manual_versions_retained_outdated','provenance_and_sibling_unchanged','no_generation_charge_for_restore'],'limitations':['Synthetic exports test durability/selection, not MP4 encoding or S6 render validation.','Silent WAV ranges prove extraction and provenance structurally; speech alignment and safe audible joins require S5.','Manual compatibility witness is conservative and deliberately simplified; production domain signatures still require implementation tests.','Process exits and fsync ordering do not emulate controller/power-loss faults on the eventual host filesystem.']}
if __name__=='__main__':run('S7',experiment)
