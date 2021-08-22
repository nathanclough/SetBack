from ui.select_team import SelectTeam
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager
from protocol_factory import SetbackClientFactory
from twisted.internet import reactor
from homepage import HomePage
from setback import GetGamesResult
from select_team import SelectTeam
from state_manager import StateManager
import json
import uuid

# A simple kivy App, with a textbox to enter messages, and
# a large label to display all the messages received from
# the server
class SetbackApp(App):
    connection = None
    textbox = None
    label = None

    # Handlers for each response where key is request id 
    response_handlers = {}

    def build(self):
        self.stateManager = StateManager()
        self.stateManager.response_handlers = self.response_handlers
        self.homepage = HomePage(self.response_handlers,name ="homepage")
        self.select_team = SelectTeam(name ="select_team")
        self.stateManager.add_widget(self.homepage)
        self.stateManager.add_widget(self.select_team)
        self.connect_to_server()
        return self.stateManager
        
    def connect_to_server(self):
        reactor.connectTCP('localhost', 8000, SetbackClientFactory(self))

    def on_connection(self, connection):
        self.print_message("Connected successfully!")
        self.connection = connection
        self.stateManager.set_connection(connection)

    def print_message(self, msg):
        self.homepage.connection_status_label = msg
   
if __name__ == '__main__':
    SetbackApp().run()