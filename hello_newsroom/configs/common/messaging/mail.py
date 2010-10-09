#!/usr/bin/env python

from django.core.mail import send_mail

def sendMessage(address, message):
   send_mail('Beatboxr alert', message, 'beatboxr@ymail.com', [address], fail_silently=False) 


if __name__ == '__main__':
    sendMessage('smelendez@gmail.com', 'hello')
