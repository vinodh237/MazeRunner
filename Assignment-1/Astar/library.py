from math import sqrt
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors



def mod(x):
    """
    :param x: any number
    :return: |x|
    """
    if x >= 0:
        return x
    else:
        return -x

def ManhattanDistance(x1,y1,x2,y2):
    """
    :param x1: x coordinate of point-1
    :param y1: y coordinate of point-1
    :param x2: x coordinate of point-2
    :param y2: y coordinate of point-2
    :return: Manhattan distance between the points (integer)
    """
    return mod(x1-x2) + mod(y1-y2)

def EuclideanDistance(x1,y1,x2,y2):
    """
    :param x1: x coordinate of point-1
    :param y1: y coordinate of point-1
    :param x2: x coordinate of point-2
    :param y2: y coordinate of point-2
    :return: Euclidean distance between the points (integer)
    """

    return sqrt((x1-x2)**2 + (y1-y2)**2)

def generateMaze(size,prob):
    """

    :param size: length of side a square maze
    :param prob: probability than a cell can be blocked
    :return: generated matrix representation of maze
    """
    maze = np.zeros([size,size],dtype=int)
    for i in range(size):
        for j in range(size):
            if random.randint(1,100) <= 100*prob and not(i==0 and j==0) and not (i==size-1 and j==size-1):
                maze[i,j] = 1
    return maze

# def plotMatrix(mat):
#     ## improvement needed
#     plt.imshow(mat)
#     plt.show()


def plotMatrix(mat,title = "",test = False):
    """

    :param mat: matrix to plot
    :param size: dimension of matrix
    :param title: name of the algorithms used
    :return:
    """
    if test == True:
        return
    size = len(mat)
    mat[0,0] = 4
    mat[len(mat)-1,len(mat)-1] = 4
    cmap = colors.ListedColormap(['lightgray', 'red', 'green', 'yellow'])
    bounds = [0,1,2,3,4]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    plt.matshow(mat,aspect='auto', origin="upper",cmap=cmap,norm=norm, extent=[0,size,size,0])

    plt.grid(b=True, which='major', color ='white')

    plt.title(title)
    plt.xlabel('yDimension: '+str(size) + ' cells')
    plt.ylabel('xDimension: '+str(size) + ' cells')

    clr = plt.colorbar(ticks=[1,2,3,4])
    clr.set_ticklabels(["Unblocked","Blocked","Path", "Starting & Goal cells"])

    plt.tick_params(axis='both', color='white')

    plt.xticks(range(size)," ")
    plt.yticks(range(size)," ")
    plt.show()

def test():
    size = 10
    k = generateMaze(size, 0.1)
    print(k)
    plotMatrix(k)
    print("done")