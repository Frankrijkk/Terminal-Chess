
from Board import Board
from Controller import Controller
from MoveParser import MoveParser


class TerminalChessClientApplication:
    def __init__(self):
        self.target = None



    def handle_local_game(self):
        board = Board()
        board.seed_starting_board()
        moveparser = MoveParser()
        whiteController = Controller (moveparser,board,"white")
        blackController = Controller (moveparser,board,"black")
        self.alternate_controllers(whiteController,blackController,board)
        while not board.is_checkmate():
            whiteController.get_move()
            blackController.get_move()
        board.get_winner()


    def alternate_controllers(self, controller1:Controller, controller2:Controller, board):
        while not board.is_checkmate() :
            yield controller1.get_move()
            yield controller2.get_move()
        yield board.get_winner()

    def run(self):
        while True:
            print("Welcome to the terminal chess client application")
            inp = input("What would you like to do?\n1.start a new local game\n2.play with a bot\n3.join a server game\n0.exit\n>")
            match inp:
                case "1":
                    target = "local"
                    self.handle_local_game()


if __name__ == "__main__":
    app = TerminalChessClientApplication()
    app.run()