from .pieces import (
    Pawn,
    Knight,
    Bishop,
    Rook,
    Queen,
    King,
)


class Board:
    FILES = "abcdefgh"

    def __init__(self):
        self.board = [
            [None for _ in range(8)]
            for _ in range(8)
        ]

        self.turn = "white"

        self.castling_rights = {
            "white_kingside": True,
            "white_queenside": True,
            "black_kingside": True,
            "black_queenside": True,
        }

        self.en_passant_target = None

        self.halfmove_clock = 0
        self.fullmove_number = 1

        self._setup_starting_position()

    def _setup_starting_position(self):
        back_rank = [
            Rook,
            Knight,
            Bishop,
            Queen,
            King,
            Bishop,
            Knight,
            Rook,
        ]

        for file, piece_class in enumerate(back_rank):
            self.board[0][file] = piece_class("white")
            self.board[7][file] = piece_class("black")

        for file in range(8):
            self.board[1][file] = Pawn("white")
            self.board[6][file] = Pawn("black")

    def get(self, rank, file):
        self._validate(rank, file)
        return self.board[rank][file]

    def set(self, rank, file, piece):
        self._validate(rank, file)
        self.board[rank][file] = piece

    def clear(self, rank, file):
        self._validate(rank, file)

        piece = self.board[rank][file]
        self.board[rank][file] = None

        return piece

    @staticmethod
    def _validate(rank, file):
        if not (0 <= rank < 8):
            raise ValueError("Rank must be between 0 and 7.")

        if not (0 <= file < 8):
            raise ValueError("File must be between 0 and 7.")

    def copy(self):
        new = Board.__new__(Board)

        new.board = [
            row.copy()
            for row in self.board
        ]

        new.turn = self.turn
        new.castling_rights = self.castling_rights.copy()
        new.en_passant_target = self.en_passant_target
        new.halfmove_clock = self.halfmove_clock
        new.fullmove_number = self.fullmove_number

        return new

    def find_king(self, color):
        for rank in range(8):
            for file in range(8):
                piece = self.board[rank][file]

                if (
                    piece is not None
                    and piece.color == color
                    and piece.kind == "king"
                ):
                    return rank, file

        raise ValueError(f"{color} king not found.")

    def display(self):
        print()

        for rank in range(7, -1, -1):
            row = []

            for file in range(8):
                piece = self.board[rank][file]

                if piece is None:
                    row.append(".")
                else:
                    row.append(piece.symbol())

            print(f"{rank + 1} " + " ".join(row))

        print("  a b c d e f g h")
        print(f"  Turn: {self.turn}")
        print()

    def square_name(self, rank, file):
        self._validate(rank, file)
        return f"{self.FILES[file]}{rank + 1}"

    def parse_square(self, square):
        square = square.lower().strip()

        if len(square) != 2:
            raise ValueError("Invalid square.")

        file = self.FILES.index(square[0])
        rank = int(square[1]) - 1

        self._validate(rank, file)

        return rank, file

    def pieces(self, color=None):
        result = []

        for rank in range(8):
            for file in range(8):
                piece = self.board[rank][file]

                if piece is None:
                    continue

                if color is None or piece.color == color:
                    result.append(
                        (rank, file, piece)
                    )

        return result

    def count_piece(self, color, kind):
        return sum(
            1
            for _, _, piece in self.pieces(color)
            if piece.kind == kind
        )

    def switch_turn(self):
        self.turn = (
            "black"
            if self.turn == "white"
            else "white"
        )

    def fen(self):
        rows = []

        for rank in range(7, -1, -1):
            row = ""
            empty = 0

            for file in range(8):
                piece = self.board[rank][file]

                if piece is None:
                    empty += 1
                    continue

                if empty:
                    row += str(empty)
                    empty = 0

                symbols = {
                    "pawn": "p",
                    "knight": "n",
                    "bishop": "b",
                    "rook": "r",
                    "queen": "q",
                    "king": "k",
                }

                symbol = symbols[piece.kind]

                if piece.color == "white":
                    symbol = symbol.upper()

                row += symbol

            if empty:
                row += str(empty)

            rows.append(row)

        active = "w" if self.turn == "white" else "b"

        castling = ""

        if self.castling_rights["white_kingside"]:
            castling += "K"

        if self.castling_rights["white_queenside"]:
            castling += "Q"

        if self.castling_rights["black_kingside"]:
            castling += "k"

        if self.castling_rights["black_queenside"]:
            castling += "q"

        if not castling:
            castling = "-"

        if self.en_passant_target:
            ep = self.square_name(
                *self.en_passant_target
            )
        else:
            ep = "-"

        return (
            f"{'/'.join(rows)} "
            f"{active} "
            f"{castling} "
            f"{ep} "
            f"{self.halfmove_clock} "
            f"{self.fullmove_number}"
        )