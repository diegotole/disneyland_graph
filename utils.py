import csv
from collections import defaultdict
import pandas as pd
from matplotlib import pyplot as plt
from decimal import Decimal
from math import radians, cos, sin, asin, sqrt
import settings
from settings import *

RAIL_ROAD_ENTRANCE_ID = "0BF5D5A0A713B6B6A081"
MINNIES_HOUSE_ID = "0D8D702F9D13A7C3A0D4"
RAIL_ROAD_TOMORROWLAND_ID = "005DCC8A8413B6B56EFF"
SPACE_MOUNTAIN_ID = "06B1424A4613A7C17094"
from cachetools import LRUCache, cached

# @cached(cache=LRUCache(maxsize=3000))

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

        csvr = csv.reader(fin)
        next(csvr)
        for line in csvr:
            # attractions_map[line[0]] = {"name": line[1], "lat": float(line[2]), "long": float(line[3])}
            attractions_map[line[0]] = {"name": line[1], "lat": Decimal(line[2]), "long": Decimal(line[3])}
            #print(line[2], Decimal(line[2]))

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

        for e in edges:
            x1, y1 = GeoHelper.get_coord(e[0])
            x2, y2 = GeoHelper.get_coord(e[1])

            plt.plot([x1, x2], [y1, y2])

    plt.show()





def getEdgesDict(attractions_map):
    edges = set()
    max_distance = 80
    GeoHelper = GeoUtils(attractions_map)
    for k1, v1 in attractions_map.items():
        for k2, v2 in attractions_map.items():

            if k1 == k2:
                continue

            source = min(k1, k2)
            target = max(k1, k2)
            d = GeoHelper.get_distance(source, target) * 1000
            if d <= max_distance:
                edges.add((source, target))

    hard_coded_edges = set()

    hard_coded_edges.add((SPACE_MOUNTAIN_ID, SW_LAUNCH_BAY))
    hard_coded_edges.add((SPACE_MOUNTAIN_ID, SW_TOURS))

    hard_coded_edges.add((BUZZ_RIDE, SW_LAUNCH_BAY))

    # WINNIE_POOH = "0A8B71CAD913A7BD8AA9"
    # SW_ENTRANCE_ADV_LAND = "0B76231CE813D58AA419"
    # SW_ENTRANCE_FANTASY_LAND = "045BFCC4E813D58E7955"
    # SW_ENTRANCE_FRONTIER_LAND = "02E9209DE313D58F29B2"
    # DAVY_CROC = "0CC239AEC813B172106A"

    # STORY_BOOK_ "0F27749CE713A7C2EBF6"
    # SMALL_WORLD = "0600C026F613A7C19D77"
    hard_coded_edges.add((STORY_BOOK, SMALL_WORLD))

    hard_coded_edges.add((STORY_BOOK, SMALL_WORLD_HOLIDAY))

    hard_coded_edges.add((RISE_RESISTANCE, SMUGGLERS_RUN))
    hard_coded_edges.add((RISE_RESISTANCE, SW_ENTRANCE_FRONTIER_LAND))

    hard_coded_edges.add((SW_ENTRANCE_FANTASY_LAND, SMUGGLERS_RUN))
    hard_coded_edges.add((SW_ENTRANCE_ADV_LAND, SMUGGLERS_RUN))

    hard_coded_edges.add((DAVY_CROC, SW_ENTRANCE_FRONTIER_LAND))
    hard_coded_edges.add((WINNIE_POOH, SW_ENTRANCE_FRONTIER_LAND))

    hard_coded_edges.add((FORTUNE_TELLER_MST_ID, TIKI_ROOM_ID))
    hard_coded_edges.add((FORTUNE_TELLER_MST_ID, CASTLE_ID))
    hard_coded_edges.add((FORTUNE_TELLER_MST_ID, ASTRO_ORBITOR_ID))

    hard_coded_edges.add((TIKI_ROOM_ID, CASTLE_ID))
    hard_coded_edges.add((TIKI_ROOM_ID, ASTRO_ORBITOR_ID))

    hard_coded_edges.add((CASTLE_ID, ASTRO_ORBITOR_ID))

    edges = edges.union(hard_coded_edges)

    edges_dict = defaultdict(list)

    for e in edges:
        edges_dict[e[0]].append(e[1])
        edges_dict[e[1]].append(e[0])

    for k in edges_dict.keys():
        edges_dict[k] = tuple(edges_dict[k])


    return edges_dict



if __name__ == "__main__":
    f_maps = "disneyland_attractions.csv"
    f_edges = "attractions_edges.csv"

    mmap, medges = load_maps(f_maps, f_edges)

    display_dictionary(mmap)

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
