from ..evaluation import Evaluation
from ..rules import Rules


class MoveOrdering:

    @staticmethod
    def score_move(board, move):
        score = 0

        # 1. Promotions
        if move.promotion is not None:
            score += 10000

        # 2. Captures
        target = board.get(move.to_rank, move.to_file)

        if target is not None:
            attacker = board.get(move.from_rank, move.from_file)

            if attacker is not None:
                score += 1000 + target.value - attacker.value

        # 3. Checks
        child = board.copy()
        Rules.make_move(child, move)

        if Rules.in_check(child, child.turn):
            score += 500

        return score

    @classmethod
    def order_moves(cls, board, moves):
        return sorted(
            moves,
            key=lambda move: cls.score_move(board, move),
            reverse=True
        )