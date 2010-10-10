import sms
import mail


def sendSms(message, users):
    for user in users:
        sms.sendMessage(user.cellNum, message)

def sendEmail(message, users):
    for user in users:
        mail.sendMessage(user.email, message)
    

def sendMsg(message, users):
    smsUsers = []
    emailUsers = []

    for user in users:
        #if user.email:
            #emailUsers.append(user)
        #    pass

        if user.cellNum:
            smsUsers.append(user)
    
    if smsUsers:
        sendSms(message, smsUsers)
    
    if emailUsers:
        sendEmail(message, emailUsers)
        
        
