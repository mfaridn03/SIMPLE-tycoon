# Tycoon hand utilities
from Objects.consts import *
import typing
from itertools import combinations

def sort_hand(cards: typing.Sequence[str], is_rev=False) -> None:
    """
    Sort the cards in the hand
    Suit order: D C H S
    Rank order: 3 4 5 6 7 8 9 10 J Q K A 2

    If reversed, the order is
    Suit order: D C H S
    Rank order: 2 A K Q J 10 9 8 7 6 5 4 3

    Jokers are placed in the rightmost positions
    """
    temp_cards = []
    if JOKER_RED in cards:
        temp_cards.append(JOKER_RED)
        cards.remove(JOKER_RED)
    if JOKER_BLACK in cards:
        temp_cards.append(JOKER_BLACK)
        cards.remove(JOKER_BLACK)

    if is_rev:
        cards.sort(
            key=lambda card: (RANK_ORDER_REV.index(card[0]), SUIT_ORDER.index(card[1]))
        )
    else:
        cards.sort(
            key=lambda card: (RANK_ORDER.index(card[0]), SUIT_ORDER.index(card[1]))
        )

    for card in temp_cards:
        cards.append(card)


def is_eight_stop(cards: typing.Sequence[str]) -> bool:
    """
    Check if a play is an eight stop
    """
    temp_cards = [card for card in cards]
    if JOKER_RED in temp_cards:
        temp_cards.remove(JOKER_RED)
    if JOKER_BLACK in temp_cards:
        temp_cards.remove(JOKER_BLACK)

    # Isolate ranks of each remaining card, and form a set of these ranks
    # Sets contain only unique values, so common ranks will be combined into one item
    # Set size of 1 means that all ranks are common
    rank_set = set([card[0] for card in temp_cards])
    return len(rank_set) == 1 and list(rank_set)[0] == "8"

def is_joker(card: str) -> bool:
    """
    Check if a card is a Joker
    """
    return card == JOKER_RED or card == JOKER_BLACK

def play_is_joker(card: list) -> bool:
    """
    Check if a single play is a Joker
    """
    if card == None or card == []:
        return False
    return is_joker(card[0]) 


def has_joker(cards: typing.Sequence[str]) -> bool:
    """
    Check if a list of cards contains a Joker
    """
    return JOKER_RED in cards or JOKER_BLACK in cards


def is_pair(cards: typing.Sequence[str]) -> bool:
    """
    Check if the cards are a pair
    """
    sort_hand(cards)
    found_joker = is_joker(cards[0]) or is_joker(cards[1])
    ranks_match = cards[0][0] == cards[1][0]
    return len(cards) == 2 and (ranks_match or found_joker)

def get_pairs(cards: typing.Sequence[str]) -> list:
    """
    Generate list of possible pairs from a given hand
    """
    result = []
    if len(cards) < 2: 
        return result
    
    for two_cards in combinations(cards, 2):
        
        two_cards = list(two_cards)
        if is_pair(two_cards):
            result.append(two_cards)
    return result

def is_joker_pair(cards: typing.Sequence[str]) -> bool:
    """
    Check if both cards of a pair are Jokers
    """
    return is_joker(cards[0]) and is_joker(cards[1])


def is_triple(cards: list):
    """
    Check if the cards are a triple
    """
    if len(cards) != 3:
        return False

    temp_cards = [card for card in cards]
    if JOKER_RED in temp_cards:
        temp_cards.remove(JOKER_RED)
    if JOKER_BLACK in temp_cards:
        temp_cards.remove(JOKER_BLACK)

    # Isolate ranks of each remaining card, and form a set of these ranks
    # Sets contain only unique values, so common ranks will be combined into one item
    # Set size of 1 means that all ranks are common so we have a triple
    rank_set = set([card[0] for card in temp_cards])
    return len(rank_set) == 1


