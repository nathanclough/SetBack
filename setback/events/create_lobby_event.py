from setback.events.event_base import EventBase

class CreateLobbyEvent(EventBase):
    def __init__(self,name,id) -> None:
        super().__init__("create_lobby_event")
        self.name = name
        self.id = id
