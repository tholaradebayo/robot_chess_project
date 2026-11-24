import random
from dataclasses import dataclass


@dataclass(frozen=True)
class TTEntry:
    depth: int
    score: float
    flag: str


class ZobristHash:
    """
    Generates a unique 64-bit hash for a chess position.

    The hash includes:
    - piece type
    - piece color
    - piece square
    - side to move
    - castling rights
    - en-passant target
    """

    def __init__(self):
        rng = random.Random(20260910)

        self.piece_keys = {}

        colors = ["white", "black"]
        pieces = [
            "pawn",
            "knight",
            "bishop",
            "rook",
            "queen",
            "king",
        ]

        for color in colors:
            for piece in pieces:
                for rank in range(8):
                    for file in range(8):
                        self.piece_keys[
                            (color, piece, rank, file)
                        ] = rng.getrandbits(64)

        self.turn_key = rng.getrandbits(64)

        # Four possible castling rights:
        # White kingside, White queenside,
        # Black kingside, Black queenside.
        self.castling_keys = {
            "white_kingside": rng.getrandbits(64),
            "white_queenside": rng.getrandbits(64),
            "black_kingside": rng.getrandbits(64),
            "black_queenside": rng.getrandbits(64),
        }

        # One key for every possible en-passant square.
        self.en_passant_keys = {
            (rank, file): rng.getrandbits(64)
            for rank in range(8)
            for file in range(8)
        }

    def hash(self, board):
        value = 0

        # ---------------------------------------------------------
        # 1. Pieces
        # ---------------------------------------------------------
        for rank in range(8):
            for file in range(8):
                piece = board.get(rank, file)

                if piece is not None:
                    value ^= self.piece_keys[
                        (piece.color, piece.kind, rank, file)
                    ]

        # ---------------------------------------------------------
        # 2. Side to move
        # ---------------------------------------------------------
        if board.turn == "black":
            value ^= self.turn_key

        # ---------------------------------------------------------
        # 3. Castling rights
        # ---------------------------------------------------------
        rights = self._castling_rights(board)

        for right in rights:
            value ^= self.castling_keys[right]

        # ---------------------------------------------------------
        # 4. En-passant target
        # ---------------------------------------------------------
        if board.en_passant_target is not None:
            value ^= self.en_passant_keys[board.en_passant_target]

        return value

    def _castling_rights(self, board):
        """
        Determine current castling rights from king/rook positions
        and their has_moved state.

        This avoids depending on a separate castling-rights attribute
        in Board.
        """

        rights = set()

        # -------------------------
        # White
        # -------------------------
        white_king = board.get(7, 4)

        if (
            white_king is not None
            and white_king.color == "white"
            and white_king.kind == "king"
            and not white_king.has_moved
        ):
            white_kingside_rook = board.get(7, 7)

            if (
                white_kingside_rook is not None
                and white_kingside_rook.color == "white"
                and white_kingside_rook.kind == "rook"
                and not white_kingside_rook.has_moved
            ):
                rights.add("white_kingside")

            white_queenside_rook = board.get(7, 0)

            if (
                white_queenside_rook is not None
                and white_queenside_rook.color == "white"
                and white_queenside_rook.kind == "rook"
                and not white_queenside_rook.has_moved
            ):
                rights.add("white_queenside")

        # -------------------------
        # Black
        # -------------------------
        black_king = board.get(0, 4)

        if (
            black_king is not None
            and black_king.color == "black"
            and black_king.kind == "king"
            and not black_king.has_moved
        ):
            black_kingside_rook = board.get(0, 7)

            if (
                black_kingside_rook is not None
                and black_kingside_rook.color == "black"
                and black_kingside_rook.kind == "rook"
                and not black_kingside_rook.has_moved
            ):
                rights.add("black_kingside")

            black_queenside_rook = board.get(0, 0)

            if (
                black_queenside_rook is not None
                and black_queenside_rook.color == "black"
                and black_queenside_rook.kind == "rook"
                and not black_queenside_rook.has_moved
            ):
                rights.add("black_queenside")

        return rights


class TranspositionTable:
    EXACT = "exact"
    LOWERBOUND = "lowerbound"
    UPPERBOUND = "upperbound"

    def __init__(self):
        self.table = {}
        self.hits = 0
        self.stores = 0

    def clear(self):
        self.table.clear()
        self.hits = 0
        self.stores = 0

    def get(self, key):
        entry = self.table.get(key)

        if entry is not None:
            self.hits += 1

        return entry

    def store(self, key, depth, score, flag):
        self.table[key] = TTEntry(
            depth=depth,
            score=score,
            flag=flag,
        )

        self.stores += 1

    def __len__(self):
        return len(self.table)