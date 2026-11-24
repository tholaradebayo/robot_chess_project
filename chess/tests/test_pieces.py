from chess.pieces import (
    Piece,
    Pawn,
    Knight,
    Bishop,
    Rook,
    Queen,
    King,
)


def test_piece_classes():
    assert Pawn("white").kind == "pawn"
    assert Knight("white").kind == "knight"
    assert Bishop("white").kind == "bishop"
    assert Rook("white").kind == "rook"
    assert Queen("white").kind == "queen"
    assert King("white").kind == "king"


def test_piece_colors():
    assert Pawn("white").color == "white"
    assert Pawn("black").color == "black"


def test_piece_symbols():
    assert Pawn("white").symbol() == "♙"
    assert Knight("white").symbol() == "♘"
    assert Bishop("white").symbol() == "♗"
    assert Rook("white").symbol() == "♖"
    assert Queen("white").symbol() == "♕"
    assert King("white").symbol() == "♔"

    assert Pawn("black").symbol() == "♟"
    assert Knight("black").symbol() == "♞"
    assert Bishop("black").symbol() == "♝"
    assert Rook("black").symbol() == "♜"
    assert Queen("black").symbol() == "♛"
    assert King("black").symbol() == "♚"


def test_piece_string():
    assert str(Pawn("white")) == "♙"
    assert str(King("black")) == "♚"


def test_piece_values():
    assert Pawn("white").value == 100
    assert Knight("white").value == 320
    assert Bishop("white").value == 330
    assert Rook("white").value == 500
    assert Queen("white").value == 900
    assert King("white").value == 20000


def test_piece_equality():
    assert Pawn("white") == Pawn("white")
    assert Pawn("white") != Pawn("black")
    assert Pawn("white") != Knight("white")


def test_piece_hash():
    pieces = {
        Pawn("white"),
        Pawn("white"),
        Pawn("black"),
    }

    assert len(pieces) == 2


def test_piece_factory():
    assert Piece("white", "pawn").kind == "pawn"
    assert Piece("black", "queen").kind == "queen"