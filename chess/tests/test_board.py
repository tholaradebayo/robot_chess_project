from chess.board import Board


def test_initial_board():
    board = Board()

    assert board.get(0, 0).kind == "rook"
    assert board.get(0, 4).kind == "king"
    assert board.get(1, 0).kind == "pawn"

    assert board.get(7, 0).kind == "rook"
    assert board.get(7, 4).kind == "king"
    assert board.get(6, 0).kind == "pawn"


def test_empty_squares():
    board = Board()

    assert board.get(2, 0) is None
    assert board.get(3, 3) is None


def test_square_helpers():
    board = Board()

    assert board.square_name(0, 0) == "a1"
    assert board.square_name(7, 7) == "h8"

    assert board.parse_square("a1") == (0, 0)
    assert board.parse_square("h8") == (7, 7)


def test_set_and_clear():
    board = Board()

    piece = board.get(1, 0)

    board.clear(1, 0)

    assert board.get(1, 0) is None

    board.set(3, 0, piece)

    assert board.get(3, 0) == piece


def test_find_king():
    board = Board()

    white_king = board.find_king("white")
    black_king = board.find_king("black")

    assert white_king == (0, 4)
    assert black_king == (7, 4)


def test_copy_is_independent():
    board = Board()
    copied = board.copy()

    copied.clear(1, 0)

    assert board.get(1, 0) is not None
    assert copied.get(1, 0) is None


def test_initial_fen():
    board = Board()

    fen = board.fen()

    assert fen.startswith(
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
    )

    assert " w " in fen