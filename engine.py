"""Simulates the specified tries"""

from interface import Game, prompt
import numpy as np
import matplotlib.pyplot as plt
import os

def get_number_of_simulation_tries():
    """prompts user for simulation turns, and validates"""
    simulation_tries_prompt = "Simulate how many games?: "
    beads_per_bowl_prompt = "How many balls in each bowl {3, 4, 5, 6}?: "
    player1_strategy_prompt = "Which strategy should player 1 use {1, 2}?: "
    player2_strategy_prompt = "Which strategy should player 2 use {1, 2}?: "


    player1_strategy = prompt(player1_strategy_prompt, range(1, 3))
    player2_strategy = prompt(player2_strategy_prompt, range(1, 3))
    beads_per_bowl = prompt(beads_per_bowl_prompt, range(3, 7))
    simulation_tries = prompt(simulation_tries_prompt, range(1000))

    return simulation_tries, beads_per_bowl, player1_strategy, player2_strategy


def file_check(filename):
    """
    checks if the outfall pdf file is already in this directory
    if so, then delete it.
    """
    this_dir = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(this_dir, filename)
    if os.path.exists(file_path):
        os.remove(file_path)

def plot_bar(diction, filename):
    """:param: dictionary whose keys are players and values are their scores
    plots results from simulation as percentage of wins (y-axis) against 
    the respective player's scores on the (x-axis). Then write image to pdf file"""
    xlabels = list(diction.keys())
    y_values = [diction[key] for key in xlabels]

    bar_width = 0.90

    x = np.arange(len(y_values))

    fig, ax = plt.subplots()
    ax.bar(x, y_values, width=bar_width)
    ax.set_xticks(x + (bar_width/2.0))
    ax.set_xticklabels(xlabels)

    file_check(filename)
    plt.savefig(filename)

def main():
    simulations, beads_per_bowl, player1_strat, player2_strat = get_number_of_simulation_tries()
    all_games = []
    games_won_by_player1 = []
    games_won_by_player2 = []

    for _ in range(simulations):
        game = Game(beads_per_bowl, player1_strat, player2_strat)
        game.run()
        all_games.append(game)
        # downside this is expensive in terms of memory should we have a sufficiently
        # huge number of iterations
        if game.winner and game.winner.title == 'player1':
            games_won_by_player1.append(game)
        elif game.winner and game.winner.title == 'player2':
            games_won_by_player2.append(game)
    
    print_fmt = "{} has won {} out of {}"
    if len(games_won_by_player1) > len(games_won_by_player2):
        overall_winner = 'player 1  '
        tries = len(games_won_by_player1)
    elif len(games_won_by_player1) < len(games_won_by_player2):
        overall_winner = 'player 2  '
        tries = len(games_won_by_player2)
    print_message = print_fmt.format(overall_winner, tries, len(all_games))
    
    if len(games_won_by_player1) == len(games_won_by_player2):
        print_fmt = "Players drawed at {} tries out of {}"
        print_message = print_fmt.format(len(games_won_by_player1), len(all_games))
    print(print_message)
    filename = "outfall.pdf"
    data = {"player1": len(games_won_by_player1), "player2": len(games_won_by_player2)}
    plot_bar(data, filename)

main()