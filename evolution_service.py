from settings import TOTAL_ROWS, RAIL_ROAD_ENTRANCE_ID
from utils import display_dictionary
import time
from collections import defaultdict
from utils import load_maps, getEdgesDict, GeoUtils
import random
import statistics
from matplotlib import pyplot as pl
from cachetools import cached, LRUCache
from functools import reduce


class Environment:
    population_size = 100
    gene_size = 50 - 1
    generation_kill = 10
    mutation_factor = 1000

    population_size = 300
    gene_size = 200
    generation_kill = 50
    mutation_factor = 1000

    current_best = float("inf")

    def print_stats(self):

        l = [p.fitness for p in self.population]
        maxi = max(l)
        mini = min(l)
        sumi = sum(l)
        avgi = sumi / len(self.population)
        stdi = statistics.stdev(l)

        # print(f"max {maxi}, min {mini}, avg {avgi}, std dev {stdi}")
        self.stats["max"].append(maxi)
        self.stats["min"].append(mini)
        self.stats["avg"].append(avgi)
        self.stats["std"].append(stdi)

    def display_stats(self):

        x_size = len(self.stats["max"])

        pl.plot([x for x in range(x_size)], self.stats["max"], label="max")
        pl.plot([x for x in range(x_size)], self.stats["min"], label="min")
        pl.plot([x for x in range(x_size)], self.stats["avg"], label="avg")
        pl.plot([x for x in range(x_size)], self.stats["std"], label="std")
        pl.legend()
        pl.show()

    def __init__(self, attractions_map, edges_dict):
        self.attractions_map = attractions_map
        self.edges_dict = edges_dict
        self.population = []

        self.stats = defaultdict(list)
        self.GeoHelper = GeoUtils(attractions_map)

    def loadPopulation(self):
        for i in range(self.population_size):
            sol = Env_Solution(self, gene_size=self.gene_size)
            sol.create_genes()
            self.population.append(sol)

    def sort(self):
        self.population.sort(key=lambda x: x.fitness, reverse=False)

    def end_generation(self):

        self.sort()
        if self.current_best > self.population[0].fitness:
            print(f"new best: {self.current_best} to {self.population[0].fitness} ")
            self.current_best = self.population[0].fitness

        for i in range(self.generation_kill):
            self.population.pop()

        random_indexes = [random.randint(0, self.population_size - self.generation_kill - 1) for i in
                          range(self.generation_kill * 2)]

        new_candidates = []
        for _ in range(self.generation_kill):
            candidate = self.crossover(self.population[random_indexes.pop()], self.population[random_indexes.pop()])

            new_candidates.append(candidate)
        # for i in range(self.generation_kill):
        #     sol = Env_Solution(self, gene_size=self.gene_size)
        #     sol.create_genes()
        #     new_candidates.append(sol)

        if random.randint(1, self.mutation_factor) == 1:
            new_candidates[0].mutate()
            pass

        self.population.extend(new_candidates)

    def display_best_solution(self):

        display_dictionary(self.attractions_map, self.population[0].getEdges())

    def crossover(self, sol1, sol2):
        commons = sol1.path_set.intersection(sol2.path_set)

        needle = commons.pop()

        index1 = sol1.path.index(needle)
        index2 = sol2.path.index(needle)
        path = [sol1.path[i] for i in range(index1 + 1)]
        path2 = [sol2.path[i] for i in range(index2 + 1, len(sol2.path))]
        path += path2
        # path = [sol1.path[i] if i <= index else sol2.path[i] for i in range(self.gene_size)]
        sol3 = Env_Solution(self, gene_size=len(path))
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

    def getEdges(self):

        p1 = self.path[0]
        myedges = []

        for i in range(1, len(self.path)):
            myedges.append((p1, self.path[i]))
            p1 = self.path[i]

        return myedges

    def mutate(self):
        mutation_start = random.randint(0, len(self.path))
        curr = self.path[mutation_start]
        for i in range(mutation_start + 1, self.size):
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
        for i in range(self.size):
            rnd_i = random.randint(0, len(self.env.edges_dict[curr]) - 1)
            curr = self.env.edges_dict[curr][rnd_i]
            self.path[i] = curr

        self.path_set = set(self.path)

        self.get_fitness()

    # @profile
    def get_fitness(self):

        distance = 0

        # did not find all the rides
        diff = TOTAL_ROWS - len(set(self.path))
        path_size = len(self.path)

        if diff > 0:
            # penalty for each ride missing
            distance += (diff * 1000)
            # tmp = distance

        else:
            good_path = set()
            for idx, val in enumerate(self.path):
                good_path.add(val)

                if len(good_path) == TOTAL_ROWS:
                    path_size = idx
                    # print(f"smaller {path_size}, total {len(self.path)}")
                    break

        # t1 = time.time()
        # # self.path_size = path_size
        # distance2 = distance
        # for r in range(1, path_size):
        #     tmp += self.env.GeoHelper.get_distance(self.path[r - 1], self.path[r])

        # t2 = time.time()
        distance = reduce(
            lambda tot, curr: tot + self.env.GeoHelper.get_distance(self.path[curr - 1], self.path[curr])
            , (i for i in range(1, path_size)), distance)

        # t3 = time.time()

        self.fitness = distance
        # print(f"loop took {t2-t1} , reduce took {t3-t2}")
        # print(tmp, distance, "blah")

if __name__ == "__main__":
    t1 = time.time()
    attraction_map = load_maps()
    Island = Environment(attraction_map, getEdgesDict(attraction_map))

    Island.loadPopulation()

    for i in range(1000):  # use 1000
        Island.end_generation()
        Island.print_stats()
    # Island.population[0].mutate()

    # Island.print_stats()
    Island.display_stats()
    Island.display_best_solution()

    print(Island.population[0].fitness)
    print(f"took: {time.time() - t1}")
    pass
