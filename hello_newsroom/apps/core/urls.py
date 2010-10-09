from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from core import views

urlpatterns = patterns('',
    url(r'^community_area/(\d+).kml',
        views.comm_area_kml,name="comm_area_kml"),
    url(r'^neighborhood/(.*).kml',
        views.neighborhood_kml,name="neighborhood_kml"),
    url(r'^ward/(\d+).kml',
        views.wards_kml,name="wards_kml"),
    url(r'^cpddistrict/(\d+\w+).kml',
        views.cpddistrict_kml,name="cpddistrict_kml"),
    url(r'^cpdarea/(\d+).kml',
        views.cpdarea_kml,name="cpdarea_kml"),
    url(r'^cpdbeat/(\d+).kml',
        views.cpdbeat_kml,name="cpdbeat_kml"),
    url(r'',
        views.index,name="search"),
    url('',r'^admin', include(admin.site.urls))
)


