"""
chess/evaluation.py

Chess position evaluation.

Positive score  -> advantage White
Negative score  -> advantage Black
Zero            -> approximately equal

The evaluation is currently based on:
    1. Material
    2. Piece-square tables
    3. Pawn structure
    4. Bishop pair
    5. Mobility

This will later become the foundation for the
self-learning chess evaluation system.
"""

from .rules import Rules


class Evaluation:

    # ---------------------------------------------------------
    # PIECE VALUES
    # ---------------------------------------------------------

    PIECE_VALUES = {
        "pawn": 100,
        "knight": 320,
        "bishop": 330,
        "rook": 500,
        "queen": 900,
        "king": 20000,
    }

    # ---------------------------------------------------------
    # PIECE-SQUARE TABLES
    # ---------------------------------------------------------
    #
    # Values are from White's perspective.
    #
    # rank 1 -> index 0
    # rank 8 -> index 7
    #
    # Black's values are mirrored vertically.
    # ---------------------------------------------------------

    PAWN_TABLE = [
        [0,   0,   0,   0,   0,   0,   0,   0],
        [50,  50,  50,  50,  50,  50,  50,  50],
        [10,  10,  20,  30,  30,  20,  10,  10],
        [5,   5,  10,  25,  25,  10,   5,   5],
        [0,   0,   0,  20,  20,   0,   0,   0],
        [5,  -5, -10,   0,   0, -10,  -5,   5],
        [5,  10,  10, -20, -20,  10,  10,   5],
        [0,   0,   0,   0,   0,   0,   0,   0],
    ]

    KNIGHT_TABLE = [
        [-50, -40, -30, -30, -30, -30, -40, -50],
        [-40, -20,   0,   0,   0,   0, -20, -40],
        [-30,   0,  10, 15, 15, 10,   0, -30],
        [-30,   5,  15, 20, 20, 15,   5, -30],
        [-30,   0,  15, 20, 20, 15,   0, -30],
        [-30,   5,  10, 15, 15, 10,   5, -30],
        [-40, -20,   0,   5,   5,   0, -20, -40],
        [-50, -40, -30, -30, -30, -30, -40, -50],
    ]

    BISHOP_TABLE = [
        [-20, -10, -10, -10, -10, -10, -10, -20],
        [-10,   0,   0,   0,   0,   0,   0, -10],
        [-10,   0,   5,  10, 10,   5,   0, -10],
        [-10,   5,   5,  10, 10,   5,   5, -10],
        [-10,   0,  10, 10, 10, 10,   0, -10],
        [-10,  10,  10, 10, 10, 10, 10, -10],
        [-10,   5,   0,   0,   0,   0,   5, -10],
        [-20, -10, -10, -10, -10, -10, -10, -20],
    ]

    ROOK_TABLE = [
        [0,   0,   0,   0,   0,   0,   0,   0],
        [5,  10,  10,  10,  10,  10,  10,   5],
        [-5,  0,   0,   0,   0,   0,   0,  -5],
        [-5,  0,   0,   0,   0,   0,   0,  -5],
        [-5,  0,   0,   0,   0,   0,   0,  -5],
        [-5,  0,   0,   0,   0,   0,   0,  -5],
        [-5,  0,   0,   0,   0,   0,   0,  -5],
        [0,   0,   0,   5,   5,   0,   0,   0],
    ]

    QUEEN_TABLE = [
        [-20, -10, -10,  -5,  -5, -10, -10, -20],
        [-10,   0,   0,   0,   0,   0,   0, -10],
        [-10,   0,   5,   5,   5,   5,   0, -10],
        [-5,    0,   5,   5,   5,   5,   0,  -5],
        [0,     0,   5,   5,   5,   5,   0,  -5],
        [-10,   5,   5,   5,   5,   5,   0, -10],
        [-10,   0,   5,   0,   0,   0,   0, -10],
        [-20, -10, -10,  -5,  -5, -10, -10, -20],
    ]

    KING_TABLE = [
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-20, -30, -30, -40, -40, -30, -30, -20],
        [-10, -20, -20, -20, -20, -20, -20, -10],
        [20,  20,   0,   0,   0,   0,  20,  20],
        [20,  30,  10,   0,   0,  10,  30,  20],
    ]

    TABLES = {
        "pawn": PAWN_TABLE,
        "knight": KNIGHT_TABLE,
        "bishop": BISHOP_TABLE,
        "rook": ROOK_TABLE,
        "queen": QUEEN_TABLE,
        "king": KING_TABLE,
    }

    # ---------------------------------------------------------
    # MAIN EVALUATION
    # ---------------------------------------------------------

    @classmethod
    def evaluate(cls, board):
        """
        Evaluate the current position.

        Positive = White advantage.
        Negative = Black advantage.
        """

        score = 0

        score += cls.material_score(board)
        score += cls.position_score(board)
        score += cls.pawn_structure_score(board)
        score += cls.bishop_pair_score(board)
        score += cls.mobility_score(board)

        return score

    # ---------------------------------------------------------
    # MATERIAL
    # ---------------------------------------------------------

    @classmethod
    def material_score(cls, board):
        score = 0

        for _, _, piece in board.pieces():

            value = cls.PIECE_VALUES[piece.kind]

            if piece.color == "white":
                score += value
            else:
                score -= value

        return score

    # ---------------------------------------------------------
    # POSITION
    # ---------------------------------------------------------

    @classmethod
    def position_score(cls, board):
        score = 0

        for rank, file, piece in board.pieces():

            table = cls.TABLES[piece.kind]

            if piece.color == "white":
                table_rank = rank
                value = table[table_rank][file]

                score += value

            else:
                table_rank = 7 - rank
                value = table[table_rank][file]

                score -= value

        return score

    # ---------------------------------------------------------
    # PAWN STRUCTURE
    # ---------------------------------------------------------

    @classmethod
    def pawn_structure_score(cls, board):
        score = 0

        for color in ("white", "black"):

            pawn_files = {}

            for rank, file, piece in board.pieces(color):

                if piece.kind != "pawn":
                    continue

                pawn_files[file] = (
                    pawn_files.get(file, 0) + 1
                )

            # Doubled pawns.
            for count in pawn_files.values():

                if count > 1:

                    penalty = 20 * (count - 1)

                    if color == "white":
                        score -= penalty
                    else:
                        score += penalty

        return score

    # ---------------------------------------------------------
    # BISHOP PAIR
    # ---------------------------------------------------------

    @classmethod
    def bishop_pair_score(cls, board):
        score = 0

        for color in ("white", "black"):

            bishops = board.count_piece(
                color,
                "bishop"
            )

            if bishops >= 2:

                if color == "white":
                    score += 30
                else:
                    score -= 30

        return score

    # ---------------------------------------------------------
    # MOBILITY
    # ---------------------------------------------------------

    @classmethod
    def mobility_score(cls, board):
        """
        Give a small bonus to the side with more legal moves.

        This is deliberately kept small because mobility should
        not overpower material.
        """

        try:
            white_moves = len(
                Rules.legal_moves(
                    board,
                    "white"
                )
            )

            black_moves = len(
                Rules.legal_moves(
                    board,
                    "black"
                )
            )

            return (white_moves - black_moves) * 2

        except ValueError:
            return 0

    # ---------------------------------------------------------
    # FINAL POSITION SCORE
    # ---------------------------------------------------------

    @classmethod
    def evaluate_for_side(cls, board, color):
        """
        Return evaluation from a specific side's perspective.

        Example:

            evaluate_for_side(board, "white")

        Positive means good for White.

        For Black, the score is reversed.
        """

        score = cls.evaluate(board)

        if color == "white":
            return score

        return -score