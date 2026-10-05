from django.urls import path
from alpha.views import health

urlpatterns = [path("health/", health, name="health")]
