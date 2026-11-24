from .move import Move
from .pieces import (
    Pawn,
    Knight,
    Bishop,
    Rook,
    Queen,
    King,
)


KNIGHT_OFFSETS = [
    (-2, -1),
    (-2, 1),
    (-1, -2),
    (-1, 2),
    (1, -2),
    (1, 2),
    (2, -1),
    (2, 1),
]

KING_OFFSETS = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
]

BISHOP_DIRECTIONS = [
    (-1, -1),
    (-1, 1),
    (1, -1),
    (1, 1),
]

ROOK_DIRECTIONS = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
]

QUEEN_DIRECTIONS = (
    BISHOP_DIRECTIONS +
    ROOK_DIRECTIONS
)


class Rules:

    @staticmethod
    def inside(rank, file):
        return 0 <= rank < 8 and 0 <= file < 8

    @staticmethod
    def opponent(color):
        return (
            "black"
            if color == "white"
            else "white"
        )

    # ---------------------------------------------------------
    # ATTACK DETECTION
    # ---------------------------------------------------------

    @staticmethod
    def is_square_attacked(board, rank, file, by_color):
        for r, f, piece in board.pieces(by_color):

            dr = rank - r
            df = file - f

            # Pawn
            if piece.kind == "pawn":
                direction = (
                    1 if by_color == "white"
                    else -1
                )

                if dr == direction and abs(df) == 1:
                    return True

            # Knight
            elif piece.kind == "knight":
                if (dr, df) in KNIGHT_OFFSETS:
                    return True

            # King
            elif piece.kind == "king":
                if max(abs(dr), abs(df)) == 1:
                    return True

            # Bishop / Rook / Queen
            elif piece.kind in (
                "bishop",
                "rook",
                "queen",
            ):
                if Rules._sliding_attack(
                    board,
                    r,
                    f,
                    rank,
                    file,
                    piece.kind,
                ):
                    return True

        return False

    @staticmethod
    def _sliding_attack(
        board,
        start_rank,
        start_file,
        target_rank,
        target_file,
        kind,
    ):
        dr = target_rank - start_rank
        df = target_file - start_file

        if kind in ("bishop", "queen"):
            if abs(dr) == abs(df) and dr != 0:
                step_r = 1 if dr > 0 else -1
                step_f = 1 if df > 0 else -1

                return Rules._path_clear(
                    board,
                    start_rank,
                    start_file,
                    target_rank,
                    target_file,
                    step_r,
                    step_f,
                )

        if kind in ("rook", "queen"):
            if (
                (dr == 0 and df != 0)
                or
                (df == 0 and dr != 0)
            ):
                step_r = 0 if dr == 0 else (
                    1 if dr > 0 else -1
                )

                step_f = 0 if df == 0 else (
                    1 if df > 0 else -1
                )

                return Rules._path_clear(
                    board,
                    start_rank,
                    start_file,
                    target_rank,
                    target_file,
                    step_r,
                    step_f,
                )

        return False

    @staticmethod
    def _path_clear(
        board,
        start_rank,
        start_file,
        target_rank,
        target_file,
        step_r,
        step_f,
    ):
        r = start_rank + step_r
        f = start_file + step_f

        while (r, f) != (target_rank, target_file):
            if board.get(r, f) is not None:
                return False

            r += step_r
            f += step_f

        return True

    # ---------------------------------------------------------
    # CHECK
    # ---------------------------------------------------------

    @staticmethod
    def in_check(board, color):
        king_rank, king_file = board.find_king(color)

        return Rules.is_square_attacked(
            board,
            king_rank,
            king_file,
            Rules.opponent(color),
        )

    # ---------------------------------------------------------
    # PSEUDO-LEGAL MOVES
    # ---------------------------------------------------------

    @staticmethod
    def pseudo_legal_moves(board, color=None):
        if color is None:
            color = board.turn

        moves = []

        for rank, file, piece in board.pieces(color):

            if piece.kind == "pawn":
                moves.extend(
                    Rules._pawn_moves(
                        board,
                        rank,
                        file,
                        piece,
                    )
                )

            elif piece.kind == "knight":
                moves.extend(
                    Rules._knight_moves(
                        board,
                        rank,
                        file,
                        piece,
                    )
                )

            elif piece.kind == "bishop":
                moves.extend(
                    Rules._sliding_moves(
                        board,
                        rank,
                        file,
                        piece,
                        BISHOP_DIRECTIONS,
                    )
                )

            elif piece.kind == "rook":
                moves.extend(
                    Rules._sliding_moves(
                        board,
                        rank,
                        file,
                        piece,
                        ROOK_DIRECTIONS,
                    )
                )

            elif piece.kind == "queen":
                moves.extend(
                    Rules._sliding_moves(
                        board,
                        rank,
                        file,
                        piece,
                        QUEEN_DIRECTIONS,
                    )
                )

            elif piece.kind == "king":
                moves.extend(
                    Rules._king_moves(
                        board,
                        rank,
                        file,
                        piece,
                    )
                )

        return moves

    @staticmethod
    def _pawn_moves(board, rank, file, piece):
        moves = []

        direction = (
            1 if piece.color == "white"
            else -1
        )

        start_rank = (
            1 if piece.color == "white"
            else 6
        )

        promotion_rank = (
            7 if piece.color == "white"
            else 0
        )

        # One square forward.
        new_rank = rank + direction

        if Rules.inside(new_rank, file):
            if board.get(new_rank, file) is None:

                if new_rank == promotion_rank:
                    for promotion in (
                        "queen",
                        "rook",
                        "bishop",
                        "knight",
                    ):
                        moves.append(
                            Move(
                                rank,
                                file,
                                new_rank,
                                file,
                                promotion=promotion,
                            )
                        )
                else:
                    moves.append(
                        Move(
                            rank,
                            file,
                            new_rank,
                            file,
                        )
                    )

                # Two squares forward.
                if rank == start_rank:
                    two_rank = rank + 2 * direction

                    if board.get(two_rank, file) is None:
                        moves.append(
                            Move(
                                rank,
                                file,
                                two_rank,
                                file,
                            )
                        )

        # Captures.
        for df in (-1, 1):
            new_file = file + df
            new_rank = rank + direction

            if not Rules.inside(new_rank, new_file):
                continue

            target = board.get(
                new_rank,
                new_file,
            )

            if (
                target is not None
                and target.color != piece.color
                and target.kind != "king"
            ):
                if new_rank == promotion_rank:
                    for promotion in (
                        "queen",
                        "rook",
                        "bishop",
                        "knight",
                    ):
                        moves.append(
                            Move(
                                rank,
                                file,
                                new_rank,
                                new_file,
                                promotion=promotion,
                            )
                        )
                else:
                    moves.append(
                        Move(
                            rank,
                            file,
                            new_rank,
                            new_file,
                        )
                    )

            # En passant.
            if (
                board.en_passant_target
                == (new_rank, new_file)
            ):
                moves.append(
                    Move(
                        rank,
                        file,
                        new_rank,
                        new_file,
                        is_en_passant=True,
                    )
                )

        return moves

    @staticmethod
    def _knight_moves(
        board,
        rank,
        file,
        piece,
    ):
        moves = []

        for dr, df in KNIGHT_OFFSETS:
            r = rank + dr
            f = file + df

            if not Rules.inside(r, f):
                continue

            target = board.get(r, f)

            if target is None:
                moves.append(
                    Move(rank, file, r, f)
                )

            elif (
                target.color != piece.color
                and target.kind != "king"
            ):
                moves.append(
                    Move(rank, file, r, f)
                )

        return moves

    @staticmethod
    def _sliding_moves(
        board,
        rank,
        file,
        piece,
        directions,
    ):
        moves = []

        for dr, df in directions:
            r = rank + dr
            f = file + df

            while Rules.inside(r, f):
                target = board.get(r, f)

                if target is None:
                    moves.append(
                        Move(rank, file, r, f)
                    )

                else:
                    if (
                        target.color != piece.color
                        and target.kind != "king"
                    ):
                        moves.append(
                            Move(rank, file, r, f)
                        )

                    break

                r += dr
                f += df

        return moves

    @staticmethod
    def _king_moves(
        board,
        rank,
        file,
        piece,
    ):
        moves = []

        for dr, df in KING_OFFSETS:
            r = rank + dr
            f = file + df

            if not Rules.inside(r, f):
                continue

            target = board.get(r, f)

            if target is None:
                moves.append(
                    Move(rank, file, r, f)
                )

            elif (
                target.color != piece.color
                and target.kind != "king"
            ):
                moves.append(
                    Move(rank, file, r, f)
                )

        # Castling.
        moves.extend(
            Rules._castling_moves(
                board,
                rank,
                file,
                piece,
            )
        )

        return moves

    # ---------------------------------------------------------
    # CASTLING
    # ---------------------------------------------------------

    @staticmethod
    def _castling_moves(
        board,
        rank,
        file,
        piece,
    ):
        moves = []

        if piece.kind != "king":
            return moves

        if Rules.in_check(board, piece.color):
            return moves

        opponent = Rules.opponent(piece.color)

        # White kingside.
        if piece.color == "white" and rank == 0 and file == 4:
            if board.castling_rights["white_kingside"]:
                rook = board.get(0, 7)

                if (
                    isinstance(rook, Rook)
                    and rook.color == "white"
                    and board.get(0, 5) is None
                    and board.get(0, 6) is None
                    and not Rules.is_square_attacked(
                        board, 0, 5, opponent
                    )
                    and not Rules.is_square_attacked(
                        board, 0, 6, opponent
                    )
                ):
                    moves.append(
                        Move(
                            0, 4, 0, 6,
                            is_castling=True
                        )
                    )

            if board.castling_rights["white_queenside"]:
                rook = board.get(0, 0)

                if (
                    isinstance(rook, Rook)
                    and rook.color == "white"
                    and board.get(0, 1) is None
                    and board.get(0, 2) is None
                    and board.get(0, 3) is None
                    and not Rules.is_square_attacked(
                        board, 0, 3, opponent
                    )
                    and not Rules.is_square_attacked(
                        board, 0, 2, opponent
                    )
                ):
                    moves.append(
                        Move(
                            0, 4, 0, 2,
                            is_castling=True
                        )
                    )

        # Black kingside.
        if piece.color == "black" and rank == 7 and file == 4:
            if board.castling_rights["black_kingside"]:
                rook = board.get(7, 7)

                if (
                    isinstance(rook, Rook)
                    and rook.color == "black"
                    and board.get(7, 5) is None
                    and board.get(7, 6) is None
                    and not Rules.is_square_attacked(
                        board, 7, 5, opponent
                    )
                    and not Rules.is_square_attacked(
                        board, 7, 6, opponent
                    )
                ):
                    moves.append(
                        Move(
                            7, 4, 7, 6,
                            is_castling=True
                        )
                    )

            if board.castling_rights["black_queenside"]:
                rook = board.get(7, 0)

                if (
                    isinstance(rook, Rook)
                    and rook.color == "black"
                    and board.get(7, 1) is None
                    and board.get(7, 2) is None
                    and board.get(7, 3) is None
                    and not Rules.is_square_attacked(
                        board, 7, 3, opponent
                    )
                    and not Rules.is_square_attacked(
                        board, 7, 2, opponent
                    )
                ):
                    moves.append(
                        Move(
                            7, 4, 7, 2,
                            is_castling=True
                        )
                    )

        return moves

    # ---------------------------------------------------------
    # LEGAL MOVES
    # ---------------------------------------------------------

    @staticmethod
    def legal_moves(board, color=None):
        if color is None:
            color = board.turn

        legal = []

        for move in Rules.pseudo_legal_moves(
            board,
            color,
        ):
            test_board = board.copy()

            Rules.make_move(
                test_board,
                move,
                switch_turn=False,
            )

            if not Rules.in_check(
                test_board,
                color,
            ):
                legal.append(move)

        return legal

    # ---------------------------------------------------------
    # MAKE MOVE
    # ---------------------------------------------------------

    @staticmethod
    def make_move(
        board,
        move,
        switch_turn=True,
    ):
        piece = board.get(
            move.from_rank,
            move.from_file,
        )

        if piece is None:
            raise ValueError(
                "There is no piece on the starting square."
            )

        captured = board.get(
            move.to_rank,
            move.to_file,
        )

        # En passant capture.
        if move.is_en_passant:
            capture_rank = (
                move.to_rank - 1
                if piece.color == "white"
                else move.to_rank + 1
            )

            captured = board.clear(
                capture_rank,
                move.to_file,
            )

        # Move piece.
        board.clear(
            move.from_rank,
            move.from_file,
        )

        # Promotion.
        if move.promotion:
            classes = {
                "queen": Queen,
                "rook": Rook,
                "bishop": Bishop,
                "knight": Knight,
            }

            piece = classes[move.promotion](
                piece.color
            )

        board.set(
            move.to_rank,
            move.to_file,
            piece,
        )

        # Castling rook movement.
        if move.is_castling:
            if move.to_file == 6:
                rook = board.clear(
                    move.to_rank,
                    7,
                )

                board.set(
                    move.to_rank,
                    5,
                    rook,
                )

            elif move.to_file == 2:
                rook = board.clear(
                    move.to_rank,
                    0,
                )

                board.set(
                    move.to_rank,
                    3,
                    rook,
                )

        # Update castling rights.
        Rules._update_castling_rights(
            board,
            piece,
            move,
            captured,
        )

        # En passant target.
        board.en_passant_target = None

        if (
            piece.kind == "pawn"
            and abs(
                move.to_rank - move.from_rank
            ) == 2
        ):
            board.en_passant_target = (
                (
                    move.from_rank
                    + move.to_rank
                ) // 2,
                move.from_file,
            )

        # Halfmove clock.
        if piece.kind == "pawn" or captured is not None:
            board.halfmove_clock = 0
        else:
            board.halfmove_clock += 1

        # Fullmove number.
        if piece.color == "black":
            board.fullmove_number += 1

        if switch_turn:
            board.switch_turn()

        return captured

    @staticmethod
    def _update_castling_rights(
        board,
        piece,
        move,
        captured,
    ):
        color = piece.color

        if piece.kind == "king":
            board.castling_rights[
                f"{color}_kingside"
            ] = False

            board.castling_rights[
                f"{color}_queenside"
            ] = False

        if piece.kind == "rook":
            if color == "white":
                if move.from_rank == 0:
                    if move.from_file == 0:
                        board.castling_rights[
                            "white_queenside"
                        ] = False

                    elif move.from_file == 7:
                        board.castling_rights[
                            "white_kingside"
                        ] = False

            else:
                if move.from_rank == 7:
                    if move.from_file == 0:
                        board.castling_rights[
                            "black_queenside"
                        ] = False

                    elif move.from_file == 7:
                        board.castling_rights[
                            "black_kingside"
                        ] = False

        # Capturing a rook removes its castling rights.
        if captured is not None and captured.kind == "rook":
            if captured.color == "white":
                if move.to_rank == 0:
                    if move.to_file == 0:
                        board.castling_rights[
                            "white_queenside"
                        ] = False

                    elif move.to_file == 7:
                        board.castling_rights[
                            "white_kingside"
                        ] = False

            else:
                if move.to_rank == 7:
                    if move.to_file == 0:
                        board.castling_rights[
                            "black_queenside"
                        ] = False

                    elif move.to_file == 7:
                        board.castling_rights[
                            "black_kingside"
                        ] = False

    # ---------------------------------------------------------
    # GAME STATUS
    # ---------------------------------------------------------

    @staticmethod
    def is_checkmate(board, color=None):
        if color is None:
            color = board.turn

        return (
            Rules.in_check(board, color)
            and not Rules.legal_moves(board, color)
        )

    @staticmethod
    def is_stalemate(board, color=None):
        if color is None:
            color = board.turn

        return (
            not Rules.in_check(board, color)
            and not Rules.legal_moves(board, color)
        )

    @staticmethod
    def status(board):
        color = board.turn

        if Rules.is_checkmate(board, color):
            winner = Rules.opponent(color)

            return f"checkmate: {winner} wins"

        if Rules.is_stalemate(board, color):
            return "stalemate: draw"

        if Rules.in_check(board, color):
            return f"{color} is in check"

        return f"{color} to move"