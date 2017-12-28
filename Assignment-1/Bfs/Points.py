# stores attributes for each cell
class Points:
    def __init__(self):
        self.i = -1
        self.j = -1
        self.dist = 0
# coordinates for the cell
    def ptVal(self, a,b):
        self.i = a
        self.j = b
# parent cell of the cell
    def parent(self, par):
        self.parent = par
# distance from starting cell
    def distance(self, d):
        self.dist = d
# print the coordinates of the cell
    def print(self):
        print("x:", self.i, end=" ")
        print("y:", self.j, end=" ")
