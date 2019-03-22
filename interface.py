"""
This module creates a logical model /representation of the board.
Actions include:
    impelementation of an appropriate data structure to represent the bowls and the Nest
    a factory method that takes required arguments to create the board
    
"""
from random import choice

class Player:
    """
    Represents a player instance
    """
    def __init__(self, bowls_range_start, bowls_range_end, board, strategy):
        """
        :param bowls_range_start: lower bound index for the bowls owned by this user
        :param bowls_range_end: the upper bound index not included
        :param board: A Board obj
        :param strategy: an integer denoting wither of the 2 strategies
        """
        # store a reference to the board, The board should be visible to each user
        self.board = board
        self.bowls_range_start = bowls_range_start
        self.bowls_range_end = bowls_range_end
        res = self.count_beads() # returns tuple (nested_beads, beads in normal bowls)
        self.beads_in_nest = res[0]
        self.beads_in_bowls = res[1]
        self.owned_bowls_range = range(self.bowls_range_start, self.bowls_range_end)
        # a player should also know his strategy
        self.strategy = strategy
        self.total_beads = self.beads_in_nest + self.beads_in_bowls

    def __repr__(self):
        return "<(Player) nested beads: %d; beads_in_bowls: %d; strategy: %d>" % \
               (self.beads_in_nest, self.beads_in_bowls, self.strategy)

    def count_beads(self):
        """
        :param: int: start: the lowerbound index delimiter for bowls belonging to this player
        :param: int: start: the upperbound index delimiter for bowls belonging to this player
        :returns: tuple: containing beads in this players nest and total beads in his bowls respectively
        range format -> (start: end] # the end is not included in the range but the start is.
        """
        start = self.bowls_range_start
        end = self.bowls_range_end
        beads_in_nest = 0
        beads_in_bowls = 0
        for bowl in self.board.bowls[start: end]:
            if bowl.type == 'Nest':
                beads_in_nest += bowl.beads
            if bowl.type == 'Bowl':
                beads_in_bowls += bowl.beads
        return beads_in_nest, beads_in_bowls
    
    def _move(self, start_index):
        """ perform a legal move"""
        # empty bowl at index then iterate over next k bowls while adding beads
        _bowls = self.board.bowls
        beads_to_move = _bowls[start_index].beads
        _bowls[start_index].beads = 0
        for idx in range(start_index + 1, start_index + beads_to_move + 1):
            i = idx % len(_bowls) # to create a form of loop back somewhat like a circular list
            current_bowl = _bowls[i]
            if current_bowl.type == 'Nest':
                # we check that this home bowl is owned by this user
                if not self.owns_bowl(i):
                    beads_to_move += 1
                    continue
            current_bowl.beads += 1
            # special conditions: if this is the last bead placement then we have 2 situations
            # :situation1: this bowl is this players nest and thus they get an extra move
            # :situation2: this bowl is empty
            if current_bowl.type == 'Nest' and current_bowl.beads == 1 and idx == start_index + beads_to_move:
                self.move()
            if current_bowl.beads == 1 and idx == start_index + beads_to_move:
                # capture beads in this bowl and those of the opposite bowl
                current_bowl.beads = 0
                _bowls[self.bowls_range_end - 1].beads += _bowls[self.opposite_bowl(i)].beads + 1
                _bowls[self.opposite_bowl(i)].beads = 0
        return self.state_checker()

    def get_starting_index(self):
        """
        curates the indexes that are valid for selection as a point this player can start his turn
        then returns a single index as per the players selected strategy
        """
        valid_indices = []
        max_beads = 0
        if self.strategy == 1:
            # randomly and uniformly select from occupied bowls
            valid_indices = [index for index in self.owned_bowls_range
                             if self.board.bowls[index].beads and self.board.bowls[index].type == 'Bowl']
        if self.strategy == 2:
            # filter the bowls with the most beads
            for index in self.owned_bowls_range:
                if self.board.bowls[index].type == "Nest":
                    continue # excepts the nest bowl as an invalid index to pick from
                if self.board.bowls[index].beads > max_beads:
                    max_beads = self.board.bowls[index].beads
                    valid_indices = [index]
                elif self.board.bowls[index].beads == max_beads:
                    valid_indices.append(index)
        return choice(valid_indices)

    def move(self):
        choosen_index = self.get_starting_index()
        return self._move(choosen_index)
            
    def state_checker(self):
        """
        :param: None: 
        :returns: True to indicate that both players have valid moves else False 
        to indicate that atleast one player has no legal moves
        Checks for the sufficient conditions to indicate a game over """
        # check if the current player after his turn if he still has beads in his bowls
        return bool(self.beads_in_bowls)

    def owns_bowl(self, bowl_index):
        """
        :param: int: bowl_index: The index of a bowl , a _Node on the self.board.bowls list
        :return: True if bowl is owned by this player else False
        Checks that a bowl located at the given bowl_index is owned by the player
        Particularly useful when dealing with the Nest bowls
        """
        return bowl_index in self.owned_bowls_range

    def opposite_bowl(self, bowl_index):
        """
        :param: int: bowl_index: The index of a bowl , a _Node on the self.board.bowls list
        :return: int: index of a bowl that would be opposite the bowl indexed by the bowl_index argument
        """
        return (len(self.board.bowls) - 2) - bowl_index


