from setback import Deck
import pytest

def test_create_deck():
    deck = Deck()
    assert deck is not None 

def test_deck_has_54_cards():
    deck = Deck()
    assert len(deck.Cards) == 54

def test_shuffle_two_decks_not_equal():
    deck1 = Deck()
    deck2 = Deck()

    deck1.shuffle()
    deck2.shuffle()

    assert not deck1.Cards == deck2.Cards

def test_draw_no_args_returns_one_card():
    deck = Deck()
    deck.shuffle()

    hand = deck.draw_cards()

    assert len(hand) == 1 and hand[0] != ""

def test_draw_three_returns_three_cards():
    deck = Deck()
    deck.shuffle()

    hand = deck.draw_cards(3)

    assert len(hand) == 3
