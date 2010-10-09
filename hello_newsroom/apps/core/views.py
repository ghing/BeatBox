import logging

from django.shortcuts import render_to_response
from django.contrib.gis.geos import *
from django.contrib.gis.measure import Distance
from django.contrib.gis.shortcuts import render_to_kml
from django.contrib.auth import authenticate, login
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
    
    if request.user.is_authenticated():
        # Do something for authenticated users.
        pass
    else:
        return render_to_response('user-screen.html', template_dict)

def mobile_login(request): 
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect('/core/m/')
            # Redirect to a success page.
        else:
            # Return a 'disabled account' error message
            pass
    else:
        # Return an 'invalid login' error message.
        pass