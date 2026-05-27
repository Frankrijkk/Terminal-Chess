from Board import Board
from Pieces import Piece

import re


class MoveParser:

    def __init__(self,board:Board):
        self.piece_regex:str = r"^[A-H]"
        self.pawn_regex:str = r"^[a-h][1-8]"
        self.move_regex:str = r"[a-h][1-8]"
        self.attack_regex=r"x"
        self.board = board


    def parse(self,move:str,color:str)->Move|None:
        if move.startswith(":"):
            command = move[1:]
            self.command(command)
            return None


        if re.match(self.attack_regex,move):
            is_attacking = True
            splitmoves = move.split("x")
            piece = splitmoves[0]
            aftertake = splitmoves[1]
            positionafter = aftertake[0] + aftertake[1]
            try:
                p:Piece = self.getPiece(piece,color)
                finito:tuple[int,int] = self.getPos(positionafter)





    def command(self,command):
        print(command)


    def  getPos(self,string:str):
        if len(string) != 2:
            raise ValueError("Position must be 2 characters long")



class PieceNotFound(Exception):
    def __init__(self,message:str):
        self.message = message
        super().__init__(self.message)

class Move:
    def __init__(self,piece:Piece,move:tuple[int,int],is_attacking:bool):
        self.piece = piece
        self.move = move
        self.is_attacking = is_attacking



if __name__ == "__main__":
    print("xa5".split("x"))