import Astar.library as lib
import Dfs.stk as s
import numpy as np
import time
from Dfs.node import Node


class DFS:
    rows = 0
    columns = 0
    nodesExpanded = 0
    pathLength = 0
    fringeSize = 0
    maze = None
    success = False
    timeTaken = 0.0
    def __init__(self,maze):

        # Define a class which contain the parameters of the solution like nodes expanded, path length and fringe size
        self.maze = maze
        self.threshold_time = 60
        # Calculate the length of the row and the column of the maze

        self.rows = len(maze)
        self.columns = len(maze[0])

        # Calculate the order in which the algorithm will expand its children, so we have chosen the following order
        # up, left, down, right. Since, it is a stack implementation, when we pop the elements the right most element
        # is given preference and would help us in reaching the goal faster

        self.rowTraverse = np.array([-1, 0, 0, 1])
        self.columnTraverse = np.array([0, -1, 1, 0])

        self.startTime = time.time()

        # print(startTime)
        node = Node(0,0,None)                                          # Create the source node
        visited = np.zeros([len(maze), len(maze[0])], dtype=int)       # Create a 2-D array to trace the nodes visited

        self.Search(visited, node)                            # Function to perform DFS operation


        self.endTime = time.time()
        # Calculate the time taken to perform DFS operation
        self.timeTaken = (self.endTime - self.startTime)
        print("Total time taken to perform DFS is:", self.timeTaken, "seconds")
        if self.timeTaken > self.threshold_time:
            self.success = False


    def Search(self, visited, node):
        """

        :param visited: array to keep track of the visisted nodes
        :param node: the source node from where the search would start
        :return: none
        """

        # push the source node into the stack
        stack = s.Stk()
        stack.push(node)

        # The while loop will run until there are no nodes left to be explored
        while len(stack.L)>0 and time.time() - self.startTime < self.threshold_time:

            # Pop each node inside the stack whose children are fully explored
            currentNode = stack.pop()

            # Calculate the size of the fringe which would be the max size of the stack possible
            if (len(stack.L) > self.fringeSize) :
                self.fringeSize = len(stack.L)

            # We define goal at the right bottom corner which is maze[rows - 1][columns - 1]
            if currentNode.x == self.rows - 1 and currentNode.y == self.columns - 1:
                print("Destination Reached")
                self.success = True
                # Trace the shortest path for the algorithm to reach the goal node, by back tracking from the
                # goal node, and also assign the value of 2 for shortest path in the maze to show it in the plot
                while currentNode != None and not (currentNode.x == 0 and currentNode.y == 0):
                    self.maze[currentNode.x][currentNode.y] = 2
                    currentNode = currentNode.parent
                    self.pathLength = self.pathLength + 1

                print("Total number of nodes expanded are", self.nodesExpanded)
                self.pathLength = self.pathLength + 1
                print("Total length of the shortest path is: ", self.pathLength)
                print("Fringe Size is: ", self.fringeSize)
                self.maze[currentNode.x][currentNode.y] = 2
                return

            # Put the children of each node starting from the source node inside the stack and mark them
            # as visited. After that explore the child that was entered last and so on

            for k in range(4):

                if currentNode.x + self.rowTraverse[k] <= self.rows - 1 and currentNode.x + self.rowTraverse[k] >= 0 and \
                currentNode.y + self.columnTraverse[k] <= self.columns - 1 and currentNode.y + self.columnTraverse[k] >= 0 \
                and visited[currentNode.x + self.rowTraverse[k]][currentNode.y + self.columnTraverse[k]] == 0 and \
                self.maze[currentNode.x + self.rowTraverse[k]][currentNode.y + self.columnTraverse[k]] == 0:

                    nextNode = Node(currentNode.x + self.rowTraverse[k], currentNode.y + self.columnTraverse[k], currentNode)

                    stack.push(nextNode)

                    visited[nextNode.x][nextNode.y] = 1
                    self.nodesExpanded = self.nodesExpanded + 1
                    # print(nextNode.x, nextNode.y)

            # If the maze is not solvable
            if len(stack.L) == 0:
                print("Goal node cannot be reached")

# Test Case
# Create and object of DFS class and plot the maze after finding the goal node through DFS algorithm.
# def test():
#     dfs1 = DFS()
#     lib.plotMatrix(maze, dfs1.rows)
#     print("done")
