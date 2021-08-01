from setback.game.deck import Deck
from setback.game.player import Player

class Manager():
    def __init__(self) -> None:
        self.deck = None
        self.players = None
    
    def create_game(self, players:list[Player]) -> None:
        # Assign the players 
        self.players = players
        
        # Create a new deck
        self.deck = Deck()

        for x in range(6):
            for p in self.players:
                p.give_cards(self.deck.draw_cards(1))
  