from Astar.library import generateMaze,plotMatrix
from Astar.Astar import Astar
from Dfs.dfs import DFS
import Bfs.BFS as b
import Bfs.Points as points

from math import sqrt
import random
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib.pyplot as plot
import copy


POPULATION_SIZE = 10
DIMENSION_SIZE = 10
NUM_WALLS = 20
NUM_GENERATIONS = 10
START_NODE = 0
DEST_NODE = DIMENSION_SIZE - 1
MAX_NON_IMPROVEMENT_ITERATIONS = 3
MUTATION_PROBABILITY = 0.2
SEARCH_TYPE = {
    "DFS":1,
    "BFS":2,
    "AStarEuclid":3,
    "AStarManhattan":4
}

isTest = True

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

def generate_random_mazes(population_size, num_walls, dimension_size):
    """
    Generates the intial population required for Genetic Algorithm with fixed number of blockages
    :param population_size: Number of mazes to generated
    :param num_walls: Number of blockages per maze
    :return:
    """
    generated_mazes = []
    for generation in range(population_size):
        maze = np.zeros([dimension_size, dimension_size], dtype=int)
        c = 0
        while (c<num_walls):
            x_coordinate = random.randint(0, DIMENSION_SIZE - 1)
            y_coordinate = random.randint(0, DIMENSION_SIZE - 1)
            if not ((x_coordinate == START_NODE and y_coordinate == START_NODE) or (
                            x_coordinate == DEST_NODE and y_coordinate == DEST_NODE)) and \
                            maze[x_coordinate,y_coordinate] == 0:
                maze[x_coordinate,y_coordinate] = 1
                c+=1
        generated_mazes.append({
            "maze": maze
        })
    return generated_mazes

def search_algorithm(maze,search_type):
    """
    Returns the Statistics returned from appropiate search types
    :param maze: maze on which search algorithm to be run
    :param search_type: Search Types
    :return:
    """
    output = {
        "is_path_exists":False,
        "path_length":0,
        "nodes_expanded":0,
        "fringe_length":0
    }
    if search_type == SEARCH_TYPE["AStarEuclid"]:
        result = runAstar(copy.copy(maze['maze']),False)
    elif search_type == SEARCH_TYPE["AStarManhattan"]:
        result = runAstar(copy.copy(maze['maze']), True)
    elif search_type == SEARCH_TYPE["DFS"]:
        result = rundfs(copy.copy(maze['maze']))
    elif search_type == SEARCH_TYPE["BFS"]:
        result = runBfs(copy.copy(maze['maze']))
    output["is_path_exists"] = result["success"]
    output["path_length"] = result["pathLength"]
    output["nodes_expanded"] = result["nodesExpanded"]
    output["fringe_length"] = result["fringeSize"]
    return output


def crossover(maze_1, maze_2):
    """
    Cross Overs the Two mazes to produce a single maze based on choosen value to split
    :param maze_1: Maze to be reproduced
    :param maze_2: Maze to be reproduced with
    :return:
    """
    maze_1_list = [] # Holds the Blockages in Maze 1 Which are not in Maze2
    maze_2_list = [] # Holds the Blockages in Maze 2 Which are not in Maze1
    result_maze = np.zeros([DIMENSION_SIZE, DIMENSION_SIZE], dtype=int) # Resultant Maze
    for i in range(DIMENSION_SIZE):
        for j in range(DIMENSION_SIZE):
            if maze_1['maze'][i][j] == 1 and maze_2['maze'][i][j] == 1: # Common Blockages are directly put it into resultant maze
                result_maze[i][j] = 1
            elif maze_1['maze'][i][j] == 1: # Stores the blockages in Maze 1 and Not in Maze2
                maze_1_list.append((i,j))
            elif maze_2['maze'][i][j] == 1: # Stores the blockages in Maze 2 and Not in Maze1
                maze_2_list.append((i, j))
    if len(maze_1_list)!=0:
        c = random.randint(0,len(maze_1_list)) # Randomly selects a number to split  maze_1_list and maze_2_list
        i = 0
        while(i<c):
            result_maze[maze_1_list[i][0],maze_1_list[i][1]] = 1 # Copying first C values from Maze_1_list to resultant maze
            i+=1
        i = c
        while i<len(maze_2_list): # # Copying values C+1 to end of the list from Maze_2_list to resultant maze
            result_maze[maze_2_list[i][0], maze_2_list[i][1]] = 1
            i+=1
    return result_maze


