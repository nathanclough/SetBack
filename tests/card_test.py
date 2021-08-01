from setback import Card

def test_create_card():
    card = Card("2","h")
    assert not None == card
