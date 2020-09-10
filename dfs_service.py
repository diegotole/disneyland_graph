import settings
from collections import defaultdict
import csv
from decimal import Decimal
import time


# from numba import jit

class DFS:

    def __init__(self, disney_area):
        self.edges_dict = defaultdict(set)
        self.distance = {}
        self.visited = set()
        self.path = []
        self.solutions = []
        self.disney_area = disney_area

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

        # print(f"possible solutions {possible_solutions}")

    # @profile
    # @jit(nopython=True)
    def find(self, curr_key):

        for k in self.edges_dict[curr_key]:

            if k not in self.disney_area:
                continue

            if k not in self.visited:
                self.visited.add(k)
                self.path.append(k)
                if len(self.visited) == len(self.disney_area):
                    self.solutions.append(list(self.path))

                self.find(k)
                self.path.pop()
                self.visited.remove(k)

                self.jump_count += 1
                if self.jump_count > 10_000_000:
                    return
                if self.jump_count % 1_000_000 == 0:
                    print(self.jump_count)

    def start(self):

        for source in self.disney_area:
            self.path = [source]
            self.visited = set([source])
            self.find(source)
            # print(source)

        print(f" solutions {len(self.solutions)} ")
        return self.solutions




solution_map = {}
t0 = time.time()
for region in settings.REGIONS_LIST:
    t1 = time.time()
    d = DFS(region[0])
    solution_map[region[1]] = d.start()
    print(f" {region[1]} region took {time.time() - t1}\n")

print(f" full test took {time.time() - t0}")
