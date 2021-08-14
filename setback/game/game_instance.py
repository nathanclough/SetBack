from logging import logMultiprocessing
import uuid
from setback.game.player import Player
class Game:
    def __init__(self,team_one=[],team_two=[],name="", id =None) -> None:
        if(id == None):
            self.id = str(uuid.uuid4())
        else:
            self.id = id
        self.team_one = team_one
        self.team_two = team_two 
        self.name = name
    
    def is_full(self):
        return len(self.team_one) == 2 and len(self.team_two) == 2

    @classmethod
    def from_json(cls,data):
        team_one = list(map(Player.from_json, data["team_one"]))
        team_two = list(map(Player.from_json, data["team_two"]))
        return cls(team_one,team_two,data["name"],data["id"])