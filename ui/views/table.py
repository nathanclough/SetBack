from kivy.event import EventDispatcher
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from setback import Player

class Table(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

    def on_game_update_event(self, *largs):
        # Set the current team 
        user = self.manager.player
        self.ids.current_user.set_user(user)
        
        teamate = [player for player in self.manager.teams[self.manager.player.team] if player.id != self.manager.player.id ].pop()
        self.ids.current_teamate.set_user(teamate)

        # Set the opposing team
        self.ids.other_team_player_two.set_user(self.manager.teams[user.get_opposing_team_number()][0])
        self.ids.other_team_player_one.set_user(self.manager.teams[user.get_opposing_team_number()][1])

    def on_enter(self, *args):
        self.manager.bind(on_game_update_event=self.on_game_update_event)
        if not self.manager.game is None:
            self.on_game_update_event()
        return super().on_enter(*args)
