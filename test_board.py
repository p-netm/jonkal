import unittest
from unittest.mock import patch
from kalaha.interface import Board, create_board, prompt

class BoardTest(unittest.TestCase):
    """Verifies the internal representational structure of the board
    is as it should be ; also tests utility functions that are involved
    in creating a board although not directly part of the board"""
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_underlying_representation(self):
        """
        for variable values of bowls and number of beads, make
        sure the representaion is correct
        """
        board = Board(3, 5)
        self.assertIsInstance(board.bowls, list)
        self.assertEqual(board.bowls[len(board.bowls) // 2 - 1].type, 'Nest')
        for index in range(1, 13):
            idx = index - 1
            if index % 6 != 0:
                self.assertEqual(board.bowls[idx].beads, 3)
                self.assertEqual(board.bowls[idx].type, 'Bowl')
            else:
                self.assertEqual(board.bowls[idx].beads, 0)
                self.assertEqual(board.bowls[idx].type, 'Nest')

    def test_re_underlying_representation(self):
        """
        for variable values of bowls and number of beads, make
        sure the representaion is correct
        """
        board = Board(6, 7) # 7 bowls with 6 beads per bowl
        for index in range(1, 17):
            idx = index - 1
            if index % 8 != 0:
                self.assertEqual(board.bowls[idx].beads, 6)
                self.assertEqual(board.bowls[idx].type, 'Bowl')
            else:
                self.assertEqual(board.bowls[idx].beads, 0)
                self.assertEqual(board.bowls[idx].type, 'Nest')

    def test_repr(self):
        """check if we have errors in serializing object to string"""
        self.assertIsInstance(repr(Board(3)), str)
        self.assertIsInstance(repr(Board(3, 7)), str)

    def test__prompt_method(self):
        with patch('builtins.input', return_value=1):
            self.assertTrue(prompt('some prompt', range(1, 5)), range(1, 5))
            self.assertTrue(prompt('some prompt', [1, 2, 3, 4]), range(1, 5))

    def test_create_board_factory_method(self):
        board = create_board(4)
        self.assertEqual(board.bowls[0].beads, 4)

