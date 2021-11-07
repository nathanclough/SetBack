from setback.events.event_base import EventBase

class PlaceBidEvent(EventBase):
    def __init__(self) -> None:
        super().__init__("place_bid_event")
        self.bid = 0
        self.player_id = ""