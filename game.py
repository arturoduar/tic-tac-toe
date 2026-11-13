"""
Tic-Tac-Toe core game logic and AI implementation.
"""

import math
import random
from typing import Dict, List, Optional, Tuple, Any

WINNING_COMBINATIONS = [
    [0, 1, 2],  # Top row
    [3, 4, 5],  # Middle row
    [6, 7, 8],  # Bottom row
    [0, 3, 6],  # Left col
    [1, 4, 7],  # Middle col
    [2, 5, 8],  # Right col
    [0, 4, 8],  # Diagonal top-left to bottom-right
    [2, 4, 6],  # Diagonal top-right to bottom-left
]


class TicTacToeGame:
    def __init__(
        self,
        mode: str = "ai_hard",
        human_player: str = "X",
        starting_player: str = "X",
    ):
        self.board: List[str] = [""] * 9
        self.current_player: str = starting_player
        self.starting_player: str = starting_player
        self.human_player: str = human_player
        self.ai_player: str = "O" if human_player == "X" else "X"
        self.mode: str = mode  # "pvp", "ai_easy", "ai_medium", "ai_hard"
        self.winner: Optional[str] = None  # "X", "O", "draw", or None
        self.winning_line: Optional[List[int]] = None
        self.game_over: bool = False
        self.move_history: List[Dict[str, Any]] = []

        # If it's an AI game and AI starts, trigger AI move
        if self.is_ai_game() and self.current_player == self.ai_player:
            self.trigger_ai_move()

    def is_ai_game(self) -> bool:
        return self.mode in ("ai_easy", "ai_medium", "ai_hard")

    def reset(self, alternate_starter: bool = False):
        if alternate_starter:
            self.starting_player = "O" if self.starting_player == "X" else "X"
        self.board = [""] * 9
        self.current_player = self.starting_player
        self.winner = None
        self.winning_line = None
        self.game_over = False
        self.move_history = []

        if self.is_ai_game() and self.current_player == self.ai_player:
            self.trigger_ai_move()

    def set_settings(self, mode: Optional[str] = None, human_player: Optional[str] = None):
        if mode in ("pvp", "ai_easy", "ai_medium", "ai_hard"):
            self.mode = mode
        if human_player in ("X", "O"):
            self.human_player = human_player
            self.ai_player = "O" if human_player == "X" else "X"
        self.reset()

    def available_moves(self, board: Optional[List[str]] = None) -> List[int]:
        b = board if board is not None else self.board
        return [i for i, cell in enumerate(b) if cell == ""]

    def make_move(self, index: int, player: Optional[str] = None) -> bool:
        """
        Attempt to make a move at the given board index (0-8).
        Returns True if move was valid and placed, False otherwise.
        """
        if self.game_over:
            return False
        if not (0 <= index <= 8):
            return False
        if self.board[index] != "":
            return False

        move_player = player if player else self.current_player
        self.board[index] = move_player
        self.move_history.append({"index": index, "player": move_player})

        # Check win or draw
        winner, line = self.check_winner_state(self.board)
        if winner:
            self.winner = winner
            self.winning_line = line
            self.game_over = True
        elif not self.available_moves():
            self.winner = "draw"
            self.winning_line = None
            self.game_over = True
        else:
            # Switch turn
            self.current_player = "O" if move_player == "X" else "X"
            # If next turn belongs to AI
            if self.is_ai_game() and self.current_player == self.ai_player and not self.game_over:
                self.trigger_ai_move()

        return True

    def trigger_ai_move(self) -> Optional[int]:
        if self.game_over:
            return None
        move = self.get_ai_move()
        if move is not None and self.board[move] == "":
            self.board[move] = self.ai_player
            self.move_history.append({"index": move, "player": self.ai_player})

            winner, line = self.check_winner_state(self.board)
            if winner:
                self.winner = winner
                self.winning_line = line
                self.game_over = True
            elif not self.available_moves():
                self.winner = "draw"
                self.winning_line = None
                self.game_over = True
            else:
                self.current_player = self.human_player
            return move
        return None

    def undo_move(self) -> bool:
        """Undo last turn (or two moves if vs AI so it's the human's turn again)."""
        if not self.move_history:
            return False

        if self.is_ai_game():
            # If game is over, we might need to undo 1 or 2 moves
            moves_to_undo = 2 if len(self.move_history) >= 2 else len(self.move_history)
            for _ in range(moves_to_undo):
                last = self.move_history.pop()
                self.board[last["index"]] = ""
            self.current_player = self.human_player
        else:
            last = self.move_history.pop()
            self.board[last["index"]] = ""
            self.current_player = last["player"]

        self.winner = None
        self.winning_line = None
        self.game_over = False
        return True

    @staticmethod
    def check_winner_state(board: List[str]) -> Tuple[Optional[str], Optional[List[int]]]:
        for line in WINNING_COMBINATIONS:
            a, b, c = line
            if board[a] and board[a] == board[b] == board[c]:
                return board[a], line
        return None, None

    def get_ai_move(self) -> Optional[int]:
        open_moves = self.available_moves()
        if not open_moves:
            return None

        if self.mode == "ai_easy":
            return random.choice(open_moves)

        elif self.mode == "ai_medium":
            # 60% chance to play optimal minimax or smart move, 40% random
            if random.random() < 0.60:
                return self._minimax_best_move()
            return random.choice(open_moves)

        elif self.mode == "ai_hard":
            return self._minimax_best_move()

        return random.choice(open_moves)

    def _minimax_best_move(self) -> int:
        open_moves = self.available_moves()

        # Quick check for opening move on empty board to save time and add variety
        if len(open_moves) == 9:
            # Prefer corners or center
            return random.choice([0, 2, 4, 6, 8])

        # If human played first corner, playing center is optimal
        if len(open_moves) == 8 and 4 in open_moves:
            return 4

        best_score = -math.inf
        best_moves = []

        for move in open_moves:
            self.board[move] = self.ai_player
            score = self._minimax(self.board, 0, False, -math.inf, math.inf)
            self.board[move] = ""

            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)

        return random.choice(best_moves)

    def _minimax(
        self,
        board: List[str],
        depth: int,
        is_maximizing: bool,
        alpha: float,
        beta: float,
    ) -> int:
        winner, _ = self.check_winner_state(board)
        if winner == self.ai_player:
            return 10 - depth
        elif winner == self.human_player:
            return depth - 10
        elif not self.available_moves(board):
            return 0

        if is_maximizing:
            max_eval = -math.inf
            for move in self.available_moves(board):
                board[move] = self.ai_player
                eval_score = self._minimax(board, depth + 1, False, alpha, beta)
                board[move] = ""
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = math.inf
            for move in self.available_moves(board):
                board[move] = self.human_player
                eval_score = self._minimax(board, depth + 1, True, alpha, beta)
                board[move] = ""
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval

    def to_dict(self) -> Dict[str, Any]:
        return {
            "board": self.board,
            "currentPlayer": self.current_player,
            "humanPlayer": self.human_player,
            "aiPlayer": self.ai_player,
            "mode": self.mode,
            "winner": self.winner,
            "winningLine": self.winning_line,
            "gameOver": self.game_over,
            "moveCount": len(self.move_history),
        }
