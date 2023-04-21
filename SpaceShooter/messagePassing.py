from comm import CommsListener, CommsSender
import sys 
import json


class Rabbit:
    def __init__(self, creds, callback=None):
        self.creds = creds
        self.callback = callback

        if self.callback != None:
            self.commsListener.threadedListener(self.callback)
        
        self.user = self.creds["user"]

        self.commsListener = CommsListener(**self.creds)
        self.commsSender = CommsSender(**self.creds)
    
    def send(self, target, body):
        self.commsSender.send(target=target, sender=self.user, body=json.dumps(body), closeConnection=False)

    def setCallback(self, callback):

        self.callback = callback
        self.commsListener.threadedListen(self.callback)