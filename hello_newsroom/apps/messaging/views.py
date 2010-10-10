from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist

from datetime import datetime
from core import models
import re
from messaging import sendMsg, sendSms

REGISTER, INCIDENT, NOTIFY, APPROVE = range(4)

class SMSParseError(Exception):
    # Raised when SMS fails to parse
    def __init__(self, reason):
        self.reason = reason
        pass

def parse_sms(msg):
    """ Parse an SMS message and return a beat and message.
    Returns type, beat, message.
    """

    msg = msg.lower()

    # REGISTER
    if msg.startswith("register"):
        try:
            _, beatnum = msg.strip().split(" ")
            print beatnum
            beat = models.CpdBeats.objects.get(beat_num = beatnum)
            return (REGISTER, beat, None)

        except: 
            raise SMSParseError("Usage: register <beat-number> %s"% beatnum)

    # NOTIFY
    elif msg.startswith("notify"):
        try:
            _, incident = msg.split(" ")
            return (NOTIFY, _, incident)
        except: raise SMSParseError("Usage: NOTIFY <incident-number>")

    # INCIDENT
    else:
        if re.match("^\d+ ", msg):
            try: 
                beatnum, msg = msg.split(" ", 1)
                beat = models.CpdBeats.objects.get(beat_num = beatnum)
            except ValueError:
                raise SMSParseError("Usage: [beat-number] report %s" % beatnum)


            return (INCIDENT, beat, msg)
        return (INCIDENT, None, msg)
            

def notify_admin(incident):
    incidentbeat = incident.beatOccurence

    beatAdmins = models.BeatUser.objects.filter(cpdBeatIntersection=incidentbeat).filter(user__is_staff=True).all()
    #Fix me beatAdmins = incident.beatOccurence.BeatUser_set.filter(user__is_staff=True).all()
    sendMsg(incident.msg, beatAdmins)




def notify_beat(incident):
    incidentbeat = incident.beatOccurence

    beatUsers = models.BeatUser.objects.filter(cpdBeatIntersection=incidentbeat).all()

    sendMsg(incident.msg, beatUsers)

    




def twilio(request):
    """Handle an incoming HTTP request from twilio.
    Request will contain from, to and body parameters.
    See reference at http://www.twilio.com/docs/api/2010-04-01/twiml/sms/twilio_request."""

    # Log the SMS request
    timestamp = datetime.now()
    sms = models.SMS.objects.create(smsfrom=request.REQUEST['From'], smsto=request.REQUEST['To'], body=request.REQUEST['Body'], time=datetime.now())
    sms.save()



    # Parse the SMS
    try: msgtype, beat, message = parse_sms(sms.body)
    except SMSParseError as e:
        # Handle error condition
        return render_to_response('twilio_responses/parseerror.xml', {'reason': e.reason})


    if msgtype == REGISTER:
        cellNum = request.REQUEST['From']
        if models.BeatUser.objects.filter(cellNum = cellNum).exists():
            return render_to_response('twilio_responses/parseerror.xml', {'reason': 'You are already registered'}) 

        beatuser = models.BeatUser(cpdBeatIntersection=beat, cellNum = cellNum)
        user = models.User()
        user.username=cellNum
        user.password = cellNum
        user.save()
        beatuser.user = user
        beatuser.save()
        return render_to_response('twilio_responses/registrationreceived.xml')

    if msgtype == INCIDENT:
        # Log an incident

        # Is the user registered?
        try: user = models.BeatUser.objects.get(cellNum = sms.smsfrom)
        except ObjectDoesNotExist: 
            return render_to_response('twilio_responses/parseerror.xml', {'reason': 'First register by texting register <beat number>'})

        

        if not beat:
            # Assume the user's in his home beat, unless he specified one
            beat = user.cpdBeatIntersection

        incident = models.Incident(reportedBy = user, beatOccurence = beat, msg = message)
        incident.save()

        if user.user.is_staff:
            # If the admin submitted the incident, just notify the beat
            notify_beat(incident)
            return render_to_response('twilio_responses/beatnotified.xml')
        else:
            notify_admin(incident)
            # notify_beat(incident)
            return render_to_response('twilio_responses/adminnotified.xml')

    elif msgtype == NOTIFY:
        # The message should be an incident ID
        beat = user.cpdBeatIntersection
        
        try: 
            incident = models.Incident.objects.get(objid = int(msg))
        except ObjectDoesNotExist:
            return render_to_response('twilio_responses/parseerror.xml', {'reason': 'Invalid incident: %s' % msg})

        if not user.user.is_staff:
            return render_to_response('twilio_responses/parseerror.xml', {'reason': 'You\'re not the beat administrator'})

        return render_to_response('twilio_responses/beatnotified.xml')



            

    




    








