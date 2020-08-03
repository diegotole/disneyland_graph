from settings import TOTAL_ROWS, RAIL_ROAD_ENTRANCE_ID
from utils import display_dictionary,getEdgesDict
import time
from collections import defaultdict
from utils import load_maps


class DFS:
    mypath = [RAIL_ROAD_ENTRANCE_ID, ]
    mypath_set = set([RAIL_ROAD_ENTRANCE_ID, ])
    mycounter = defaultdict(int)
    solutions = []
    short_stop = 200
    hops = 0
    stop_search = 1_000_000
    last_print_time = time.time()
    print_interval = 60 * 5
    mydict = load_maps()
    edges_dict = None

    @classmethod
    def reset_me(cls):
        cls.mypath = [RAIL_ROAD_ENTRANCE_ID, ]
        # cls.mypath_set = set([RAIL_ROAD_ENTRANCE_ID,])
        cls.mycounter = defaultdict(int)
        cls.solutions = []
        cls.short_stop = 200
        cls.hops = 0
        cls.stop_search = 10_000_000

    @classmethod
    def add_solution(cls):

        cls.solutions.append(
            list(cls.mypath)
        )

    @classmethod
    def should_stop(cls):
        # if len(cls.mypath) > cls.short_stop:
        #     return True
        #
        # return False
        # cls.mypath_set = set(cls.mypath)
        sumi = len(cls.mycounter.keys())
        missing = TOTAL_ROWS - sumi
        # print("missing:", missing, "sumi:", sumi)

        # missing = TOTAL_ROWS - len(cls.mypath_set)  # 55 - 1 = 54
        remaining_slots = cls.short_stop - len(cls.mypath)  # 80 - 1

        if missing > remaining_slots:  # 54 > 79
            # print(" no good outcome looking here ",missing, remaining_slots)
            return True

        return False

    @classmethod
    def pop_path(cls):
        # print("@@@@@inside pop path")
        # if len(cls.mypath):
        #     k = cls.mypath.pop()
        #     # cls.mypath_set.remove(k)
        #     cls.mycounter[k] -= 1
        #     if cls.mycounter[k] < 0:
        #         cls.mycounter.pop(k)
        k = cls.mypath.pop()
        # k = ""
        cls.mycounter[k] -= 1

    @classmethod
    def append_path(cls, k):
        cls.mypath.append(k)
        # cls.mypath_set.add(k)
        cls.mycounter[k] += 1

    @classmethod
    def start(cls):
        cls.reset_me()

        cls.jump(RAIL_ROAD_ENTRANCE_ID)

    @classmethod
    def jump(cls, curr_key):

        cls.hops += 1
        if cls.hops >= cls.stop_search:
            # raise Exception("TOO LONG HERE")
            # print("STOPPED ME, jump limit reached")
            return

        if cls.should_stop():
            # print("about to pop and come back")
            # cls.pop_path()
            return

        # if cls.hops % 1_000_000 == 0:
        t = time.time()
        if (t - cls.last_print_time) > cls.print_interval:
            # print(cls.hops, curr_key, len(cls.mypath), len(cls.solutions))

            edges = [(cls.mypath[i - 1], cls.mypath[i]) for i in range(1, len(cls.mypath))]
            display_dictionary(cls.mydict, edges)

            cls.last_print_time = t

        if len(set(cls.mypath)) == TOTAL_ROWS:
            cls.add_solution()

            # cls.pop_path()
            return
        else:
            # print(len(set(cls.mypath)), TOTAL_ROWS)
            pass

        for k in cls.edges_dict[curr_key]:
            # if k in cls.mypath_set:
            #     continue

            cls.append_path(k)
            cls.jump(k)
            cls.pop_path()








if __name__ == "__main__":
    attraction_map  = load_maps()
    DFS.edges_dict = getEdgesDict(attraction_map)
    DFS.start()
    print(DFS.hops)
    for s in DFS.solutions:
        print(s)
    pass
