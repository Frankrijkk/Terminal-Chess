from enum import Enum
from Pieces import *
from Pieces import Piece


class CanTakeStatus(Enum):
    CAN_TAKE = 1
    CANNOT_TAKE = 0
    EN_PASSANT = 2

class Board:


    def __init__(self):
        self.board:list[list[Piece]] =[]

        self.is_white_castle_king_side_available = True
        self.is_white_castle_queen_side_available = True
        self.is_black_castle_king_side_available = True
        self.is_black_castle_queen_side_available = True

        self.en_passant_candidates:list[tuple[int,int,str]] = []

        self.knights:list[Knight]=[]
        self.bishops:list[Bishop]=[]
        self.queens:list[Queen]=[]
        self.rooks:list[Rook]=[]
        self.pawns:list[Pawn]=[]
        self.kings:list[King]=[]

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
        for row in self.board:
            for p in row:
                if isinstance(p,Pawn):
                    self.pawns.append(p)
                if isinstance(p,King):
                    self.kings.append(p)
                if isinstance(p,Rook):
                    self.rooks.append(p)
                if isinstance(p,Bishop):
                    self.bishops.append(p)
                if isinstance(p,Queen):
                    self.queens.append(p)
                if isinstance(p,Knight):
                    self.knights.append(p)






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

        if isinstance(piece,Pawn):
            if piece.color == "white" and piece.position[0]==1 and finito[0]==3:

                self.en_passant_candidates.append((piece.position[0]+1,piece.position[1],piece.color))
            if piece.color == "black" and piece.position[0]==6 and finito[0]==4:
                self.en_passant_candidates.append((piece.position[0]-1,piece.position[1],piece.color))
        piece.move(finito)
        self.board[finito[0]][finito[1]] = piece
        self.board[piece.position[0]][piece.position[1]] = Piece((piece.position[0], piece.position[1]))

    def can_take(self,attacking_piece:Piece,finito:tuple[int,int])->CanTakeStatus:
        if finito[0]<0 or finito[0]>7 or finito[1]<0 or finito[1]>7:
            return CanTakeStatus.CANNOT_TAKE
        if attacking_piece.can_attack(finito):
            way = attacking_piece.on_the_way(finito)
            for point in way[:-1]:
                if self.board[point[0]][point[1]].is_piece():
                    return CanTakeStatus.CANNOT_TAKE
            if not self.board[way[-1][0]][way[-1][1]].is_piece() or self.board[way[-1][0]][way[-1][1]].color == attacking_piece.color:
                return CanTakeStatus.CANNOT_TAKE

            return CanTakeStatus.CAN_TAKE
        return CanTakeStatus.CANNOT_TAKE

    def take(self,attacking_piece:Piece,finito:tuple[int,int],is_en_passant:bool=False):
        if not is_en_passant:
            removed = self.board[finito[0]][finito[1]]
        else:
            if attacking_piece.color == "white":
                removed = self.board[finito[0]-1][finito[1]]
            else:
                removed = self.board[finito[0]+1][finito[1]]
        if isinstance(removed,Pawn):
            self.pawns.remove(removed)
        if isinstance(removed,Queen):
            self.queens.remove(removed)
        if isinstance(removed,Rook):
            self.rooks.remove(removed)
        if isinstance(removed,Bishop):
            self.bishops.remove(removed)
        if isinstance(removed,Knight):
            self.knights.remove(removed)

        self.move(attacking_piece,finito)


