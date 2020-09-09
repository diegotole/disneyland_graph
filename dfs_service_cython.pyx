import settings
from collections import defaultdict
import csv
from decimal import Decimal
import time
from numba import jit

# edges_dict = defaultdict(set)
myedges_dict = {}
distance = {}
visited = set()
path = []
solutions = []

# jump_count = 0

with open(settings.ATTRACTIONS_EDGES_FNAME) as fin:
    csvr = csv.DictReader(fin)

    for line in csvr:
        source, target, distance_km = int(line["source"]), int(line["target"]), Decimal(line["distance_km"])

        if source not in myedges_dict:
            myedges_dict[source] = set()

        myedges_dict[source].add(target)
        distance[(source, target)] = distance_km

possible_solutions = 1
for key in myedges_dict:
    possible_solutions *= (len(myedges_dict[key]) - 1)

possible_solutions /= (len(myedges_dict[settings.RAIL_ROAD_ENTRANCE_ID]) - 1)
possible_solutions *= (len(myedges_dict[settings.RAIL_ROAD_ENTRANCE_ID]))

print(f"possible solutions {possible_solutions}")


# @profile
# @jit(nopython=True)
stop_me = 0

def find(curr_key, visited, path,jump_count, edges_dict, solutions):
    global stop_me

    stop_me += 1
    if stop_me > 10_000_000:
        return

    if stop_me % 3_000_000 == 0:
        print(stop_me)

    for k in edges_dict[curr_key]:
    # for idx in range(len(edges_dict[curr_key]):

        if k not in visited:
            visited.add(k)
            if len(visited) == settings.TOTAL_ROWS:
                solutions.append(list(path))
                return

            path.append(k)
            find(k, visited, path, jump_count, edges_dict, solutions)
            path.pop()
            visited.remove(k)




def start():
    t1 = time.time()
    find(settings.RAIL_ROAD_ENTRANCE_ID, set([0]), [0], 0, myedges_dict, set([0]))
    print(f" time took {time.time() - t1}")

# d = DFS()
# d.start()

# start()

