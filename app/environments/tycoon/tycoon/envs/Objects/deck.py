import random

from Objects.consts import *
from Objects.utils import *


class Deck:
    def __init__(self):
        self.cards = []
        self.reset()

    def __str__(self):
        return " ".join(self.cards)

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()

    def is_empty(self):
        return self.cards == []

    def reset(self):
        self.cards = []

        for suit in ["S", "H", "D", "C"]:
            # set up number cards (10 = 0)
            for rank in range(2, 11):
                if rank == 10:
                    rank = "0"

                self.cards.append(f"{rank}{suit}")

            # set up face cards
            for face in ["J", "Q", "K", "A"]:
                self.cards.append(f"{face}{suit}")

        # ZR = Red Joker, ZB = Black Joker
        self.cards.append(JOKER_RED)
        self.cards.append(JOKER_BLACK)

        sort_hand(self.cards)
