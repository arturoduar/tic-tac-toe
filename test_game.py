"""
Unit tests for the Tic-Tac-Toe game engine and AI.
"""

import unittest
from game import TicTacToeGame


class TestTicTacToeGame(unittest.TestCase):
    def test_initial_state(self):
        game = TicTacToeGame(mode="pvp")
        self.assertEqual(game.board, [""] * 9)
        self.assertEqual(game.current_player, "X")
        self.assertFalse(game.game_over)
        self.assertIsNone(game.winner)
        self.assertEqual(len(game.available_moves()), 9)

    def test_valid_moves(self):
        game = TicTacToeGame(mode="pvp")
        self.assertTrue(game.make_move(0))
        self.assertEqual(game.board[0], "X")
        self.assertEqual(game.current_player, "O")

        self.assertTrue(game.make_move(1))
        self.assertEqual(game.board[1], "O")
        self.assertEqual(game.current_player, "X")

    def test_invalid_moves(self):
        game = TicTacToeGame(mode="pvp")
        self.assertTrue(game.make_move(0))
        # Occupied cell
        self.assertFalse(game.make_move(0))
        # Out of bounds
        self.assertFalse(game.make_move(-1))
        self.assertFalse(game.make_move(9))

    def test_horizontal_win(self):
        game = TicTacToeGame(mode="pvp")
        # X: 0, 1, 2
        # O: 3, 4
        game.make_move(0)  # X
        game.make_move(3)  # O
        game.make_move(1)  # X
        game.make_move(4)  # O
        game.make_move(2)  # X wins
        self.assertTrue(game.game_over)
        self.assertEqual(game.winner, "X")
        self.assertEqual(game.winning_line, [0, 1, 2])

    def test_vertical_win(self):
        game = TicTacToeGame(mode="pvp")
        game.make_move(0)  # X
        game.make_move(1)  # O
        game.make_move(3)  # X
        game.make_move(2)  # O
        game.make_move(6)  # X wins
        self.assertTrue(game.game_over)
        self.assertEqual(game.winner, "X")
        self.assertEqual(game.winning_line, [0, 3, 6])

    def test_diagonal_win(self):
        game = TicTacToeGame(mode="pvp")
        game.make_move(0)  # X
        game.make_move(1)  # O
        game.make_move(4)  # X
        game.make_move(2)  # O
        game.make_move(8)  # X wins
        self.assertTrue(game.game_over)
        self.assertEqual(game.winner, "X")
        self.assertEqual(game.winning_line, [0, 4, 8])

    def test_draw_game(self):
        game = TicTacToeGame(mode="pvp")
        # X O X
        # X X O
        # O X O
        # Sequence:
        # X: 0, O: 1, X: 2
        # O: 5, X: 3, O: 6
        # X: 4, O: 8, X: 7
        moves = [0, 1, 2, 5, 3, 6, 4, 8, 7]
        for m in moves:
            game.make_move(m)
        self.assertTrue(game.game_over)
        self.assertEqual(game.winner, "draw")
        self.assertIsNone(game.winning_line)

    def test_minimax_ai_blocks_immediate_win(self):
        # Human is X, AI is O
        game = TicTacToeGame(mode="ai_hard", human_player="X")
        # X plays 0
        game.make_move(0)
        # Force a board state where human threatens to win on 2
        # Board: X at 0, 1. AI should block at 2.
        game.board = ["X", "X", "", "", "O", "", "", "", ""]
        game.current_player = "O"
        move = game._minimax_best_move()
        self.assertEqual(move, 2)

    def test_minimax_ai_takes_immediate_win(self):
        # AI is O
        game = TicTacToeGame(mode="ai_hard", human_player="X")
        # AI has 0, 1, empty 2. Human has 3, 4.
        game.board = ["O", "O", "", "X", "X", "", "", "", ""]
        game.current_player = "O"
        move = game._minimax_best_move()
        self.assertEqual(move, 2)

    def test_undo_pvp(self):
        game = TicTacToeGame(mode="pvp")
        game.make_move(0)
        self.assertEqual(game.board[0], "X")
        self.assertTrue(game.undo_move())
        self.assertEqual(game.board[0], "")
        self.assertEqual(game.current_player, "X")


if __name__ == "__main__":
    unittest.main()
