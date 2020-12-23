from EvAlgo import EvAlgo
import random


class FindFour(EvAlgo):
    def measureFitness(self, gene):
        # Return the y value of our equation
        if gene in self.memo:
            return self.memo[gene]
        else:
            result = -abs(gene[0]-4)
            self.memo[gene] = result
            return result

    def randomGene(self):
        # Return a random x value
        return (random.randint(-100, 100),)

    def reproduce(self, parentA, parentB):
        # Return the average of the 2 x values of our equation, plus some mutation
        return ((parentA[0]+parentB[0])//2 + random.randint(-10, 10),)

    def printGene(self, gene):
        print(str(gene[0])+". ", end='')

def main():
    x = FindFour(5, 20)
    x.evolve(4)
    x.result()


if __name__ == "__main__":
    main()
