from setback.events.event_base import EventBase

class GameStartedEvent(EventBase):
    
    def __init__(self,current_bidder="") -> None:
        super().__init__("game_started_event")
        self.current_bidder = current_bidder
        
    @classmethod
    def from_json(cls, data):
        return cls(data["current_bidder"])