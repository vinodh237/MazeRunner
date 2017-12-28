from Astar.library import generateMaze,plotMatrix
from Astar.Astar import Astar
from Dfs.dfs import DFS
import Bfs.BFS as b
import Bfs.Points as points
from Astar.genetic import genetic_algorithm
import math

import numpy as np
import matplotlib.pyplot as plot
from copy import copy

def runBfs(maze):
    size = len(maze)
    # define the starting, goal cell and visited matrix
    source = points.Points()
    destination = points.Points()
    source.ptVal(0, 0)  # set start cell to first cell in the maze
    source.distance(0)  # set the distance of start cell from itself to 0
    destination.ptVal(size - 1, size - 1)  # set goal cell to last cell in the maze
    destination.distance(0)  # set the distance of goal cell from start cell to 0
    print("BFS")
    #randomizeBFS: if False, follows optimal strategy to reach goal node
    #if True, time to reach goal node may increase
    randomizeBFS = True
    ans = b.startBFS(maze, source, destination, randomizeBFS,plot=not isTest)
    if(isTest == False):
        plot.show()

    InfoMap = {}

    InfoMap['timeTaken'] = ans['timeTaken']
    InfoMap['success'] = ans['pathExists']
    InfoMap['pathLength'] = ans['distance']
    InfoMap['nodesExpanded'] = ans['numberOfCellsExplored']
    InfoMap['fringeSize'] = ans['fringeSize']

    return InfoMap

def runAstar(maze,ismanhattan = True):
    k = Astar(maze,ismanhattan=ismanhattan)
    if k.success == True:
        plotMatrix(k.getShortestPath(),test=isTest)
    InfoMap = {}
    InfoMap['timeTaken'] = k.timeTaken
    InfoMap['success'] = k.success
    InfoMap['pathLength'] = k.solutionPathLength
    InfoMap['nodesExpanded'] = k.nodesExplored
    InfoMap['fringeSize'] = k.maxFringeSize
    return InfoMap

def rundfs(maze):
    dfs1 = DFS(maze)
    plotMatrix(maze, dfs1.rows,test=isTest)
    InfoMap = {}
    InfoMap['timeTaken'] = dfs1.timeTaken
    InfoMap['success'] = dfs1.success
    InfoMap['pathLength'] = dfs1.pathLength
    InfoMap['nodesExpanded'] = dfs1.nodesExpanded
    InfoMap['fringeSize'] = dfs1.fringeSize
    return InfoMap

def ques1():
    f = open("output/question1","w")
    f.write("A-star\t\t\tBFS\t\t\tDFS\n")
    for j in [0.0,0.05,0.1,0.15,0.2,0.25,0.30,0.35,0.4]: ## for values above path doesn't exist in most of the cases,0.5,0.6,0.7,0.8,0.9
        f.write("------------------- "+ str(j) + " ----------------------------\n")
        for i in [100,200,400,600,800,1000,1200,1400,1600,1800]:
            maze = generateMaze(i,prob=j)
            mapA = runAstar(copy(maze))
            mapB = runBfs(maze=copy(maze))
            # successB = ans['pathExists']
            # timetakenB = ans['timeTaken']
            mapC = rundfs(maze=copy(maze))

            f.write(str(mapA['timeTaken'])+"\t" + str(mapB['timeTaken']) + "\t"+str(mapC['timeTaken']) + "\n")
            f.write(str(mapA['success']) + "\t" + str(mapB['success']) + "\t" + str(mapC['success']) + "\n")
        print("-----------------------------"+str(j)+"----------------------------\n")
        f.write("################################################################\n")
    f.close()

# while debug change this flag to True, it will skip plotting the mazes
isTest = True

def ques2():
    maze = generateMaze(1000, prob=0.2)
    runAstar(copy(maze))

    runBfs(copy(maze))
    rundfs(copy(maze))

def ques3(dim):
# as dfs is fast we cab use it find if path exists or not
    f = open('output/question3_sol','w')
    samples = 100
    for p0 in [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]:
        success_Count = 0
        for i in range(samples):
            maze = generateMaze(size=dim,prob=p0)
            mapD = rundfs(maze)
            if mapD['success'] == True:
                success_Count += 1
        f.write(str(p0)+"------"+str(success_Count)+"\n")
        print(str(p0)+"\n")
    f.close()

def ques4(dim,p0):
    ## DFS doesn't return shortest path
    samples =10
    spacing = 0.05
    total = int(math.ceil(p0/spacing))
    meanValues = np.zeros([total+1,3])
    for i in range(total+1):
        p = i*spacing
        path = np.zeros([samples, 3])
        for j in range(samples):
            currentRow = j
            g = generateMaze(dim,p)
            k1 = runAstar(copy(g))
            path[currentRow,0] = k1['pathLength']
            k2 = runBfs(copy(g))
            path[currentRow,1] = k2['pathLength']
            k3 = rundfs(copy(g))
            path[currentRow,2] = k3['pathLength']
        if nonZeroElements(path[:,0]) >0:
            meanValues[i,0] = np.sum(path[:,0]/nonZeroElements(path[:,0]))
        if nonZeroElements(path[:,1]) >0:
            meanValues[i, 1] = np.sum(path[:,1]/nonZeroElements(path[:,1]))
        if nonZeroElements(path[:,2]) >0:
            meanValues[i, 2] = np.sum(path[:,2]/nonZeroElements(path[:,2]))

    return meanValues

# def ques5(p0):



