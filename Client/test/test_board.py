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


def is_board_validity(board:Board):
    for i in range(0,8):
        for j in range(0,8):
            assert board.board[i][j] is not None
            assert isinstance(board.board[i][j],Piece)
            assert tuple(board.board[i][j].position) == (i,j)


def test_board_moves():
    board = Board()
    board.seed_starting_board()
    piece = board.board[0][0]

    # Pawn from E2 to E4
    assert board.can_move(board.board[1][4], (3, 4))
    board.move(board.board[1][4], (3, 4))
    # Pawn from D2 to D3
    assert board.can_move(board.board[1][3], (2, 3))
    board.move(board.board[1][3], (2, 3))

    # Knight from G1 to F3
    assert board.can_move(board.board[0][6], (2, 5))
    board.move(board.board[0][6], (2, 5))

    # Knight from B1 to C3
    assert board.can_move(board.board[0][1], (2, 2))
    board.move(board.board[0][1], (2, 2))

    # Rook from A1 to A3
    assert not board.can_move(board.board[0][0], (2, 0))

    # Bishop from C1 to A3
    assert not board.can_move(board.board[0][2], (2, 0))

    # Queen from D1 to D3
    assert not board.can_move(board.board[0][3], (2, 3))

    # King from E1 to E2
    assert  board.can_move(board.board[0][4], (1, 4))

    # Pawn from E2 to F3
    assert not board.can_move(board.board[1][4], (2, 5))

    is_board_validity(board)

# ==========================================
# PAWNS
# ==========================================

def test_legal_pawn_double_step():
    board = Board()
    board.seed_starting_board()
    # Moving 2 steps forward from starting rank (White E2 to E4)
    assert board.can_move(board.board[1][4], (3, 4))

def test_legal_pawn_single_step():
    board = Board()
    board.seed_starting_board()
    # Moving 1 step forward (Black D7 to D6)
    assert board.can_move(board.board[6][3], (5, 3))

def test_legal_pawn_two_single_step():
    board = Board()
    board.seed_starting_board()
    p = board.board[1][1]
    assert board.can_move(p, (2, 1))
    board.move(p, (2, 1))
    assert board.can_move(p, (3, 1))
    board.move(p, (3, 1))

def test_illegal_pawn_diagonal_without_capture():
    board = Board()
    board.seed_starting_board()
    # Diagonal move on an empty square (E2 to D3)
    assert not board.can_move(board.board[1][4], (2, 3))

def test_illegal_pawn_exceed_max_range():
    board = Board()
    board.seed_starting_board()
    # Moving 3 steps forward (E2 to E5)
    assert not board.can_move(board.board[1][4], (4, 4))

def test_illegal_pawn_backward_move():
    board = Board()
    board.seed_starting_board()
    # Moving backwards (E2 to E1)
    assert not board.can_move(board.board[1][4], (0, 4))


# =========================================
# Takes
def test_legal_pawn_diagonal_left_take():
    board = Board()
    board.seed_starting_board()

    # Setup: Move White E2 to E4
    p1 = board.board[1][4]
    if board.can_move(p1, (3, 4)):
        board.move(p1, (3, 4))

    # Setup: Move Black D7 to D5
    p2 = board.board[6][3]
    if board.can_move(p2, (4, 3)):
        board.move(p2, (4, 3))

    # LEGAL TAKE: White E4 Pawn captures Black D5 Pawn diagonally
    attacker = board.board[3][4]
    assert board.take(attacker, (4, 3))

def test_legal_pawn_diagonal_right_take():
    board = Board()
    board.seed_starting_board()
    # Setup: Move White E2 to E4
    p1 = board.board[1][4]
    if board.can_move(p1, (3, 4)):
        board.move(p1, (3, 4))

    # Setup: Move Black D7 to D5
    p2 = board.board[6][5]
    if board.can_move(p2, (4, 5)):
        board.move(p2, (4, 5))

    # LEGAL TAKE: White E4 Pawn captures Black D5 Pawn diagonally
    attacker = board.board[3][4]
    assert board.take(attacker, (4, 5))


def test_illegal_pawn_straight_take():
    board = Board()
    board.seed_starting_board()
    # Setup: Move White E2 to E4
    p1 = board.board[1][4]
    if board.can_move(p1, (3, 4)):
        board.move(p1, (3, 4))

    # Setup: Move Black E7 to E5 (Head-to-head collision)
    p2 = board.board[6][4]
    if board.can_move(p2, (4, 4)):
        board.move(p2, (4, 4))

    # ILLEGAL TAKE: Pawns cannot take pieces straight ahead
    attacker = board.board[3][4]
    assert not board.take(attacker, (4, 4))

# ==========================================
# KNIGHTS
# ==========================================

def test_legal_knight_l_shape_jump_white():
    board = Board()
    board.seed_starting_board()
    # L-shape jump over pawns (White G1 to F3)
    assert board.can_move(board.board[0][6], (2, 5))

