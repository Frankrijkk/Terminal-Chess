
from Pieces import *


class Board:


    def __init__(self):
        self.board:list[list[Piece]] =[]

    def seed_starting_board(self):
        starting_board:list[list[Piece ]] = [
            [Rook((0, 0),"white"), Knight((0, 1),"white"), Bishop((0, 2),"white"), Queen((0, 3),"white"), King((0, 4),"white"), Bishop((0, 5),"white"), Knight((0, 6),"white"),
             Rook((0, 7),"white")],  # 1
            [Pawn((1, i),"white") for i in range(8)],  # 2
            [Piece((2, i)) for i in range(8)],  # 3
            [Piece((3, i)) for i in range(8)],  # 4
            [Piece((4, i)) for i in range(8)],  # 5
            [Piece((5, i)) for i in range(8)],  # 6
            [Pawn((6,i),"white") for i in range(8)], #7
            [Rook((7, 0),"black"), Knight((7, 1),"black"), Bishop((7, 2),"black"), Queen((7, 3),"black"), King((7, 4),"black"), Bishop((7, 5),"black"), Knight((7, 6),"black"),
             Rook((7, 7),"black")],  # 8

        ]
        self.board = starting_board