def ques5(dim, p):
    f = open('output/question5','w+')

    spacing = 0.05
    total = int(math.ceil(p / spacing))
    for i in range(total + 1):
        p0 = i * spacing
        pLength_dfs = 0
        iter_dfs = 0
        pLength_astar_m = 0
        iter_astar_m = 0
        pLength_astar_e = 0
        iter_astar_e = 0

        for j in range(10):
            while True:
                maze = generateMaze(size=dim, prob=p0)
                s = rundfs(copy(maze))
                if s['success'] is True:
                    f.write("DFS")
                    f.write(str(p0) + "------" + str(s) + "\n")
                    pLength_dfs += s['pathLength']
                    iter_dfs += 1
                    break

            isManhattan = True
            a = runAstar(copy(maze), isManhattan)

            if a['success'] is True:
                f.write("A*-Manhattan")
                f.write(str(p0) + "------" + str(a) + "\n")
                pLength_astar_m += a['pathLength']
                iter_astar_m += 1

            isManhattan = False
            a = runAstar(copy(maze), isManhattan)

            if a['success'] is True:
                f.write("A*-Euclidean")
                f.write(str(p0) + "------" + str(a) + "\n")
                pLength_astar_e += a['pathLength']
                iter_astar_e += 1


        mean_dfs = pLength_dfs/iter_dfs
        mean_astar_m = pLength_astar_m/iter_astar_m
        mean_astar_e = pLength_astar_e / iter_astar_e

        f.write("average path length(A*-Manhattan): " + str(mean_astar_m))
        f.write("average path length(A*-Euclidean): " + str(mean_astar_e))
        f.write("average path length(DFS): "+str(mean_dfs))
    f.writable()

    f.close()
ques5(100, 0.3)

def ques6(dim,p):
    # spacing = 0.05
    # total = int(math.ceil(p0 / spacing))
    # for i in range(total+1):
    #     p = i*spacing
    #     g = generateMaze(dim,p)
    #     runAstar(copy(g))
    #     runBfs(copy(g))
    #     rundfs(copy(g))
    f = open('output/question6_1','w+')


    spacing = 0.05
    total = int(math.ceil(p / spacing))
    for i in range(total + 1):
        nodes_astar_m = 0
        iter_astar_m = 0
        nodes_astar_e = 0
        iter_astar_e = 0
        for j in range(10):
            p0 = i * spacing
            while True:
                isManhattan = True
                maze = generateMaze(size=dim, prob=p0)
                a = runAstar(copy(maze), isManhattan)
                if a['success'] is True:
                    f.write("A*-Manhattan")
                    f.write(str(p0) + "------" + str(a) + "\n")
                    nodes_astar_m += a['nodesExpanded']
                    iter_astar_m += 1
                    break


            isManhattan = False
            a = runAstar(copy(maze), isManhattan)

            if a['success'] is True:
                f.write("A*-Euclidean")
                f.write(str(p0) + "------" + str(a) + "\n")
                nodes_astar_e += a['nodesExpanded']
                iter_astar_e += 1


        mean_astar_m = nodes_astar_m/iter_astar_m
        mean_astar_e = nodes_astar_e / iter_astar_e

        f.write("average nodes expanded(A*-Manhattan): " + str(mean_astar_m))
        f.write("average nodes expanded(A*-Euclidean): " + str(mean_astar_e)+"\n")
    f.writable()

    f.close()
# ques6(100, 0.3)

def ques7(dim, p):

    f = open('output/question7', 'w+')

    spacing = 0.05
    total = int(math.ceil(p / spacing))
    for i in range(total + 1):
        nodes_dfs = nodes_bfs = 0
        iter_dfs = iter_bfs = 0
        nodes_astar_m = 0
        iter_astar_m = 0

        for j in range(10):
             p0 = i * spacing
             while True:
                 maze = generateMaze(size=dim, prob=p0)
                 s = rundfs(copy(maze))
                 if s['success'] is True:
                     f.write("DFS")
                     f.write(str(p0) + "------" + str(s) + "\n")
                     nodes_dfs += s['nodesExpanded']
                     iter_dfs += 1
                     break

             b = runBfs(copy(maze))
             if b['success'] is True:
                 f.write("BFS")
                 f.write(str(p0) + "------" + str(b) + "\n")
                 nodes_bfs += b['nodesExpanded']
                 iter_bfs += 1

             isManhattan = True
             a = runAstar(copy(maze), isManhattan)
             if a['success'] is True:
                 f.write("A*-Manhattan")
                 f.write(str(p0) + "------" + str(a) + "\n")
                 nodes_astar_m += a['nodesExpanded']
                 iter_astar_m += 1

        mean_dfs = nodes_dfs/iter_dfs
        mean_bfs = nodes_bfs/iter_bfs
        mean_astar_m = nodes_astar_m/iter_astar_m

        f.write("average nodes expanded(DFS): " + str(mean_dfs))
        f.write("average nodes expanded(BFS): " + str(mean_bfs)+"\n")
        f.write("average nodes expanded(A*-Manhattan): " + str(mean_astar_m))

    f.writable()
    f.close()

def nonZeroElements(a):
    return len(np.nonzero(a)[0])

def Ques10():
    """

    :return:
    """
    results = genetic_algorithm()
    print(results)

Ques10()

# ques4(dim=100,p0 = 1.0)
isTest = False
# maze = generateMaze(100,0.0)
# runAstar(maze=maze,ismanhattan=False)

# ques3(dim=1000)