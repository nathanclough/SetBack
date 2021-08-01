from setback import Player 
from setback import Deck
import pytest
def test_create_player():
    player = Player("Player 1","Team One")
    assert not None == player

def test_give_cards():
    player = Player("Name","Team") 
    cards = Deck().draw_cards(3)

    player.give_cards(cards)

    assert len(player.cards) == 3

def test_give_cards_adds_to_current_cards():
    player = Player("Name","Team") 
    deck =  Deck()

    cards = deck.draw_cards(3)
    player.give_cards(cards)

    moreCards = deck.draw_cards(2)
    player.give_cards(moreCards)

    assert len(player.cards) == 5

def test_give_cards_user_card_more_than_six_throws_exception():
    player = Player("Name","Team") 
    cards =  Deck().draw_cards(7)
    
    with pytest.raises(Exception):
        player.give_cards(cards)

    
