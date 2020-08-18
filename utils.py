import csv
from collections import defaultdict, Counter
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import cm
from decimal import Decimal
from math import radians, cos, sin, asin, sqrt
import settings
from settings import *
import shelve
# RAIL_ROAD_ENTRANCE_ID = "0BF5D5A0A713B6B6A081"
# MINNIES_HOUSE_ID = "0D8D702F9D13A7C3A0D4"
# RAIL_ROAD_TOMORROWLAND_ID = "005DCC8A8413B6B56EFF"
# SPACE_MOUNTAIN_ID = "06B1424A4613A7C17094"
from cachetools import LRUCache, cached
import time


# @cached(cache=LRUCache(maxsize=3000))


def pre_calculate_distances(edges_dict, myshelve):
    # edges_dict = getEdgesDict(load_maps())

    # curr = RAIL_ROAD_ENTRANCE_ID
    # myshelve = {}
    edges = 0
    gg = GeoUtils(load_maps())
    for source in edges_dict:
        for target in edges_dict[source]:

            edges += 1
            key1 = repr((source, target))
            key2 = repr((target, source))

            dist = gg.get_distance(source, target)

            if key1 not in myshelve:
                myshelve[key1] = dist

            if key2 not in myshelve:
                myshelve[key2] = dist
    print(f"done {edges} edges")
    return myshelve


