from setback.game.game_instance import Game

class GetGamesResult():
    def __init__(self,games) -> None:
        self.games = games

    @classmethod
    def from_json(cls,data):
        games = {}
        for game in data["games"]:
            game = Game.from_json(data["games"][game])
            games[game.id] = game
        return cls(games)
