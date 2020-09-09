import settings
from collections import defaultdict
import csv
from decimal import Decimal
import time
from numba import jit

class DFS:

    def __init__(self):
        self.edges_dict = defaultdict(set)
        self.distance = {}
        self.visited = set()
        self.path = []
        self.solutions = []

        self.jump_count = 0

        with open(settings.ATTRACTIONS_EDGES_FNAME) as fin:
            csvr = csv.DictReader(fin)

            for line in csvr:
                source, target, distance = int(line["source"]), int(line["target"]), Decimal(line["distance_km"])
                self.edges_dict[source].add(target)
                self.distance[(source, target)] = distance

        possible_solutions = 1
        for key in self.edges_dict:
            possible_solutions *= (len(self.edges_dict[key]) - 1)

        possible_solutions /= (len(self.edges_dict[settings.RAIL_ROAD_ENTRANCE_ID]) - 1)
        possible_solutions *= (len(self.edges_dict[settings.RAIL_ROAD_ENTRANCE_ID]))

        print(f"possible solutions {possible_solutions}")

    # @profile
    @jit(nopython=True)
    def find(self, curr_key):


        for k in self.edges_dict[curr_key]:

            if k not in self.visited:
                self.visited.add(k)
                if len(self.visited) == settings.TOTAL_ROWS:
                    self.solutions.append(list(self.path))

                self.path.append(k)
                self.find(k)
                self.path.pop()
                self.visited.remove(k)

                self.jump_count+=1
                if self.jump_count > 10_000_000:
                    return
                if self.jump_count % 1_000_000 == 0:
                    print(self.jump_count)



    def start(self):
        self.find( settings.RAIL_ROAD_ENTRANCE_ID )
        print("here")


t1 = time.time()
d = DFS()
d.start()
print(f" time took {time.time() - t1}")