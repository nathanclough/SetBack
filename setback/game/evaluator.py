from setback.game.play_result import PlayResult
from setback.game.card import Card
from setback.common.rank import Rank
from setback.common.suit import Suit
from setback.game.play_result import PlayResult
class Evaluator():
    def __init__(self,trump: Suit) -> None:
        self.trump = trump
        
        # Set the suit of the jick 
        if(trump == Suit.H):
            self.jick = Suit.D
        elif(trump == Suit.D):
            self.jick = Suit.H
        elif(trump == Suit.S):
            self.jick = Suit.C
        else:
            self.jick = Suit.S

    def get_play_result(self,cards_played: list[Card]) -> PlayResult:
        points = 0 
        highest_rank_card = cards_played[0]
        highest_rank = self.get_rank(cards_played[0])

        for card in cards_played:
            points += self.get_points(card)
            rank = self.get_rank(card)
            if(rank > highest_rank):
                highest_rank_card = card
                highest_rank = rank
        
        return PlayResult(highest_rank_card.player,points,cards_played)


    def get_rank(self,card:Card):
        rank = card.rank
        if(card.suit == self.trump):
            rank += 17
        elif(card.rank == Rank.JA and card.suit == self.jick ):
            rank += 16
        
        return rank

    def get_points(self,card:Card):
        if( card.suit == self.trump and 
        (card.rank == Rank.A or 
        card.rank == Rank.JA or 
        card.rank == Rank.JO or 
        card.rank == Rank.jo or 
        card.rank == 2)):
            return 1 
        elif(card.rank == Rank.JA and card.suit == self.jick):
            return 1
        else:
            return 0