def test_legal_knight_l_shape_jump_black():
    board = Board()
    board.seed_starting_board()
    # L-shape jump over pawns (Black B8 to C6)
    assert board.can_move(board.board[7][1], (5, 2))

def test_illegal_knight_straight_line():
    board = Board()
    board.seed_starting_board()
    # Moving in a straight line (G1 to G3)
    assert not board.can_move(board.board[0][6], (2, 6))

def test_illegal_knight_friendly_fire():
    board = Board()
    board.seed_starting_board()
    # Landing on own pawn (G1 to E2)
    assert not board.can_move(board.board[0][6], (1, 4))


def test_legal_knight_take():
    board = Board()
    board.seed_starting_board()
    # Setup: Move White Knight G1 to F3
    n1 = board.board[0][6]
    if board.can_move(n1, (2, 5)):
        board.move(n1, (2, 5))

    # Setup: Move Black E7 to E5
    p1 = board.board[6][4]
    if board.can_move(p1, (4, 4)):
        board.move(p1, (4, 4))

    # LEGAL TAKE: Knight on F3 jumps to take Pawn on E5
    attacker = board.board[2][5]
    assert board.take(attacker, (4, 4))


def test_illegal_knight_take_friendly_fire():
    board = Board()
    board.seed_starting_board()
    # ILLEGAL TAKE: Knight on G1 tries to take friendly White Pawn on E2
    attacker = board.board[0][6]
    assert not board.take(attacker, (1, 4))

# ==========================================
# BISHOPS (No legal moves in starting pos)
# ==========================================
def test_legal_bishop_diagonal_move():
    board = Board()
    board.seed_starting_board()
    #E2 to E4
    assert board.can_move(board.board[1][4], (3, 4))
    board.move(board.board[1][4], (3, 4))
    #F1 to C4
    assert board.can_move(board.board[0][5], (3, 2))

def test_illegal_bishop_path_blocked():
    board = Board()
    board.seed_starting_board()
    # Valid diagonal pattern, but cannot jump pawns (F1 to D3)
    assert not board.can_move(board.board[0][5], (2, 3))

def test_illegal_bishop_straight_move():
    board = Board()
    board.seed_starting_board()
    # Moving straight forward like a Rook (C1 to C3)
    assert not board.can_move(board.board[0][2], (2, 2))

def test_illegal_bishop_friendly_fire():
    board = Board()
    board.seed_starting_board()
    # Trying to capture own pawn (C1 to B2)
    assert not board.can_move(board.board[0][2], (1, 1))


def test_legal_bishop_take():
    board = Board()
    board.seed_starting_board()
    # Setup: Move White E2 to E4 to open diagonal
    p1 = board.board[1][4]
    if board.can_move(p1, (3, 4)):
        board.move(p1, (3, 4))

    # Setup: Move White Bishop F1 to C4
    b1 = board.board[0][5]
    if board.can_move(b1, (3, 2)):
        board.move(b1, (3, 2))

    # Setup: Move Black F7 to F5
    p2 = board.board[6][1]
    if board.can_move(p2, (4, 1)):
        board.move(p2, (4, 1))

    # LEGAL TAKE: Bishop on C4 takes Black Pawn on F5
    attacker = board.board[3][2]
    assert board.take(attacker, (4, 1))

def test_illegal_bishop_take_blocked():
    board = Board()
    board.seed_starting_board()
    # ILLEGAL TAKE: Bishop on C1 tries to take Black Pawn on A3, but White B2 pawn is in the way
    attacker = board.board[0][2]
    assert not board.take(attacker, (2, 0))

# ==========================================
# ROOKS (No legal moves in starting pos)
# ==========================================
def test_legal_rook_straight_move():
    board = Board()
    board.seed_starting_board()
    # Setup: Move Pawn from A2 to A4 to open the A-file
    assert board.can_move(board.board[1][0], (3, 0))
    board.move(board.board[1][0], (3, 0))

    # LEGAL: Move Rook from A1 to A3
    assert board.can_move(board.board[0][0], (2, 0))
def test_illegal_rook_path_blocked():
    board = Board()
    board.seed_starting_board()
    # Valid straight pattern, but cannot jump pawns (H1 to H3)
    assert not board.can_move(board.board[0][7], (2, 7))

def test_illegal_rook_diagonal_move():
    board = Board()
    board.seed_starting_board()
    # Moving diagonally like a Bishop (A1 to B2)
    assert not board.can_move(board.board[0][0], (1, 1))

def test_illegal_rook_diagonal_take():
    board = Board()
    board.seed_starting_board()
    # Setup: Open the A file
    p1 = board.board[1][0]
    if board.can_move(p1, (3, 0)):
        board.move(p1, (3, 0))

    # ILLEGAL TAKE: Rook on A1 tries to capture diagonally like a Bishop to B2
    attacker = board.board[0][0]
    assert not board.take(attacker, (1, 1))


