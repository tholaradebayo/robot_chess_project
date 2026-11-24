import pytest

from chess.move import (
    Move,
    parse_square,
    square_name,
    parse_uci,
)


def test_square_name():
    assert square_name(0, 0) == "a1"
    assert square_name(0, 7) == "h1"
    assert square_name(7, 0) == "a8"
    assert square_name(7, 7) == "h8"


def test_parse_square():
    assert parse_square("a1") == (0, 0)
    assert parse_square("h1") == (0, 7)
    assert parse_square("a8") == (7, 0)
    assert parse_square("h8") == (7, 7)


def test_parse_square_uppercase():
    assert parse_square("A1") == (0, 0)
    assert parse_square("H8") == (7, 7)


def test_invalid_square_length():
    with pytest.raises(ValueError):
        parse_square("a")

    with pytest.raises(ValueError):
        parse_square("a11")

    with pytest.raises(ValueError):
        parse_square("abc")


def test_invalid_square_file():
    with pytest.raises(ValueError):
        parse_square("i1")


def test_invalid_square_rank():
    with pytest.raises(ValueError):
        parse_square("a9")


def test_parse_square_none():
    with pytest.raises(TypeError):
        parse_square(None)


def test_square_name_invalid_coordinates():
    with pytest.raises(ValueError):
        square_name(-1, 0)

    with pytest.raises(ValueError):
        square_name(8, 0)

    with pytest.raises(ValueError):
        square_name(0, -1)

    with pytest.raises(ValueError):
        square_name(0, 8)


def test_move_uci():
    move = Move(
        from_rank=1,
        from_file=4,
        to_rank=3,
        to_file=4,
    )

    assert move.from_square == "e2"
    assert move.to_square == "e4"
    assert move.uci == "e2e4"


def test_move_string():
    move = Move(
        from_rank=1,
        from_file=4,
        to_rank=3,
        to_file=4,
    )

    assert str(move) == "e2e4"


def test_parse_uci():
    move = parse_uci("e2e4")

    assert move.from_square == "e2"
    assert move.to_square == "e4"
    assert move.uci == "e2e4"


def test_parse_uci_uppercase():
    move = parse_uci("E2E4")

    assert move.uci == "e2e4"


def test_promotion_queen():
    move = parse_uci("a7a8q")

    assert move.promotion == "queen"
    assert move.uci == "a7a8q"


def test_promotion_rook():
    move = parse_uci("a7a8r")

    assert move.promotion == "rook"
    assert move.uci == "a7a8r"


def test_promotion_bishop():
    move = parse_uci("a7a8b")

    assert move.promotion == "bishop"
    assert move.uci == "a7a8b"


def test_promotion_knight():
    move = parse_uci("a7a8n")

    assert move.promotion == "knight"
    assert move.uci == "a7a8n"


def test_move_flags():
    move = Move(
        from_rank=0,
        from_file=4,
        to_rank=0,
        to_file=6,
        is_castling=True,
    )

    assert move.is_castling
    assert not move.is_en_passant


def test_en_passant_flag():
    move = Move(
        from_rank=4,
        from_file=4,
        to_rank=5,
        to_file=3,
        is_en_passant=True,
    )

    assert move.is_en_passant
    assert not move.is_castling


def test_invalid_coordinates():
    with pytest.raises(ValueError):
        Move(-1, 0, 0, 0)

    with pytest.raises(ValueError):
        Move(0, 8, 0, 0)

    with pytest.raises(ValueError):
        Move(0, 0, 8, 0)

    with pytest.raises(ValueError):
        Move(0, 0, 0, 8)


def test_invalid_promotion():
    with pytest.raises(ValueError):
        Move(
            6,
            0,
            7,
            0,
            promotion="king",
        )


def test_invalid_uci():
    with pytest.raises(ValueError):
        parse_uci("e2")

    with pytest.raises(ValueError):
        parse_uci("e2e4x")

    with pytest.raises(ValueError):
        parse_uci("e2e9")

    with pytest.raises(ValueError):
        parse_uci("e2e4k")