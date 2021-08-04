from dataclasses import dataclass
from setback.game.card import Card

@dataclass
class PlayResult():
    winner: int
    points_won: int
    winning_team: int
    cards_played: list[Card]