from enum import Enum

from MoveParser import Move
from models.Pieces import *
from models.Pieces import Piece


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

        self.white_pieces = []
        self.black_pieces = []

        self.winner:str|None = None

        self.back_rank = lambda color: 0 if color == "white" else 7 if color == "black" else -1


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
                if p.color == "white":
                    self.white_pieces.append(p)
                elif p.color == "black":
                    self.black_pieces.append(p)

    def is_checkmate(self):
        king:King|None = None
        for p in self.white_pieces:
            if isinstance(p,King):
                king = p
                break
        if king is None:
            self.winner = "black"
            return True
        king = None
        for p in self.black_pieces:
            if isinstance(p,King):
                king = p
                break
        if king is None:
            self.winner = "white"
            return True

        return False
    def get_winner(self):
        return self.winner

    def can_castle(self,color:str,is_king_side)->bool:
        line = self.back_rank(color)
        if is_king_side:
            return self.check_castle_moves(color,is_king_side) and not self.board[line][6].is_piece() and  not self.board[line][5].is_piece()
        else:
            return self.check_castle_moves(color,is_king_side) and not self.board[line][1].is_piece() and  not self.board[line][2].is_piece()and  not self.board[line][3].is_piece()



    def castle (self,color:str,is_king_side:bool)->bool:
        if self.can_castle(color,is_king_side):
            line = 0 if color=="white" else 7 if color=="black" else -1
            self.move(self.board[line][4],(line,6 if is_king_side else 2))
            self.move(self.board[line][7 if is_king_side else 0],(line,5 if is_king_side else 3))
            return True
        return False


    def make_turn(self,move:Move,color:str):
        pieces:list[Piece]|None = self.white_pieces if color=="white" else self.black_pieces if color=="black" else None
        if pieces is None:
            raise ValueError("invalid Color")
        start_row = None
        start_col = None
        valid_pieces:list[Piece] = []
        is_attack_en_poissont = False
        if move.start_pos is not None:
            start_row = move.start_pos[0] if move.start_pos[0]>=0 else None
            start_col = move.start_pos[1] if move.start_pos[1]>=0 else None
        if move.is_check or move.is_mate:
            if not move.piece.can_attack(tuple([k for k in pieces if isinstance(k,King)][0].position)):
                return False


        for p in pieces:
            if not isinstance(p,type(move.piece)):
                continue
            if start_row is not None and p.position[0] !=start_row:
                continue
            if start_col is not None and p.position[1] !=start_col:
                continue
            if move.is_attacking:
                attack_status = self.can_take(p,move.finito)
                if attack_status == CanTakeStatus.CANNOT_TAKE:
                    continue
                elif attack_status == CanTakeStatus.EN_PASSANT:
                    is_attack_en_poissont = True
                    valid_pieces.append(p)
                elif attack_status == CanTakeStatus.CAN_TAKE:
                    valid_pieces.append(p)
            else:
                if not self.can_move(p,move.finito):
                    continue
                else :
                    valid_pieces.append(p)
        if len(valid_pieces) !=1:
            return False

        if move.is_attacking:
            self.take(valid_pieces[0],move.finito,is_attack_en_poissont)
        else:
            self.move(valid_pieces[0],move.finito)
        if move.promotes_to is not None:
            pieces[pieces.index(valid_pieces[0])] = move.promotes_to
            self.board[move.finito[0]][move.finito[1]] = move.promotes_to
        return True

    def can_move(self,piece:Piece,finito:tuple[int,int])->bool:
        # if isinstance(piece,King):
        #     if not finito in self.check_king_moves(piece):
        #         return False
        if finito[0]<0 or finito[0]>7 or finito[1]<0 or finito[1]>7:
            return False
        if piece.can_move(finito):
            for point in piece.on_the_way(finito):
                if self.board[point[0]][point[1]].is_piece():
                    return False
            return True
        return False


    def move(self,piece:Piece,finito:tuple[int,int]):
        for p in self.en_passant_candidates:
            if piece.color==p[2]:
                self.en_passant_candidates.remove(p)


        if isinstance(piece,Pawn):
            if piece.color == "white" and piece.position[0]==1 and finito[0]==3:

                self.en_passant_candidates.append((piece.position[0]+1,piece.position[1],"black"))
            if piece.color == "black" and piece.position[0]==6 and finito[0]==4:
                self.en_passant_candidates.append((piece.position[0]-1,piece.position[1],"white"))
        self.board[finito[0]][finito[1]] = piece
        self.board[piece.position[0]][piece.position[1]] = Piece((piece.position[0], piece.position[1]))
        piece.move(finito)

    def can_take(self,attacking_piece:Piece,finito:tuple[int,int])->CanTakeStatus:
        if finito[0]<0 or finito[0]>7 or finito[1]<0 or finito[1]>7:
            return CanTakeStatus.CANNOT_TAKE
        if attacking_piece.can_attack(finito):
            way = list(attacking_piece.on_the_way(finito))
            for point in way[:-1]:
                if self.board[point[0]][point[1]].is_piece():
                    return CanTakeStatus.CANNOT_TAKE
            if (way[-1][0],way[-1][1],attacking_piece.color) in self.en_passant_candidates:
                return CanTakeStatus.EN_PASSANT
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
                self.board[finito[0]-1][finito[1]] = Piece((finito[0]-1,finito[1]))
            else:
                removed = self.board[finito[0]+1][finito[1]]
                self.board[finito[0] - 1][finito[1]] = Piece((finito[0] - 1, finito[1]))
        if removed.color == "white":
            self.white_pieces.remove(removed)
        elif removed.color == "black":
            self.black_pieces.remove(removed)

        self.move(attacking_piece,finito)

    def check_castle_moves(self,color:str,is_king_side:bool)->bool:
        rookmoved: bool = True
        toiterate=[]
        if color == "white":
            toiterate = self.white_pieces
        elif color=="black":
            toiterate = self.black_pieces

        for rk in [p for p in toiterate if (isinstance(p,King) or isinstance(p,Rook)) ]:

            if isinstance(rk,King):
                if rk.has_moved:
                    return False
            elif isinstance(rk,Rook):
                if rk.position ==[0,7 if is_king_side else 0]:
                    if not rk.has_moved:
                        rookmoved = True
                    else:
                        rookmoved = False
        return rookmoved

    def get_board_string(self,color):
        # ANSI Color Codes
        BG_LIGHT = "\033[47m"  # White/Light Gray background
        BG_DARK = "\033[100m"  # Dark Gray background
        TEXT_BLACK = "\033[30m"  # Forces piece color to be visible
        RESET = "\033[0m"  # Resets formatting to terminal default

        pieces = {
            'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
            'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟',
            '.': ' '
        }

        result = "\n   a b c d  e f g h\n  +================+\n"
        if color=="white":
            for rank_idx in range(7,-1,-1):
                rank_label = rank_idx+1
                result+=(str(rank_label)+" |")
                for file_idx in range(8):
                    piece = self.board[rank_idx][file_idx]
                    piece_char = str(piece).upper() if piece.color == "white" else str(piece).lower() if piece.color=="black"else "."
                    symbol = pieces.get(piece_char, " ")
                    if (rank_idx + file_idx) % 2 == 0:
                        bg_color = BG_LIGHT
                    else:
                        bg_color = BG_DARK
                    result += f"{bg_color}{TEXT_BLACK}{symbol} {RESET}"
                result +=f"| {rank_label}\n"
            result+= "  +================+\n   a b c d  e f g h\n"
        elif color=="black":
            for rank_idx in range(0,8):
                rank_label = rank_idx+1
                result+=(str(rank_label)+" |")
                for file_idx in range(8):
                    piece = self.board[rank_idx][file_idx]
                    piece_char = str(piece).upper() if piece.color == "white" else str(piece).lower() if piece.color=="black"else "."
                    symbol = pieces.get(piece_char, " ")
                    if (rank_idx + file_idx) % 2 == 0:
                        bg_color = BG_LIGHT
                    else:
                        bg_color = BG_DARK
                    result += f"{bg_color}{TEXT_BLACK}{symbol} {RESET}"
                result +=f"| {rank_label}\n"
            result+= "  +================+\n   a b c d  e f g h\n"

        return result










