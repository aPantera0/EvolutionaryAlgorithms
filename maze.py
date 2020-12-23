"""
A maze solver that solves a maze by genetic evolution.
A genome represents a possible path, pathes evolve. 
"""
from EvAlgo import EvAlgo
import random
import functools


class Maze(EvAlgo):
    def __init__(self, popSize, generations, maze, genePool=[], propKilled=.5, propMutated=.5):
        super().__init__(popSize, generations, genePool, propKilled, propMutated)
        # The maze will always start at the upper left and end at the lower right
        # 1 represents a wall, 0 represents no wall
        self.maze = maze
        self.borderChar = '██'
        self.wallChar = '██'
        self.pathChar = '██'
        self.emptyChar = '  '
        self.printRed = lambda x: print('\033[91m' + str(x) + '\033[0m', end='')
        self.printCyan = lambda x: print('\033[96m' + str(x) + '\033[0m', end='')
        self.printGreen = lambda x: print('\033[92m' + str(x) + '\033[0m', end='')
        self.height = len(self.maze)
        self.width = len(self.maze[0])
        self.numCells = self.width*self.height
        self.countCells = lambda z: functools.reduce(lambda x,y: x+sum(y), z, 0)

    def printGene(self, path=[]):
        # If no path provided, seed an empty one
        if not path:
            path=[[False]*self.width for x in range(self.height)]
        print("\n",(self.width+2) * self.borderChar, sep = '')
        for i,row in enumerate(self.maze):
            print(self.borderChar, end='')
            for j,cell in enumerate(row):
                # If it is the start or end, print a cyan path char
                if (i == 0 and j == 0) or (i == self.height-1 and j == self.width-1):
                    self.printCyan(self.pathChar)
                # If there is both a wall and a path there, print a red path char
                elif cell and path[i][j]:
                    self.printRed(self.pathChar)
                # If there is just a path there, print a green path char
                elif path[i][j]:
                    self.printGreen(self.pathChar)
                # If there is nothign there, print the empty char
                elif not cell:
                    print(self.emptyChar, end='')
                # If there is a wall there, print the wall char
                else:
                    print(self.wallChar, end='')
            print(self.borderChar)
        print((self.width+2) * self.borderChar)
        
    def measureFitnessHelper(self, gene):
        """return a higher number the more fit the geneome (path) is.
        If a path is invalid, it will recieve a fitness score lower than the lowest possible valid path score.
        A path will recieve a higher score the closer it is to the exit.
        A path will recieve a lower score the more cells it occupies.
        The most fit genome will be a path that completes the maze, and occupies the minimum number of cells.
        """
        # Step 1: Start at the start cell, and create a new path consisting of every cell you can get to by just moving adjacently to the start cell.
        # Step 2: If the path found in step 1 contains the end state, the path is a solution, the fitness is the
        #            total number of cells in the maze times 2, minus the number of cells occupied by the path. Do not continue.
        # Step 3: Start from the end cell, move along the maze in every direction there isn't a wall. For example, if you can move up and left, do both during this one iteration. 
        # Step 4: Make n iterations of Step 3, until you hit the first cell occupied by the new path found in step 1. The fitness is the total number of cells in the maze minus n. 

        # Step 1
        newPath = [[False]*self.width for x in range(self.height)]
        newPath[0][0] = True
        cellsVisited = [(0,0)]
        foundNewCels = True
        while foundNewCels:
            newCellsVisited = []
            for cell in cellsVisited:
                for adjacent in [ (cell[0],cell[1]-1) , (cell[0],cell[1]+1) , (cell[0]+1,cell[1]) , (cell[0]-1,cell[1]) ]:
                    if adjacent[0] >= 0 and adjacent[1] >= 0 and adjacent[0] < self.height and adjacent[1] < self.width and not self.maze[adjacent[0]][adjacent[1]] and not newPath[adjacent[0]][adjacent[1]] and gene[adjacent[0]][adjacent[1]]:
                        newPath[adjacent[0]][adjacent[1]] = True        
                        newCellsVisited += [(adjacent[0], adjacent[1])]   
            if not newCellsVisited:
                foundNewCels = False
            else:
                cellsVisited = newCellsVisited

        # Step 2
        if newPath[self.height-1][self.width-1]:
            return 2*self.numCells - self.countCells(gene)

        # Step 3
        visited = [[False]*self.width for x in range(self.height)]
        visited[self.height-1][self.width-1] = True
        cellsVisited = [(self.height-1, self.width-1)]
        foundPath = False
        iterations = 0
        while not foundPath:
            iterations += 1
            newCellsVisited = []
            for cell in cellsVisited:
                for adjacent in [ (cell[0],cell[1]-1) , (cell[0],cell[1]+1) , (cell[0]+1,cell[1]) , (cell[0]-1,cell[1]) ]:
                    if adjacent[0] >= 0 and adjacent[1] >= 0 and adjacent[0] < self.height and adjacent[1] < self.width and not self.maze[adjacent[0]][adjacent[1]] and not visited[adjacent[0]][adjacent[1]]:
                        visited[adjacent[0]][adjacent[1]] = True        
                        newCellsVisited += [(adjacent[0], adjacent[1])]   
                        if newPath[adjacent[0]][adjacent[1]]:
                            foundPath = True
                            break
            cellsVisited = newCellsVisited

        # Step 4
        return self.numCells-iterations
    
    def measureFitness(self, gene):
        if gene in self.memo:
            return self.memo[gene]
        else:
            result = self.measureFitnessHelper(gene)
            self.memo[gene] = result
            return result

    def randomGene(self):
        path = [[False]*self.width for x in range(self.height)]
        path[0][0] = True
        path[self.height-1][self.width-1] = True
        for i in range(self.height):
            for j in range(self.width):
                if not self.maze[i][j]:
                    if random.uniform(0,1) < .4:
                        path[i][j] = True
        return tuple(map(tuple,path))

    def reproduce(self, parentA, parentB):
        # Probability that cell will be occupied if:
        # Both parents: .8
        # One parent: .5
        # No parent: .2
        path = [[False]*self.width for x in range(self.height)]
        path[0][0] = True
        path[self.height-1][self.width-1] = True
        for i in range(self.height):
            for j in range(self.width):
                if not self.maze[i][j]:
                    if parentA[i][j] and parentB[i][j]:
                        if random.uniform(0,1) < .8:
                            path[i][j] = True
                    elif parentA[i][j] or parentB[i][j]:
                        if random.uniform(0,1) < .5:
                            path[i][j] = True
                    else:
                        if random.uniform(0,1) < .2:
                            path[i][j] = True
        return tuple(map(tuple,path))

def main():
    x = Maze(500, 1000, [
            [0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1], 
            [0, 1, 0, 0, 0, 0], 
            [0, 0, 0, 1, 1, 0], 
            [0, 1, 0, 0, 1, 0],
            [0, 0, 0, 0, 1, 0], 
        ])
    x.evolve([1,10,100,1000])
    x.result()

if __name__ == "__main__":
    main()
