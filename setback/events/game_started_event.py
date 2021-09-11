from setback.events.event_base import EventBase

class GameStartedEvent(EventBase):
    def __init__(self) -> None:
        super().__init__("game_started_event")
