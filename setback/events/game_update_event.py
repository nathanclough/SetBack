from setback.game.game_instance import Game
from setback.events.event_base import EventBase

class GameUpdateEvent(EventBase):
    def __init__(self,game) -> None:
        super().__init__("game_update_event")
        self.game = game
    
    @classmethod
    def from_json(cls, data):
        game = Game.from_json(data["game"])
        player_id = data["player_id"]
        result = cls(game)
        result.player_id = player_id
        return result