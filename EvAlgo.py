from abc import ABC, abstractmethod
import random
import pandas
import matplotlib

class EvAlgo(ABC):
    def __init__(self, popSize, generations, genePool=[], propKilled=.5, propMutated=.5, graph=[]):
        self.popSize = popSize
        self.generations = generations
        self.genePool = genePool
        self.memo = {}
        if propKilled >= 1 or propKilled <= 0:
            raise ValueError(
                "Invalid proportion killed, must be between 0 and 1")
        if propMutated >= 1 or propMutated <= 0:
            raise ValueError(
                "Invalid proportion mutated, must be between 0 and 1")
        self.propKilled = propKilled
        self.propMutated = propMutated
        self.graph = graph

    def seedGenePool(self):
        for i in range(self.popSize):
            self.genePool += [self.randomGene()]

    def evolve(self, printFrequency=0):
        # Seed gene pool if one wasn't provided
        if not self.genePool:
            self.seedGenePool()
        # Perform all generations
        for i in range(self.generations):
            # Measure fitness of entire gene pool, and sort least fit to most fit
            self.genePool.sort(key=self.measureFitness)
            numKilled = int(self.popSize * self.propKilled)
            # Kill propKilled proportion of the population, and replace them
            for j in range(numKilled):
                if random.uniform(0, 1) < self.propMutated:
                    # Mutate
                    self.genePool[j] = self.randomGene()
                else:
                    # Reproduce
                    self.genePool[j] = self.reproduce(self.genePool[random.randint(
                        numKilled + 1, self.popSize-1)], self.genePool[random.randint(numKilled + 1, self.popSize-1)])
            if printFrequency and i != self.generations-1:
                if type(printFrequency) == int:
                    if (i+1) % printFrequency == 0:
                        self.result(i+1)
                if type(printFrequency) == tuple or type(printFrequency) == list:
                    if (i+1) in printFrequency:
                        self.result(i+1)
            self.graph += [self.measureFitness(self.genePool[-1])]
                
    def result(self, generation=0):
        if not generation:
            generation = self.generations
        print("The most fit gene in generation "+ str(generation) +": ", end='')
        self.printGene(self.genePool[-1])
        print("Achieved measure of fitness: ",
            self.measureFitness(self.genePool[-1]))
        if generation == self.generations:
            pandas.DataFrame(data = self.graph, columns=['Fitness']).plot()

    def printGene(self, gene):
        print(gene)

    @abstractmethod
    def measureFitness(self, gene):
        """return a higher number the more fit the geneome is"""
        pass

    @abstractmethod
    def randomGene(self):
        """return a random gene (tuple)"""
        pass

    @abstractmethod
    def reproduce(self, parentA, parentB):
        """Return a child gene (tuple) resulting from two parents"""
        pass