def is_revolution(cards: list) -> bool:
    """
    Check if the cards are a revolution
    """
    if len(cards) != 4:
        return False

    temp_cards = [card for card in cards]
    if JOKER_RED in temp_cards:
        temp_cards.remove(JOKER_RED)
    if JOKER_BLACK in temp_cards:
        temp_cards.remove(JOKER_BLACK)

    # Isolate ranks of each remaining card, and form a set of these ranks
    # Sets contain only unique values, so common ranks will be combined into one item
    # Set size of 1 means that all ranks are common so we have a revolution
    rank_set = set([card[0] for card in temp_cards])
    return len(rank_set) == 1


def is_higher_play(is_this_higher: list, than_this: list, is_rev=False):
    """
    Compare values of two plays, based on rank order and Tycoon rules
    """
    if is_this_higher == []:
        return True
    
    if len(is_this_higher) != len(than_this):
        raise ValueError("Compared lists are of different sizes")
    if len(is_this_higher) > 4 or len(is_this_higher) < 1:
        raise ValueError(
            "List sizes are invalid, list is of size " + len(is_this_higher)
        )

    if len(is_this_higher) == 1:
        # One exception - if last card was any Joker and next card is the Three of Spades
        # then the Three of Spades is a higher play
    
        if has_joker(than_this) and is_this_higher == ["3S"]:
            return True
        return get_card_score(is_this_higher, is_rev) > get_card_score(
            than_this, is_rev
        )

    elif len(is_this_higher) == 2:
        return get_pair_score(is_this_higher, is_rev) > get_pair_score(
            than_this, is_rev
        )

    elif len(is_this_higher) == 3:
        return get_triple_score(is_this_higher, is_rev) > get_triple_score(
            than_this, is_rev
        )

    elif len(is_this_higher) == 4:
        return get_revolution_score(is_this_higher, is_rev) > get_revolution_score(
            than_this, is_rev
        )


def get_card_score(card: list, is_rev=False) -> int:
    """
    Get the score of a card

    In regular scoring, singles are scored as such:
    3   -   0
    4   -   1
    5   -   2
    6   -   3
    7   -   4
    8   -   5
    9   -   6
    0   -   7
    J   -   8
    Q   -   9
    K   -   10
    A   -   11
    2   -   12
    Z   -   13
    """
    card_string = card[0]
    if is_joker(card_string):
        return 13

    if is_rev:
        return RANK_ORDER_REV.index(card_string[0])
    else:
        return RANK_ORDER.index(card_string[0])


def get_pair_score(pair: list, is_rev=False) -> int:
    """
    Get the score of a pair
    """
    if is_joker_pair(pair):
        return 13

    # Removing all jokers of the pair and then
    # determining the score of the remaining card
    temp_cards = [card for card in pair]
    if JOKER_RED in temp_cards:
        temp_cards.remove(JOKER_RED)
    if JOKER_BLACK in temp_cards:
        temp_cards.remove(JOKER_BLACK)

    return get_card_score(list(temp_cards[0]), is_rev)


def get_triple_score(triple: list, is_rev=False) -> int:
    """
    Get the score of a triple
    """
    # Removing all jokers of the triple and then
    # determining the score of the remaining cards
    temp_cards = [card for card in triple]
    if JOKER_RED in temp_cards:
        temp_cards.remove(JOKER_RED)
    if JOKER_BLACK in temp_cards:
        temp_cards.remove(JOKER_BLACK)

    return get_card_score(list(temp_cards[0]), is_rev)


def get_revolution_score(revolution: list, is_rev=False) -> int:
    """
    Check if this is a higher revolution
    """
    # Removing all jokers of the revolution and then
    # determining the score of the remaining cards
    temp_cards = [card for card in revolution]
    if JOKER_RED in temp_cards:
        temp_cards.remove(JOKER_RED)
    if JOKER_BLACK in temp_cards:
        temp_cards.remove(JOKER_BLACK)

    return get_card_score(list(temp_cards[0]), is_rev)

def name_to_obj(playerlist_orig, playerobjects, name):
    return playerobjects[playerlist_orig.index(name)]