from chess.board import Board
from chess.search.quiescence import Quiescence


def test_quiescence_initial_position():
    board = Board()

    search = Quiescence()

    score = search.search(
        board,
        float("-inf"),
        float("inf"),
        True
    )

    assert isinstance(score, (int, float))
    assert search.nodes_searched > 0


def test_quiescence_has_depth_limit():
    board = Board()

    search = Quiescence(max_depth=2)

    score = search.search(
        board,
        float("-inf"),
        float("inf"),
        True
    )

    assert isinstance(score, (int, float))
    assert search.nodes_searched > 0