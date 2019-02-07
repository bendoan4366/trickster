import numpy as np

from matplotlib import pyplot as plt


def plot_vectors(vectors, names, window_size):
    fig, axes = plt.subplots(len(vectors), sharex="all")

    for ax, vec, name in zip(axes, vectors, names):
        ax.plot(vec, "r-", alpha=0.5)
        ax.plot(np.convolve(vec, np.ones(window_size) / window_size, mode="valid"))
        ax.set_title(name)
        ax.grid()

    plt.show()