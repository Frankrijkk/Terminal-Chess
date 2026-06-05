import functools
import pickle

from Board import Board
from Controller import Controller, ForfeitException
from MoveParser import MoveParser
from logger import Logger


class TerminalChessClientApplication:
    def __init__(self):
        print()

    def handle_local_game(self):
        board = Board()
        board.seed_starting_board()
        moveparser = MoveParser()
        logger = Logger()
        whitecontroller = Controller (moveparser,board,"white",logger)
        blackcontroller = Controller (moveparser,board,"black",logger)
        while True:
            try:
                whitecontroller.get_move()
                if board.is_checkmate():
                    break
                blackcontroller.get_move()
                if board.is_checkmate():
                    break
            except ForfeitException as e:
                print("Game forfeited")
                if e.message == "white":
                    blackcontroller.victory()
                else:
                    whitecontroller.victory()
                return
        board.get_winner()
        if board.get_winner() == "white":
            whitecontroller.victory()
        else:
            blackcontroller.victory()


    def handle_bot_game(self):
        pass

    def handle_online_game(self):
        pass


    def run(self):
        while True:
            print("Welcome to the terminal chess client application")
            inp = input("What would you like to do?\n1.start a new local game\n2.Continue a game\n3.play with a bot(To be implemented)\n4.join a server game(to be implemented)\n0.exit\n>")
            match inp:
                case "1":
                    self.handle_local_game()
                case "2":
                    self.load_game()
                case "3":
                    self.handle_bot_game()
                case "4":
                    self.handle_online_game()
                case "0":
                    return

    def load_game(self):
        inp = input("Enter your game's filename: ")
        try:
            with open(inp,"rb") as f:
                game_state = pickle.load(f)
                board = game_state["board"]
                logger = game_state["logger"]
                color = game_state["current_turn"]
            whitecontroller = Controller (MoveParser(),board,"white",logger)
            blackcontroller = Controller (MoveParser(),board,"black",logger)
            if color == "black":
                blackcontroller.get_move()
        except FileNotFoundError:
            print("File not found")
            return
        while True:
            try:
                whitecontroller.get_move()
                if board.is_checkmate():
                    break
                blackcontroller.get_move()
                if board.is_checkmate():
                    break
            except ForfeitException as e:
                print("Game forfeited")
                if e.message == "white":
                    blackcontroller.victory()
                else:
                    whitecontroller.victory()
                return
        board.get_winner()
        if board.get_winner() == "white":
            whitecontroller.victory()
        else:
            blackcontroller.victory()


if __name__ == "__main__":
    app = TerminalChessClientApplication()
    app.run()