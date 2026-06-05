from MoveParser import MoveParser, Move, InvalidMove, Castle
from models.Pieces import Pawn, Queen, Knight, Rook, Bishop


def test_normal_double_pawn_move():
    moveparser = MoveParser()

    move = moveparser.parse("e4","white")

    assert isinstance(move,Move)
    assert isinstance(move.piece, Pawn)  and move.piece.color == "white" #found the right piece
    assert move.finito == (3, 4)  #found the right move
    assert move.is_attacking == False #not attacking


import pytest


# Assuming your classes are imported, e.g.:
# from chess_parser import MoveParser, Move, Castle, InvalidMove
# from pieces import Piece, Pawn, Knight, Bishop, Rook, Queen, King

def test_standard_piece_move():
    parser = MoveParser()
    move = parser.parse("Nf3", "white")

    assert isinstance(move, Move)
    assert isinstance(move.piece, Knight)
    assert move.piece.color == "white"
    assert move.finito == (2, 5)  # Rank 3 (index 2), File F (index 5)
    assert move.is_attacking is False
    assert move.is_check is False
    assert move.promotes_to is None


def test_standard_capture():
    parser = MoveParser()
    move = parser.parse("Bxc4", "black")
    assert isinstance(move, Move)
    assert isinstance(move.piece, Bishop)
    assert move.finito == (3, 2)  # Rank 4 (index 3), File C (index 2)
    assert move.is_attacking is True


def test_pawn_capture_with_disambiguation():
    parser = MoveParser()
    move = parser.parse("exd5", "white")
    assert isinstance(move, Move)
    assert isinstance(move.piece, Pawn)
    assert move.finito == (4, 3)  # Rank 5 (index 4), File D (index 3)
    assert move.is_attacking is True
    # If your parser handles start_pos for pawn captures:
    # assert move.start_pos[1] == 4  # File E is index 4


def test_move_with_check():
    parser = MoveParser()
    move = parser.parse("Qa4+", "black")
    assert isinstance(move, Move)
    assert isinstance(move.piece, Queen)
    assert move.finito == (3, 0)  # Rank 4 (index 3), File A (index 0)
    assert move.is_check is True
    assert move.is_mate is False


def test_move_with_mate():
    parser = MoveParser()
    move = parser.parse("Rh8#", "white")
    assert isinstance(move, Move)
    assert isinstance(move.piece, Rook)
    assert move.finito == (7, 7)  # Rank 8 (index 7), File H (index 7)
    assert move.is_mate is True
    # In notation, # replaces +, so is_check might be False depending on how you parse.
    # Usually, mate implies check, but strictly checking the string flags:
    assert move.is_check is False


def test_pawn_promotion():
    parser = MoveParser()
    move = parser.parse("e8=Q", "white")
    assert isinstance(move, Move)
    assert isinstance(move.piece, Pawn)
    assert move.finito == (7, 4)  # Rank 8 (index 7), File E (index 4)
    assert move.is_attacking is False
    assert isinstance(move.promotes_to, Queen)


def test_the_kitchen_sink():
    parser = MoveParser()
    move = parser.parse("exf8=N#", "white")
    assert isinstance(move, Move)
    assert isinstance(move.piece, Pawn)
    assert move.finito == (7, 5)  # Rank 8 (index 7), File F (index 5)
    assert move.is_attacking is True
    assert isinstance(move.promotes_to, Knight)
    assert move.is_mate is True


def test_full_disambiguation():
    parser = MoveParser()
    move = parser.parse("Qh4e1", "black")
    assert isinstance(move, Move)
    assert isinstance(move.piece, Queen)
    assert move.finito == (0, 4)  # Rank 1 (index 0), File E (index 4)
    if move.start_pos:  # If your code sets starting positions fully
        assert move.start_pos == (3, 7)  # Rank 4 (index 3), File H (index 7)


def test_castling_kingside():
    parser = MoveParser()
    move = parser.parse("O-O", "white")

    # Castling returns a Castle object, not a Move object
    assert isinstance(move, Castle)
    # Assuming your Castle object takes (is_kingside, color)
    assert move.color == "white"
    assert move.is_king_side is True
    # Replace with whatever your Castle class fields actually are:
    # assert move.is_kingside == True


def test_invalid_move_faceless_capture():
    parser = MoveParser()

    # A pawn capture MUST have a starting file (e.g., exd4, not xd4)
    with pytest.raises(InvalidMove):
        parser.parse("xe4", "white")


def test_invalid_move_non_pawn_promotion():
    parser = MoveParser()

    # A Queen cannot promote into a Rook
    with pytest.raises(InvalidMove):
        parser.parse("Qe8=R", "black")





def test_invalid_zero_distance_move():
    parser = MoveParser()

    # Skipping a turn by moving a piece to the exact square it is already on is illegal.
    with pytest.raises(InvalidMove):
        parser.parse("Qe4e4", "white")


def test_invalid_unpromoted_pawn_on_final_rank():
    parser = MoveParser()

    # Pawns landing on the 1st or 8th rank MUST promote.
    # Just "e8" without a promotion piece (like =Q) is an illegal move state.
    with pytest.raises(InvalidMove):
        parser.parse("e8", "white")