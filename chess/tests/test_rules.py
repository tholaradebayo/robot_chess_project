from chess.board import Board
from chess.game import Game
from chess.move import Move
from chess.pieces import Pawn, Knight, Bishop, Rook, Queen, King
from chess.rules import Rules


def moves_uci(board):
    return {move.uci for move in Rules.legal_moves(board)}


def empty_board():
    b = Board()
    b.board = [[None for _ in range(8)] for _ in range(8)]
    b.castling_rights = {k: False for k in b.castling_rights}
    b.en_passant_target = None
    return b


def test_initial_legal_move_count():
    b = Board()
    assert len(Rules.legal_moves(b)) == 20


def test_pawn_and_knight_moves():
    b = Board()
    initial = moves_uci(b)
    assert 'e2e4' in initial and 'e2e3' in initial
    assert 'g1f3' in initial and 'g1h3' in initial


def test_sliding_piece_blocking_and_capture():
    b = empty_board()
    b.set(0, 0, Rook('white'))
    b.set(0, 3, Pawn('white'))
    b.set(3, 0, Pawn('black'))
    b.set(7, 7, King('white'))
    b.set(5, 6, King('black'))
    assert 'a1a4' in moves_uci(b)
    assert 'a1a5' not in moves_uci(b)
    assert 'a1d1' not in moves_uci(b)
    assert 'a1a4' in moves_uci(b)


def test_bishop_knight_queen_moves():
    b = empty_board()
    b.set(3, 3, Bishop('white'))
    b.set(3, 5, Knight('white'))
    b.set(4, 1, Queen('white'))
    b.set(0, 4, King('white'))
    b.set(7, 4, King('black'))
    bishop = {m.uci for m in Rules.legal_moves(b) if m.from_square == 'd4'}
    assert 'd4e5' in bishop and 'd4h8' in bishop
    knight = {m.uci for m in Rules.legal_moves(b) if m.from_square == 'f4'}
    assert 'f4d5' in knight and 'f4h5' in knight


def test_make_move_updates_turn_ep_and_clocks():
    b = Board()
    move = next(m for m in Rules.legal_moves(b) if m.uci == 'e2e4')
    captured = Rules.make_move(b, move)
    assert captured is None
    assert isinstance(b.get(3, 4), Pawn)
    assert b.get(1, 4) is None
    assert b.turn == 'black'
    assert b.en_passant_target == (2, 4)
    assert b.halfmove_clock == 0
    assert b.fullmove_number == 1


def test_capture_and_halfmove_clock():
    b = empty_board()
    b.set(0, 4, King('white')); b.set(7, 4, King('black'))
    b.set(3, 3, Rook('white')); b.set(3, 6, Knight('black'))
    b.turn = 'white'
    move = next(m for m in Rules.legal_moves(b) if m.uci == 'd4g4')
    captured = Rules.make_move(b, move)
    assert isinstance(captured, Knight)
    assert isinstance(b.get(3, 6), Rook)
    assert b.halfmove_clock == 0


def test_castling_kingside():
    b = Board()
    for square in ('f1','g1','f8','g8','f2','f3'):
        r,f = b.parse_square(square); b.clear(r,f)
    white_moves = moves_uci(b)
    assert 'e1g1' in white_moves
    move = next(m for m in Rules.legal_moves(b) if m.uci == 'e1g1')
    Rules.make_move(b, move)
    assert isinstance(b.get(0, 6), King)
    assert isinstance(b.get(0, 5), Rook)
    assert not b.castling_rights['white_kingside']


def test_castling_not_through_check():
    b = Board()
    for square in ('f1','g1','f8','g8','f2','f3'):
        r,f = b.parse_square(square); b.clear(r,f)
    b.set(3, 5, Rook('black'))
    assert 'e1g1' not in moves_uci(b)


def test_en_passant():
    g = Game()
    for uci in ('e2e4','a7a6','e4e5','d7d5'):
        g.play_uci(uci)
    assert 'e5d6' in moves_uci(g.board)
    g.play_uci('e5d6')
    assert isinstance(g.board.get(5, 3), Pawn)
    assert g.board.get(4, 3) is None


def test_promotion_generates_four_choices_and_executes():
    b = empty_board()
    b.set(6, 0, Pawn('white')); b.set(0, 4, King('white')); b.set(7, 4, King('black'))
    b.turn = 'white'
    choices = {m.uci for m in Rules.legal_moves(b) if m.from_square == 'a7'}
    assert choices == {'a7a8q','a7a8r','a7a8b','a7a8n'}
    g = Game(); g.board = b
    g.play_uci('a7a8q')
    assert isinstance(g.board.get(7, 0), Queen)


def test_check_and_king_safety():
    b = empty_board()
    b.set(7, 4, King('white')); b.set(0, 4, King('black')); b.set(5, 4, Rook('black'))
    b.turn = 'white'
    assert Rules.in_check(b, 'white')
    assert Move(7,4,6,4) not in Rules.legal_moves(b)


def test_fools_mate():
    g = Game()
    for uci in ('f2f3','e7e5','g2g4','d8h4'):
        g.play_uci(uci)
    assert 'checkmate' in Rules.status(g.board)
    assert g.game_over


def test_stalemate():
    b = empty_board()
    b.set(7, 7, King('white'))
    b.set(5, 5, King('black'))
    b.set(5, 6, Queen('black'))
    b.turn = 'white'
    assert Rules.is_stalemate(b, 'white')
    assert Rules.status(b) == 'stalemate: draw'


def test_king_cannot_be_captured_as_a_move():
    b = empty_board()
    b.set(0, 0, Rook('white')); b.set(0, 7, King('white')); b.set(7, 4, King('black'))
    assert 'a1e1' in moves_uci(b)
    assert 'a1e8' not in moves_uci(b)
    b.set(7, 0, King('black'))
    assert 'a1a8' not in moves_uci(b)
