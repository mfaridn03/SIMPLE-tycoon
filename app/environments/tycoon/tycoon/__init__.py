from gym.envs.registration import register

register(
    id='Tycoon-v0',
    entry_point='tycoon.envs:TycoonEnv',
)
