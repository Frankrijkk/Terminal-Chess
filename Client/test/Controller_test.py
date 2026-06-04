from Board import Board
from Controller import Controller
from MoveParser import MoveParser
from test import move_parser_test


def test_controller_invalid_move():
    board = Board()
    board.seed_starting_board()
    mp = MoveParser()
    controlloer = Controller(mp,board,"white")
    assert not controlloer.proccess_input("e5")


def test_controller_take():
    board = Board()
    board.seed_starting_board()
    mp = MoveParser()
    whitecontroller = Controller(mp, board, "white")
    blackcontroller = Controller(mp, board, "black")
    assert whitecontroller.proccess_input("e4")
    assert blackcontroller.proccess_input("e5")
    assert whitecontroller.proccess_input("Nf3")
    assert blackcontroller.proccess_input("Nc6")
    assert whitecontroller.proccess_input("Nxe5")

def test_controller_take():
    board = Board()
    board.seed_starting_board()
    mp = MoveParser()
    whitecontroller = Controller(mp, board, "white")
    blackcontroller = Controller(mp, board, "black")
    assert whitecontroller.proccess_input("e4")
    assert blackcontroller.proccess_input("h5")
    assert whitecontroller.proccess_input("e5")
    assert blackcontroller.proccess_input("d5")
    assert whitecontroller.proccess_input("exd6")

