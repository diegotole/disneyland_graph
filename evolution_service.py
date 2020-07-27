from settings import TOTAL_ROWS, RAIL_ROAD_ENTRANCE_ID
from utils import display_dictionary, get_distance
import time
from collections import defaultdict
from utils import load_maps, getEdgesDict
import random
import statistics
from matplotlib import pyplot as pl

class Environment:
    population_size = 100
    gene_size = 50 - 1
    generation_kill = 10
    mutation_factor = 1000

    population_size = 300
    gene_size = 200
    generation_kill = 50
    mutation_factor = 1000




    def print_stats(self):

        l = [p.fitness for p in self.population]
        maxi = max( l  )
        mini = min( l  )
        sumi = sum( l  )
        avgi = sumi/len(self.population)
        stdi = statistics.stdev( l )

        # print(f"max {maxi}, min {mini}, avg {avgi}, std dev {stdi}")
        self.stats["max"].append(maxi)
        self.stats["min"].append(mini)
        self.stats["avg"].append(avgi)
        self.stats["std"].append(stdi)

    def display_stats(self):

        x_size = len(self.stats["max"])

        pl.plot(  [x for x in range(x_size)],  self.stats["max"], label="max" )
        pl.plot(  [x for x in range(x_size)],  self.stats["min"], label="min" )
        pl.plot(  [x for x in range(x_size)],  self.stats["avg"], label="avg" )
        pl.plot(  [x for x in range(x_size)],  self.stats["std"], label="std" )
        pl.legend()
        pl.show()

    def __init__(self, attractions_map, edges_dict):
        self.attractions_map = attractions_map
        self.edges_dict = edges_dict
        self.population = []

        self.stats = defaultdict(list)



    def loadPopulation(self):
        for i in range(self.population_size):
            sol = Env_Solution(self, gene_size=self.gene_size)
            sol.create_genes()
            self.population.append(sol)

    def sort(self):
        self.population.sort(key=lambda x: x.fitness, reverse=False)

    def end_generation(self):

        self.sort()

        for i in range(self.generation_kill):
            self.population.pop()

        random_indexes = [random.randint(0, self.population_size - self.generation_kill -1) for i in
                          range(self.generation_kill * 2)]

        # print("randos, ", random_indexes)
        # print(f"population size {len(self.population)} ")
        # new_candidates = [Env_Solution(self, gene_size=self.gene_size) for i in range(self.generation_kill)]
        new_candidates = []
        for i in range(self.generation_kill):
            candidate = self.crossover(self.population[random_indexes.pop()], self.population[random_indexes.pop()])

            new_candidates.append(candidate)

        if random.randint(1,self.mutation_factor) == 1:
            new_candidates[0].mutate()

        self.population.extend(new_candidates)

    def crossover(self, sol1, sol2):
        commons = sol1.path_set.intersection(sol2.path_set)

        needle = commons.pop()

        index = sol1.path.index(needle)
        path = [sol1.path[i] if i <= index else sol2.path[i] for i in range(self.gene_size)]
        sol3 = Env_Solution(self, gene_size=self.gene_size)
        sol3.get_genes(genes=path)

        return sol3


class Env_Solution:
    # size = 50 - 1
    start_pos = RAIL_ROAD_ENTRANCE_ID

    def __init__(self, env, gene_size):
        self.path = [RAIL_ROAD_ENTRANCE_ID, ]
        # self.curr = self.start_pos
        self.env = env
        self.size = gene_size

    def mutate(self):
        mutation_start = random.randint(0, self.size + 1)
        curr = self.path[mutation_start]
        for i in range(mutation_start+1,  self.size):
            rnd_i = random.randint(0, len(self.env.edges_dict[curr]) - 1)
            curr = self.env.edges_dict[curr][rnd_i]
            self.path[i] = curr

        self.path_set = set(self.path)

        self.get_fitness()

    def get_genes(self, genes):

        self.path = genes
        self.path_set = set(genes)

        self.get_fitness()

    def create_genes(self):
        curr = self.start_pos
        self.path = [0] * self.size
        for i in range( self.size):
            rnd_i = random.randint(0, len(self.env.edges_dict[curr]) - 1)
            curr = self.env.edges_dict[curr][rnd_i]
            self.path[i] = curr

        self.path_set = set(self.path)

        self.get_fitness()

    def get_fitness(self):

        distance = 0

        # did not find all the rides
        diff = TOTAL_ROWS - len(set(self.path))
        if diff > 0:
            # penalty for each ride missing
            distance += (diff * 1000)

        for r in range(1, len(self.path)):
            distance += get_distance(self.path[r - 1], self.path[r], self.env.attractions_map)

        self.fitness = distance


if __name__ == "__main__":
    attraction_map = load_maps()
    Island = Environment(attraction_map, getEdgesDict(attraction_map))

    Island.loadPopulation()

    for i in range(100):
        Island.end_generation()
        Island.print_stats()
    # Island.population[0].mutate()

    # Island.print_stats()
    Island.display_stats()
    pass
