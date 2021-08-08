# install_twisted_rector must be called before importing the reactor
from __future__ import unicode_literals
from re import S
from setback.results.get_games_result import GetGamesResult

from kivy.support import install_twisted_reactor

install_twisted_reactor()

# A Simple Client that send messages to the Echo Server
from twisted.internet import reactor, protocol, defer


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

    def clientConnectionFailed(self, connector, reason):
        self.app.print_message('Connection failed.')


from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
import json
import uuid

# A simple kivy App, with a textbox to enter messages, and
# a large label to display all the messages received from
# the server
class SetbackClientApp(App):
    connection = None
    textbox = None
    label = None
    games = []
    response_handlers = {}

    def build(self):
        root = self.setup_gui()
        self.connect_to_server()
        return root

    def setup_gui(self):
        self.textbox_layout = BoxLayout(orientation="horizontal")
        self.textbox = TextInput(size_hint_y=.1, multiline=False)
        self.textbox.bind(on_text_validate=self.create_game)
        self.textbox_label = Label(text="Create Game")
        self.textbox_layout.add_widget(self.textbox_label)
        self.textbox_layout.add_widget(self.textbox)
        
        self.label = Label(text='connecting...\n')
        
        self.menu_layout = BoxLayout(orientation="vertical")       
        self.menu_layout.add_widget(self.textbox_layout)
        self.menu_layout.add_widget(self.label)
        
        return self.menu_layout
        
    def connect_to_server(self):
        reactor.connectTCP('localhost', 8000, SetbackClientFactory(self))

    def on_connection(self, connection):
        self.print_message("Connected successfully!")
        self.connection = connection
        self.get_games()

    def get_games(self):
        id = str(uuid.uuid4)
        request = {
            "request_id" : id,
            "method": "get_games"
        }
        
        # add the handler to the dictionary 
        self.response_handlers[id] = self.handle_get_games
       
        # send the request 
        request = json.dumps(request)
        self.connection.write(request.encode('utf-8'))
    
    def handle_get_games(self, response):
        result = GetGamesResult.from_json(response)
        self.games = result.games 
        for id  in self.games:
            game = self.games[id]
            btn = Button(text=f"Join Game: {game.name}")
            # bind the button to join the game 
            # btn.bind(on_press=self.send_message(game))
            self.menu_layout.add_widget(btn)

    def create_game(self, name):
        id = str(uuid.uuid4)

        request = {
            "request_id": id,
            "method": "create_game",
            "args": {
                "name" : self.textbox.text,
                "player": {
                    "name" : "Nathan",
                    "id" : 123,
                    "team": 1
                }
            }
        }
        self.response_handlers[id] = self.handle_create_game

        request = json.dumps(request)
        self.connection.write(request.encode('utf-8'))

    def handle_create_game(self,args):
        self.get_games()        

    def print_message(self, msg):
        self.label.text += "{}\n".format(msg)


if __name__ == '__main__':
    SetbackClientApp().run()