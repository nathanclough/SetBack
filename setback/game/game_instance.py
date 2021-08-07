import uuid

class Game:
    team_one =[]
    team_two = [] 
    name = ""
    
    def __init__(self) -> None:
        self.id = uuid.uuid4