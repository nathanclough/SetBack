from setback.game.deck import Deck
from setback.game.player import Player
from setback.game.card import Card
from setback.common.list_helper import ListHelper
import random

class Dealer():
    def __init__(self,dealer_index) -> None:
        # Create a new deck
        self.deck = Deck()
        self.dealer_index = dealer_index
        self.kitty = []

    def deal(self,players: list[Player]):
        # Deal cards  
        for x in range(6):
            self.kitty.append(self.deck.draw_cards(1))
            for p in players:
                p.give_cards(self.deck.draw_cards(1))

        # Check each player for redeal 
        for p in players:
            if(self.check_for_redeal(p.cards)):
                self.__clear_cards()
                self.deal()
        
        self.dealer_index = ListHelper.get_next_index(self.dealer_index)
    
    def check_for_redeal(self,hand:list[Card]):
        max_rank = 0
        has_duce = False
        for card in hand:
            rank = card.get_rank()
            if(rank>max_rank):
                max_rank = rank
            if(rank == 2):
                has_duce = True
        
        # if they have no cards greater than 10 
        # and don't have a 2 then redeal
        return max_rank < 10 and not has_duce
    
    # deals cards so that the player has 6 total 
    def deal_cards(self,player:Player):
        count = 6 - len(player.cards)
        player.give_cards(self.deck.draw_cards(count))

    def __clear_cards(self, players: list[Player]):
        for p in players:
            p.hand = []
        
        self.kitty = []

