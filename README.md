# Robot Chess — Chess Core

This stage contains the complete chess-rule foundation before the robotics and computer-vision layers.

## Project structure

robot_chess/
├── chess/
│   ├── __init__.py
│   ├── pieces.py
│   ├── board.py
│   ├── move.py
│   ├── rules.py
│   ├── game.py
│   └── tests/
└── run_game.py

## Implemented

- 8x8 board
- all six chess pieces
- coordinate conversion
- UCI-style move input
- pawn movement and captures
- double pawn move
- en passant
- knight movement
- bishop movement
- rook movement
- queen movement
- king movement
- check detection
- legal move filtering
- checkmate
- stalemate
- kingside castling
- queenside castling
- castling-right tracking
- promotion to queen, rook, bishop, or knight
- move execution
- turn management
- FEN generation
- halfmove/fullmove counters
- game history
- automated tests

## Run

From the `robot_chess` folder:

python run_game.py

Enter moves such as:

e2e4
e7e5
g1f3

Promotion:

e7e8q

Commands:

board
moves
fen
quit

## Tests

The test suite is included but intentionally has not been run yet.

After you finish placing the files in VS Code, run:

python -m pytest -q
