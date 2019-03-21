"""
This module creates a logical model /representation of the board.
Actions include:
    impelementation of an appropriate data structure to represent the pots and the Home
    a factory method that takes required arguments to create the board
"""


class Board:
    """
    use a list and a non public lightweight _Node class to represent the
    Board and the nodes as pots
    """

    class _Node:
        """
         A storage object that represents a pot
        """

        def __init__(self, number_of_beads):
            self.beads = number_of_beads
            self.type = 'Pot' # whether this is a normal pot or its the Home

    def __init__(self, beads_per_pot):
        self.pots = []
        for idx in range(1,15):
            pot = self._Node(beads_per_pot)
            if idx % 7 == 0:
                pot.type = "Home"
                pot.beads = 0
            self.pots.append(pot)

    def __repr__(self):
        """
        A console displayable representation of the board, synonymous to visualize
        """
        data = [pot.beads for pot in self.pots]
        out_border = "".join(["+{!s:-^4}".format('-') for _ in range(8)])
        out_border += "+"
        in_border = "".join(["+"] + [" " * 4] + ['+'] + ["----+" * 6] + [" " * 4] + ["+"])
        top_row = ["|"]
        bottom_row = ["|"]
        bottom_row.append(" " * 4 + "|")
        for idx in range(6, -1, -1):
            top_row.append("{!s:^4}|".format(data[idx]))

        for idx in range(7, 13):
            bottom_row.append("{!s:^4}|".format(data[idx]))

        top_row.append(" " * 4 + "|")
        bottom_row.append("{!s:^4}|".format(data[13]))
        top_row = "".join(top_row)
        bottom_row = "".join(bottom_row)
        full_string = "{} \n{} \n{} \n{} \n{} \n"\
            .format(out_border, top_row, in_border, bottom_row, out_border)
        return full_string


def range_checker(value, range):
    """
    :param: value: the value to check if present in the specified range
    :param: range: specifies bounds in which the value can exist
    :return: True if value in range else raises ValueError
    """
    if value not in range:
        raise ValueError("required value should be in, <{}>, "
                         "<{}> is not in that range".format(range, value))
    return True

def prompt(to_prompt, range):
    """
    :param to_prompt: messaged to be displayed through prompt
    :param range:
    :return: the user input data
    Prompts the user untill fed valid data for this prompt
    """
    _prompt = to_prompt
    while True:
        try:
            user_input = int(input(_prompt))
            if range_checker(user_input, range):
                return user_input
        except ValueError as error:
            print(error.args[0])
            _prompt = "Try Again, " + to_prompt

def create_board():
    """
    :param: None:
    :return: None
    prompts the user for the required data, validates it and then returns
    a Board object
    """
    player1_strategy_prompt = "Which strategy should player 1 use {1, 2}?: "
    player2_strategy_prompt = "Which strategy should player 2 use {1, 2}?: "
    beads_per_pot_prompt = "How many balls in each pot {3, 4, 5, 6}?: "
    simulation_tries_prompt = "How many times should i simulate?: "

    player1_strategy = prompt(player1_strategy_prompt, range(1, 3))
    player2_strategy = prompt(player2_strategy_prompt, range(1, 3))
    beads_per_pot = prompt(beads_per_pot_prompt, range(3, 7))
    simulation_tries = prompt(simulation_tries_prompt, range(1000))

    new_board = Board(beads_per_pot)
    return new_board