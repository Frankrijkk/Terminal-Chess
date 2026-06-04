import datetime

from Board import Board
from MoveParser import MoveParser, Move, InvalidMove, Castle


class Controller:


    def __init__(self,moveparser:MoveParser,board:Board,color:str):

        self.moveparser = moveparser
        self.board = board
        self.color = color
        self.logString = ""

    def proccess_input(self,string:str):
        if string.startswith(":"):
            self.proccess_command(string[1:])
            return False

        try:
            move = self.moveparser.parse(string,self.color)
            if isinstance(move,Castle):
                if self.board.can_castle(self.color,move.is_king_side):
                    self.board.castle(self.color,move.is_king_side)
                    self.logString += string + " "
                    return True
            elif isinstance(move,Move):
                if self.board.make_turn(move,self.color):
                    self.logString += string + " "
                    return True

        except InvalidMove as e:
            print(e.message)
            return False




    def proccess_command(self,command:str):
        match command:
            case "quit":
                exit() #TODO add better quit handling
            case "save":
                time = str(datetime.datetime.now().timestamp())
                with open("ChessGame" + time + ".txt","w") as f:
                    f.write(self.logString)


    def get_move(self):
        while True:
            print(self.board.get_board_string(self.color))
            inp = input(f"{self.color.upper()}'s turn: ")
            if self.proccess_input(inp):
                break


