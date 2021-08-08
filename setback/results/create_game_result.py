class CreateGameResult():
    def __init__(self,name,id) -> None:
        self.name = name
        self.id = id
    @classmethod
    def from_json(cls, data):
        return cls(**data)