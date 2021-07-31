from setback.common.suit import suits
from setback.common.rank import ranks
import itertools
import random

class Deck():
    def __init__(self) -> None:   
        # Generate all ranks for each suit 
        self.Cards = list(tuple(''.join(card) for card in itertools.product(ranks, suits)))
        
        # Add jokers 
        self.Cards.append("J")
        self.Cards.append("j")
    
    def Shuffle(self):
        random.shuffle(self.Cards)

    def DrawCard(self,count=1):
        result = []
        for x in range(count):
            result.append(self.Cards.pop())
            
        return result