def mutate(maze):
    """
    Randomly Selects a Position -> Unblocks it -> Blocks Some other location
    :param maze:
    :return:
    """
    maze_list = []
    for i in range(DIMENSION_SIZE):
        for j in range(DIMENSION_SIZE):
            if maze['maze'][i][j] == 1:
                maze_list.append((i,j))
    c = random.randint(0, len(maze_list)-1) # Randomly selects a position to mutate
    while (1):
        x_coordinate = random.randint(0, DIMENSION_SIZE - 1)
        y_coordinate = random.randint(0, DIMENSION_SIZE - 1)
        if not ((x_coordinate == START_NODE and y_coordinate == START_NODE) or (x_coordinate == DEST_NODE and y_coordinate == DEST_NODE)) and \
                        maze['maze'][x_coordinate][y_coordinate] == 0:
            maze['maze'][x_coordinate][y_coordinate] = 1
            break
    maze['maze'][maze_list[c][0],maze_list[c][1]] = 0
    return maze

def genetic_alogirthm_shortest_path(intial_population,search_type):
    """
     Maximises the Shortest Path
    :param intial_population: population set to begin with
    :param search_type: search types like DFS, BFS, A*
    :return: Returns the Final Iteration set of Population and Maximum Value and Termination Reason
    """

    previous_iter_fitness_value = 0 # Used to track previous iteration maximum fitness value
    non_improvement_iterations = 0 # Used to track the number of iterations without improvement in fitness value
    hard_maze = None # Stores the hard_maze in each iteration
    max_achieved_so_far = 0
    hardest_maze_so_far = None
    max_intial_fitness = 0 # Stores Initial Fitness Vlaue before applying genetic algorithm
    intial_maze = None
    for generation in range(NUM_GENERATIONS):
        total_fitness_value = 0 # Used to compute the probability of each maze based on Fitness Value
        new_maze_population = [] #Used to Store New Set of Maze Population required for Next Iteration
        max_fitness_value = 0 # Tracks max fitness value in each iteration
        current_maze_index = 0
        indexes_to_be_deleted = [] # Stores the mazes that need to be deleted beacause they are unsolvable
        # For each we compute the fitness value
        for maze in intial_population:
            search_result = search_algorithm(maze,search_type) #calls appropriate search algorithm based on search type
            if search_result["is_path_exists"]: # To check if  a maze is solvable or not
                maze["fitness_value"] = search_result["path_length"]
            else:
                indexes_to_be_deleted.append(current_maze_index) # Keeps tracks of unsolvable mazes
                continue
            # Checks max fitness value in current population and stores in hard_maze
            if maze['fitness_value'] > max_fitness_value:
                max_fitness_value = maze['fitness_value']
                hard_maze = maze["maze"]
            # Total Fitness Value is calculated to determine the probability of each maze
            total_fitness_value += maze["fitness_value"]
            current_maze_index+=1
        if generation == 0: # Only first generation is considered
            max_intial_fitness = max_fitness_value
            intial_maze = copy.copy(hard_maze)
        # Deletes the Unsolvable mazes from intial population
        for item in indexes_to_be_deleted:
            del intial_population[item]
        # print("previos", previous_iter_fitness_value, " current", max_fitness_value)
        if max_fitness_value > max_achieved_so_far:
            max_achieved_so_far = max_fitness_value
            hardest_maze_so_far = copy.copy(hard_maze)
        if previous_iter_fitness_value >= max_fitness_value and max_fitness_value !=0:
            non_improvement_iterations += 1 # To check if there are successive iterations with no change in fitness value
            if non_improvement_iterations >= MAX_NON_IMPROVEMENT_ITERATIONS: # Returns the Current Solution if the max number of non improved successive iterations
                return {"reason": "Terminated Due to Max Number of Iterations without improvement",
                        "max_fitness_value": max_fitness_value,"hard_maze":hard_maze,"max_intial_fitness":max_intial_fitness,"max_achieved_so_far":max_achieved_so_far,"hardest_maze_so_far":hardest_maze_so_far,"intial_maze":intial_maze}
        else:
            # print("increased", max_fitness_value)
            non_improvement_iterations = 0 # Resets non improved successive iterations to zero if the current iteration fitness value differs from preceding iteration
        previous_iter_fitness_value = max_fitness_value
        for maze in intial_population: # calculates the probability of each maze
            maze["fitness_probability"] = maze["fitness_value"] / total_fitness_value
        for parent_maze in intial_population: # For Selecting Two states randomly based on probability distribution # Selection Process
            random_1 = random.random()
            random_2 = random.random()
            intial_start = 0
            pair_1 = None
            pair_2 = None
            for maze in intial_population:
                intial_end = intial_start + maze["fitness_probability"]
                if random_1 > intial_start and random_1 <= intial_end:
                    pair_1 = maze
                if random_2 > intial_start and random_2 <= intial_end:
                    pair_2 = maze
                if pair_1 and pair_2:
                    new_maze = {'maze': crossover(pair_1, pair_2)} #Crossovers the Two selected states to produce 1 output states
                    if random.randint(0, 1) < MUTATION_PROBABILITY:
                        new_maze = mutate(new_maze) # Mutates a single blockage( Wall)
                    new_maze_population.append(new_maze) # Appends the new maze generated after crossover and mutation to use for next iterations
                    break
                intial_start = intial_end
        intial_population = new_maze_population # To pass the newly generated mazes to next iteration
    max_fitness_value = 0
    hard_maze = None
    # Calculates the maximum fitness and hard maze after the maximum number of iterations are reached
    for individual in intial_population:
        search_result = search_algorithm(individual, search_type)
        if search_result["is_path_exists"] and max_fitness_value < search_result["path_length"]:
            max_fitness_value = search_result["path_length"]
            hard_maze = individual
    if max_achieved_so_far < max_fitness_value:
        max_achieved_so_far = max_fitness_value
        hardest_maze_so_far = copy.copy(hard_maze)
    #Returns after termination condition
    return {"reason": "Terminated due to Max Iterations",
            "max_fitness_value": max_fitness_value,"hard_maze":hard_maze,"max_intial_fitness":max_intial_fitness,"max_achieved_so_far":max_achieved_so_far,"hardest_maze_so_far":hardest_maze_so_far,"intial_maze":intial_maze}


