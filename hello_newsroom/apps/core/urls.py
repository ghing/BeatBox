from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from core import views
from messaging.views import twilio

urlpatterns = patterns('',
    url(r'^m/register', views.mobile_register),
    url(r'^m/login', views.mobile_login),
    url(r'^m', views.mobile_index),
    url(r'^smshook', twilio),
    url(r'^admin', include(admin.site.urls)),
    url(r'', views.mobile_index,name="registersubmit")
)


