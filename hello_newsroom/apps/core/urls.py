from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from core import views

urlpatterns = patterns('',
    url(r'',
        views.index,name="search"),
    url(r'^smstest',
        views.test_sms),
    url(r'^admin', include(admin.site.urls))
)


