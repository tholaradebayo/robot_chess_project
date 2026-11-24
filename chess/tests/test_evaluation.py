from chess.board import Board
from chess.evaluation import Evaluation
from chess.pieces import Queen


def test_initial_evaluation():
    board = Board()

    score = Evaluation.evaluate(board)

    assert abs(score) < 1e-6


def test_white_material_advantage():
    board = Board()

    # Remove one white pawn and one black pawn
    # so that we have an empty square for the test queen.
    board.clear(1, 0)
    board.clear(6, 0)

    board.set(3, 3, Queen("white"))

    score = Evaluation.evaluate(board)

    assert score > 0


def test_evaluation_side_sign():
    board = Board()

    white_score = Evaluation.evaluate_for_side(
        board,
        "white",
    )

    black_score = Evaluation.evaluate_for_side(
        board,
        "black",
    )

    assert white_score == -black_score


def test_bishop_pair_evaluation():
    board = Board()

    score = Evaluation.evaluate(board)

    assert isinstance(score, (int, float))