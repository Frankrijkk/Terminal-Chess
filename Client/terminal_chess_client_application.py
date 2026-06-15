import functools
import pickle

from websockets.sync.client import connect

from Board import Board
from Controller import Controller, ForfeitException
from MoveParser import MoveParser
from logger import Logger
import websockets

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
        inp = input("Enter the server's IP address and port in this format 'IP:PORT': ")
        uri = f"ws://{inp}/ws"
        board = Board()
        board.seed_starting_board()
        moveparser = MoveParser()
        logger = Logger()
        white_controller = Controller(moveparser,board,"white",logger)
        black_controller = Controller(moveparser,board,"black",logger)
        try:
            with connect(uri) as websocket:

                print("Searching for a game...")
                data = websocket.recv()
                if data == "FOUND":
                    print("Found Game!! Joining...")
                data = websocket.recv()
                if data == "WHITE":
                    print("Youre white")
                    you = white_controller
                    enemy = black_controller
                    color= "white"
                elif data == "BLACK":
                    print("Youre black")
                    you = black_controller
                    enemy = white_controller
                    color = "black"
                else:
                    print("Invalid color")
                    return
                data = websocket.recv()
                if data == "START":
                    print("Starting game")
                    if color == "black":
                        try:
                            print(board.get_board_string("black"))
                            print("WHITE's Turn...")
                            move = websocket.recv()
                            if move.startswith("ff"):
                                print("Game forfeited")
                                print(move.split(" ")[1] + " lost")
                                print("You won")
                                return
                            enemy.proccess_input(move)
                        except Exception as e:
                            print(f"Error:{e}")
                            return
                    while True:
                        try:

                            move = you.get_move()
                            print(f"sending move: {move}")
                            print(board.get_board_string(you.color))
                            websocket.send(move)

                            response = websocket.recv()
                            print(response)
                            if response.startswith("CHECKMATE"):
                                print("Game over")
                                print(response.split(" ")[1] + " won")
                                return

                            enemymove = websocket.recv()
                            print(enemymove)
                            if enemymove.startswith("CHECKMATE"):
                                print("Game over")
                                print(enemymove.split(" ")[1] + " won")
                                return
                            elif enemymove.startswith("ff"):
                                print("Game forfeited")
                                print(enemymove.split(" ")[1] + " lost")
                                print("You won")
                                return
                            enemy.proccess_input(enemymove)

                        except ForfeitException as e:
                            print("Game forfeited")
                            if e.message == "white":
                                websocket.send("ff white")
                            else:
                                websocket.send("ff black")
                            return

        except websockets.exceptions.ConnectionClosed as e:
            print(f"Connection closed with  {e} ")
        except Exception as e:
            print(f"An error occurred, couldn't connect")


    def run(self):
        while True:
            print("Welcome to the terminal chess client application")
            inp = input("What would you like to do?\n1.start a new local game\n2.Continue a game\n3.play with a bot(To be implemented)\n4.join a server game\n0.exit\n>")
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