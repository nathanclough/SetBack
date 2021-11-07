from kivy.uix.boxlayout import BoxLayout
from setback import Player
from kivy.properties import StringProperty, BooleanProperty, NumericProperty

class UserLabel(BoxLayout):
    name = StringProperty("name")
    team = NumericProperty(2)
    id = ""
    active_turn = BooleanProperty(False)
    bid = StringProperty("...")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def set_user(self, player :Player):
        self.name = player.name
        self.team = player.team
        self.id = player.id

    def bid_update(self,current_bidder_id):
        self.active_turn = True if current_bidder_id == self.id else False
