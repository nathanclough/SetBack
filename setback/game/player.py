from setback.game.card import Card

class Player():
    def __init__(self,name,team) -> None:
        self.name = name
        self.team = team
        self.cards = []
        self.position = 0
    
    def give_cards(self,cards):
        if(len(self.cards) + len(cards) > 6):
            raise Exception("Player can only have 6 cards")
        self.cards.extend(cards)
    

    