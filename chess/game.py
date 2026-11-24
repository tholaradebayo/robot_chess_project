from .board import Board
from .move import Move, parse_uci
from .rules import Rules


class Game:

    def __init__(self):
        self.board = Board()
        self.game_over = False

    def legal_moves(self):
        return Rules.legal_moves(self.board)

    def play(self, move: Move):
        if self.game_over:
            raise ValueError("Game is already over.")

        legal_moves = self.legal_moves()

        if move not in legal_moves:
            raise ValueError(f"Illegal move: {move}")

        Rules.make_move(self.board, move)

        status = Rules.status(self.board)

        if "checkmate" in status or "stalemate" in status:
            self.game_over = True

        return status

    def play_uci(self, text: str):
        move = parse_uci(text)

        for legal_move in self.legal_moves():
            if (
                legal_move.from_rank == move.from_rank
                and legal_move.from_file == move.from_file
                and legal_move.to_rank == move.to_rank
                and legal_move.to_file == move.to_file
                and legal_move.promotion == move.promotion
            ):
                return self.play(legal_move)

        raise ValueError(f"Illegal move: {text}")

    def display(self):
        self.board.display()
        print()
        print("Status:", Rules.status(self.board))

    def show_moves(self):
        moves = self.legal_moves()

        for move in moves:
            print(move.uci)

    def run(self):
        print("Robot Chess")
        print("Enter moves in UCI format, e.g. e2e4")
        print("Type 'moves' to see legal moves.")
        print("Type 'board' to display the board.")
        print("Type 'quit' to exit.")

        while not self.game_over:

            self.display()

            command = input("\nMove: ").strip().lower()

            if command == "quit":
                break

            if command == "board":
                self.display()
                continue

            if command == "moves":
                self.show_moves()
                continue

            try:
                self.play_uci(command)
            except ValueError as error:
                print("Error:", error)