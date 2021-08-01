from setback import Manager
from setback import Player

def test_create_manager():
    m = Manager()
    assert not m == None

def test_manager_start_game_takes_four_players():
    players = [ Player("player1","team1"),
        Player("player2","team1"),
        Player("player3","team2"),
        Player("player4","team2")
        ]
    
    m = Manager()
    m.create_game(players)

    for player in players: 
        assert len(player.cards) == 6