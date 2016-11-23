#votey URL Configuration

from votes import views
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
	 url(r'^$', views.home, name='home'),
         url(r'^votes/', include('votes.urls')),
	 url(r'^admin/', admin.site.urls),
         url(r'^login/$', auth_views.login, {'template_name': 'votes/login.html'}, name='login'),
	 url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    	 url(r'^register/success/$', views.register_success),
]