class GeoUtils:

    def __init__(self, mymap):

        self.geo_locations = mymap

    @cached(cache=LRUCache(maxsize=3000))
    def get_coord(self, id1):
        try:
            return (self.geo_locations[id1]['long'], self.geo_locations[id1]['lat'])
        except Exception as e:
            pass
        raise e

    @cached(cache=LRUCache(maxsize=3000))
    def get_distance(self, id1, id2):
        # point1 = get_coord(id1, mymap)
        # point2 = get_coord(id2, mymap)
        point1 = (self.geo_locations[id1]['long'], self.geo_locations[id1]['lat'])
        point2 = (self.geo_locations[id2]['long'], self.geo_locations[id2]['lat'])

        return self.haversine(point1[0], point1[1], point2[0], point2[1])

    @cached(cache=LRUCache(maxsize=3000))
    def haversine(self, lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)
        """
        lon1, lat1, lon2, lat2 = Decimal(lon1), Decimal(lat1), Decimal(lon2), Decimal(lat2)

        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        r = 6371  # Radius of earth in kilometers. Use 3956 for miles
        return c * r


def load_df(f_attractions, f_edges):
    df = pd.read_csv(f_attractions)

    df[['lat', 'long']] = (df[['lat', 'long']] - df[['lat', 'long']].min()) / (
            df[['lat', 'long']].max() - df[['lat', 'long']].min())

    df_edges = pd.read_csv(f_edges)

    return df, df_edges


def load_maps(f_attractions=settings.ATTRACTIONS_FNAME, rotated=False):
    attractions_map = {}
    # attractions_edges = defaultdict(set)

    with open(f_attractions) as fin:

        csvr = csv.DictReader(fin)
        # next(csvr)
        for line in csvr:
            # attractions_map[line[0]] = {"name": line[1], "lat": float(line[2]), "long": float(line[3])}
            line['lat'] , line['long'] = Decimal(line['lat']), Decimal(line['long'])
            attractions_map[int(line['id'])] = line
            # print(line[2], Decimal(line[2]))

    # with open(f_edges) as fin:
    #
    #     csvr = csv.reader(fin)
    #     next(csvr)
    #
    #     for line in csvr:
    #         attractions_edges[line[0]].add(line[1])

    if rotated:
        print("rotating")
        tmp = {x: attractions_map[x]['lat'] for x in attractions_map}

        for idx, key in enumerate(attractions_map):
            attractions_map[key]['lat'] = attractions_map[key]['long']
            attractions_map[key]['long'] = tmp[key]

    return attractions_map


def display_dictionary(mymap, edges=None):
    ##ROTATE coordinates
    # df['tmp'] = df['rot_x']
    # df['rot_x'] = df['rot_y']
    # df['rot_y'] = df['tmp']

    GeoHelper = GeoUtils(mymap)
    plt.figure(figsize=(10, 10))
    plt.scatter([mymap[x]['long'] for x in mymap], [mymap[x]['lat'] for x in mymap])

    plt.scatter([mymap[RAIL_ROAD_ENTRANCE_ID]['long'], ], [mymap[RAIL_ROAD_ENTRANCE_ID]['lat'], ], color="red")
    plt.annotate("Rail Road Entrance", (mymap[RAIL_ROAD_ENTRANCE_ID]['long'], mymap[RAIL_ROAD_ENTRANCE_ID]['lat']))

    plt.scatter([mymap[MINNIES_HOUSE_ID]['long'], ], [mymap[MINNIES_HOUSE_ID]['lat'], ], color="black")
    plt.annotate("Minnie's house", (mymap[MINNIES_HOUSE_ID]['long'], mymap[MINNIES_HOUSE_ID]['lat']))

    plt.scatter([mymap[RAIL_ROAD_TOMORROWLAND_ID]['long'], ], [mymap[RAIL_ROAD_TOMORROWLAND_ID]['lat'], ],
                color="yellow")
    plt.annotate("Rail Road Tomorrowland",
                 (mymap[RAIL_ROAD_TOMORROWLAND_ID]['long'], mymap[RAIL_ROAD_TOMORROWLAND_ID]['lat']))

    plt.scatter([mymap[SPACE_MOUNTAIN_ID]['long'], ], [mymap[SPACE_MOUNTAIN_ID]['lat'], ],
                color="purple")
    plt.annotate("Space Mountain",
                 (mymap[SPACE_MOUNTAIN_ID]['long'], mymap[SPACE_MOUNTAIN_ID]['lat']))

    if edges:

        edges_coord = [
            tuple(
                sorted(
                    (GeoHelper.get_coord(e[0]), GeoHelper.get_coord(e[1]))
                )

            )

            for e in edges
        ]
        edges_count = Counter(edges_coord)
        pass
        # edges_count = {}
        for key in edges_count:

            # if sorted()
            edges_count[key] =  edges_count[key]**8
        # edges_count[
        #     ((Decimal('-117.9188180645016'), Decimal('33.80996898917935')),
        #      (Decimal('-117.9187237144692'), Decimal('33.81059829734667')))
        # ] = 999999

        total = sum(edges_count.values(), 0.0)
        for key in edges_count:
            edges_count[key] = edges_count[key] / total
        mycolors = []
        for e in edges:
            x1, y1 = GeoHelper.get_coord(e[0])
            x2, y2 = GeoHelper.get_coord(e[1])

            color_key =  tuple(  sorted( ((x1, y1), (x2, y2))  )  )

            plt.plot([x1, x2], [y1, y2], color=plt.cm.jet(edges_count.get(color_key)))  # color = color
            mycolors.append(  plt.cm.jet(edges_count.get(color_key))  )
        # x = [  point[0]  for line in edges_coord for point in line]
        # y = [  point[1]  for line in edges_coord for point in line]
        # for
        # plt.plot(x ,y,  cmap=plt.cm.RdBu   )
        # plt.plot( [ x[0]  for x in pair for pair in edges_coord ] , [x[1] for x in edges_coord ]    )

    plt.show()


def getEdgesDict(attractions_map):

    parsed_edges_dict = defaultdict(list)
    with open(settings.ATTRACTIONS_EDGES_FNAME) as fin:
        csvr = csv.DictReader(fin)
        for line in csvr:
            parsed_edges_dict[int(line['source'])].append(int(line['target']))
            parsed_edges_dict[ (int(line['source']), int(line['target']  ))    ] = Decimal(line["distance_meters"])

    return parsed_edges_dict






if __name__ == "__main__":
    f_maps = "disneyland_attractions.csv"
    f_edges = "attractions_edges.csv"

    # mmap, medges = load_maps(f_maps, f_edges)
    #
    # display_dictionary(mmap)
    t1 = time.time()
    with shelve.open('my_distances') as db_distances:
        pre_calculate_distances(getEdgesDict(load_maps()), db_distances)
    print(f"time took:{time.time() - t1}")

# def display_df(x,y ):
#     plt.figure(figsize=(10,10))
#
#     plt.scatter( x, y)
#
#     plt.scatter( (RAIL_ROAD_ENTRANCE_ROW['rot_x'].values[0] ,), (RAIL_ROAD_ENTRANCE_ROW['rot_y'].values[0] ,) , color="red" )
#     plt.scatter( (MINNIES_HOUSE_ROW['rot_x'].values[0] ,), (MINNIES_HOUSE_ROW['rot_y'].values[0] ,) , color="black" )
#     plt.scatter( (RAIL_ROAD_TOMORROWLAND_ROW['rot_x'].values[0] ,), (RAIL_ROAD_TOMORROWLAND_ROW['rot_y'].values[0] ,) , color="yellow" )
#
#
#     plt.show()
