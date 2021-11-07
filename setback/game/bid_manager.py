from setback import Game, Player
from queue import Queue
from random import randint

class BidManager():
    is_active = True
    __bid_list = []
    __dealer_index = 0
    __current_bid_index = 0
    __dealer = None
    __current_bidder = None
    __bids = {}

    def __init__(self, game :Game) -> None:
        self.__create_bid_list(game.team_one,game.team_two)
        
        # Set the dealer
        self.__dealer_index = randint(0,3)
        self.__dealer = self.__bid_list[self.__dealer_index]

        # Set the current bidder
        self.__current_bid_index = self.__increment_index(self.__dealer_index)
        self.__current_bidder = self.__bid_list[self.__current_bid_index]
    
    def __create_bid_list(self, team_one: list[Player],team_two: list[Player]):
        for x in range(4):
            if x % 2 == 0:
                self.__bid_list.append(team_one.pop())
            else:
                self.__bid_list.append(team_two.pop())
    
    def __increment_index(self, index: int) -> int:
        index += 1
        if index > 3:
            return 0
        else:
            return index
    
    def place_bid(self, id: str, bid: int) -> str:
        if(self.__current_bidder.id == id):
            self.__current_bidder.current_bid = bid
            self.__bids[id] = bid
        else:
            raise Exception(f"not player_id: '{id}'s turn")
        
        self.__current_bid_index = self.__increment_index(self.__current_bid_index)
        self.__current_bidder = self.__bid_list[self.__current_bid_index]
        
        if self.__current_bidder.current_bid == -1:
            return self.__current_bidder.id
        else:
            self.is_active = False 
            return None
        
    def get_current_bidder(self):
        return self.__current_bidder.id
    
    def get_bids(self):
        return self.__bids