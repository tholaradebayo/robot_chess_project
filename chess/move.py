from dataclasses import dataclass


FILES = "abcdefgh"

PROMOTION_TO_UCI = {
    "queen": "q",
    "rook": "r",
    "bishop": "b",
    "knight": "n",
}

UCI_TO_PROMOTION = {
    "q": "queen",
    "r": "rook",
    "b": "bishop",
    "n": "knight",
}


def square_name(rank: int, file: int) -> str:
    if not (0 <= rank < 8 and 0 <= file < 8):
        raise ValueError("Square coordinates must be between 0 and 7.")

    return f"{FILES[file]}{rank + 1}"


def parse_square(square: str) -> tuple[int, int]:
    if not isinstance(square, str):
        raise TypeError("Square must be a string.")

    if len(square) != 2:
        raise ValueError(f"Invalid square: {square}")

    file_char = square[0].lower()
    rank_char = square[1]

    if file_char not in FILES:
        raise ValueError(f"Invalid file: {file_char}")

    if rank_char not in "12345678":
        raise ValueError(f"Invalid rank: {rank_char}")

    return int(rank_char) - 1, FILES.index(file_char)


@dataclass(frozen=True)
class Move:
    from_rank: int
    from_file: int
    to_rank: int
    to_file: int

    promotion: str | None = None
    is_castling: bool = False
    is_en_passant: bool = False

    def __post_init__(self):
        for value in (
            self.from_rank,
            self.from_file,
            self.to_rank,
            self.to_file,
        ):
            if not 0 <= value < 8:
                raise ValueError("Move coordinates must be between 0 and 7.")

        if self.promotion is not None:
            if self.promotion not in PROMOTION_TO_UCI:
                raise ValueError(
                    f"Invalid promotion piece: {self.promotion}"
                )

    @property
    def from_square(self) -> str:
        return square_name(self.from_rank, self.from_file)

    @property
    def to_square(self) -> str:
        return square_name(self.to_rank, self.to_file)

    @property
    def uci(self) -> str:
        result = self.from_square + self.to_square

        if self.promotion is not None:
            result += PROMOTION_TO_UCI[self.promotion]

        return result

    def __str__(self) -> str:
        return self.uci


def parse_uci(uci: str) -> Move:
    if not isinstance(uci, str):
        raise TypeError("UCI move must be a string.")

    uci = uci.strip().lower()

    if len(uci) not in (4, 5):
        raise ValueError(f"Invalid UCI move: {uci}")

    from_square = uci[:2]
    to_square = uci[2:4]

    from_rank, from_file = parse_square(from_square)
    to_rank, to_file = parse_square(to_square)

    promotion = None

    if len(uci) == 5:
        promotion_char = uci[4]

        if promotion_char not in UCI_TO_PROMOTION:
            raise ValueError(
                f"Invalid promotion piece: {promotion_char}"
            )

        promotion = UCI_TO_PROMOTION[promotion_char]

    return Move(
        from_rank=from_rank,
        from_file=from_file,
        to_rank=to_rank,
        to_file=to_file,
        promotion=promotion,
    )