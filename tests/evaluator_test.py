from setback import Evaluator, Card, Rank, Suit, Player

def test_get_play_result_trump_ace_wins():
    
    card1 = Card(Rank.A,Suit.H)
    card1.player = Player("Player1",1)
    card2 = Card(Rank.K,Suit.H)
    card2.player = Player("Player2",2)
    card3 = Card(Rank.Q,Suit.H)
    card3.player = Player("Player3",1)
    card4 = Card(Rank.JA,Suit.H)
    card4.player = Player("Player4",2)

    cards = [card1, card2, card3, card4]

    evaluator = Evaluator(Suit.H)
    result = evaluator.get_play_result(cards)

    assert result.winner.team == 1 and result.points_won == 2

def test_get_play_result_not_trump_ace_loses():
    
    card1 = Card(Rank.A,Suit.S)
    card1.player = Player("Player1",1)
    card2 = Card(Rank.K,Suit.H)
    card2.player = Player("Player2",2)
    card3 = Card(Rank.Q,Suit.H)
    card3.player = Player("Player3",1)
    card4 = Card(Rank.JA,Suit.H)
    card4.player = Player("Player4",2)

    cards = [card1, card2, card3, card4]

    evaluator = Evaluator(Suit.H)
    result = evaluator.get_play_result(cards)

    assert result.winner.team == 2 and result.points_won == 1

def test_get_play_result_jick_gets_point():
    
    card1 = Card(Rank.A,Suit.S)
    card1.player = Player("Player1",1)
    card2 = Card(Rank.JA,Suit.D)
    card2.player = Player("Player2",2)
    card3 = Card(Rank.Q,Suit.H)
    card3.player = Player("Player3",1)
    card4 = Card(Rank.JA,Suit.H)
    card4.player = Player("Player4",2)

    cards = [card1, card2, card3, card4]

    evaluator = Evaluator(Suit.H)
    result = evaluator.get_play_result(cards)

    assert result.winner.team == 1 and result.points_won == 2

def test_get_play_result_trump_beats_non_trump():
    
    card1 = Card(2,Suit.S)
    card1.player = Player("Player1",1)
    card2 = Card(Rank.JA,Suit.D)
    card2.player = Player("Player2",2)
    card3 = Card(Rank.Q,Suit.H)
    card3.player = Player("Player3",1)
    card4 = Card(Rank.JA,Suit.H)
    card4.player = Player("Player4",2)

    cards = [card1, card2, card3, card4]

    evaluator = Evaluator(Suit.S)
    result = evaluator.get_play_result(cards)

    assert result.winner.team == 1 and result.points_won == 1