import settings
from collections import defaultdict
import csv
from decimal import Decimal
import time
from itertools import permutations
import shelve
from functools import lru_cache


class MySolutionMap(dict):
    def __hash__(self):
        return 1

def distance_obj():
    with open(settings.ATTRACTIONS_EDGES_FNAME) as fin:
        csvr = csv.DictReader(fin)

        obj = {}

        for line in csvr:
            d = Decimal(line["distance_km"])
            obj[(int(line['source']), int(line['target']))] = d
            obj[( int(line['target']), int(line['source']))] = d

    return obj


def calculate_path_distance(path, dist_obj):
    tot = Decimal("0.0")
    # print(f"measuring list size {len(path)}")
    for i in range(1, len(path)):
        tot += dist_obj[path[i - 1], path[i]]

    return tot





def filter_dups(solutions, dist_obj):
    obj = {}
    best_ones = {}
    for path in solutions:

        key = (path[0], path[-1])
        if key not in best_ones:
            best_ones[key] = float("inf")

        d = calculate_path_distance(path, dist_obj)

        if d < best_ones[key]:
            best_ones[key] = d
            obj[key] = path

    return obj




@lru_cache(100)
def find_best_connection_distance(r_source, r_target, solution_map):
    # check each end node from region1 against all start node from region2
    tmp_distance = Decimal(float("inf"))
    # get all solutions for source

    resp_source, resp_target = None, None

    for sol_source in solution_map[r_source]:
        for sol_target in solution_map[r_target]:
            s1, s2 = sol_source[0], sol_source[-1]
            t1, t2 = sol_target[0], sol_target[-1]

            tmp_distance = min(distances.get((s1, t1), float("inf")), tmp_distance)
            tmp_distance = min(distances.get((s1, t2), float("inf")), tmp_distance)
            tmp_distance = min(distances.get((s2, t1), float("inf")), tmp_distance)
            tmp_distance = min(distances.get((s2, t2), float("inf")), tmp_distance)

    return Decimal(tmp_distance)



def validate_connection(r_source, r_target, solution_map, valid_source_node):
    # check each end node from region1 against all start node from region2
    tmp_distance = Decimal(float("inf"))
    # get all solutions for source

    resp_source, resp_target = None, None

    valid_targets = set()

    for sol_source in solution_map[r_source]:
        for sol_target in solution_map[r_target]:
            s1, s2 = sol_source[0], sol_source[-1]
            t1, t2 = sol_target[0], sol_target[-1]

            if s2 not in valid_source_node:
                continue
            # tmp_distance = min(distances.get((s1, t1), float("inf")), tmp_distance)
            # tmp_distance = min(distances.get((s1, t2), float("inf")), tmp_distance)
            # tmp_distance = min(distances.get((s2, t1), float("inf")), tmp_distance)
            # tmp_distance = min(distances.get((s2, t2), float("inf")), tmp_distance)
            if distances.get((s2, t1), -1)  != -1:
                valid_targets.add(t2)


    return valid_targets

@lru_cache(100)
def connection_exists(r_source, r_target, solution_map):

    tmp_distance = float("inf")

    for sol_source in solution_map[r_source]:
        for sol_target in solution_map[r_target]:
            s1, s2 = sol_source[0], sol_source[-1]
            t1, t2 = sol_target[0], sol_target[-1]

            tmp_distance = min(distances.get((s1, t1), float("inf")), tmp_distance)
            tmp_distance = min(distances.get((s1, t2), float("inf")), tmp_distance)
            tmp_distance = min(distances.get((s2, t1), float("inf")), tmp_distance)
            tmp_distance = min(distances.get((s2, t2), float("inf")), tmp_distance)


    return tmp_distance != float("inf")


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

                if len(set(self.visited) - settings.SW_EXTRAS_CONNECTORS) == len(
                        set(self.disney_area) - settings.SW_EXTRAS_CONNECTORS):
                    # if len(self.visited) == len(self.disney_area):
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

        # print(f" solutions {len(self.solutions)} ")
        return self.solutions



distances = distance_obj()

if __name__ == "__main__":

    with shelve.open("db_dfs_service") as db:

        if "synched" not in db:

            distances = distance_obj()

            # nested loop,region to region connection
            all_regions_connections = permutations([region_name for region_list, region_name in settings.REGIONS_LIST])
            all_regions_connections = list(all_regions_connections)
            print(f" permutations of all regions {len(list(all_regions_connections))}\n")

            solution_map = MySolutionMap()
            t0 = time.time()
            for region_list, region_name in settings.REGIONS_LIST:
                t1 = time.time()
                d = DFS(region_list)
                solutions = d.start()
                filtered_solutions = filter_dups(solutions, distances)
                # solution_map[region_name] = d.start()
                solution_map[region_name] = filtered_solutions

                print(
                    f" {region_name} region took {time.time() - t1}, total solutions {len(solutions)} after filter {len(filtered_solutions)}\n")

            print(f" full searches took {time.time() - t0}")

            # permutation of all region connects
            # we need to start in main street, so no reason to generate permutations where main street is not first
            perms = permutations([name for _, name in settings.REGIONS_LIST if name != settings.MAIN_STREET_NAME])
            perms = list(perms)
            perms = [[settings.MAIN_STREET_NAME] + list(p) for p in perms]

            print(f"found {len(perms)} region to region paths")
    # starting in main street,
    # inside each solution for source region,check exit node
    # check if exit node has connection with entry node from next region
    # if none found, exit path

    best_distance = float("inf")
    my_inf = Decimal(float("inf"))
    for path in perms:

        curr_path_distance = Decimal(float("inf"))

        for i in range(1, len(path)):
            r_source = path[i - 1]
            r_target = path[i]

            # tmp_distance = my_inf
            # # get all solutions for source
            # for sol_source in solution_map[r_source]:
            #     for sol_target in solution_map[r_target]:
            #         s1, s2 = sol_source[0], sol_source[-1]
            #         t1, t2 = sol_target[0], sol_target[-1]
            #
            #         tmp_distance = min(distances.get((s1, t1), float("inf")), tmp_distance)
            #         tmp_distance = min(distances.get((s1, t2), float("inf")), tmp_distance)
            #         tmp_distance = min(distances.get((s2, t1), float("inf")), tmp_distance)
            #         tmp_distance = min(distances.get((s2, t2), float("inf")), tmp_distance)
            tmp_distance = find_best_connection_distance(r_source, r_target, solution_map)

            if tmp_distance == my_inf:
                print(f"no connection between {r_source} {r_target}")
                break
            else:

                curr_path_distance += tmp_distance

        best_distance = min(best_distance, curr_path_distance)

    print(f"best distance path: {best_distance}")
