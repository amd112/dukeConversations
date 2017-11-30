"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views


from . import views


urlpatterns = [
	#main page, /
	url(r'^$', views.index, name = 'index'),
	#registering for dinner /register
	url(r'^register$', views.register, name = 'registration'),
	#reviewing dinner /review
	url(r'^review$', views.review, name = 'review'),
	#registering for dinner /confirm
	url(r'^confirm$', views.confirm, name = 'confirmation'),
	url(r'^confirmr$', views.confirm_review, name = 'confirmation'),
	#registering for website /signup
	url(r'^signup$', views.signup, name = 'signup'),
	#logging in to system /login
	url(r'^login$', views.log_in, name = 'login'),
	url(r'^edit$', views.edit, name = 'edit'),
	url(r'^home$', views.loginhome, name = 'loginhome'),
	url(r'^logout$', views.log_out, name = 'logout'),
	url('^password$', views.password, name = 'password'),
	url(r'^emailpage$', views.sendSimpleEmail, name = 'emailpage'),
	url('^', include('django.contrib.auth.urls')),
	url(r'^change_password/$', views.change_password, name='change_password'),
]