import pytest
from Pieces import Pawn


def test_pawn_move():
    p = Pawn((1,1),"white")
    assert p.can_move((2,1)) #normal 1 up
    assert p.can_move((3,1)) # normal 2 up
    assert not p.can_move((1,1)) # no same position'
    assert not p.can_move((4,1)) # no 3 up
    assert not p.can_move((1,2)) # no sideways
    assert not p.can_move((1,0)) # no down
    assert not p.can_move((2,2)) # no diagonal
    p2 = Pawn((2,3),"white")
    assert p2.can_move((3,3)) # normal 1 up
    assert not p2.can_move((4,3)) # no 2 up


    pb = Pawn((6,1),"black")
    assert pb.can_move((5,1)) # normal 1 down
    assert pb.can_move((4,1)) # normal 2 down
    assert not pb.can_move((6,1)) # no same position
    assert not pb.can_move((3,1)) # no 3 down
    assert not pb.can_move((7,1)) # no up
    assert not pb.can_move((6,2)) # no diagonal
    assert not pb.can_move((7,1)) # no sideways
    pb2 = Pawn((5,2),"black")
    assert pb2.can_move((4,2))
    assert not pb2.can_move((3,2))