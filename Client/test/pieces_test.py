from models.Pieces import Pawn, Bishop, Knight, Queen, King, Rook


def test_pawn_can_move():

    p = Pawn((1,1),"white")
    assert p.can_move((2,1)) #normal 1 up
    assert p.can_move((3,1)) # normal 2 up
    assert not p.can_move((1,1)) # no same position
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



def test_bishop_can_move():
    b = Bishop((3,4),"white")
    possible_moves = [(0,1),(1,2),(2,3),(4,5),(5,6),(6,7),(7,0),(6,1),(5,2),(4,3),(2,5),(1,6),(0,7)]
    for i in range(0,8):
        for j in range(0,8):
            if (i,j) in possible_moves:
                assert b.can_move((i,j))
            else:
                assert not b.can_move((i,j))
def test_knight_can_move():
    k = Knight((3,4),"white")
    possible_moves = [(1,3),(2,2),(4,2),(5,3),(5,5),(4,6),(2,6),(1,5)]
    for i in range(0,8):
        for j in range(0,8):
            if (i,j) in possible_moves:
                assert k.can_move((i,j))
            else:
                assert not k.can_move((i,j))

def test_queen_can_move():
    q = Queen((3,4),"white")
    assert q.can_move((2,4))
    assert q.can_move((2,3))
    assert q.can_move((2,5))
    assert q.can_move((3,5))
    assert q.can_move((0,7))
    assert q.can_move((6,7))
    assert q.can_move((0,4))
    assert q.can_move((6,4))
    assert q.can_move((3,1))
    assert q.can_move((3,7))
    assert q.can_move((0,1))
    assert q.can_move((0,7))
    assert not q.can_move((1,3))
    assert not q.can_move((2,1))
    assert not q.can_move((4,6))
    assert not q.can_move((1,7))
    assert not q.can_move((1,1))
    assert not q.can_move((2,7))

def test_king_move():
    k = King((3,4),"white")
    possible_moves = [(2,3),(2,4),(2,5),(3,5),(4,5),(4,4),(4,3),(3,3)]
    for i in range(0,8):
        for j in range(0,8):
            if (i,j) in possible_moves:
                assert k.can_move((i,j))
            else:
                assert not k.can_move((i,j))
def test_rook_move():
    r = Rook((3,4),"white")
    possible_moves = [(2,4),(1,4),(0,4),(4,4),(5,4),(6,4),(7,4),(3,0),(3,1),(3,2),(3,3),(3,5),(3,6),(3,7)]
    for i in range(0,8):
        for j in range(0,8):
            if (i,j) in possible_moves:
                assert r.can_move((i,j))
            else:
                assert not r.can_move((i,j))