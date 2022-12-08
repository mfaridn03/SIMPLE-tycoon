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
        pass

    def reset(self):
        self.wrapper.reset()

    def render(self, mode="human", close=False):
        pass

    def observation(self):
        pass

    def legal_actions(self):
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
