from setback.events.event_base import EventBase

class BidUpdateEvent(EventBase):
    def __init__(self) -> None:
        super().__init__("bid_update_event")
        self.current_bidder_id = ""
        self.bids = {}
    
