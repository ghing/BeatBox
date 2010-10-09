import logging

from django.shortcuts import render_to_response
from django.contrib.gis.geos import *
from django.contrib.gis.measure import Distance
from django.contrib.gis.shortcuts import render_to_kml

from geopy import geocoders

from core import models

log = logging.getLogger("hello_newsroom")

# NOTE: Under load, this strategy is likely to max out your Google API Key. 
# Where possible, geocode addresses using client side calls.
GEOCODER = geocoders.Google()
def index(request):
    template_dict = {}
    try:
        query = request.REQUEST['query']
        client_geocode = request.REQUEST.get('geocode')
        if client_geocode:
            address = request.REQUEST.get('address')
            remainder = None
            point = make_point(client_geocode)
        else:
            log.warn("Geocode was not received in query. Trying to geocode again.")
            address, remainder, point = geocode(query)
            

        template_dict['query'] = query
        template_dict['address'] = address
        template_dict['remainder'] = remainder
        template_dict['point'] = point
        print point
        try:
            template_dict['community_area'] = models.CommunityArea.objects.get(geom__contains=point)
        except models.CommunityArea.DoesNotExist:
            print 'CA dont exist'
            pass
        try:
            template_dict['neighborhood'] = models.Neighborhoods.objects.get(geom__contains=point)
        except models.Neighborhoods.DoesNotExist:
            print 'Neighborhood dont exist'
            pass
        try:
            template_dict['cpddistrict'] = models.CpdDistricts.objects.get(geom__contains=point)
        except models.CpdDistricts.DoesNotExist:
            print 'CPDDist dont exist'
            pass

        try:
            template_dict['cpdbeats'] = models.CpdBeats.objects.get(geom__contains=point)
        except models.CpdBeats.DoesNotExist:
            print 'CpdBeats dont exist'
            pass

        try:
            template_dict['wards'] = models.Wards.objects.get(geom__contains=point)
        except models.Wards.DoesNotExist:
            print 'Wards dont exist'
            pass
        try:
            template_dict['cpdareas'] = models.CpdAreas.objects.get(geom__contains=point)
        except models.CpdAreas.DoesNotExist:
            print 'CpdAreas dont exist'
            pass


    except KeyError:
        pass # no query
    return render_to_response('core/index.html', template_dict)
#TODO: need to assure that there are no collisions when just passing back the 
# numeric identifiers for lookups.... for ex, if someone enters an address where the 
# beat number and community area number are the same will there be a problem returning
# both kml files?
def comm_area_kml(request, area_number):    
    ca = models.CommunityArea.objects.get(area_number=area_number)
    intersects = findIntersections(ca.geom)
    return render_to_kml('core/comarea/community_area.kml', {'comm_area':ca,'intersects':intersects})
def neighborhood_kml(request, field):
    ca = models.Neighborhoods.objects.get(pri_neigh=field)
    intersects = findIntersections(ca.geom)
    return render_to_kml('core/neighborhood/neighborhood.kml', {'neighborhood': ca, 'intersects':intersects })
def cpddistrict_kml(request, field):
    ca = models.CpdDistricts.objects.get(dist_label=field)
    intersects = findIntersections(ca.geom)
    return render_to_kml('core/cpddistrict/cpddistrict.kml', {'cpddistrict': ca,'intersects':intersects })
def cpdbeat_kml(request, field):
    ca = models.CpdBeats.objects.get(objectid=field)
    intersects = findIntersections(ca.geom)
    return render_to_kml('core/cpdbeat/cpdbeat.kml', {'cpdbeat': ca,'intersects':intersects })
def wards_kml(request, field):
    ca = models.Wards.objects.get(ward=field)
    intersects = findIntersections(ca.geom)
    return render_to_kml('core/ward/ward.kml', {'ward': ca,'intersects':intersects })
def cpdarea_kml(request, field):
    ca = models.CpdAreas.objects.get(area_num=field)
    intersects = findIntersections(ca.geom)
    return render_to_kml('core/cpdarea/cpdarea.kml', {'cpdarea': ca,'intersects':intersects })

def geocode(query):
    results = list(GEOCODER.geocode(query,exactly_one=False))
    address = point = remainder = None
    print results
    if results:
        first = results[0]
        remainder = results[1:]
        address, lat_lon = first
        point2 = fromstr('POINT('+lat_lon[1] + ' ' + lat_lon[0] + ')', srid=4269)
            
    return (address, remainder, point)

def make_point(lon_lat_str):
    return Point(tuple(map(float,lon_lat_str.split(","))), srid=4269)


def findIntersections(geom):
    wards = models.Wards.objects.filter(geom__intersects=geom)
    ca = models.CommunityArea.objects.filter(geom__intersects=geom)
    districts = models.CpdDistricts.objects.filter(geom__intersects=geom)
    areas = models.CpdAreas.objects.filter(geom__intersects=geom)
    beats = models.CpdBeats.objects.filter(geom__intersects=geom)
    intersectsStr = ''
    for ward in wards:
        intersectsStr = intersectsStr + '<br>Intersects ward:' + ward.ward + '</br>'
    for c in ca: 
        intersectsStr = intersectsStr + '<br>Intersects community area:' + c.community + '</br>'
    for district in districts:
        intersectsStr = intersectsStr + '<br>Intersects police district:' + district.dist_num + '</br>'
    for area in areas:
        area = intersectsStr + '<br>Intersects police area:' + area.area_num + '</br>'
    for beat in beats:
        beat = intersectsStr + '<br>Intersects police beat:' + beat.beat + '</br>'
    return intersectsStr
