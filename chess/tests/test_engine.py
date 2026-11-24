import pytest

from chess.board import Board
from chess.engine import Engine
from chess.evaluation import Evaluation
from chess.rules import Rules


def test_engine_returns_legal_move():
    board = Board()
    engine = Engine(depth=2)

    move = engine.choose_move(board)

    assert move in Rules.legal_moves(board)


def test_engine_returns_move_for_black():
    board = Board()

    # e2e4
    legal = Rules.legal_moves(board)
    move = next(
        m for m in legal
        if m.uci == "e2e4"
    )

    Rules.make_move(board, move)

    engine = Engine(depth=2)

    black_move = engine.choose_move(board)

    assert black_move in Rules.legal_moves(board)


def test_engine_depth_validation():
    with pytest.raises(ValueError):
        Engine(depth=0)

    with pytest.raises(ValueError):
        Engine(depth=-1)


def test_engine_nodes_searched():
    board = Board()
    engine = Engine(depth=2)

    engine.choose_move(board)

    assert engine.nodes_searched > 0


def test_evaluate_move():
    board = Board()
    engine = Engine(depth=1)

    legal_moves = Rules.legal_moves(board)

    move = next(
        m for m in legal_moves
        if m.uci == "e2e4"
    )

    score = engine.evaluate_move(board, move)

    assert isinstance(score, (int, float))


def test_engine_move_is_uci_compatible():
    board = Board()
    engine = Engine(depth=1)

    move = engine.choose_move(board)

    assert isinstance(move.uci, str)
    assert len(move.uci) in (4, 5)