from kivy.event import EventDispatcher
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from setback import Player

class Table(Screen):
    user_name = StringProperty("")
    user_team = StringProperty("")
    teamate_name = StringProperty("")
    teamate_team = StringProperty("")

    def __init__(self, **kw):
        super().__init__(**kw)

    def on_game_update_event(self, *largs):
        self.user_name = self.manager.player.name
        self.user_team = f"Team {self.manager.player.team}"

        teamate = [player for player in self.manager.teams[self.manager.player.team] if player.id != self.manager.player.id ].pop()
        self.teamate_name = teamate.name
        self.teamate_team = f"Team {teamate.team}"
    
    def on_enter(self, *args):
        self.manager.bind(on_game_update_event=self.on_game_update_event)
        if not self.manager.game is None:
            self.on_game_update_event()
        return super().on_enter(*args)
