from ..evaluation import Evaluation
from ..rules import Rules
from .move_ordering import MoveOrdering


class Quiescence:

    def __init__(self, max_depth=4):
        self.max_depth = max_depth
        self.nodes_searched = 0

    def search(self, board, alpha, beta, maximizing, depth=0):
        self.nodes_searched += 1

        # Prevent unlimited tactical searching
        if depth >= self.max_depth:
            return Evaluation.evaluate(board)

        stand_pat = Evaluation.evaluate(board)

        if maximizing:
            if stand_pat >= beta:
                return beta

            if stand_pat > alpha:
                alpha = stand_pat

        else:
            if stand_pat <= alpha:
                return alpha

            if stand_pat < beta:
                beta = stand_pat

        # Only search captures and promotions.
        # Checks are deliberately excluded for now
        # to keep the quiescence tree controlled.
        tactical_moves = self._tactical_moves(board)

        if not tactical_moves:
            return stand_pat

        tactical_moves = MoveOrdering.order_moves(
            board,
            tactical_moves
        )

        if maximizing:
            best = stand_pat

            for move in tactical_moves:
                child = board.copy()
                Rules.make_move(child, move)

                score = self.search(
                    child,
                    alpha,
                    beta,
                    False,
                    depth + 1
                )

                best = max(best, score)
                alpha = max(alpha, best)

                if beta <= alpha:
                    break

            return best

        else:
            best = stand_pat

            for move in tactical_moves:
                child = board.copy()
                Rules.make_move(child, move)

                score = self.search(
                    child,
                    alpha,
                    beta,
                    True,
                    depth + 1
                )

                best = min(best, score)
                beta = min(beta, best)

                if beta <= alpha:
                    break

            return best

    def _tactical_moves(self, board):
        moves = Rules.legal_moves(board)
        tactical = []

        for move in moves:

            # Promotions
            if move.promotion is not None:
                tactical.append(move)
                continue

            # Captures
            target = board.get(
                move.to_rank,
                move.to_file
            )

            if target is not None:
                tactical.append(move)

        return tactical