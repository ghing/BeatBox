import logging

from django.shortcuts import render_to_response
from django.contrib.gis.geos import *
from django.contrib.gis.measure import Distance
from django.contrib.gis.shortcuts import render_to_kml
from django.http import HttpResponseRedirect 



from core import models

log = logging.getLogger("hello_newsroom")

def test_sms(request):
    return render_to_response('core/index.html')
    

def index(request):
    template_dict = {}
    beat = models.CpdBeats.objects.get(beat_num='2313')
    thisuser = models.User.objects.create_user(username='john2', email='lennon@thebeatles.com', password='johnpassword')
    beatuser = models.BeatUser(user=thisuser, cpdBeatIntersection=beat)
    beatuser.save()
    template_dict['beatuser'] = beatuser    
    return render_to_response('core/index.html', template_dict)

def mobile_index(request):
    template_dict = {}
    print 'hello2'
    return render_to_response('user-screen.html', template_dict)

def mobile_register(request):
    template_dict = {}
    if request.method != 'POST': 
        return render_to_response('register.html', template_dict)
    else:
        template_dict = {}
        fUsername = request.POST.get('fUsername', '')
        fPass = request.POST.get('fPassword','')
        fBeatNum = request.POST.get('fBeatNum','')
        fCellNum = request.POST.get('fCellNum','')
        print fUsername
        beat = models.CpdBeats.objects.get(beat_num=fBeatNum)
        thisuser = models.User.objects.create_user(username=fUsername, password=fPass)
        beatuser = models.BeatUser(user=thisuser, cpdBeatIntersection=beat, cellNum = fCellNum)
        beatuser.save()

        return HttpResponseRedirect('/core/m')