def genetic_alogirthm_nodes_expanded(intial_population, search_type):
    """
     Maximises the Nodes Explored
    :param intial_population: population set to begin with
    :param search_type: search types like DFS, BFS, A*
    :return: Returns the Final Iteration set of Population and Maxium Value and Termination Reason
    """

    previous_iter_fitness_value = 0  # Used to track previous iteration maximum fitness value
    non_improvement_iterations = 0  # Used to track the number of iterations without improvement in fitness value
    hard_maze = None  # Stores the hard_maze in each iteration
    max_intial_fitness = 0 # Stores Initial Fitness Value before applying genetic algorithm
    max_achieved_so_far = 0
    hardest_maze_so_far = None
    intial_maze = None
    for generation in range(NUM_GENERATIONS):
        total_fitness_value = 0  # Used to compute the probability of each maze based on Fitness Value
        new_maze_population = []  # Used to Store New Set of Maze Population required for Next Iteration
        max_fitness_value = 0  # Tracks max fitness value in each iteration
        current_maze_index = 0
        indexes_to_be_deleted = []  # Stores the mazes that need to be deleted beacause they are unsolvable
        # For each we compute the fitness value
        for maze in intial_population:
            search_result = search_algorithm(maze,
                                             search_type)  # calls appropriate search algorithm based on search type
            if search_result["is_path_exists"]:  # To check if  a maze is solvable or not
                maze["fitness_value"] = search_result["nodes_expanded"]
            else:
                indexes_to_be_deleted.append(current_maze_index)  # Keeps tracks of unsolvable mazes
                continue
            # Checks max fitness value in current population and stores in hard_maze
            if maze['fitness_value'] > max_fitness_value:
                max_fitness_value = maze['fitness_value']
                hard_maze = maze["maze"]
            # Total Fitness Value is calculated to determine the probability of each maze
            total_fitness_value += maze["fitness_value"]
            current_maze_index += 1
        if generation == 0: # Only first generation is considered
            max_intial_fitness = max_fitness_value
            intial_maze = copy.copy(hard_maze)
        # Deletes the Unsolvable mazes from intial population
        for item in indexes_to_be_deleted:
            del intial_population[item]
        # print("previos", previous_iter_fitness_value, " current", max_fitness_value)
        if max_fitness_value > max_achieved_so_far:
            max_achieved_so_far = max_fitness_value
            hardest_maze_so_far = copy.copy(hard_maze)
        if previous_iter_fitness_value >= max_fitness_value and max_fitness_value !=0:
            non_improvement_iterations += 1  # To check if there are successive iterations with no change in fitness value
            if non_improvement_iterations >= MAX_NON_IMPROVEMENT_ITERATIONS:  # Returns the Current Solution if the max number of non improved successive iterations
                return {"reason": "Terminated Due to Max Number of Iterations without improvement","max_fitness_value": max_fitness_value,
                        "hard_maze": hard_maze,"max_intial_fitness":max_intial_fitness,"max_achieved_so_far":max_achieved_so_far,"hardest_maze_so_far":hardest_maze_so_far,"intial_maze":intial_maze}
        else:
            # print("increased", max_fitness_value)
            non_improvement_iterations = 0  # Resets non improved successive iterations to zero if the current iteration fitness value differs from preceding iteration
        previous_iter_fitness_value = max_fitness_value
        for maze in intial_population:  # calculates the probability of each maze
            maze["fitness_probability"] = maze["fitness_value"] / total_fitness_value
        for parent_maze in intial_population:  # For Selecting Two states randomly based on probability distribution # Selection Process
            random_1 = random.random()
            random_2 = random.random()
            intial_start = 0
            pair_1 = None
            pair_2 = None
            for maze in intial_population:
                intial_end = intial_start + maze["fitness_probability"]
                if random_1 > intial_start and random_1 <= intial_end:
                    pair_1 = maze
                if random_2 > intial_start and random_2 <= intial_end:
                    pair_2 = maze
                if pair_1 and pair_2:
                    new_maze = {'maze': crossover(pair_1,
                                                  pair_2)}  # Crossovers the Two selected states to produce 1 output states
                    if random.randint(0, 1) < MUTATION_PROBABILITY:
                        new_maze = mutate(new_maze)  # Mutates a single blockage( Wall)
                    new_maze_population.append(
                        new_maze)  # Appends the new maze generated after crossover and mutation to use for next iterations
                    break
                intial_start = intial_end
        intial_population = new_maze_population  # To pass the newly generated mazes to next iteration
    max_fitness_value = 0
    hard_maze = None
    # Calculates the maximum fitness and hard maze after the maximum number of iterations are reached
    for individual in intial_population:
        search_result = search_algorithm(individual, search_type)
        if search_result["is_path_exists"] and max_fitness_value < search_result["nodes_expanded"]:
            max_fitness_value = search_result["nodes_expanded"]
            hard_maze = individual
    if max_achieved_so_far < max_fitness_value:
        max_achieved_so_far = max_fitness_value
        hardest_maze_so_far = copy.copy(hard_maze)
    # Returns after termination condition
    return {"reason": "Terminated due to Max Iterations","max_fitness_value": max_fitness_value, "hard_maze": hard_maze,"max_intial_fitness":max_intial_fitness,"max_achieved_so_far":max_achieved_so_far,"hardest_maze_so_far":hardest_maze_so_far,"intial_maze":intial_maze}



