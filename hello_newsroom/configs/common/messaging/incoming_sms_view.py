from django.http import HttpResponse
from django.shortcuts import render_to_response

from datetime import datetime
import core.models # check me

class SMSParseError(Exception):
    # Raised when SMS fails to parse
    def __init__(self, reason):
        self.reason = reason
        pass

def parse_sms(msg):
    """ Parse an SMS message and return a beat and message."""
    pass
def twilio(request):
    """Handle an incoming HTTP request from twilio.
    Request will contain from, to and body parameters.
    See reference at http://www.twilio.com/docs/api/2010-04-01/twiml/sms/twilio_request."""

    # Log the SMS request
    timestamp = datetime.now()
    sms = models.Sms.objects.create(request.from, request.to, request.body, datetime.now)
    sms.save()

    # Look up (or create) the user by phone #
    user, isNewUser = models.User.objects.get_or_create(cell = sms.from)


    # Parse the SMS
    try: beat, msgtype, message = parse_sms(sms.body)
    except SMSParseError as e:
        # Handle error condition
        return render_to_response('twilio_responses/parseerror.xml', {'reason': e.reason})


    if msgtype == INCIDENT:
    # Log an incident

    
    # Register user to beat, if they don't currently have a beat
    # Otherwise, they stay in their existing beat

    if not user.beat:
        user.beat = beat
        user.save()

    incident = Incident.objects.create(reportedby = user, beat = beat, msg = message)

    




    








