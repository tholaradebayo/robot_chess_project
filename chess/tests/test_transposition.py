from chess.board import Board
from chess.search.transposition import (
    ZobristHash,
    TranspositionTable,
)


def test_zobrist_hash_is_consistent():
    board = Board()
    hasher = ZobristHash()

    key1 = hasher.hash(board)
    key2 = hasher.hash(board)

    assert key1 == key2


def test_different_turn_has_different_hash():
    board = Board()
    hasher = ZobristHash()

    white_key = hasher.hash(board)

    board.turn = "black"

    black_key = hasher.hash(board)

    assert white_key != black_key


def test_different_en_passant_state_has_different_hash():
    board = Board()
    hasher = ZobristHash()

    normal_key = hasher.hash(board)

    board.en_passant_target = (2, 4)

    ep_key = hasher.hash(board)

    assert normal_key != ep_key


def test_different_castling_rights_have_different_hash():
    board = Board()
    hasher = ZobristHash()

    initial_key = hasher.hash(board)

    # Simulate the white king having moved.
    white_king = board.get(7, 4)
    white_king.has_moved = True

    changed_key = hasher.hash(board)

    assert initial_key != changed_key


def test_different_rook_castling_rights_have_different_hash():
    board = Board()
    hasher = ZobristHash()

    initial_key = hasher.hash(board)

    # Simulate the h1 rook having moved.
    rook = board.get(7, 7)
    rook.has_moved = True

    changed_key = hasher.hash(board)

    assert initial_key != changed_key


def test_transposition_table_store_and_get():
    table = TranspositionTable()

    table.store(
        key=12345,
        depth=3,
        score=150,
        flag=TranspositionTable.EXACT,
    )

    entry = table.get(12345)

    assert entry is not None
    assert entry.depth == 3
    assert entry.score == 150
    assert entry.flag == TranspositionTable.EXACT


def test_transposition_table_bounds():
    table = TranspositionTable()

    table.store(
        key=1,
        depth=2,
        score=100,
        flag=TranspositionTable.LOWERBOUND,
    )

    table.store(
        key=2,
        depth=2,
        score=-100,
        flag=TranspositionTable.UPPERBOUND,
    )

    assert table.get(1).flag == TranspositionTable.LOWERBOUND
    assert table.get(2).flag == TranspositionTable.UPPERBOUND


def test_transposition_table_miss():
    table = TranspositionTable()

    assert table.get(99999) is None


def test_transposition_table_clear():
    table = TranspositionTable()

    table.store(
        key=12345,
        depth=3,
        score=150,
        flag=TranspositionTable.EXACT,
    )

    table.clear()

    assert table.get(12345) is None
    assert len(table) == 0