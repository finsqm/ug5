#!/usr/bin/env python
import logging
import sys
import numpy as np
import matplotlib.pyplot as plt

HEADS = 'H'
TAILS = 'T'

logging.basicConfig(level=logging.WARNING)

class Player(object):
    """ Class for a player in the matching pennies game
    """
    def __init__(self, matcher, new_game_policy):
        """
        Player 1 stores variables for estimating Player 2 and vice versa
        e.g. p1.N is the number of heads played by player 2
        """
        self.N = 0.0
        self.M = 0.0
        self.total = 0.0
        self.matcher = matcher
        self.new_game = True
        self.new_game_policy = new_game_policy

    def play(self):
        if self.new_game:
            self.new_game = False
            return self.new_game_policy
        if self.N > self.M:
            if self.matcher:
                return HEADS
            else:
                return TAILS
        else:
            if self.matcher:
                return TAILS
            else:
                return HEADS

    def update(self, other_players_move):
        if other_players_move == HEADS:
            self.N += 1
        else:
            self.M += 1
        self.total += 1

    def get_sigma(self):
        return (self.N / self.total, self.M / self.total)

def matching_pennies_game(num_iterations, starting_policy):
    player_1 = Player(matcher=True, new_game_policy=starting_policy[0])
    player_2 = Player(matcher=False, new_game_policy=starting_policy[1])
    player_1_sigma_0 = []
    player_2_sigma_0 = []
    for i in xrange(num_iterations):
        # Each player moves
        player_1_move = player_1.play()
        player_2_move = player_2.play()
        # Each player updates their estimates
        player_1.update(player_2_move)
        player_2.update(player_1_move)
        if i % 10 == 0:
            player_1_sigma = player_1.get_sigma()
            player_1_sigma_0.append(player_1_sigma[0])

            player_2_sigma = player_2.get_sigma()
            player_2_sigma_0.append(player_2_sigma[0])

            logging.info("Player 1's estimate of player 2 sigma: {0}".format(player_1_sigma))
            logging.info("Player 2's estimate of player 1 sigma: {0}".format(player_2_sigma))

    x_axis = np.arange(0, num_iterations, 10)
    logging.debug(x_axis.shape)
    logging.debug(len(player_1_sigma_0))
    plt.figure(1)

    plt.title('Estimated Sigma')
    plt.xlabel('Iteration')
    plt.ylabel('Probability of Heads')
    plt.plot(x_axis, player_1_sigma_0, label='Player 1')
    plt.plot(x_axis, player_2_sigma_0, label='Player 2')

    plt.legend()
    plt.show()

if __name__ == "__main__":
    num_iterations = int(sys.argv[1])
    starting_policy = []

    if sys.argv[2] == 'heads':
        starting_policy.append(HEADS)
    else:
        starting_policy.append(TAILS)

    if sys.argv[3] == 'heads':
        starting_policy.append(HEADS)
    else:
        starting_policy.append(TAILS)

    matching_pennies_game(num_iterations, starting_policy)