def genetic_alogirthm_fringe_length(intial_population, search_type):
    """
     Maximises the Fringe Length
    :param intial_population: population set to begin with
    :param search_type: search types like DFS, BFS, A*
    :return: Returns the Final Iteration set of Population and Maxium Value and Termination Reason
    """

    previous_iter_fitness_value = 0  # Used to track previous iteration maximum fitness value
    non_improvement_iterations = 0  # Used to track the number of iterations without improvement in fitness value
    hard_maze = None  # Stores the hard_maze in each iteration
    max_achieved_so_far = 0
    hardest_maze_so_far = None
    max_intial_fitness = 0  # Stores Initial Fitness Vlaue before applying genetic algorithm
    intial_maze = None
    for generation in range(NUM_GENERATIONS):
        total_fitness_value = 0  # Used to compute the probability of each maze based on Fitness Value
        new_maze_population = []  # Used to Store New Set of Maze Population required for Next Iteration
        max_fitness_value = 0  # Tracks max fitness value in each iteration
        current_maze_index = 0
        indexes_to_be_deleted = []  # Stores the mazes that need to be deleted beacause they are unsolvable
        # For each we compute the fitness value
        for maze in intial_population:
            search_result = search_algorithm(maze,
                                             search_type)  # calls appropriate search algorithm based on search type
            if search_result["is_path_exists"]:  # To check if  a maze is solvable or not
                maze["fitness_value"] = search_result["fringe_length"]
            else:
                indexes_to_be_deleted.append(current_maze_index)  # Keeps tracks of unsolvable mazes
                continue
            # Checks max fitness value in current population and stores in hard_maze
            if maze['fitness_value'] > max_fitness_value:
                max_fitness_value = maze['fitness_value']
                hard_maze = maze["maze"]
            # Total Fitness Value is calculated to determine the probability of each maze
            total_fitness_value += maze["fitness_value"]
            current_maze_index += 1
        if generation == 0: # Only first generation is considered
            max_intial_fitness = max_fitness_value
            intial_maze = copy.copy(hard_maze)
        # Deletes the Unsolvable mazes from intial population
        for item in indexes_to_be_deleted:
            del intial_population[item]
        # print("previos", previous_iter_fitness_value, " current", max_fitness_value)
        if max_fitness_value > max_achieved_so_far:
            max_achieved_so_far = max_fitness_value
            hardest_maze_so_far = copy.copy(hard_maze)
        if previous_iter_fitness_value >= max_fitness_value and max_fitness_value !=0:
            non_improvement_iterations += 1  # To check if there are successive iterations with no change in fitness value
            if non_improvement_iterations >= MAX_NON_IMPROVEMENT_ITERATIONS:  # Returns the Current Solution if the max number of non improved successive iterations
                return {"reason": "Terminated Due to Max Number of Iterations without improvement","max_fitness_value": max_fitness_value,
                        "hard_maze": hard_maze,"max_intial_fitness":max_intial_fitness,"max_achieved_so_far":max_achieved_so_far,"hardest_maze_so_far":hardest_maze_so_far,"intial_maze":intial_maze}
        else:
            # print("increased", max_fitness_value)
            non_improvement_iterations = 0  # Resets non improved successive iterations to zero if the current iteration fitness value differs from preceding iteration
        previous_iter_fitness_value = max_fitness_value
        for maze in intial_population:  # calculates the probability of each maze
            maze["fitness_probability"] = maze["fitness_value"] / total_fitness_value
        for parent_maze in intial_population:  # For Selecting Two states randomly based on probability distribution # Selection Process
            random_1 = random.random()
            random_2 = random.random()
            intial_start = 0
            pair_1 = None
            pair_2 = None
            for maze in intial_population:
                intial_end = intial_start + maze["fitness_probability"]
                if random_1 > intial_start and random_1 <= intial_end:
                    pair_1 = maze
                if random_2 > intial_start and random_2 <= intial_end:
                    pair_2 = maze
                if pair_1 and pair_2:
                    new_maze = {'maze': crossover(pair_1,
                                                  pair_2)}  # Crossovers the Two selected states to produce 1 output states
                    if random.randint(0, 1) < MUTATION_PROBABILITY:
                        new_maze = mutate(new_maze)  # Mutates a single blockage( Wall)
                    new_maze_population.append(
                        new_maze)  # Appends the new maze generated after crossover and mutation to use for next iterations
                    break
                intial_start = intial_end
        intial_population = new_maze_population  # To pass the newly generated mazes to next iteration
    max_fitness_value = 0
    hard_maze = None
    # Calculates the maximum fitness and hard maze after the maximum number of iterations are reached
    for individual in intial_population:
        search_result = search_algorithm(individual, search_type)
        if search_result["is_path_exists"] and max_fitness_value < search_result["fringe_length"]:
            max_fitness_value = search_result["fringe_length"]
            hard_maze = individual
    if max_achieved_so_far < max_fitness_value:
        max_achieved_so_far = max_fitness_value
        hardest_maze_so_far = copy.copy(hard_maze)
    # Returns after termination condition
    return {"reason": "Terminated due to Max Iterations","max_fitness_value": max_fitness_value, "hard_maze": hard_maze,"max_intial_fitness":max_intial_fitness,"max_achieved_so_far":max_achieved_so_far,"hardest_maze_so_far":hardest_maze_so_far,"intial_maze":intial_maze}

