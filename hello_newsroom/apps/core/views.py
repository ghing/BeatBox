import logging

from django.shortcuts import render_to_response
from django.contrib.gis.geos import *
from django.contrib.gis.measure import Distance
from django.contrib.gis.shortcuts import render_to_kml
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.template import RequestContext
from messaging.views import notify_admin, notify_beat

from core import models
from messaging import *

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
        return HttpResponseRedirect('/core/m/report')
    else:
        return render_to_response('user-screen.html', template_dict)
def mobile_logout(request):
    logout(request)
    return HttpResponseRedirect('/core/m/')

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
    
def mobile_report(request):
    template_dict = {}
    return render_to_response('report-mobile.html',template_dict,context_instance=RequestContext(request))

def mobile_register(request):
    template_dict = {}
    if request.method != 'POST': 
        return render_to_response('register.html', template_dict)
    else:
        fUsername = request.POST.get('fUsername', '')
        fPass = request.POST.get('fPassword','')
        fBeatNum = request.POST.get('fBeatNum','')
        fCellNum = request.POST.get('fCellNum','')
        print fUsername
        beat = models.CpdBeats.objects.get(beat_num=fBeatNum)
        thisuser = models.User.objects.create_user(username=fUsername, password=fPass, email='a@a.com')
        beatuser = models.BeatUser(user=thisuser, cpdBeatIntersection=beat, cellNum = fCellNum)
        beatuser.save()

        return HttpResponseRedirect('/core/m')

def mobile_listusers(request):
    template_dict = {}
    if not request.user.is_authenticated() or not request.user.is_staff:
        return render_to_response('user-screen.html', template_dict)

    beatUser = models.BeatUser.objects.get(user=request.user)
    beat = beatUser.cpdBeatIntersection

    users = models.BeatUser.objects.filter(cpdBeatIntersection=beat).all()

    return render_to_response('list-users-mobile.html', {'user_list' : users, 'beat' : beat})

def mobile_listincidents(request):
    template_dict = {}
    if not request.user.is_authenticated() or not request.user.is_staff:
        return render_to_response('user-screen.html', template_dict)

    beatUser = models.BeatUser.objects.get(user=request.user)
    beat = beatUser.cpdBeatIntersection

    incidents = models.Incident.objects.filter(beatOccurence=beat).all()

    return render_to_response('list-incidents-mobile.html', {'incident_list' : incidents, 'beat' : beat})


def mobile_notifybeat(request):
    template_dict = {}
    if not request.user.is_authenticated() or not request.user.is_staff:
        return render_to_response('user-screen.html', template_dict)

    incident = models.Incident.objects.get(objid=request.REQUEST['incident'])
    notify_beat(incident)
    return render_to_response('thankyou.html', {})




def mobile_incident(request):
    template_dict = {}
    if request.method != 'POST':
        return HttpResponseRedirect('/core/m')
    else:
        if request.user.is_authenticated():
            report = request.POST.get('fReport','')
            beatuser = models.BeatUser.objects.get(user=request.user)
            beatoccurence = models.CpdBeats.objects.get(beat_num=beatuser.cpdBeatIntersection.beat_num)
            incident = models.Incident(reportedBy=beatuser, msg=report,beatOccurence=beatoccurence)
            uid = incident.save()
            notify_admin(incident)
            return render_to_response('thankyou.html', {})
        else:
            return render_to_response('user-screen.html', template_dict)

   
            
