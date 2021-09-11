from setback.game.game_instance import Game
from setback.events.event_base import EventBase

class UpdateJoinableGamesEvent(EventBase):
    def __init__(self,games) -> None:
        super().__init__("update_joinable_games_event")
        self.games = games

    @classmethod
    def from_json(cls,data):
        games = []
        for game in data["games"]:
            game = Game.from_json(game)
            games.append(game)
        return cls(games)
