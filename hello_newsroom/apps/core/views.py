import logging
import json

from django.shortcuts import render_to_response
from django.contrib.gis.geos import *
from django.contrib.gis.measure import Distance
from django.contrib.gis.shortcuts import render_to_kml
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from messaging.views import notify_admin, notify_beat

from core import models
from messaging import *

from bigdoorkit import Client

log = logging.getLogger("hello_newsroom")

def test_sms(request):
    return render_to_response('core/index.html')
    

def index(request):
#    template_dict = {}
#    beat = models.CpdBeats.objects.get(beat_num='2313')
#    thisuser = models.User.objects.create_user(username='john2', email='lennon@thebeatles.com', password='johnpassword')
#    beatuser = models.BeatUser(user=thisuser, cpdBeatIntersection=beat)
#    beatuser.save()
#    template_dict['beatuser'] = beatuser    
#    return render_to_response('core/index.html', template_dict)
    return HttpResponseRedirect('/core/m/')


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
        fAdmin = request.POST.get('fAdmin','')
        print fUsername
        print fAdmin
        adminFlag = False
        if fAdmin == 'on':
            adminFlag = True
        beat = models.CpdBeats.objects.get(beat_num=fBeatNum)
        thisuser = models.User.objects.create_user(username=fUsername, password=fPass, email='a@a.com')
        thisuser.is_staff = adminFlag
        thisuser.save()
        beatuser = models.BeatUser(user=thisuser, cpdBeatIntersection=beat, cellNum = fCellNum)
        beatuser.save()
        #probably want some sort of feedback here
        return HttpResponseRedirect('/core/m/incident')

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

    incidents = models.Incident.objects.filter(beatOccurence=beat).order_by('-voteTotal')

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

def api_listbeats(request):
    beat_nums = []
    for beat_num in models.BeatUser.objects.values('cpdBeatIntersection__beat_num').distinct():
        beat_nums.append(beat_num['cpdBeatIntersection__beat_num'])

    # Don't set mime type for testing so I can view in browser.
    return HttpResponse(json.dumps(beat_nums))

    #return HttpResponse(json.dumps(beat_nums), mimetype='application/json')

def mobile_incident_vote(request):
    template_dict = {}
    if not request.user.is_authenticated():
        return render_to_response('user-screen.html', template_dict)

    try:
        vote = int(request.GET['vote'])
    except (ValueError, KeyError), e:
        #deal with the error here
        raise

    if vote > 0:
        # vote up
        vote_value = 1
    else:
        vote_value = -1

    incident_uid = request.GET['objid']
    incident = models.Incident.objects.get(objid=incident_uid)

    app_key = 'e608258751c54fb4adba113c7998dc69'
    secret_key = 'beec8efa9a014573b12e59498554b9c0'
    # create an instance of the bigdoor client
    c = Client(secret_key, app_key)

    # create request post data
    payload = dict(amount=vote_value,
                   verbosity=9,
                   allow_negative_balance=1)
    # execute transaction for incident
    resp = c.post('named_transaction_group/612563/execute/incident:%d' % incident.id,
                  payload=payload)

    balances = resp['end_user']['currency_balances']

    # this probably wants to be pulled from settings
    vote_currency_id = 1065 
    vote_balance = [c for c in balances if c['id'] == vote_currency_id][0]

    incident.voteTotal = vote_balance
    incident.save()

    return HttpResponseRedirect('/core/m/list_incidents')
