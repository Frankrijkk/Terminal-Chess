import math


class Piece:
    def __init__(self,position:tuple[int,int],color:str|None=None):
        if position[0]>7 or position[1]>7 or position[0]<-1 or position[1]<-1:
            raise ValueError(
                "Position must be between 0 and 7"
            )

        self.color:str|None = color
        self.position:list = list(position)
        self.has_moved:bool = False


    def __str__(self):
        return "_"

    def can_move(self,finito:tuple[int,int])->bool:
        print("Can't move a nothing")
        return False


    def can_attack(self,finito:tuple[int,int])->bool:
        return self.can_move(finito)


    def move(self,finito:tuple[int,int]):
        self.position = list(finito)
        self.has_moved = True


    def on_the_way(self,finito:tuple[int,int])->list[tuple[int,int]]:
        difference = [b - a for a, b in zip(self.position, finito)]
        result = []
        N = math.gcd(abs(difference[0]),abs(difference[1]))
        dy = difference[0]//N
        dx = difference[1]//N
        for i in range(1,N+1):
            result.append((self.position[0]+i*dy,self.position[1]+i*dx))
        return result

    def is_piece(self)->bool:
        return False

class King(Piece):
    def __init__(self,position:tuple[int,int],color:str|None=None):
        super().__init__(position,color)
        if self.color not in ["white","black"]:
            raise ValueError(
                "Color must be either white or black"
            )
    def can_move(self,finito:tuple[int,int])->bool:
        difference = [b - a for a, b in zip(self.position, finito)]
        return (abs(difference[0]) == 1 and abs(difference[1]) == 0) or (abs(difference[0]) == 0 and abs(difference[1]) == 1) or (abs(difference[0]) == 1 and abs(difference[1]) ==1)

    def is_piece(self)->bool:
        return True

    def __str__(self):
        return "K"

class Queen(Piece):
    def __init__(self,position:tuple[int,int],color:str|None=None):
        super().__init__(position,color)
        if self.color not in ["white","black"]:
            raise ValueError(
                "Color must be either white or black"
            )
    def can_move(self,finito:tuple[int,int])->bool:
        difference = [b - a for a, b in zip(self.position, finito)]

        return ((difference[0] == 0 and difference[1] != 0) or (difference[1] == 0 and difference[0] != 0)) or (abs(difference[0]) == abs(difference[1]))


    def is_piece(self) -> bool:
        return True
    def __str__(self):
        return "Q"

class Rook(Piece):
    def __init__(self,position:tuple[int,int],color:str|None=None):
        super().__init__(position,color)
        if self.color not in ["white","black"]:
            raise ValueError(
                "Color must be either white or black"
            )
    def can_move(self,finito:tuple[int,int])->bool:
        difference = [b - a for a, b in zip(self.position, finito)]
        return (difference[0] == 0 and  difference[1]!=0) or (difference[1] == 0 and difference[0]!=0)

    def is_piece(self) -> bool:
        return True


    def __str__(self):
        return "R"





class Bishop(Piece):

    def __init__(self,position:tuple[int,int],color:str|None=None):
        super().__init__(position,color)
        if self.color not in ["white","black"]:
            raise ValueError(
                "Color must be either white or black"
            )

    def can_move(self,finito:tuple[int,int])->bool:
        difference = [a - b for a, b in zip(self.position, finito)]
        if difference[0] == 0 and difference[1] == 0:
            return False
        return abs(difference[0]) == abs(difference[1])
        # if the difference (movement vector) in the x and y is in the form of 1,1 2,2 3,3 -3,3 then the bishop can move

    def is_piece(self) -> bool:
        return True

    def __str__(self):
        return "B"


class Knight(Piece):
    def __init__(self,position:tuple[int,int],color:str|None=None):
        super().__init__(position,color)
        if self.color not in ["white","black"]:
            raise ValueError(
                "Color must be either white or black"
            )

    def can_move(self,finito:tuple[int,int])->bool:
        difference = [a - b for a, b in zip(self.position, finito)]
        return (abs(difference[0])==1 and abs(difference[1])==2) or (abs(difference[0])==2 and abs(difference[1])==1)

    def is_piece(self) -> bool:
        return True


    def __str__(self):
        return "N"

class Pawn(Piece):

    def __init__(self,position:tuple[int,int],color:str|None=None):
        super().__init__(position,color)
        if self.color not in ["white","black"]:
            raise ValueError(
                "Color must be either white or black"
            )

    def can_move(self,finito:tuple[int,int])->bool:
        difference = [b - a for a, b in zip(self.position, finito)]
        if difference[1] != 0:
            return False
        if self.color == "white":
            if self.position[0] == 1:
                return difference[0] == 2 or difference[0] == 1
            return difference[0] == 1
        if self.color == "black":
            if self.position[0] == 6:
                return difference[0] == -2 or difference[0] == -1
            return difference[0] == -1
        return False

    def is_piece(self) -> bool:
        return True


    def can_attack(self,finito:tuple[int,int]) ->bool:
        difference = [b - a for a, b in zip(self.position, finito)]
        return abs(difference[0]) == 1 and abs(difference[1]) == 1 or abs(difference[0]) == 1 and abs(difference[1]) == -1

    def __str__(self):
        return "P"

