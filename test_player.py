import unittest
from .interface import Player, create_player, Board
from unittest.mock import patch

class PlayerTest(unittest.TestCase):
    """
    Incharge of unittesting methods in the Person Class
    """
    def setUp(self):
        
        self.board = Board(3) # 3 beads per bowl
        pass

    def tearDown(self):
        pass

    def _utility(self, strategy=1, board=None):
        board = self.board if not board else board
        with patch('prompt', return_value=strategy):
            player = create_player('player1', board)
        return player

    def list_rep(self, board):
        """returns the list representaion of the board"""
        return [bowl.beads for bowl in board.bowls]

    def test_create_player(self):
        """Verifies we have """
        player = self._utility(1)
        self.assertIsInstance(player.board, Board)
        self.assertEqual(player.strategy, 1)
        self.assertEqual(player.beads_in_nest, 0)
        self.assertEqual(player.beads_in_bowls, 18)
        self.assertEqual(player.total_beads, 18)
        self.assertListEqual(list(player.owned_bowls_range), [list(range(0, 7))])
    
    def test_repr(self, board):
        """No edgecases just confirms this code terminates without errors"""
        player = self._utility()
        self.assertIsInstance(repr(player), str)

    def test_count_beads_method(self):
        player = self._utility()
        response = player.count_beads()
        self.assertTupleEqual(response, (0, 18))

    def test_list_rep(self):
        board = Board(3, 3)
        expected = [3, 3, 3, 0, 3, 3, 3, 0]
        self.assertListEqual(self.list_rep(board), expected)

    def test_player_move(self):
        """An integration test that looks at the in memory logical interpretation
        and sees if a player moves mutates it as they should"""
        # use a cut down kalaha board version where each player gets 3 bowls with each 3 beads
        board = Board(3, 3)
        player = self._utility(1, board)
        move1 = [3,0,4,1,4,3,3,0]
        move2 = [0,1,5,2,4,3,3,0]
        move3 = [1,1,0,3,5,4,4,0]
        move5 = [0,0,0,14,0,0,4,0]
        player._move(1)
        self.assertListEqual(self.list_rep(board), move1)
        player.move(0)
        self.assertListEqual(self.list_rep(board), move2)
        res = player._move(2)
        self.assertListEqual(self.list_rep(board), move3)
        self.assertTrue(res)
        player.move(1)
        res = player.move(0)
        self.assertListEqual(self.list_rep(board), move5)
        self.assertFalse(res)