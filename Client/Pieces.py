

class Piece:
    def __init__(self,position:tuple[int,int],color:str|None=None):
        if position[0]>7 or position[1]>7 or position[0]<0 or position[1]<0:
            raise ValueError(
                "Position must be between 0 and 7"
            )

        self.color:str|None = color
        self.position:list = list(position)


    def can_move(self,finito:tuple[int,int])->bool:
        print("Can't move a nothing")
        raise ValueError("Can't move a nothing")

    def can_attack(self,finito:tuple[int,int])->bool:
        print(f"Can't atttack with a nothing")
        raise  ValueError("can' attack with a nothing")

    def move(self,finito:tuple[int,int]):
            self.position = list(finito)


class King(Piece):
    def __init__(self,position:tuple[int,int],color:str|None=None):
        super().__init__(position,color)
        if self.color not in ["white","black"]:
            raise ValueError(
                "Color must be either white or black"
            )
    def can_move(self,finito:tuple[int,int])->bool:
        difference = [a - b for a, b in zip(self.position, finito)]
        return (abs(difference[0]) == 1 and abs(difference[1]) == 0) or (abs(difference[0]) == 0 and abs(difference[1]) == 1) or (abs(difference[0]) == 1 and abs(difference[1]) ==1)


class Queen(Piece):
    def __init__(self,position:tuple[int,int],color:str|None=None):
        super().__init__(position,color)
        if self.color not in ["white","black"]:
            raise ValueError(
                "Color must be either white or black"
            )
    def can_move(self,finito:tuple[int,int])->bool:
        difference = [a - b for a, b in zip(self.position, finito)]

        return ((difference[0] == 0 and difference[1] != 0) or (difference[1] == 0 and difference[0] != 0)) or (abs(difference[0]) == abs(difference[1]))



class Rook(Piece):
    def __init__(self,position:tuple[int,int],color:str|None=None):
        super().__init__(position,color)
        if self.color not in ["white","black"]:
            raise ValueError(
                "Color must be either white or black"
            )
    def can_move(self,finito:tuple[int,int])->bool:
        difference = [a - b for a, b in zip(self.position, finito)]
        return (difference[0] == 0 and  difference[1]!=0) or (difference[1] == 0 and difference[0]!=0)


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
            return
        return abs(difference[0]) == abs(difference[1])
        # if the difference (movement vector) in the x and y is in the form of 1,1 2,2 3,3 -3,3 then the bishop can move



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