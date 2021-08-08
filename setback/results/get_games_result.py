from setback.game.game_instance import Game

class GetGamesResult():
    def __init__(self,games) -> None:
        self.games = games

    @classmethod
    def from_json(cls,data):
        games = list(map(Game.from_json, data["games"]))
        return cls(games)
