from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from protocol_factory import SetbackClientFactory
from twisted.internet import reactor
from state_manager import StateManager

# Even though some of these are not used they must be 
# imported so that the builder can recognize the class
from views.user_label import UserLabel
from views.score_board import ScoreBoard
from ui.views.select_team import SelectTeam
from views.table import Table
from views.homepage import HomePage
from views.select_team import SelectTeam




class SetbackApp(App):
    connection = None

    def build(self):
        self.stateManager = StateManager()
        self.homepage = HomePage(name ="homepage")
        self.select_team = SelectTeam(name ="select_team")
        self.table = Table(name="table")
        self.stateManager.add_widget(self.homepage)
        self.stateManager.add_widget(self.select_team)
        self.stateManager.add_widget(self.table)
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