from Astar.library import generateMaze,plotMatrix
import numpy as np
from Astar.MHeap import mHeap
from Astar.Nde import node
import time
import numpy as np
from math import sqrt

class Astar(object):

    def __init__(self,G,ismanhattan = True,isOptimizeEucledian = False):

        ## Parameters
        self.ismanhattanDistance = ismanhattan
        self.timeLimit = 60

        ## Variables
        self.matrix = G
        self.Visited = np.zeros_like(G) #0-- not visited , 1-- visited , 2-- finished
        self.dim = len(G)
        self.priorityQueue = mHeap()
        self.destinationNode = None

        self.E = np.zeros([self.dim, self.dim])
        if ismanhattan == False and isOptimizeEucledian == True:
            self.makeE()

        # Useful information
        self.success = False
        self.solutionPathLength = 0
        self.timeTaken= 0.0
        self.maxFringeSize = 0.0
        self.nodesExplored = 0.0

        self.explore()

    def explore(self):
        """

        :return: True , if the algorithm is succesful in reaching
                    the goal state in the given time else False
        """
        i = 0
        j = 0
        startTime = time.time()
        currentTime = time.time()
        self.priorityQueue.insert(node(i,j,g=0,dim = self.dim,isManhattan =self.ismanhattanDistance))
        self.maxFringeSize = len(self.priorityQueue.L)
        self.nodesExplored += 1 ## updating nodes explored
        while(len(self.priorityQueue.L) > 1 and self.timeTaken <= 60 ):
            current_pos = self.priorityQueue.popMin()
            i = current_pos.i
            j = current_pos.j
            if i == self.dim-1 and j == self.dim-1:
                self.solutionPathLength = current_pos.value
                self.success = True
                self.destinationNode = current_pos
                print("goal achieved!!")
                break
            children = self.getChildNodes(i,j)
            count = 0
            for child in children:
                if self.Visited[child[0],child[1]] == 0:
                    self.Visited[child[0], child[1]] = 1
                    self.nodesExplored += 1   ## updating nodes explored
                    n = node(child[0],child[1],g=current_pos.g+1,
                                                    dim = self.dim,parent=current_pos,
                                                     isManhattan =self.ismanhattanDistance)
                    if self.ismanhattanDistance == False:
                        n.value = self.E[child[0],child[1]]
                    self.priorityQueue.insert(
                                                n
                                              )
                    count +=1
            ## update maxfringe size if it less than the current queue size
            if self.maxFringeSize < len(self.priorityQueue.L):
                self.maxFringeSize = len(self.priorityQueue.L)
            currentTime = time.time()
            # if count ==0:
            #     self.Visited[i,j] = 2
            # child = self.priorityQueue.popMin()
            self.timeTaken = currentTime - startTime
        if len(self.priorityQueue.L) <= 1 or currentTime - startTime > 60:
            print("failed and time taken : "+ str(currentTime -startTime))
            return False
        else:
            print("time taken:" + str(currentTime - startTime))
            return True

    def getChildNodes(self, a,b):
        """

        :param a: row of the node
        :param b: column of the node
        :return: list of indexes of child nodes
        """
        children = []
        L = []
        ## adding all possible neighbours to a list
        L.append([a - 1, b])
        L.append([a + 1, b])
        L.append([a, b - 1])
        L.append([a, b + 1])
        for m, n in L:
            ## check whether each point is a valid neighbour or not
            if self.IsvalidPoint(m, n) == True:
                children.append([m, n])
        return children

    def makeE(self):
        for i in range(self.dim):
            for j in range(self.dim):
                self.E[i, j] = sqrt((self.dim - i) ** 2 + (self.dim - j) ** 2)

    def getShortestPath(self):
        """

        :return: returns shortest path in a matrix form
                        where path nodes are '1' and remaining are zero
        """
        i  = self.dim -1
        j  = self.dim -1
        currentNode = self.destinationNode
        shortestPathMatrix = self.matrix
        while currentNode.i !=0 or currentNode.j !=0:
            shortestPathMatrix[currentNode.i,currentNode.j] = 2
            currentNode = currentNode.parent
        shortestPathMatrix[0,0] = 2
        return shortestPathMatrix

    def getValue(self):
        count = 0
        # flatten and then count len(y[y==1])
        for i in range(self.dim):
            for j in range(self.dim):
                if self.Visited[i,j] == 1:
                    count += 1
        return count

    def IsvalidPoint(self,m,n):
        ## return False if point is not in maze limit
        if  m < 0 or n < 0 or m >= self.dim or n >= self.dim or self.matrix[m,n] == 1:
            return False
        return True

def test():
    g = generateMaze(10,0.0)
    k = Astar(g,ismanhattan=True)
    if k.success == True:
        plotMatrix(k.getShortestPath())
# test()