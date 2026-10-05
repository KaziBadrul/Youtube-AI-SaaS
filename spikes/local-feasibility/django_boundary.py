"""S1 only: disposable server-rendered boundary; never mount in the Alpha app."""
import json, os, re
from pathlib import Path
from django.conf import settings
ROOT=Path(os.environ['SPIKE_ROOT']);BASE=Path(__file__).parent
settings.configure(SECRET_KEY='public-local-spike-key-not-for-deployment',DEBUG=False,ALLOWED_HOSTS=['testserver','127.0.0.1','localhost'],ROOT_URLCONF=__name__,INSTALLED_APPS=['django.contrib.auth','django.contrib.contenttypes','django.contrib.sessions'],DATABASES={'default':{'ENGINE':'django.db.backends.sqlite3','NAME':str(ROOT/'state.sqlite3'),'OPTIONS':{'timeout':5}}},MIDDLEWARE=['django.contrib.sessions.middleware.SessionMiddleware','django.middleware.csrf.CsrfViewMiddleware','django.contrib.auth.middleware.AuthenticationMiddleware'],TEMPLATES=[{'BACKEND':'django.template.backends.django.DjangoTemplates','DIRS':[BASE/'templates'],'APP_DIRS':False}],USE_TZ=True,SESSION_COOKIE_HTTPONLY=True)
import django
django.setup()
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse,HttpResponseForbidden
from django.shortcuts import render
from django.urls import path
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
from core import Store
store=Store(ROOT)

def access(request,scene):
    rows=store.read('SELECT * FROM scenes WHERE id=?',(scene,))
    if not rows:raise PermissionError()
    with store.connection() as c:store.project(c,rows[0]['project'],request.user.id)
    return rows[0]

@login_required
@ensure_csrf_cookie
def page(request):
    return render(request,'boundary.html',{'scenes':store.read('SELECT s.* FROM scenes s JOIN projects p ON p.id=s.project WHERE p.owner=? AND p.deleted IS NULL',(request.user.id,))})
@login_required
def scene(request,scene):
    try:return JsonResponse(access(request,scene))
    except PermissionError:return HttpResponseForbidden()
@login_required
@require_POST
def autosave(request,scene):
    try:
        body=json.loads(request.body);result=store.edit(scene,body['rev'],body['words'],request.user.id)
        return JsonResponse({'result':result,'scene':access(request,scene)},status={'saved':200,'conflict':409,'locked':423}[result])
    except PermissionError:return HttpResponseForbidden()
@login_required
@require_POST
def command(request,scene):
    try:
        body=json.loads(request.body);record=access(request,scene)
        if body.get('kind')=='create' and not body.get('text','').strip():return JsonResponse({'error':'input required'},status=400)
        if body.get('kind')=='render' and store.read('SELECT id FROM scenes WHERE project=? AND outdated=1',(record['project'],)):return JsonResponse({'error':'outdated narration'},status=409)
        if body.get('kind')=='create' and body.get('mode') not in ['topic','script']:return JsonResponse({'error':'explicit interpretation required'},status=400)
        job=store.admit(body['key'],scene,request.user.id,kind='render' if body.get('kind')=='render' else 'generate')
        if body.get('kind')=='create':
            with store.tx() as c:c.execute('INSERT OR IGNORE INTO meta VALUES(?,?)',('original:'+job,json.dumps({'mode':body['mode'],'text':body['text']})))
        return JsonResponse({'job':job,'state':'queued'},status=202)
    except PermissionError:return HttpResponseForbidden()
@login_required
def progress(request,job):
    rows=store.read('SELECT j.* FROM jobs j JOIN projects p ON p.id=j.project WHERE j.id=? AND p.owner=? AND p.deleted IS NULL',(job,request.user.id))
    if not rows:return HttpResponseForbidden()
    return JsonResponse({'job':rows[0],'events':store.read('SELECT stage FROM progress WHERE job=? ORDER BY seq',(job,))})
@login_required
@require_POST
def cancel(request,job):
    response=progress(request,job)
    if response.status_code!=200:return response
    store.cancel(job);return JsonResponse({'state':'cancelling'})
@login_required
def scope(request,scene):
    try:
        s=access(request,scene);ids=[r['id'] for r in store.read('SELECT id FROM scenes WHERE project=?',(s['project'],))];return JsonResponse({'message':f'Regenerating narration updates Scenes {ids}. Their words stay unchanged.','rev':s['rev'],'scenes':ids})
    except PermissionError:return HttpResponseForbidden()
@login_required
def asset(request,scene):
    try:access(request,scene)
    except PermissionError:return HttpResponseForbidden()
    data=(ROOT/'media'/'fixture.wav').read_bytes();r=request.headers.get('Range')
    if r:
        m=re.fullmatch(r'bytes=(\d+)-(\d*)',r)
        if not m:return HttpResponse(status=416)
        start=int(m[1]);end=int(m[2]) if m[2] else len(data)-1
        if start> end or end>=len(data):return HttpResponse(status=416)
        response=HttpResponse(data[start:end+1],status=206,content_type='audio/wav');response['Content-Range']=f'bytes {start}-{end}/{len(data)}'
    else:response=HttpResponse(data,content_type='audio/wav')
    response['Accept-Ranges']='bytes';response['Cache-Control']='private, no-store';return response
@login_required
def javascript(request):return HttpResponse((BASE/'static'/'boundary.js').read_text(),content_type='text/javascript')
urlpatterns=[path('',page),path('scene/<int:scene>',scene),path('save/<int:scene>',autosave),path('command/<int:scene>',command),path('scope/<int:scene>',scope),path('progress/<str:job>',progress),path('cancel/<str:job>',cancel),path('asset/<int:scene>',asset),path('boundary.js',javascript)]
