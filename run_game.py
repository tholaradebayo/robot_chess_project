from chess.board import Board
from chess.engine import Engine

board = Board()
engine = Engine(depth=3)

move = engine.select_move(board)

print("Engine selected:", move.uci)
print("Nodes searched:", engine.nodes_searched)
print("TT hits:", engine.tt_hits)
print("TT entries:", engine.tt_entries)