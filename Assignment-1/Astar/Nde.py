from Astar.library import ManhattanDistance,EuclideanDistance
class node(object):
    def __init__(self,i,j,g,dim,parent=None,isManhattan = True):
        self.i = i
        self.j = j
        self.g = g # cost to reach upto this node
        self.parent = parent
        if isManhattan == True:
            self.value = float(g) + ManhattanDistance(i,j,dim-1,dim-1)
        # else:
        #     self.value = float(g) + EuclideanDistance(i,j,dim-1,dim-1)
