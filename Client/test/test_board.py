import pytest

from Board import Board
from Pieces import Piece


def test_create_board():
    board = Board()
    board.seed_starting_board()
    for i in range(0,8):
        for j in range(0,8):
            assert board.board[i][j] is not None
            assert isinstance(board.board[i][j],Piece)
            assert tuple(board.board[i][j].position) == (i,j)


