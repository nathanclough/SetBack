# install_twisted_rector must be called before importing the reactor
from __future__ import unicode_literals
from re import S
from setback.results.get_games_result import GetGamesResult

from kivy.support import install_twisted_reactor
install_twisted_reactor()

# A Simple Client that send messages to the Echo Server
from twisted.internet import protocol
import json
from time import sleep

class SetbackClient(protocol.Protocol):
    def connectionMade(self):
        self.factory.app.on_connection(self.transport)

    def dataReceived(self, data):
        response = data.decode('utf-8')
        response = json.loads(data)
        
        # Get the handler and run it 
        handle_method = self.factory.app.response_handlers.pop(response["request_id"])
        handle_method(response["response"])

class SetbackClientFactory(protocol.ClientFactory):
    protocol = SetbackClient

    def __init__(self, app):
        self.app = app

    def startedConnecting(self, connector):
        self.app.print_message('Started to connect.')

    def clientConnectionLost(self, connector, reason):
        self.app.print_message('Lost connection.')
        self.reconnect()
         

    def clientConnectionFailed(self, connector, reason):
        self.app.print_message('Connection failed.')
        self.reconnect()

    def reconnect(self):
        connected = False
        while not connected :
            try:
                self.app.print_message('Reconnecting ...')
                self.app.connect_to_server()
                connected = True
            except:
                sleep(2)
