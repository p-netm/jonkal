import unittest
from .interface import Player, create_player, Board

class PlayerTest(unittest.TestCase):
    """
    Incharge of unittesting methods in the Person Class
    """
    def setUp(self):
        self.board = Board(3) # 3 beads per bowl
        pass

    def tearDown(self):
        pass

    def _utility(self, strategy=1, board=None, title='player1'):
        board = self.board if not board else board
        player = create_player(title, board, strategy)
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
        self.assertListEqual(list(player.owned_bowls_range), list(range(0, 7)))
    
    def test_repr(self):
        """No edgecases just confirms this code terminates without errors"""
        player = self._utility()
        self.assertIsInstance(repr(player), str)

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
        self.assertEqual(player.title, 'player1')
        move1 = [3, 0, 4, 1, 4, 3, 3, 0]
        move2 = [0, 1, 5, 2, 4, 3, 3, 0]
        move3 = [1, 1, 0, 3, 5, 4, 4, 0]
        move5 = [0, 0, 0, 14, 0, 0, 4, 0]
        player._move(1)
        self.assertListEqual(self.list_rep(board), move1)
        player._move(0)
        self.assertListEqual(self.list_rep(board), move2)
        res = player._move(2)
        self.assertListEqual(self.list_rep(board), move3)
        self.assertTrue(res)
        player._move(1)
        res = player._move(0)
        self.assertListEqual(self.list_rep(board), move5)
        self.assertFalse(res)

    def test_two_players_moves(self):
        """just as test_player_move function but simulates for both players instead of one"""
        board = Board(3, 3)

        player1 = self._utility(1, board)
        player2 = self._utility(2, board, 'player2')
        self.assertEqual(player1.title, 'player1')
        self.assertEqual(player2.title, 'player2')
        move1 = [3, 0, 4, 1, 4, 3, 3, 0]
        move2 = [4, 0, 4, 1, 0, 4, 4, 1]
        move3 = [0, 1, 5, 2, 1, 4, 4, 1]
        move4 = [1, 2, 6, 2, 1, 4, 0, 2]
        move5 = [1, 0, 7, 3, 1, 4, 0, 2]
        move6 = [2, 1, 7, 3, 1, 0, 1, 3]
        move7 = [2, 0, 8, 3, 1, 0, 1, 3]
        move8 = [2, 0, 8, 3, 0, 0, 1, 4]
        player1._move(1)
        self.assertListEqual(self.list_rep(board), move1)
        res = player2._move(4)
        self.assertListEqual(self.list_rep(board), move2)
        self.assertTrue(res)

        player1._move(0)
        self.assertListEqual(self.list_rep(board), move3)
        res = player2._move(6)
        self.assertListEqual(self.list_rep(board), move4)
        self.assertTrue(res)

        player1._move(1)
        self.assertListEqual(self.list_rep(board), move5)
        res = player2._move(5)
        self.assertListEqual(self.list_rep(board), move6)
        self.assertTrue(res)

        player1._move(1)
        self.assertListEqual(self.list_rep(board), move7)
        res = player2._move(4)
        self.assertListEqual(self.list_rep(board), move8)
        self.assertTrue(res)
