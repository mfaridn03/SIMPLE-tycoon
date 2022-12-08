from Objects.utils import sort_hand
from typing import Optional, List


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.order = -1

    def play(self, data: dict) -> list:
        pass
    
    def choose_play_direction(self, data: dict) -> bool:
        """
        The 2nd last player must choose whether play is clockwise or counter-clockwise
        
        result of True means keep default direction
        result of False means change to opposite direction
        """
        return True

