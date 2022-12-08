import gym
import numpy as np

import config

from stable_baselines import logger
from tycoon.envs.game import Game


class TycoonEnv(gym.Env):
    metadata = {"render.modes": ["human"]}

    def __init__(self, verbose=False, manual=False):
        super().__init__()
        self.name = "tycoon"
        self.manual = manual

        num_player = 4
        self.n_player = num_player

        self.game = Game()

    def step(self, action):
        pass

    def reset(self):
        pass

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
