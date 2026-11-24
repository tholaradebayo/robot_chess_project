class Piece:
    VALUES = {
        "pawn": 100,
        "knight": 320,
        "bishop": 330,
        "rook": 500,
        "queen": 900,
        "king": 20000,
    }

    SYMBOLS = {
        "white": {
            "king": "♔",
            "queen": "♕",
            "rook": "♖",
            "bishop": "♗",
            "knight": "♘",
            "pawn": "♙",
        },
        "black": {
            "king": "♚",
            "queen": "♛",
            "rook": "♜",
            "bishop": "♝",
            "knight": "♞",
            "pawn": "♟",
        },
    }

    VALID_COLORS = {"white", "black"}
    VALID_KINDS = {
        "pawn",
        "knight",
        "bishop",
        "rook",
        "queen",
        "king",
    }

    def __init__(self, color, kind):
        if color not in self.VALID_COLORS:
            raise ValueError("Color must be 'white' or 'black'.")

        if kind not in self.VALID_KINDS:
            raise ValueError(f"Invalid piece type: {kind}")

        self.color = color
        self.kind = kind

    @property
    def value(self):
        return self.VALUES[self.kind]

    def symbol(self):
        return self.SYMBOLS[self.color][self.kind]

    def is_white(self):
        return self.color == "white"

    def is_black(self):
        return self.color == "black"

    def __str__(self):
        return self.symbol()

    def __repr__(self):
        return f"Piece({self.color!r}, {self.kind!r})"

    def __eq__(self, other):
        if not isinstance(other, Piece):
            return NotImplemented

        return (
            self.color == other.color
            and self.kind == other.kind
        )

    def __hash__(self):
        return hash((self.color, self.kind))


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, "pawn")


class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, "knight")


class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color, "bishop")


class Rook(Piece):
    def __init__(self, color):
        super().__init__(color, "rook")


class Queen(Piece):
    def __init__(self, color):
        super().__init__(color, "queen")


class King(Piece):
    def __init__(self, color):
        super().__init__(color, "king")


def create_piece(color, kind):
    classes = {
        "pawn": Pawn,
        "knight": Knight,
        "bishop": Bishop,
        "rook": Rook,
        "queen": Queen,
        "king": King,
    }

    if kind not in classes:
        raise ValueError(f"Invalid piece type: {kind}")

    return classes[kind](color)