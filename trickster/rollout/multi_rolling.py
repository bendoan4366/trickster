import numpy as np

from .abstract import MultiRolloutBase
from .rolling import Rolling


class MultiRolling(MultiRolloutBase):

    def __init__(self, agent, envs: list, rollout_configs=None):
        super().__init__(agent, envs, rollout_configs)
        self.rollouts = [Rolling(self.agent, env, config) for env, config in zip(envs, self.rollout_configs)]

    def roll(self, steps, verbose=0, push_experience=True):
        rewards = np.empty(self.num_rollouts)

        for i, rolling in enumerate(self.rollouts):
            history = rolling.roll(steps, verbose=0, push_experience=push_experience)
            rewards[i] = history["mean_reward"]
            if verbose:
                print("Rolled in env #{}, got total reward of {:.4f}".format(i, rewards[i]))

        return {"mean_reward": rewards.mean(), "rewards": rewards}
