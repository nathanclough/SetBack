from setback.common.suit import suits
from setback.common.rank import Rank, normal_ranks
from setback.game.card import Card
import itertools
import random

class Deck():
    def __init__(self) -> None:   
        # Generate all ranks for each suit 
        self.Cards = list( Card(rankSuitTuple[0],rankSuitTuple[1]) for rankSuitTuple in itertools.product(normal_ranks, suits))
        
        # Add big and little jokers 
        self.Cards.append(Card(Rank.JO,None))
        self.Cards.append(Card(Rank.jo,None))
    
    def shuffle(self) -> None:
        random.shuffle(self.Cards)

    def draw_cards(self,count=1) ->list[Card]:
        result = []
        for x in range(count):
            result.append(self.Cards.pop())
            
        return result