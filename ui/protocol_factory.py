from time import sleep
from twisted.internet import protocol
from ui.protocol import SetbackClient

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