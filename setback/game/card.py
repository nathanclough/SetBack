from setback.common.rank import Rank
from setback.common.suit import Suit

class Card():
    def __init__(self,rank: int, suit: Suit) -> None:
        self.Rank = rank
        self.Suit = suit

    def get_rank(self) -> Rank:
        return self.Rank 
