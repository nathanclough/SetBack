from kivy.uix.screenmanager import ScreenManager
from setback import Player

class StateManager(ScreenManager):
    game_id = ""
    game = None
    player = Player("Player",2)
    connection = None
    response_handlers = {}
    event_handlers = None
    def set_connection(self, connection):
        self.connection = connection