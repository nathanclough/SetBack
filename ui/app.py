from ui.select_team import SelectTeam
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager
from client import SetbackClientFactory
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
class SetbackClientApp(App):
    connection = None
    textbox = None
    label = None

    # Handlers for each response where key is request id 
    response_handlers = {}

    def build(self):
        screenManager = StateManager()
        self.homepage = HomePage(self.response_handlers)
        self.select_team = SelectTeam(self.response_handlers)
        screenManager.add_widget(self.homepage.render())
        screenManager.add_widget(self.select_team.render())
        self.connect_to_server()
        return screenManager
        
    def connect_to_server(self):
        reactor.connectTCP('localhost', 8000, SetbackClientFactory(self))

    def on_connection(self, connection):
        self.print_message("Connected successfully!")
        self.connection = connection
        self.homepage.set_connection(connection)
        self.select_team.set_connection(connection)

    def print_message(self, msg):
        self.homepage.connection_status_label.text = msg
   
if __name__ == '__main__':
    SetbackClientApp().run()