from setback.game.game_instance import Game

class GameUpdateEvent():
    def __init__(self,game) -> None:
        self.event = "game_update_event"
        self.game = game
    
    @classmethod
    def from_json(cls, data):
        game = Game.from_json(data["game"])
        return cls(game)