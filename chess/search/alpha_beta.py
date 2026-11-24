from ..evaluation import Evaluation
from ..rules import Rules
from .move_ordering import MoveOrdering
from .quiescence import Quiescence
from .transposition import ZobristHash, TranspositionTable


class AlphaBeta:

    def __init__(self):
        self.nodes_searched = 0
        self.tt_hits = 0

        self.quiescence = Quiescence()
        self.hasher = ZobristHash()
        self.transposition_table = TranspositionTable()

    def search(self, board, depth):
        self.nodes_searched = 0
        self.tt_hits = 0

        self.quiescence.nodes_searched = 0
        self.transposition_table.clear()

        maximizing = board.turn == "white"

        best_score = float("-inf") if maximizing else float("inf")
        best_move = None

        moves = Rules.legal_moves(board)

        if not moves:
            return None

        moves = MoveOrdering.order_moves(board, moves)

        for move in moves:
            child = board.copy()
            Rules.make_move(child, move)

            score = self._alpha_beta(
                child,
                depth - 1,
                float("-inf"),
                float("inf"),
                not maximizing
            )

            if maximizing:
                if score > best_score:
                    best_score = score
                    best_move = move
            else:
                if score < best_score:
                    best_score = score
                    best_move = move

        return best_move

    def _alpha_beta(self, board, depth, alpha, beta, maximizing):
        self.nodes_searched += 1

        original_alpha = alpha
        original_beta = beta

        # Check transposition table
        key = self.hasher.hash(board)
        entry = self.transposition_table.get(key)

        if entry is not None and entry.depth >= depth:
            self.tt_hits += 1

            if entry.flag == TranspositionTable.EXACT:
                return entry.score

            if entry.flag == TranspositionTable.LOWERBOUND:
                alpha = max(alpha, entry.score)

            elif entry.flag == TranspositionTable.UPPERBOUND:
                beta = min(beta, entry.score)

            if alpha >= beta:
                return entry.score

        # Quiescence search at leaf
        if depth == 0:
            return self.quiescence.search(
                board,
                alpha,
                beta,
                maximizing
            )

        moves = Rules.legal_moves(board)

        if not moves:
            return Evaluation.evaluate(board)

        moves = MoveOrdering.order_moves(board, moves)

        if maximizing:
            best = float("-inf")

            for move in moves:
                child = board.copy()
                Rules.make_move(child, move)

                score = self._alpha_beta(
                    child,
                    depth - 1,
                    alpha,
                    beta,
                    False
                )

                best = max(best, score)
                alpha = max(alpha, best)

                if beta <= alpha:
                    break

        else:
            best = float("inf")

            for move in moves:
                child = board.copy()
                Rules.make_move(child, move)

                score = self._alpha_beta(
                    child,
                    depth - 1,
                    alpha,
                    beta,
                    True
                )

                best = min(best, score)
                beta = min(beta, best)

                if beta <= alpha:
                    break

        # Determine what kind of result we obtained.
        if best <= original_alpha:
            flag = TranspositionTable.UPPERBOUND

        elif best >= original_beta:
            flag = TranspositionTable.LOWERBOUND

        else:
            flag = TranspositionTable.EXACT

        self.transposition_table.store(
            key,
            depth,
            best,
            flag
        )

        return best