

from models.Pieces import Piece, King, Knight, Bishop, Rook, Queen, Pawn

import re


class MoveParser:

    def __init__(self):

        self.master_regex = re.compile(
            r"^(?P<piece>[KQRBN])?"  
            r"(?P<disambiguation>[a-h]?[1-8]?)?"  
            r"(?P<capture>x)?" 
            r"(?P<destination>[a-h][1-8])" 
            r"(?:=(?P<promotion>[QRBN]))?"  
            r"(?P<check>[+#])?$"
        )


    def parse(self,inp:str,color:str)->Move|Castle|None:
        if inp.startswith(":"):
            raise InvalidMove("Command in the parser")

        if inp == "O-O":
            return Castle(True,color)
        if inp == "O-O-O":
            return Castle(False,color)



        match = self.master_regex.match(inp)
        if not match:
            raise InvalidMove("Invalid move")

        groups = match.groupdict()

        pos_after = self.get_pos(groups["destination"])

        if not groups['piece']:
            piece = Pawn(pos_after,color)
        else:
            piece = self.get_piece(groups["piece"],color,pos_after)

        is_attacking = groups["capture"] =="x"

        start_here = groups["disambiguation"]
        start_pos = None
        if start_here:
            start_pos = self.get_start(start_here)



        is_check = groups["check"] =="+"
        is_mate = groups["check"] =="#"

        if groups["promotion"]:
            promotes_to = self.get_piece(groups["promotion"],color,pos_after)
        else:
            promotes_to = None
        self.validate(pos_after,piece,is_attacking,start_pos,is_check,is_mate,promotes_to,color)

        return Move(piece,pos_after,is_attacking,start_pos,is_check,is_mate,promotes_to)


    @staticmethod
    def validate(pos_after:tuple[int,int], piece:Piece, is_attacking:bool, start_pos:tuple[int,int]|None, is_check:bool, is_mate:bool, promotes_to:Piece|None, color:str):
        if is_attacking and isinstance(piece,Pawn) and not start_pos:
            raise InvalidMove(f"Invalid pawn Capture - must include starting file")
        if promotes_to and not isinstance(piece,Pawn):
            raise InvalidMove("Invalid promotion, only pawns can promote")

        if isinstance(piece,Pawn):
            dest_rank = pos_after[0]
            if dest_rank in [0,7] and not promotes_to:
                raise InvalidMove("Pawn must promote on the first or last rank")

        if start_pos == pos_after:
            raise InvalidMove("Invalid move, cannot move to the same position")

    def get_start(self,string:str)->tuple[int,int]:
        if len(string)==2:
            return self.get_pos(string)
        if len(string)==1:
            if string[0].isdigit():
                return int(string[0])-1,-1
            elif string[0] in ["a","b","c","d","e","f","g","h"]:
                return -1,ord(string[0])-ord("a")
        raise InvalidMove("Invalid disambiguation")


    @staticmethod
    def get_piece(string, color:str,pos_after:tuple[int,int])->Piece:
        match string:
            case "K":
                return King(pos_after,color)
            case "N":
                return Knight(pos_after,color)
            case "B":
                return Bishop(pos_after,color)
            case "R":
                return Rook(pos_after,color)
            case "Q":
                return Queen(pos_after,color)
            case "_":
                raise InvalidMove("Invalid piece")
        raise InvalidMove("Invalid piece")



    @staticmethod
    def  get_pos(string:str)->tuple[int,int]:
        if len(string) != 2:
            raise InvalidMove("Position must be 2 characters long")
        first = ord(string[0]) - ord("a")
        second = int(string[1]) -1
        return second,first



class InvalidMove(Exception):
    def __init__(self,message:str):
        self.message = message
        super().__init__(self.message)

class Move:
    def __init__(self,piece:Piece,finito:tuple[int,int],is_attacking:bool,start_pos = None,is_check:bool=False,is_mate:bool=False,promotes_to:Piece|None=None):
        self.piece:Piece = piece
        self.finito:tuple[int,int] = finito
        self.is_attacking:bool = is_attacking
        self.start_pos:tuple[int,int]|None = start_pos
        self.is_check:bool = is_check
        self.is_mate:bool = is_mate
        self.promotes_to:Piece|None = promotes_to

class Castle:
    def __init__(self,is_king_side:bool,color:str):
        self.is_king_side = is_king_side
        self.color = color

