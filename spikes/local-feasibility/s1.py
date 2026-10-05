import ast,json,os,subprocess,sys,tempfile,time
from pathlib import Path
from core import Store,durable,wav_bytes
from evidence import BASE,run

def experiment():
 with tempfile.TemporaryDirectory(prefix='alpha-s1-') as tmp:
  os.environ['SPIKE_ROOT']=tmp;s=Store(tmp);s.initialize();durable(s.media/'fixture.wav',wav_bytes())
  import django_boundary
  from django.core.management import call_command
  from django.contrib.auth import get_user_model
  from django.test import Client
  import django
  call_command('migrate',verbosity=0)
  User=get_user_model();alice=User.objects.create_user('alice',password='local-test-only');bob=User.objects.create_user('bob',password='local-test-only')
  a=Client(enforce_csrf_checks=True);b=Client(enforce_csrf_checks=True);anonymous=Client()
  assert a.login(username='alice',password='local-test-only');assert b.login(username='bob',password='local-test-only')
  page=a.get('/');assert page.status_code==200 and b'Create Video' in page.content and b'Scene 1' in page.content
  token=a.cookies['csrftoken'].value
  def post(path,data,client=a):return client.post(path,json.dumps(data),content_type='application/json',HTTP_X_CSRFTOKEN=client.cookies.get('csrftoken',a.cookies['csrftoken']).value)
  checks=[]
  assert anonymous.get('/asset/1').status_code==302;assert b.get('/asset/1').status_code==403;assert a.get('/asset/3').status_code==403
  response=a.get('/asset/1',HTTP_RANGE='bytes=0-43');assert response.status_code==206 and len(response.content)==44 and response['Cache-Control']=='private, no-store';assert a.get('/asset/1',HTTP_RANGE='bytes=999999-').status_code==416
  assert a.post('/save/1','{}',content_type='application/json').status_code==403;checks+=['session_auth_private_assets_cross_user_range_csrf']
  assert post('/save/1',{'rev':0,'words':'New approved narration.'}).status_code==200
  assert post('/save/1',{'rev':0,'words':'Stale overwrite.'}).status_code==409
  assert s.read('SELECT words,outdated FROM scenes WHERE id=2')[0]=={'words':'Sibling approved words.','outdated':0};checks+=['optimistic_autosave_conflict_selective_invalidation']
  t=time.perf_counter();r=post('/command/1',{'key':'one','kind':'create','mode':'script','text':'Exact original script!'});assert r.status_code==202;latency=time.perf_counter()-t
  job=r.json()['job'];assert post('/command/1',{'key':'one','kind':'create','mode':'script','text':'Changed duplicate'}).json()['job']==job
  assert json.loads(s.read('SELECT value FROM meta WHERE key=?',('original:'+job,))[0]['value'])['text']=='Exact original script!'
  assert a.get('/scope/1').json()['scenes']==[1,2]
  worker=subprocess.Popen([sys.executable,str(BASE/'s1worker.py'),tmp]);states=set();stages=set()
  while worker.poll() is None:
   d=a.get('/progress/'+job).json();states.add(d['job']['state']);stages.update(x['stage'] for x in d['events']);time.sleep(.03)
  assert worker.returncode==0;final=a.get('/progress/'+job).json();assert final['job']['state']=='completed' and len(final['events'])==3
  assert b.get('/progress/'+job).status_code==403;checks+=['one_tap_queue_idempotency_script_preservation_separate_worker_polling']
  with s.tx() as c:c.execute('UPDATE scenes SET outdated=0 WHERE project=1')
  renderjob=post('/command/1',{'key':'render','kind':'render'}).json()['job'];claimed=s.claim();assert claimed[0]==renderjob
  assert post('/save/1',{'rev':1,'words':'Forbidden edit'}).status_code==423
  assert a.get('/asset/1').status_code==200;assert post('/cancel/'+renderjob,{}).status_code==200
  assert not s.finish(renderjob,claimed[1],confirmed=False);assert s.finish(renderjob,claimed[1],confirmed=True)
  assert post('/save/1',{'rev':1,'words':'Allowed after confirmed stop'}).status_code==200
  assert s.delete(1,100)=='deleted';assert a.get('/asset/1').status_code==403;checks+=['render_lock_server_enforcement_reads_cancel_confirmed_unlock_deleted_denial']
  # Reuse only an AST-extracted pure formatter, no import-time SDK/client execution.
  legacy=Path('/Users/kazibadrul/Python Codes/YoutubeAI/python-scripts/make_video.py');tree=ast.parse(legacy.read_text())
  funcs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='seconds_to_srt'];namespace={};exec(compile(ast.Module(body=funcs,type_ignores=[]),str(legacy),'exec'),namespace)
  assert namespace['seconds_to_srt'](65.25)=='00:01:05,250';checks+=['safe_legacy_helper_python_runtime']
  js=subprocess.run(['node',str(BASE/'static/boundary.test.js')],capture_output=True,text=True,check=True)
  checks+=['executed_vanilla_js_scene_autosave_regen_polling_checks']
  return {'checks':checks,'django':django.get_version(),'command_response_seconds':latency,'worker_states_observed':sorted(states),'worker_events':final['events'],'js_test_output':js.stdout.strip(),'limitations':['No full visual/browser-device acceptance; JS runs in a deterministic DOM/fetch witness plus real Django HTTP tests.','Provider/alignment native dependencies and FFmpeg caption/render compatibility remain S4/S5/S6; only safe Python helper and separate fake-child execution tested.','Fixtures are not product models or production code.']}
if __name__=='__main__':run('S1',experiment)