class Board:
    """
    use a list and a non public lightweight _Node class to represent the
    Board and the nodes as bowls
    """

    class _Node:
        """
        A storage object that represents a bowl
        """

        def __init__(self, number_of_beads):
            self.beads = number_of_beads
            self.type = 'Bowl' # defines whether this is a bowl or nest(bowl by default)

        def __repr__(self):
            return "<node(%s) %d>" % (self.type, self.beads)

    def __init__(self, beads_per_bowl, num_of_bowls_per_player=6):
        """
        :param beads_per_bowl: denotes the number of beads in each bowl at the start of game
        :param num_of_bowls_per_player: denotes number of bowls ecluding nest usually six
        """
        self.bowls = []
        total_bowls = (num_of_bowls_per_player + 1) * 2
        for idx in range(1, total_bowls+1):
            bowl = self._Node(beads_per_bowl)
            if idx % (total_bowls // 2) == 0:
                bowl.type = 'Nest'
                bowl.beads = 0
            self.bowls.append(bowl)

    def __repr__(self):
        """
        A console displayable representation of the board, synonymous to visualize
        """
        data = [bowl.beads for bowl in self.bowls]
        bowls_len = len(self.bowls)
        out_border = "".join(["+{!s:-^4}".format('-') for _ in range(bowls_len // 2 + 1 )])
        out_border += "+"
        in_border = "".join(["+"] + [" " * 4] + ['+'] + ["----+" * ((bowls_len - 1) // 2)] + [" " * 4] + ["+"])
        top_row = ["|"]
        bottom_row = ["|"]
        bottom_row.append(" " * 4 + "|")
        for idx in range((bowls_len - 1 ) // 2, -1, -1):
            top_row.append("{!s:^4}|".format(data[idx]))

        for idx in range(bowls_len // 2, bowls_len - 1):
            bottom_row.append("{!s:^4}|".format(data[idx]))

        top_row.append(" " * 4 + "|")
        bottom_row.append("{!s:^4}|".format(data[-1]))
        top_row = "".join(top_row)
        bottom_row = "".join(bottom_row)
        full_string = "{} \n{} \n{} \n{} \n{} \n"\
            .format(out_border, top_row, in_border, bottom_row, out_border)
        return full_string


class Game:
    """
    A composition game that will take the player and board interfaces and
    interleave them together. Also takes charge of the simulation runs and the report
    generation.
    """
    def __init__(self):
        self.board = create_board()
        # defines the indexes delimiters that define bowls at certain index belong to which player
        self.player1 = create_player('player1', self.board)
        self.player2 = create_player('player2', self.board)
        self.current_player = None
        self.winner = None

    def __repr__(self):
        return "{}\n\n{}\n\n{}".format(repr(self.player1), repr(self.board), repr(self.player2))

    def run(self):
        """
        Executes a single instance of game play that is from the first player move to until
        the game ends(dictated by the first player to run out of legal moves)
        """
        players = [self.player1, self.player2]
        count = 0

        self.current_player = players[count % len(players)]
        # execute a single iteration of the game i.e each player gets their turn to play/move
        while self.current_player:
            action = self.current_player.move()
            if action:
                # Truthy value denotes player move executed successfully and still has legal moves
                # implying move to next player
                count += 1
            else:
                # implies that current_player exhausted legal moves; time to determine winner
                self.current_player = None
        if self.player1.total_beads > self.player2.total_beads:
            self.winner = self.player1
        else:
            self.winner = self.player2



# Some utility methods : factory methods and get_user_input functionalities
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
            if user_input in range:
                return user_input
        except ValueError as error:
            _prompt = "Accepted_values {}, ".format(str(list(range))) + to_prompt


def create_board():
    """
    :param: None:
    :return: None
    prompts the user for the required data pertaining to the board,
     validates it and then returns a Board object
    """
    beads_per_bowl_prompt = "How many balls in each bowl {3, 4, 5, 6}?: "
    beads_per_bowl = prompt(beads_per_bowl_prompt, range(3, 7))
    new_board = Board(beads_per_bowl)
    return new_board

def create_player(name, board):
    """
    :params: name: either player1 or player2;
        helps define the indexes ranges for bowls that the player will own
    :params: board: a instance of Board class
    Factory method to create and return a player with the required instance fields
    populated with required data
    """
    player1_strategy_prompt = "Which strategy should player 1 use {1, 2}?: "
    player2_strategy_prompt = "Which strategy should player 2 use {1, 2}?: "

    prompt_message = player1_strategy_prompt if '1' in name else player2_strategy_prompt
    start = 0 if '1' in name else  (len(board.bowls) // 2) + 1
    end = len(board.bowls) // 2 if '1' in name else  len(board.bowls) - 1

    strategy = prompt(prompt_message, range(1, 3))
    new_player = Player(start, end, board, strategy)
    return new_player