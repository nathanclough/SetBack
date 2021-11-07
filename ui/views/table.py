from kivy.event import EventDispatcher
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from setback import Player
from ui.views.bid_popup import BidPopup

class Table(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.user_labels = {}

    def on_game_update_event(self, *largs):
        # Set the current team 
        user = self.manager.player
        self.ids.current_user.set_user(user)
        self.user_labels[user.id] = self.ids.current_user
        
        teamate = [player for player in self.manager.teams[self.manager.player.team] if player.id != self.manager.player.id ].pop()
        
        self.ids.current_teamate.set_user(teamate)
        self.user_labels[teamate.id] = self.ids.current_teamate
        
        # Set the opposing team
        other_team_one = self.manager.teams[user.get_opposing_team_number()][0]
        other_team_two = self.manager.teams[user.get_opposing_team_number()][1]
        
        self.ids.other_team_player_one.set_user(other_team_one)
        self.ids.other_team_player_two.set_user(other_team_two)

        self.user_labels[other_team_one.id] = self.ids.other_team_player_one
        self.user_labels[other_team_two.id] = self.ids.other_team_player_two
        self.on_bid_update()

    def on_bid_update(self, *largs): 
        for id in self.user_labels.keys():
            self.user_labels[id].bid_update(self.manager.current_bidder_id)
        
        if self.manager.player.id == self.manager.current_bidder_id:
            bid_pop = BidPopup()
            bid_pop.open()
        
    def on_enter(self, *args):
        self.manager.bind(on_game_update_event=self.on_game_update_event)
        self.manager.bind(on_bid_update_event=self.on_bid_update)

        if not self.manager.game is None:
            self.on_game_update_event()
        return super().on_enter(*args)
