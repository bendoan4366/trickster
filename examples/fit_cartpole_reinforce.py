import numpy as np

import gym

from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

from trickster.agent import REINFORCE
from trickster.rollout import Trajectory, RolloutConfig
from trickster.utility import visual

env = gym.make("CartPole-v1")
input_shape = env.observation_space.shape
num_actions = env.action_space.n

policy = Sequential([Dense(16, activation="relu", input_shape=input_shape),
                     Dense(16, activation="relu"),
                     Dense(num_actions, activation="softmax")])
policy.compile(loss="categorical_crossentropy", optimizer=Adam(5e-3))

agent = REINFORCE(policy, action_space=num_actions)

rollout = Trajectory(agent, env, config=RolloutConfig(max_steps=300))

rewards = []
losses = []

for episode in range(1, 501):
    rollout_history = rollout.rollout(verbose=0, push_experience=True)
    agent_history = agent.fit(batch_size=-1, verbose=0, reset_memory=True)

    rewards.append(rollout_history["reward_sum"])
    losses.append(agent_history["loss"])

    print("\rEpisode {:>4} RWD: {:>6.1f}, UTILITY: {: >8.4f}".format(
        episode,
        np.mean(rewards[-10:]),
        np.mean(losses[-10:])), end="")

    if episode % 10 == 0:
        print()

visual.plot_vectors([rewards, losses], ["Rewards", "Utility"], smoothing_window_size=10)
