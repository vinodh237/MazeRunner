import Bfs.library as mz
import numpy as np
import Bfs.que as Q
from Bfs.Points import Points
import time
import random

# Parameters

# step count, Down, Right, Up and Left movement(optimized precedence order) & count of possible directions
step = 1
rowMov = [0, step, -step, 0]
colMov = [step, 0, 0, -step]
possibleDirections = 4
randomOrder = [0, 1, 2, 3]


# Member Variables


# keeps track of all the cells visited
# visited = np.zeros([size, size], dtype=int)

# keeps track of cells that are to be explored
explored = Q.queue()

# UnBlocked, Blocked, Path, Visited
isUnblocked = 0
isBlocked = 1
inPath = 2
isSeen = True
start_goal = 4

# FringeSize, max size of queue possible
fringeSize = 0
numberOfCellsExplored = 0

# Time Limit of 60 seconds
timeLimit = 60

# Functions

# to validate if the coordinates of a cell are within the maze or not
def validate(s, x, y):
    """

    :param s: size of the maze
    :param x: x-coordinate of the cell
    :param y: y-coordinate of the cell
    :return: whether a cell is within the limits of the maze or not
    """
    if (x >= 0 and x < s and y >= 0 and y < s):
        return True
    else:
        return False

def markPath(maze, source, node):
    while node is not source:
        maze[node.i][node.j] = inPath
        node = node.parent

    maze[node.i][node.j] = inPath


# to perform Breadth-First-Search on the given matrix
def BFS(maze, size, source, destination):
    """

    :param maze: the maze matrix
    :param source: source cell
    :param destination: destinationination cell
    :return: whether a valid path from source to goal node exists or not
    """
    statistics = {
        "fringeSize":0,
        "numberOfCellsExplored": 0,
        "pathExists": False,
        "timeTaken": 0,
        "distance": 0
    }
    # startTime = datetime.datetime.now().second
    startTime = time.time()

    visited = np.zeros([size, size], dtype=bool)
    visited[source.i][source.j] = isSeen

    explored = Q.queue()
    explored.enque(source)
    statistics["fringeSize"] = explored.size()

    while len(explored.L) > 0:

        # currentTime = datetime.datetime.now().second
        currentTime = time.time()

        statistics["timeTaken"] = (currentTime - startTime)
        if (statistics["timeTaken"] > timeLimit):
            return statistics

        node = explored.top()

        if (node.i == destination.i and node.j == destination.j):
            destination.distance(node.dist)
            statistics["distance"] = node.dist
            statistics["timeTaken"] = (currentTime - startTime)
            markPath(maze, source, node)
            statistics["pathExists"] = True #if a path is found
            return statistics

        else:

            node = explored.deque()

            for k in range(possibleDirections):
                #adjacent Nodes to the current node
                adjNode = Points()
                adjNode.ptVal(node.i + rowMov[randomOrder[k]], node.j + colMov[randomOrder[k]])

                if (validate(size, adjNode.i, adjNode.j)):
                    if (not maze[adjNode.i][adjNode.j]
                        and not visited[adjNode.i][adjNode.j]):
                        adjNode.parent(node)
                        adjNode.distance(node.dist + step)
                        visited[adjNode.i][adjNode.j] = isSeen
                        explored.enque(adjNode)
                        statistics["numberOfCellsExplored"] += 1
                        statistics["fringeSize"] = explored.size() if statistics["fringeSize"]<explored.size() \
                            else statistics["fringeSize"]

    markPath(maze, source, node)
    return statistics    #if no possible path found


# generate maze
# maze = mz.generateMaze(size, p)

# call BFS on the maze
def startBFS(maze, source, destination, randomizeBFS,plot=True):

    size = len(maze)

    if randomizeBFS:
        random.shuffle(randomOrder)

    ans = BFS(maze, size, source, destination)

    # start and goal nodes to be represented with different colors
    maze[0][0] = maze[size-1][size-1] = start_goal

    if ans["timeTaken"]>60:
        print("Goal cannot be reached within the specified Time Limit.")

    if ans["pathExists"] == True:
        print("Distance from Starting cell: ", ans["distance"])
        print("No of cells explored: ", ans["numberOfCellsExplored"])
        print("Max Queue Size required: ", ans["fringeSize"])
        print("Path searched in: ", ans["timeTaken"], " seconds")
        if plot== True:
            mz.plotMatrix(maze, size, 'Breadth First Search')
    else:
        if plot == True:# ans["pathExists"] == False:
            print("No path from start to goal node exists")

    return ans

