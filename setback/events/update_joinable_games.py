from setback.game.game_instance import Game

class UpdateJoinableGamesEvent():
    def __init__(self,games) -> None:
        self.games = games
        self.event = "update_joinable_games_event"
    @classmethod
    def from_json(cls,data):
        games = []
        for game in data["games"]:
            game = Game.from_json(game)
            games.append(game)
        return cls(games)
