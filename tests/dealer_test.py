from setback import Dealer, Player

def test_deal_players_have_six_cards():
    players = [ Player("player1","team1"),
    Player("player2","team1"),
    Player("player3","team2"),
    Player("player4","team2")
    ]
    
    dealer = Dealer(1)
    dealer.deal(players)
    
    for player in players: 
        assert len(player.cards) == 6

def test_deal_next_dealer_is_set():
    players = [ Player("player1","team1"),
    Player("player2","team1"),
    Player("player3","team2"),
    Player("player4","team2")
    ]

    dealer = Dealer(3)
    dealer.deal(players)
    
    assert dealer.dealer_index == 0
