"""Disposable private loopback status boundary, never production code."""
import sqlite3
from django.conf import settings
settings.configure(DEBUG=False,SECRET_KEY='disposable-local-no-provider-secret',ROOT_URLCONF=__name__,ALLOWED_HOSTS=['127.0.0.1','localhost'],MIDDLEWARE=[])
import django
django.setup()
from django.http import JsonResponse
from django.urls import path
from django.core.wsgi import get_wsgi_application

def status(request):
    with sqlite3.connect('/out/state.sqlite3',timeout=5) as db:
        rows=db.execute('SELECT phase,status FROM job ORDER BY id DESC LIMIT 1').fetchall()
    return JsonResponse({'job':rows,'private_local_fixture':True})
urlpatterns=[path('status',status)]
application=get_wsgi_application()
