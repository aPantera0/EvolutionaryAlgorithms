from EvAlgo import EvAlgo
import random


class myEvol(EvAlgo):
    def measureFitness(self, gene):
        if gene in self.memo:
            return self.memo[gene]
        else:
            result = -abs(4-gene[0])
            self.memo[gene] = result
            return result

    def randomGene(self):
        return (random.randint(-100, 100),)

    def reproduce(self, parentA, parentB):
        # Just the average of the 2 numbers plus some mutation
        return ((parentA[0]+parentB[0])//2 + random.randint(-10, 10),)


def main():
    x = myEvol(10, 100)
    x.evolve()
    x.result()


if __name__ == "__main__":
    main()