def test_legal_rook_take():
    board = Board()
    board.seed_starting_board()
    # Setup: Move White A2 to A4
    p1 = board.board[1][0]
    if board.can_move(p1, (3, 0)):
        board.move(p1, (3, 0))

    # Setup: Move White Rook A1 to A3
    r1 = board.board[0][0]
    if board.can_move(r1, (2, 0)):
        board.move(r1, (2, 0))

    # Setup: Move Black D7 to D5
    p2 = board.board[6][3]
    if board.can_move(p2, (4, 3)):
        board.move(p2, (4, 3))


    # LEGAL TAKE: Rook on A3 moves horizontally to take Pawn on D3
    # Wait, Rook on A3 (2,0) taking D3 (2,3) assuming the D-pawn moved to D5 (4,3)
    # Let's target the D5 pawn (4,3) by moving Rook to A5 first
    if board.can_move(r1, (2,3)):
        board.move(r1, (2, 3))

    attacker = board.board[2][3]
    assert board.take(attacker, (4, 3))


def test_illegal_rook_teleportation():
    board = Board()
    board.seed_starting_board()
    # Completely random invalid square jump (A1 to G7)
    assert not board.can_move(board.board[0][0], (6, 6))

# ==========================================
# QUEENS (No legal moves in starting pos)
# ==========================================

def test_legal_queen_diagonal_move():
    board = Board()
    board.seed_starting_board()
    # Setup: Move Pawn from E2 to E4 to open the D1 Queen's diagonal path
    assert board.can_move(board.board[1][4], (3, 4))
    board.move(board.board[1][4], (3, 4))

    # LEGAL: Move Queen from D1 to H5
    assert board.can_move(board.board[0][3], (4, 7))


def test_legal_queen_straight_move():
    board = Board()
    board.seed_starting_board()
    # Setup: Move Pawn from D2 to D4 to open the D-file
    assert board.can_move(board.board[1][3], (3, 3))
    board.move(board.board[1][3], (3, 3))

    # LEGAL: Move Queen from D1 to D3
    assert board.can_move(board.board[0][3], (2, 3))

def test_illegal_queen_path_blocked():
    board = Board()
    board.seed_starting_board()
    # Valid straight pattern, but pawn is in the way (D1 to D3)
    assert not board.can_move(board.board[0][3], (2, 3))

def test_illegal_queen_l_shape_move():
    board = Board()
    board.seed_starting_board()
    # Moving in an L-shape like a Knight (D1 to B3)
    assert not board.can_move(board.board[0][3], (2, 1))

def test_illegal_queen_friendly_fire():
    board = Board()
    board.seed_starting_board()
    # Trying to move onto the King's square (D1 to E1)
    assert not board.can_move(board.board[0][3], (0, 4))


def test_legal_queen_take():
    board = Board()
    board.seed_starting_board()
    # Setup: Move White E2 to E4
    p1 = board.board[1][4]
    if board.can_move(p1, (3, 4)):
        board.move(p1, (3, 4))

    # Setup: Move Black H7 to H6
    p2 = board.board[6][7]
    if board.can_move(p2, (5, 7)):
        board.move(p2, (5, 7))

    # LEGAL TAKE: Queen on D1 zips out to take H5 (assuming H-pawn moved there, let's take H6)
    attacker = board.board[0][3]
    # D1 (0,3) to H5 (4,7) is a valid diagonal. Let's assume Black H pawn is on H5 (4,7)
    if board.can_move(p2, (4, 7)):
        board.move(p2, (4, 7))

    assert board.take(attacker, (4, 7))


def test_illegal_queen_knight_take():
    board = Board()
    board.seed_starting_board()
    # ILLEGAL TAKE: Queen on D1 tries to jump in an L-shape to take C3
    attacker = board.board[0][3]
    assert not board.take(attacker, (2, 2))
# ==========================================
# KINGS (No legal moves in starting pos)
# ==========================================

def test_illegal_king_exceed_max_range():
    board = Board()
    board.seed_starting_board()
    # Moving two squares forward (E1 to E3)
    assert not board.can_move(board.board[0][4], (2, 4))

def test_illegal_king_friendly_fire():
    board = Board()
    board.seed_starting_board()
    # Moving onto own pawn's square (E1 to E2)
    assert not board.can_move(board.board[0][4], (1, 4))

def test_illegal_king_l_shape_move():
    board = Board()
    board.seed_starting_board()
    # Moving like a Knight (E1 to C2)
    assert not board.can_move(board.board[0][4], (1, 2))


def test_legal_king_single_step():
    board = Board()
    board.seed_starting_board()
    # Setup: Move Pawn from E2 to E4 to clear the E2 square
    assert board.can_move(board.board[1][4], (3, 4))
    board.move(board.board[1][4], (3, 4))

    # LEGAL: Move King from E1 to E2
    assert board.can_move(board.board[0][4], (1, 4))