import twilio

API_VERSION = '2010-04-01'

ACCOUNT_SID = 'ACe9788dd10fb4edf1cbcab82c967da9be'
ACCOUNT_TOKEN = '25faedbb5b24c8404c6a8a4ed72b2373'

CALLER_ID = '(312) 489-8287'

account = twilio.Account(ACCOUNT_SID, ACCOUNT_TOKEN)

def sendMessage(number, message):
    d = {
    'From': CALLER_ID,
    'To' : number,
    'Body' :  message
}

    request_url = '/%s/Accounts/%s/SMS/Messages' % (API_VERSION, ACCOUNT_SID) 
    print request_url
    print d
    account.request(request_url, 'POST', d)

if __name__ == '__main__':
    sendMessage("3126851452", "hello")
