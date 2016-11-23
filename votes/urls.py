# -*- coding: latin-1 -*-
from django.conf.urls import url

from . import views
from django.contrib.auth import views as auth_views


app_name = 'votes'
urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', auth_views.login, {'template_name': 'votes/login.html'}, name='login'),
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^log/$', views.log, name='log'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]
