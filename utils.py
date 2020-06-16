import csv
from collections import defaultdict
import pandas as pd
from matplotlib import pyplot as plt
from decimal import Decimal
from math import radians, cos, sin, asin, sqrt

RAIL_ROAD_ENTRANCE_ID = "0BF5D5A0A713B6B6A081"
MINNIES_HOUSE_ID = "0D8D702F9D13A7C3A0D4"
RAIL_ROAD_TOMORROWLAND_ID = "005DCC8A8413B6B56EFF"
SPACE_MOUNTAIN_ID = "06B1424A4613A7C17094"

def get_coord(id1, mymap):
    return (mymap[id1]['long'], mymap[id1]['lat'])


def get_distance(id1, id2, mymap):
    point1 = get_coord(id1, mymap)
    point2 = get_coord(id2, mymap)

    return haversine(point1[0], point1[1], point2[0], point2[1])


def load_df(f_attractions, f_edges):
    df = pd.read_csv(f_attractions)

    df[['lat', 'long']] = (df[['lat', 'long']] - df[['lat', 'long']].min()) / (
            df[['lat', 'long']].max() - df[['lat', 'long']].min())

    df_edges = pd.read_csv(f_edges)

    return df, df_edges


def load_maps(f_attractions, rotated=False):
    attractions_map = {}
    # attractions_edges = defaultdict(set)

    with open(f_attractions) as fin:

        csvr = csv.reader(fin)
        next(csvr)
        for line in csvr:
            # attractions_map[line[0]] = {"name": line[1], "lat": float(line[2]), "long": float(line[3])}
            attractions_map[line[0]] = {"name": line[1], "lat": Decimal(line[2]), "long": Decimal(line[3])}
            print(line[2], Decimal(line[2]))

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
            x1, y1 = get_coord(e[0], mymap)
            x2, y2 = get_coord(e[1], mymap)

            plt.plot([x1, x2], [y1, y2])

    plt.show()


def haversine(lon1, lat1, lon2, lat2):
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
