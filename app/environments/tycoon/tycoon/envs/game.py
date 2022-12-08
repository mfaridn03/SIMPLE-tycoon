# Setting up a deck of cards
from Objects.exceptions import *
from Objects.utils import *
from Objects.deck import Deck
from Players.__players import *
from Objects.consts import MAX_ROUNDS

import random
import typing


class Game:
    def __init__(self, playerlist=None):
        self.playerlist = playerlist
        if len(playerlist) < 3 or len(playerlist) > 54:
            raise NotEnoughPlayersError("Require 2-54 players for a valid game")

        namelist = [p.name for p in playerlist]
        if len(set(namelist)) < len(playerlist):
            raise DuplicatePlayerNamesError("Can't have duplicate player names")

        self.num_players = len(playerlist)
        self.deck = Deck()
        self.data = {
            "playerlist": [],  # Contains names, current order
            "playerlist_orig": [],  # Contains names, original order
            "is_start_of_round": True,
            "is_start_of_game": True,
            "play_to_beat": [],
            "round_history": [
                [[]]
            ],  # First inner lists are per round, second inner lists are per trick, within trick lists are tuples containing player name and card played
            "round_end_history": [],  # First inner lists are per round, containing info from self.end_of_round_order
            "hand_sizes": [],
            "scores": [],  # Score array reflects player order in player_list_original
            "score_history": [],  # Each inner list corresponds to player in playerlist_orig
            "round_no": 0,
            "trick_no": 0,
            "is_rev": False,
        }
        self.trick_end = False
        self.round_end = False
        self.game_end = False

        self.data["hand_sizes"] = [0] * self.num_players
        self.data["scores"] = [0] * self.num_players

        self.playerlist = []  # Contains names, current order
        self.playerlist_orig = []  # Contains names, original order
        self.playerobjects = playerlist  # Contains player objects, original order

        self.num_finished = 0  # Number of players who have finished a round
        self.end_of_round_order = [
            None
        ] * self.num_players  # 0th index means tycoon, last index means beggar, this is order in which people finished a round
        self.finished_players = [
            False
        ] * self.num_players  # Contains booleans indicating if players have finished for a round

        self.second_last_play = None  # Records the second last played move (not a pass)

        self.times_usurped = [0] * self.num_players
        self.times_started = [0] * self.num_players

    def deal(self):
        # Reset and shuffle the deck
        self.deck.reset()
        self.deck.shuffle()

        # Empty all hands
        for idx, player in enumerate(self.playerobjects):
            player.hand = []
            self.data["hand_sizes"][idx] = 0

        # Randomise starting player
        offset = random.randint(0, self.num_players - 1)

        # Deal cards to each player until deck is empty; deck size is fixed at 54
        for i in range(54):
            card = self.deck.deal()
            curr_player = (i + offset) % self.num_players
            self.playerobjects[curr_player].hand.append(card)
            self.data["hand_sizes"][curr_player] += 1

    def init_game(self):
        if not self.playerlist:
            raise NotEnoughPlayersError("No player list provided")

        self.deal()
        # Player that has 3D will start the game
        other_player_names = []
        firstplayer = None

        for player in self.playerobjects:
            if "3D" in player.hand:
                firstplayer = player
            else:
                other_player_names.append(player.name)

        # Randomise the order of the other players
        random.shuffle(other_player_names)
        self.playerlist = [firstplayer.name] + other_player_names
        self.data["playerlist"] = [name for name in self.playerlist]

        # Store original player order
        self.playerlist_orig = [name for name in self.playerlist]
        self.data["playerlist_orig"] = [name for name in self.playerlist_orig]

        # NECESSARY BUT SHITTY HACK - Order list of player objects based on above player ordering
        namelist = [p.name for p in self.playerobjects]
        indexlist = [None] * self.num_players
        for i, name in enumerate(namelist):
            indexlist[self.playerlist.index(name)] = self.playerobjects[i]
        self.playerobjects = [object for object in indexlist]

        # Resetting all game data
        self.data = {
            "playerlist": [],
            "playerlist_orig": [],
            "is_start_of_round": True,
            "is_start_of_game": True,
            "play_to_beat": [],
            "round_history": [[[]]],
            "round_end_history": [],
            "hand_sizes": [],
            "scores": [],
            "score_history": [],
            "round_no": 0,
            "trick_no": 0,
            "is_rev": False,
        }
        self.trick_end = False
        self.round_end = False
        self.game_end = False
        self.data["hand_sizes"] = [0] * self.num_players
        self.data["scores"] = [0] * self.num_players

        self.second_last_play = None

    def play_text_based(self):
        self.init_game()
        print("Game Starting")

        while not self.game_end:
            if self.data["round_no"] >= MAX_ROUNDS:
                self.game_end = True
                continue

            # Commence round
            self.print_start_of_round_info()
            self.play_round()

            ### DEBUG USAGE
            # self.end_of_round_order = ["A", "B", "C", "D"]

            # Round has ended, give scores and print winner info
            self.data["round_end_history"].append(self.end_of_round_order)
            self.score_players()
            print(
                "Player",
                self.end_of_round_order[0],
                "has won Round",
                self.data["round_no"],
            )
            print("Scores are:")
            for i, name in enumerate(self.playerlist):
                print(name + ": " + str(self.data["scores"][i]))

            # Reset data at round end
            self.data["round_no"] += 1
            self.data["trick_no"] = 0
            self.data["is_start_of_round"] = True
            self.data["play_to_beat"] = []
            self.data["round_history"].append([])
            self.data["round_history"][self.data["round_no"]].append([])
            self.data["is_rev"] = False
            self.round_end = False
            self.trick_end = False
            self.finished_players = [False] * self.num_players
            self.num_finished = 0

            self.deal()

            # Setup next round player order
            self.reset_player_order()
            self.end_of_round_order = [None] * self.num_players

        # Game has ended, print game status and final scores
        print("Game End")
        print("Scores:", self.data["scores"])

        print()
        print("Players:", " ".join(self.playerlist_orig))
        print("times usurped", self.times_usurped)
        print("times started", self.times_started)
        pass

    def print_start_of_round_info(self):
        """
        Print start of round info including round number and player hands
        """
        print("\nBeginning Round", self.data["round_no"])
        print("Player hands are:")
        for name in self.playerlist:
            idx = self.playerlist_orig.index(name)
            playerobj = self.playerobjects[idx]
            sort_hand(playerobj.hand)
            print(playerobj.name, ":", playerobj.hand)
        print("-----------------")
        pass

    def score_players(self):
        """
        Players are given scores for a round based on the following rules:
        First place       - 20 points
        Second place      - 15 points
        Second last place - 5 points
        Last place        - 0 points
        Other places      - 10 points

        Since player counts of less than 4 do not allow for this division of scoring,
        only first place and last place are considered as special cases
        """
        this_round_scores = [0] * self.num_players
        print(self.end_of_round_order)
        if self.num_players <= 3:
            # Fuck you, why would you do this
            for win_order, name in enumerate(self.end_of_round_order):
                idx = self.playerlist_orig.index(name)
                score = 10
                if win_order == 0:
                    score = 20
                elif win_order == self.num_players - 1:
                    score = 0

                this_round_scores[idx] += score
                self.data["scores"][idx] += score
        else:
            for win_order, name in enumerate(self.end_of_round_order):
                idx = self.playerlist_orig.index(name)
                score = 10
                if win_order == 0:
                    score = 20
                elif win_order == 1:
                    score = 15
                elif win_order == self.num_players - 2:
                    score = 5
                elif win_order == self.num_players - 1:
                    score = 0

                this_round_scores[idx] += score
                self.data["scores"][idx] += score
        self.data["score_history"].append(this_round_scores)
        pass

    def reset_player_order(self):
        """
        Player order is reset for a new round, keeping players in their original seating
        2nd last place of previous round decides whether play is clockwise or anticlockwise
        Last place of previous round is first player in current round
        """
        loser = self.end_of_round_order[-1]
        second_loser = self.end_of_round_order[-2]
        sl_idx = self.playerlist_orig.index(second_loser)
        clockwise = self.playerobjects[sl_idx].choose_play_direction(self.data)

        # Reverse player order if 2nd loser chooses anticlockwise
        self.playerlist = self.playerlist_orig
        if not clockwise:
            self.playerlist.reverse()

        # Rearrange playerlist to start with loser
        first_idx = self.playerlist_orig.index(loser)
        self.playerlist = self.playerlist[first_idx:] + self.playerlist[:first_idx]
        self.data["playerlist"] = [name for name in self.playerlist]
        pass

    def play_round(self):

        # Resetting variables
        self.round_end = False
        current_player_index = 0  # Index of current player
        last_played_card_index = (
            None  # Index of the player who last played a card (not pass)
        )
        round_no = self.data["round_no"]

        while not self.round_end:
            while not self.trick_end:
                #### Tracking info
                if self.data["is_start_of_round"]:
                    i = self.playerlist_orig.index(
                        self.playerlist[current_player_index]
                    )
                    self.times_started[i] += 1

                # Check if trick should end
                trick_no = self.data["trick_no"]
                current_trick = self.data["round_history"][round_no][trick_no]

                if (
                    current_player_index == last_played_card_index
                    or is_eight_stop(self.data["play_to_beat"])
                    or (
                        play_is_joker(self.second_last_play)
                        and self.data["play_to_beat"] == ["3S"]
                    )
                ):
                    self.trick_end = True
                    continue

                # Check if player should be skipped (player has run out of cards)
                if self.finished_players[current_player_index]:
                    current_player_index = (current_player_index + 1) % self.num_players
                    continue

                # Play a move
                name = self.playerlist[current_player_index]
                player = name_to_obj(self.playerlist_orig, self.playerobjects, name)
                move = player.play(self.data)

                # Error checking moves
                if move == None:
                    raise NotAValidPlayError('Move played was "None", which is invalid')
                if self.data["is_start_of_round"]:
                    if move == []:
                        raise NotAValidPlayError("Must play a card on round start")

                    elif self.data["is_start_of_game"] and ("3D" not in move):
                        print(player.name, "played:", move)
                        print("Hand was: ", end="")
                        print(" ".join(player.hand))
                        raise NotAValidPlayError("Must play 3D on round start")

                if (self.second_last_play != None) and not is_higher_play(
                    move, self.data["play_to_beat"]
                ):
                    raise NotAValidPlayError(
                        player.name,
                        "played move ("
                        + " ".join(move)
                        + ") which was not a higher play than the one before",
                    )

                # Move is registered as either pass or valid play
                if move == []:
                    print("Player", player.name, "passed")
                else:
                    for card in move:
                        player.hand.remove(card)

                    print("Player", player.name, "played", " ".join(move))
                    if (
                        self.data["play_to_beat"] != None
                        and self.data["play_to_beat"] != []
                    ):
                        self.second_last_play = self.data["play_to_beat"]
                    self.data["play_to_beat"] = move

                    last_played_card_index = current_player_index

                # React to revolution play
                if is_revolution(move):
                    self.data["is_rev"] = not self.data["is_rev"]

                # Update player information if hand size is 0
                if len(player.hand) == 0:
                    print(player.name, "has emptied their hand!")
                    self.end_of_round_order[self.num_finished] = player.name
                    player_idx = self.playerlist.index(player.name)
                    self.finished_players[player_idx] = True
                    self.num_finished += 1

                    # Player beat the previous tycoon
                    if round_no > 0:
                        prev_tycoon_name = self.data["round_end_history"][round_no - 1][
                            0
                        ]
                        if self.num_finished == 1 and prev_tycoon_name != player.name:
                            print(
                                "Tycoon",
                                prev_tycoon_name,
                                "was beaten, they will now face punishment of Kancho!!!!!!!",
                            )
                            self.end_of_round_order = (
                                [self.end_of_round_order[0]]
                                + ([None] * (self.num_players - 2))
                                + [prev_tycoon_name]
                            )
                            pt_idx = self.playerlist.index(prev_tycoon_name)
                            self.finished_players[pt_idx] = True

                            #### Tracking info
                            orig_idx = self.playerlist_orig.index(prev_tycoon_name)
                            self.times_usurped[orig_idx] += 1

                # Updating round information
                self.data["is_start_of_round"] = False
                self.data["is_start_of_game"] = False
                self.data["round_history"][round_no][trick_no].append(move)
                for i, name in enumerate(self.playerlist):
                    playerobj = name_to_obj(
                        self.playerlist_orig, self.playerobjects, name
                    )
                    self.data["hand_sizes"][i] = len(playerobj.hand)

                # Update index of next player to play a card, skipping finished players
                current_player_index = (current_player_index + 1) % self.num_players

            # Print winner of trick
            self.trick_end = False
            current_player_index = last_played_card_index
            trick_winner_name = self.playerlist[last_played_card_index]
            print("Player", trick_winner_name, "has won current Trick")

            # Reset trick information
            last_played_card_index = None
            self.data["play_to_beat"] = []
            self.second_last_play = None

            # Determine if round should end
            if not (False in self.finished_players):
                self.round_end = True
                self.trick_end = True

        pass


if __name__ == "__main__":
    pass
