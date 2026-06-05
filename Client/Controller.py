import datetime
import pickle

import logger
from Board import Board
from MoveParser import MoveParser, Move, InvalidMove, Castle
from logger import log_move, Logger


class Controller:


    def __init__(self,moveparser:MoveParser,board:Board,color:str,logger:Logger ):

        self.moveparser = moveparser
        self.board = board
        self.color = color
        self.logger = logger

    @log_move
    def proccess_input(self,string:str):
        if string.startswith(":"):
            self.proccess_command(string[1:])
            return False

        try:
            move = self.moveparser.parse(string,self.color)
            if isinstance(move,Castle):
                if self.board.can_castle(self.color,move.is_king_side):
                    self.board.castle(self.color,move.is_king_side)
                    return True
                else:
                    print("Invalid castle")
            elif isinstance(move,Move):
                if self.board.make_turn(move,self.color):
                    return True
                else:
                    print("Invalid move")

        except InvalidMove as e:
            print(e.message)
            return False




    def proccess_command(self,command:str):
        match command.split():
            case ["quit"]:
                exit()
            case ["notation"]:
                self.logger.to_file()
            case ["notation",filename]:
                self.logger.to_file(filename)
            case ["ff"]:
                self.forfeit()
            case ["save"]:
                self.save()
            case ["save",filename]:
                self.save(filename)
            case ["moves"]:
                print("Chess Notation:")
                print("first choose a piece and then the destination")
                print("pieces:")
                print("R - Rook")
                print("N - Knight")
                print("B - Bishop")
                print("Q - Queen")
                print("K - King")
                print("  - Pawn(no letter)")
                print("destination: a1-h8")
                print("to castle, use O-O or O-O-O for king side and queen side respectively")
                print("If you want to capture a piece, add an x before the destination")
                print("When promoting add a +{piece} after the destination")
                print("Don't bother with check notation, just play the moves")
                print("To win - you have to take the opponent's king, not only checkmate it")
                print("Examples: Nf3 - knight to f3, Nxf3 - knight to e3, Nxe4 - knight to e4, d8=Q - pawn to d8 promoting to queen")
            case ["help"]:
                print("Commands:")
                print(":quit - Quit the game")
                print(":ff - Forfeit the game")
                print(":notation - Save the game notation to a file")
                print(":notation [filename] - Save the game notation to a file with the specified filename")
                print(":save - Save the game to a file that can be played from this point on")
                print(":save [filename]- Save the game to a file with a specified filename that can be played from this point on")
                print(":moves - shows a quick overview of chess notation")
                print(":help - Show this help message")
    def get_move(self):
        while True:
            print(self.board.get_board_string(self.color))
            inp = input(f"{self.color.upper()}'s turn: ")
            if self.proccess_input(inp):
                break

    def victory(self):
        print(f"{self.color.upper()} wins! Congratulations!")

    def forfeit(self):
        inp = input("Do you want to save the game? (y/n): ")
        if inp.lower() == "y":
            self.logger.to_file()
        raise ForfeitException(self.color)

    def save(self,filename:str|None=None):

        if filename is None:
            time = str(datetime.datetime.now().timestamp())
            filename = "Game_" + time + ".pkl"
        game_state = {
            "board":self.board,
            "logger":self.logger,
            "current_turn":self.color,
        }
        with open("games/"+filename,"wb") as f:
            pickle.dump(game_state,f)
        print ("Game saved to games/"+filename)


class ForfeitException(Exception):
    def __init__(self,message:str):
        self.message = message
        super().__init__(self.message)