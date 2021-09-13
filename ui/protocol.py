# install_twisted_rector must be called before importing the reactor
from __future__ import unicode_literals
from logging import exception
from setback.events.update_joinable_lobbies import UpdateJoinableLobbiesEvent
from kivy.support import install_twisted_reactor
install_twisted_reactor()

from twisted.internet import protocol
import json
from time import sleep

class SetbackClient(protocol.Protocol):
    def connectionMade(self):
        self.factory.app.on_connection(self.transport)

    def dataReceived(self, data):
        message = data.decode('utf-8')
        try:
            message = json.loads(data)
        except Exception as e:

           print("Message: " + message)
           print("Error: " + e)
           message={}
        if("response" in message):
                # Get the handler and run it 
                handle_method = self.factory.app.stateManager.response_handlers.pop(message["request_id"])
                handle_method(message["response"])
        elif("event" in message):
                self.factory.app.stateManager.handle_event(message)