def genetic_algorithm():
    """
    Runs the Genetic Algorithm using all kinds of searches as fitness functions
    :return:
    """
    # Creates a Random population of Population_Size
    global POPULATION_SIZE
    global DIMENSION_SIZE
    global NUM_WALLS
    global NUM_GENERATIONS
    global START_NODE
    global DEST_NODE
    global MAX_NON_IMPROVEMENT_ITERATIONS
    global MUTATION_PROBABILITY

    three_mazes = [
        {
            "POPULATION_SIZE": 10,
            "DIMENSION_SIZE":10,
            "NUM_WALLS": 30,
            "NUM_GENERATIONS": 100,
            "MAX_NON_IMPROVEMENT_ITERATIONS": 10,
            "MUTATION_PROBABILITY": 0.2
        },
        {
            "POPULATION_SIZE": 50,
            "DIMENSION_SIZE": 10,
            "NUM_WALLS": 30,
            "NUM_GENERATIONS": 100,
            "MAX_NON_IMPROVEMENT_ITERATIONS": 10,
            "MUTATION_PROBABILITY": 0.2
        },
        {
            "POPULATION_SIZE": 100,
            "DIMENSION_SIZE": 10,
            "NUM_WALLS":30,
            "NUM_GENERATIONS": 100,
            "MAX_NON_IMPROVEMENT_ITERATIONS": 10,
            "MUTATION_PROBABILITY": 0.2
        }
    ]
    for maze in three_mazes:
        POPULATION_SIZE = maze["POPULATION_SIZE"]
        DIMENSION_SIZE = maze["DIMENSION_SIZE"]
        NUM_WALLS = maze["NUM_WALLS"]
        NUM_GENERATIONS = maze["NUM_GENERATIONS"]
        START_NODE = 0
        DEST_NODE = DIMENSION_SIZE - 1
        MAX_NON_IMPROVEMENT_ITERATIONS = maze["MAX_NON_IMPROVEMENT_ITERATIONS"]
        MUTATION_PROBABILITY = maze["MUTATION_PROBABILITY"]
        intial_population = generate_random_mazes(POPULATION_SIZE, NUM_WALLS, DIMENSION_SIZE)
        maze["dfs"] = {}
        maze["dfs"]["shortest_path"] = genetic_alogirthm_shortest_path(copy.copy(intial_population),SEARCH_TYPE["DFS"])
        maze["dfs"]["nodes_explored"] = genetic_alogirthm_nodes_expanded(copy.copy(intial_population), SEARCH_TYPE["DFS"])
        maze["dfs"]["fringe_length"] = genetic_alogirthm_fringe_length(copy.copy(intial_population), SEARCH_TYPE["DFS"])

        maze["bfs"] = {}
        maze["bfs"]["shortest_path"] = genetic_alogirthm_shortest_path(copy.copy(intial_population), SEARCH_TYPE["BFS"])
        maze["bfs"]["nodes_explored"] = genetic_alogirthm_nodes_expanded(copy.copy(intial_population), SEARCH_TYPE["BFS"])
        maze["bfs"]["fringe_length"] = genetic_alogirthm_fringe_length(copy.copy(intial_population), SEARCH_TYPE["BFS"])

        maze["astar_manhattan"] = {}
        maze["astar_manhattan"]["shortest_path"] = genetic_alogirthm_shortest_path(copy.copy(intial_population), SEARCH_TYPE["AStarManhattan"])
        maze["astar_manhattan"]["nodes_explored"] = genetic_alogirthm_nodes_expanded(copy.copy(intial_population), SEARCH_TYPE["AStarManhattan"])
        maze["astar_manhattan"]["fringe_length"] = genetic_alogirthm_fringe_length(copy.copy(intial_population), SEARCH_TYPE["AStarManhattan"])

        maze["astar_euclid"] = {}
        maze["astar_euclid"]["shortest_path"] = genetic_alogirthm_shortest_path(copy.copy(intial_population), SEARCH_TYPE["AStarEuclid"])
        maze["astar_euclid"]["nodes_explored"] = genetic_alogirthm_nodes_expanded(copy.copy(intial_population), SEARCH_TYPE["AStarEuclid"])
        maze["astar_euclid"]["fringe_length"] = genetic_alogirthm_fringe_length(copy.copy(intial_population), SEARCH_TYPE["AStarEuclid"])
        # maze["dfs"]["shortest_path"]['hard_maze'] = []
        # maze["dfs"]["nodes_explored"]['hard_maze'] = []
        # maze["dfs"]["fringe_length"]['hard_maze'] = []
        # maze["dfs"]["shortest_path"]['hardest_maze_so_far'] = []
        # maze["dfs"]["nodes_explored"]['hardest_maze_so_far'] = []
        # maze["dfs"]["fringe_length"]['hardest_maze_so_far'] = []
        # print(maze)
        # break
    return three_mazes

# max_fitness_value = 0
# for individual in result["final_states"]:
#     search_length = search_alg(individual)
#     if max_fitness_value < search_length:
#         max_fitness_value = search_length

# print(max_fitness_value)
