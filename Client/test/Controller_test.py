from Board import Board
from Controller import Controller
from MoveParser import MoveParser
from logger import Logger
from models.Pieces import Knight


def test_controller_invalid_move():
    board = Board()
    board.seed_starting_board()
    mp = MoveParser()
    controlloer = Controller(mp,board,"white",Logger())
    assert not controlloer.proccess_input("e5")


def test_controller_take():
    board = Board()
    board.seed_starting_board()
    mp = MoveParser()
    whitecontroller = Controller(mp, board, "white",Logger())
    blackcontroller = Controller(mp, board, "black",Logger())
    assert whitecontroller.proccess_input("e4")
    assert blackcontroller.proccess_input("e5")
    assert whitecontroller.proccess_input("Nf3")
    assert blackcontroller.proccess_input("Nc6")
    assert whitecontroller.proccess_input("Nxe5")

def test_controller_take():
    board = Board()
    board.seed_starting_board()
    mp = MoveParser()
    whitecontroller = Controller(mp, board, "white",Logger())
    blackcontroller = Controller(mp, board, "black",Logger())
    assert whitecontroller.proccess_input("e4")
    assert blackcontroller.proccess_input("h5")
    assert whitecontroller.proccess_input("e5")
    assert blackcontroller.proccess_input("d5")
    assert whitecontroller.proccess_input("exd6")

def test_controller_knight_bug():
    board = Board()
    board.seed_starting_board()
    mp = MoveParser()
    whitecontroller = Controller(mp, board, "white",Logger())
    blackcontroller = Controller(mp, board, "black",Logger())
    assert whitecontroller.proccess_input("e4")
    assert blackcontroller.proccess_input("h6")
    assert whitecontroller.proccess_input("e5")
    assert blackcontroller.proccess_input("h5")
    assert whitecontroller.proccess_input("e6")
    assert blackcontroller.proccess_input("h4")
    assert whitecontroller.proccess_input("exd7") # TODO Check here +
    assert blackcontroller.proccess_input("h3")
    assert whitecontroller.proccess_input("dxc8=Q")
    assert blackcontroller.proccess_input("hxg2")
    assert isinstance(board.board[0][6],Knight)
    assert board.board[1][6].color == "black"

def test_castle_king_white():
    board = Board()
    board.seed_starting_board()
    mp = MoveParser()
    whitecontroller = Controller(mp, board, "white",Logger())
    blackcontroller = Controller(mp, board, "black",Logger())
    assert whitecontroller.proccess_input("e4")
    assert blackcontroller.proccess_input("e5")
    assert whitecontroller.proccess_input("Nf3")
    assert blackcontroller.proccess_input("Nf6")
    assert whitecontroller.proccess_input("Bc4")
    assert blackcontroller.proccess_input("Nc6")
    assert whitecontroller.proccess_input("O-O")

def test_castle_queen_white():
    board = Board()
    board.seed_starting_board()
    mp = MoveParser()
    whitecontroller = Controller(mp, board, "white",Logger())
    blackcontroller = Controller(mp, board, "black",Logger())
    assert whitecontroller.proccess_input("d4")
    assert blackcontroller.proccess_input("e5")
    assert whitecontroller.proccess_input("Nc3")
    assert blackcontroller.proccess_input("Nf6")
    assert whitecontroller.proccess_input("Bf4")
    assert blackcontroller.proccess_input("Nc6")
    assert whitecontroller.proccess_input("Qd2")
    assert blackcontroller.proccess_input("Bc5")
    assert whitecontroller.proccess_input("O-O-O")