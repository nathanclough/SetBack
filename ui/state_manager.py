from kivy.uix.screenmanager import ScreenManager
from setback import Player
class StateManager(ScreenManager):
    game_id = ""
    game = None
    player = Player("Player",2)