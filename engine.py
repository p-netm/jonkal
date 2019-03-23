"""Simulates the specified tries"""

from interface import Game, prompt

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

def plot_results():
    pass

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

main()