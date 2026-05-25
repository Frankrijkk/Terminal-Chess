
from Pieces import *
from Pieces import Piece


class Board:


    def __init__(self):
        self.board:list[list[Piece]] =[]

        self.is_white_castle_king_side_available = True
        self.is_white_castle_queen_side_available = True
        self.is_black_castle_king_side_available = True
        self.is_black_castle_queen_side_available = True

    def seed_starting_board(self):
        starting_board:list[list[Piece ]] = [
            [Rook((0, 0),"white"), Knight((0, 1),"white"), Bishop((0, 2),"white"), Queen((0, 3),"white"), King((0, 4),"white"), Bishop((0, 5),"white"), Knight((0, 6),"white"),
             Rook((0, 7),"white")],  # 1
            [Pawn((1, i),"white") for i in range(8)],  # 2
            [Piece((2, i)) for i in range(8)],  # 3
            [Piece((3, i)) for i in range(8)],  # 4
            [Piece((4, i)) for i in range(8)],  # 5
            [Piece((5, i)) for i in range(8)],  # 6
            [Pawn((6,i),"black") for i in range(8)], #7
            [Rook((7, 0),"black"), Knight((7, 1),"black"), Bishop((7, 2),"black"), Queen((7, 3),"black"), King((7, 4),"black"), Bishop((7, 5),"black"), Knight((7, 6),"black"),
             Rook((7, 7),"black")],  # 8

        ]

        self.board = starting_board


    def can_move(self,piece:Piece,finito:tuple[int,int])->bool:
        if finito[0]<0 or finito[0]>7 or finito[1]<0 or finito[1]>7:
            return False
        if piece.can_move(finito):
            for point in piece.on_the_way(finito):
                if self.board[point[0]][point[1]].is_piece():
                    return False
            return True
        return False


    def move(self,piece:Piece,finito:tuple[int,int]):
        self.board[finito[0]][finito[1]] = piece
        self.board[piece.position[0]][piece.position[1]] = Piece((piece.position[0], piece.position[1]))
        piece.move(finito)

    def take(self,attacking_piece:Piece,finito:tuple[int,int])->bool:
        if finito[0]<0 or finito[0]>7 or finito[1]<0 or finito[1]>7:
            return False
        if attacking_piece.can_attack(finito):
            way = attacking_piece.on_the_way(finito)
            for point in way[:-1]:
                if self.board[point[0]][point[1]].is_piece():
                    return False
            if not self.board[way[-1][0]][way[-1][1]].is_piece() or self.board[way[-1][0]][way[-1][1]].color == attacking_piece.color:
                return False
            self.move(attacking_piece,finito)

            return True
        return False