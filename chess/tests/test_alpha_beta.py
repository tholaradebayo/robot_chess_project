from chess.board import Board
from chess.search.alpha_beta import AlphaBeta


def test_alpha_beta():
    board = Board()

    engine = AlphaBeta()
    move = engine.search(board, 2)

    assert move is not None
    assert engine.nodes_searched > 0

    print("Selected:", move.uci)
    print("Nodes:", engine.nodes_searched)