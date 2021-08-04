from dataclasses import dataclass
from setback.game.player import Player
from setback.game.card import Card

@dataclass
class PlayResult():
    winner: Player
    points_won: int
    cards_played: list[Card]