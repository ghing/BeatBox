import sms
import mail


def sendSms(incident, users):
    for user in users:
        sms.sendMessage(user.cell, incident.msg)

def sendEmail(incident, users):
    for user in users:
        mail.sendMessage(user.email, incident.msg)
    

def sendMsg(incident, users):
    """ 
    smsUsers = []
    emailUsers = []

    for user in users:
        if user.email:
            emailUsers.append(user)

        if user.cell:
            smsUsers.append(user)
    
    if smsUsers:
        sendSms(incident, smsUsers)
    
    if emailUsers:
        sendEmail(incident, emailUsers)
        
        
