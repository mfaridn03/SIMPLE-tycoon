import gym
import numpy as np

import config

from stable_baselines import logger
from tycoon.envs.game import Game
from tycoon.envs.Objects.player import Player


class TycoonEnv(gym.Env):
    metadata = {"render.modes": ["human"]}

    def __init__(self, verbose=False, manual=False):
        super().__init__()
        self.name = "tycoon"
        self.manual = manual
        self.n_players = 4

        self.players = [
            Player("A"),
            Player("B"),
            Player("C"),
            Player("D"),
        ]

        self.game = Game(self.players)
        self.game.init_game()

        self.wrapper = TycoonWrapper(self.game)

        self.action_space = None
        self.observation_space = None
        self.verbose = verbose

    def step(self, action):
        """
        From the docs:

        The step method accepts an action from the current active player
        and performs the necessary steps to update the game environment.
        It should also it should update the current_player_num to the
        next player, and check to see if an end state
        of the game has been reached.
        """
        pass

    def reset(self):
        """
        From the docs:

        The reset method is called to reset the game to the starting state,
        ready to accept the first action.
        """
        self.wrapper.reset()

    def render(self, mode="human", close=False):
        """
        From the docs:

        The render function is called to output a visual or
        human readable summary of the current game state to the log file.
        """
        pass

    def observation(self):
        """
        From the docs:

        The observation function returns a numpy array that can be fed as input
        to the PPO policy network. It should return a numeric representation
        of the current game state, from the perspective of the current player,
        where each element of the array is in the range [-1,1].
        """
        pass

    def legal_actions(self):
        """
        From the docs:

        The legal_actions function returns a numpy vector of the same
        length as the action space, where 1 indicates that the
        action is valid and 0 indicates that the action is invalid.
        """
        pass


class TycoonWrapper:
    # Wrapper for the game to be used in the environment
    def __init__(self, game: Game):
        self.game = game

    def reset(self):
        self.players = [
            Player("A"),
            Player("B"),
            Player("C"),
            Player("D"),
        ]
        self.game = Game(self.players)
        self.game.init_game()
