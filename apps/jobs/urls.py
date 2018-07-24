from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^dashboard$', views.index),
    url(r'^new$', views.new),
    url(r'^addjob$', views.addjob),
    url(r'^update$', views.update),
    url(r'^show/(?P<job_id>\d+)$', views.show),
    url(r'^join/(?P<job_id>\d+)$', views.join),
    url(r'^edit/(?P<job_id>\d+)$', views.edit),
    url(r'^cancel/(?P<job_id>\d+)$', views.cancel),
    url(r'^destroy/(?P<job_id>\d+)$', views.destroy)
]