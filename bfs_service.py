from collections import deque
from settings import TOTAL_ROWS, RAIL_ROAD_ENTRANCE_ID
from utils import display_dictionary, getEdgesDict
import time
from collections import defaultdict
from utils import load_maps


class BFS:
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

    # attraction_map =
    edges_dict = getEdgesDict(load_maps())

    path_limit_size = 30

    @classmethod
    def add_solution(cls, mypath):

        cls.solutions.append(
            tuple(mypath)
        )

    @classmethod
    def start(cls):

        graph = {
            'A': ['B', 'C'],
            'B': ['D', 'E'],
            'C': ['F'],
            'D': [],
            'E': ['F'],
            'F': []
        }
        # cls.edges_dict = graph

        q = deque(  [
            (RAIL_ROAD_ENTRANCE_ID,(RAIL_ROAD_ENTRANCE_ID,) )
            ]
        )
        # q = deque([
        #     ('A', ('A',))
        # ])

        # all_paths = { ('A',) }
        all_paths = { (RAIL_ROAD_ENTRANCE_ID,) }






        while q:

            print( f"queue size {len(q)}" )

            for i in range(1_000_000):
                curr_key, curr_path = q.popleft()
                # print(curr_path)


                if len(cls.edges_dict[curr_key]):
                    all_paths.remove(curr_path)

                if len(set(curr_path)) == TOTAL_ROWS:
                    cls.add_solution(curr_path)
                    return

                if len(curr_path) >= cls.path_limit_size:
                    #discard here
                    print("discarding")
                    continue

                # print(f"visiting {curr_key} ")
                for k in cls.edges_dict[curr_key]:

                    new_path = curr_path+tuple([k])

                    q.append(
                        (k, new_path)
                    )


                    all_paths.add(new_path)

        print(all_paths)

if __name__ == "__main__":
    BFS.start()
