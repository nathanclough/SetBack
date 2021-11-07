class EventBase:
    def __init__(self, event_name :str,player_id:str = "") -> None:
        self.player_id = player_id
        self.event = event_name 
    
    @classmethod
    def from_json(cls, data):
        return cls(**data)
