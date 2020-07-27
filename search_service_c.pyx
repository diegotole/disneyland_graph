
from settings import TOTAL_ROWS,RAIL_ROAD_ENTRANCE_ID
from utils import display_dictionary
import time

class DFS:
    mypath = [RAIL_ROAD_ENTRANCE_ID,]
    mypath_set = set([RAIL_ROAD_ENTRANCE_ID,])
    solutions = []
    short_stop = 80
    hops = 0
    stop_search = 5_000_000
    last_print_time = time.time()
    print_interval = 60*5
    mydict = None
    edges_dict = None

    @classmethod
    def reset_me(cls):
        cls.mypath = [RAIL_ROAD_ENTRANCE_ID,]
        # cls.mypath_set = set([RAIL_ROAD_ENTRANCE_ID,])
        cls.solutions = []
        cls.short_stop = 80
        cls.hops = 0
        cls.stop_search = 5_000_000 * 100

    @classmethod
    def add_solution(cls):

        cls.solutions.append(
            list(cls.mypath)
        )

    @classmethod
    def should_stop(cls ):
        # if len(cls.mypath) > cls.short_stop:
        #     return True
        #
        # return False
        cls.mypath_set = set(cls.mypath)

        missing = TOTAL_ROWS - len(cls.mypath_set) #55 - 1 = 54
        remaining_slots = cls.short_stop - len(cls.mypath) #80 - 1

        if missing > remaining_slots: # 54 > 79
            # print(missing, remaining_slots)
            return True

        return False

    @classmethod
    def pop_path(cls):
        if len(cls.mypath):
            k = cls.mypath.pop()
            # cls.mypath_set.remove(k)

    @classmethod
    def append_path(cls, k):
        cls.mypath.append(k)
        # cls.mypath_set.add(k)

    @classmethod
    def jump(cls,  curr_key):

        # cls.hops += 1
        # if cls.hops >= cls.stop_search:
        #     # raise Exception("TOO LONG HERE")
        #     print("STOPPED ME")
        #     return

        if cls.should_stop():
            cls.pop_path()
            return

        #if cls.hops % 1_000_000 == 0:
        t = time.time()
        if (t - cls.last_print_time) > cls.print_interval:
            print(cls.hops, curr_key, len(cls.mypath), len(cls.solutions))

            edges = [ (cls.mypath[i-1],cls.mypath[i])  for i in range(1, len(cls.mypath ))  ]
            display_dictionary(cls.mydict, edges )

            cls.last_print_time = t

        if len(set(cls.mypath)) == TOTAL_ROWS:
            cls.add_solution()

            cls.pop_path()
            return

        for k in cls.edges_dict[curr_key]:

            # if k in cls.mypath_set:
            #     continue

            cls.append_path(k)
            cls.jump( k)

        cls.pop_path()

        return
