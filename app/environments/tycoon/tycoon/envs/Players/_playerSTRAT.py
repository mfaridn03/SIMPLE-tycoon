# Bot logic for slightly more intelligent player STRAT
from Objects.player import Player
from Objects.utils import *


class PlayerSTRAT(Player):
    def __init__(self):
        super().__init__("STRAT")

    def test(self, isor, isog, ptb, is_rev) -> list:
        # TODO: Define a util function to take a list of cards and pick the lowest value possible play, or otherwise pass
        # Must account for revolutions
        
        sort_hand(self.hand, is_rev)
        if isog and isor:
            return ["3D"]
        if ptb == []:
            pairs = get_pairs(self.hand)
            if pairs != []:
                return pairs[0]
                
            valid_single_play = [self.hand[0]]
        else:
            valid_single_play = [card for card in self.hand if is_higher_play([card], ptb, is_rev)]
        
        if valid_single_play == []:
            return []
        else:
            return [valid_single_play[0]]

    def play(self, data: dict) -> list:
        # must return None or a list of Card objects where None is a pass
        # will throw error if not valid
        possible_plays = self.test(data["is_start_of_round"], data["is_start_of_game"], data["play_to_beat"], data["is_rev"])
        return possible_plays