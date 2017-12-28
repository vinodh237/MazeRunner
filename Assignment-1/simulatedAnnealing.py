import random,math
from Astar.library import generateMaze
from Dfs.dfs import DFS
from copy import copy
from main import runBfs,runAstar,rundfs
class simAnneal(object):
    def __init__(self,matrix,property):
        self.current_matrix = matrix
        self.dim = len(self.current_matrix)
        self.n = 10000
        self.property = property
        # self.threshold = 0.01
        self.do()

    def do(self):
        # self.current_matrix = self.m
        for i in range(self.n):
            T = self.schedule(i)
            # if T < self.threshold:
            #     return self.current_matrix
            L = self.getneighbours(self.current_matrix)
            n = random.randint(1,len(L))-1
            delta = self.getValue(copy(L[n]),self.property) - self.getValue(copy(self.current_matrix),self.property)
            if delta > 0:
                self.current_matrix = L[n]
            else:
                exponent_value = delta/T
                prob = math.exp(exponent_value)
                if self.decision(prob):
                    self.current_matrix = L[n]

    def getneighbours(self,m):
        """
        :param m: current config
        :return: list of all neighbours according to definition
        """
        L = []
        dim = len(m)
        obsList = []
        for i in range(dim):
            for j in range(dim):
                if m[i,j] == 1:
                    obsList.append([i,j])

        for obs in obsList:
            newState = copy(m)
            i = obs[0]
            j = obs[1]
            newState[i,j] = 0
            b = self.getChildNodes(i,j)
            for k in b:
                newState[k[0],k[1]] = 1
                L.append(copy(newState))
                newState[k[0],k[1]] = 0

        return L

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

    def IsvalidPoint(self,m,n):
        ## return False if point is not in maze limit
        if  m < 0 or n < 0 or m >= self.dim or n >= self.dim or self.current_matrix[m,n] == 1:
            return False
        return True

    def getValue(self,m,property,algo='DFS'):
        ## call the corresponding algorithm
        if algo == 'DFS':
            dfs1 = rundfs(m)
            return dfs1[property]
        if algo == 'BFS':
            bfs = runBfs(m)
            return bfs[property]
        if algo == 'Astar':
            a = runAstar(m, ismanhattan=True)
            return a[property]

    def schedule(self,a):
        return 1.0/(1+math.log2(a+1))

    def decision(self,probability):
        return random.random() < probability
f= open("output/question10",'w')
g1 = generateMaze(size=6,prob=0.1)
g2 = generateMaze(size=6,prob=0.2)
g3 = generateMaze(size=6,prob=0.3)
for algo in ['DFS','BFS','Astar']:
    print("for Algorithm: "+ algo +"\n")
    for property in ['pathLength','nodesExpanded','fringeSize']:
        for g in [g1,g2,g3]:
            sA = simAnneal(g,property=property)
            print("################################################################################################")
            print("################################################################################################")
            print("Actual:"+algo+"##"+ property +"##"+str(sA.getValue(g,property=property))+"\n")
            f.write("Actual:"+algo+"##"+ property +"##"+str(sA.getValue(g,property=property))+"\n")
            print("Now:"+algo+"##"+ property +"##"+str(sA.getValue(sA.current_matrix,property=property))+"\n")
            f.write("Now:"+algo+"##"+ property +"##"+str(sA.getValue(sA.current_matrix,property=property))+"\n")
            print("################################################################################################")
            print("################################################################################################")
f.close()

