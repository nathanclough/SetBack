from setback.common.rank import Rank
from setback.common.suit import Suit

class Card():
    def __init__(self,rank: int, suit: Suit) -> None:
        self.rank = rank
        self.suit = suit
        self.player = None

    def get_rank(self) -> Rank:
        return self.rank 
