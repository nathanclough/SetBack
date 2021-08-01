from setback import Card
from setback import Suit

def test_create_card():
    card = Card("2","H")
    assert not None == card

def test_get_rank_is_correct():
    card = Card(3,Suit.H)

    rank = card.get_rank()
    assert rank == 3