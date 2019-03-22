"""Simulates the specified tries"""

from interface import Game, prompt

def get_number_of_simulation_tries():
    """prompts user for simulation turns, and validates"""
    simulation_tries_prompt = "How many times should i simulate?: "
    simulation_tries = prompt(simulation_tries_prompt, range(1000))
    return simulation_tries

def main():
    simulations = get_number_of_simulation_tries()
    all_games = []
    for _ in range(simulations):
        new_game = Game()
        new_game.run()
        all_games.append(new_game)
        # downside this is expensive in terms of memory should we have a sufficiently
        # huge number of iterations
    return all_games

main()