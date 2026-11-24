from chess.board import Board
from chess.rules import Rules
from chess.search.move_ordering import MoveOrdering


def test_move_ordering_returns_all_moves():
    board = Board()

    moves = Rules.legal_moves(board)
    ordered = MoveOrdering.order_moves(board, moves)

    assert len(ordered) == len(moves)
    assert set(ordered) == set(moves)


def test_move_ordering_promotes_captures():
    board = Board()

    moves = Rules.legal_moves(board)
    ordered = MoveOrdering.order_moves(board, moves)

    assert ordered


def test_move_scores_are_numbers():
    board = Board()

    moves = Rules.legal_moves(board)

    for move in moves:
        score = MoveOrdering.score_move(board, move)
        assert isinstance(score, (int, float))