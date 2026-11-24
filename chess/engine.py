from .evaluation import Evaluation
from .rules import Rules
from .search.alpha_beta import AlphaBeta


class Engine:
    def __init__(self, depth=3):
        if not isinstance(depth, int) or depth < 1:
            raise ValueError("Depth must be a positive integer.")

        self.depth = depth
        self.nodes_searched = 0
        self.tt_hits = 0
        self.tt_entries = 0

        self.searcher = AlphaBeta()

    def choose_move(self, board):
        move = self.searcher.search(board, self.depth)

        self.nodes_searched = self.searcher.nodes_searched
        self.tt_hits = self.searcher.tt_hits
        self.tt_entries = len(self.searcher.transposition_table)

        return move

    def select_move(self, board):
        return self.choose_move(board)

    def evaluate(self, board):
        return Evaluation.evaluate(board)

    def evaluate_move(self, board, move):
        child = board.copy()
        Rules.make_move(child, move)
        return Evaluation.evaluate(child)