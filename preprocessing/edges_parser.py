import csv
import settings
from settings import *
from math import radians, cos, sin, asin, sqrt
from decimal import Decimal
import logging


def haversine_km(lon1, lat1, lon2, lat2):
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


# those are edges that are too
def get_hard_coded_edges():
    hard_coded_edges = set()

    hard_coded_edges.add((MATTERHORN, NEMO))
    hard_coded_edges.add((NEMO, MATTERHORN))

    hard_coded_edges.add((MATTERHORN, CASTLE_ID))
    hard_coded_edges.add((CASTLE_ID, MATTERHORN))



    hard_coded_edges.add((SPACE_MOUNTAIN_ID, SW_LAUNCH_BAY))
    hard_coded_edges.add((SW_LAUNCH_BAY, SPACE_MOUNTAIN_ID))

    hard_coded_edges.add((SPACE_MOUNTAIN_ID, SW_TOURS))
    hard_coded_edges.add((SW_TOURS, SPACE_MOUNTAIN_ID))

    hard_coded_edges.add((BUZZ_RIDE, SW_LAUNCH_BAY))
    hard_coded_edges.add((SW_LAUNCH_BAY, BUZZ_RIDE))

    hard_coded_edges.add((STORY_BOOK, SMALL_WORLD))
    hard_coded_edges.add((SMALL_WORLD, STORY_BOOK))

    hard_coded_edges.add((STORY_BOOK, SMALL_WORLD_HOLIDAY))
    hard_coded_edges.add((SMALL_WORLD_HOLIDAY, STORY_BOOK))

    hard_coded_edges.add((RISE_RESISTANCE, SMUGGLERS_RUN))
    hard_coded_edges.add((SMUGGLERS_RUN, RISE_RESISTANCE))

    # hard_coded_edges.add((RISE_RESISTANCE, SW_ENTRANCE_FRONTIER_LAND))
    # hard_coded_edges.add((SW_ENTRANCE_FRONTIER_LAND, RISE_RESISTANCE))
    #
    # hard_coded_edges.add((DAVY_CROC, SW_ENTRANCE_FRONTIER_LAND))
    # hard_coded_edges.add((SW_ENTRANCE_FRONTIER_LAND, DAVY_CROC))
    #
    # hard_coded_edges.add((WINNIE_POOH, SW_ENTRANCE_FRONTIER_LAND))
    # hard_coded_edges.add((SW_ENTRANCE_FRONTIER_LAND, WINNIE_POOH))

    # hard_coded_edges.add((SW_ENTRANCE_FANTASY_LAND, SMUGGLERS_RUN))
    # hard_coded_edges.add((SMUGGLERS_RUN, SW_ENTRANCE_FANTASY_LAND))
    #
    # hard_coded_edges.add((SW_ENTRANCE_ADV_LAND, SMUGGLERS_RUN))
    # hard_coded_edges.add((SMUGGLERS_RUN, SW_ENTRANCE_ADV_LAND))

    hard_coded_edges.add((FORTUNE_TELLER_MST_ID, TIKI_ROOM_ID))
    hard_coded_edges.add((TIKI_ROOM_ID, FORTUNE_TELLER_MST_ID))



    hard_coded_edges.add((FORTUNE_TELLER_MST_ID, CASTLE_ID))
    hard_coded_edges.add((CASTLE_ID, FORTUNE_TELLER_MST_ID))

    hard_coded_edges.add((FORTUNE_TELLER_MST_ID, SHOOTING_EXPO))
    hard_coded_edges.add((SHOOTING_EXPO, FORTUNE_TELLER_MST_ID))


    hard_coded_edges.add((FORTUNE_TELLER_MST_ID, ASTRO_ORBITOR_ID))
    hard_coded_edges.add((ASTRO_ORBITOR_ID, FORTUNE_TELLER_MST_ID))

    hard_coded_edges.add((TIKI_ROOM_ID, CASTLE_ID))
    hard_coded_edges.add((CASTLE_ID, TIKI_ROOM_ID))

    hard_coded_edges.add((TIKI_ROOM_ID, ASTRO_ORBITOR_ID))
    hard_coded_edges.add((ASTRO_ORBITOR_ID, TIKI_ROOM_ID))

    hard_coded_edges.add((CASTLE_ID, ASTRO_ORBITOR_ID))
    hard_coded_edges.add((ASTRO_ORBITOR_ID, CASTLE_ID))

    hard_coded_edges.add((HAUNTED_MANSION, TOM_SAWYER_ISLAND))
    hard_coded_edges.add((TOM_SAWYER_ISLAND, HAUNTED_MANSION))

    hard_coded_edges.add((SPLASH_MOUNTAIN, TOM_SAWYER_ISLAND))
    hard_coded_edges.add((TOM_SAWYER_ISLAND, SPLASH_MOUNTAIN))

    hard_coded_edges.add((DAVY_CROC, TOM_SAWYER_ISLAND))
    hard_coded_edges.add((TOM_SAWYER_ISLAND, DAVY_CROC))


    hard_coded_edges.add(  (STORY_BOOK, ROGER_RABBIT)   )
    hard_coded_edges.add(  (ROGER_RABBIT, STORY_BOOK)   )

    hard_coded_edges.add((STORY_BOOK, RAIL_ROAD_TOON_TOWN))
    hard_coded_edges.add((RAIL_ROAD_TOON_TOWN, STORY_BOOK))


    return hard_coded_edges


def generate_edges_file():
    max_distance = 80 / 1000  # havesine returns in KM. we are checking for landmarks 80 meters away
    # print("FILE NAME: ", settings.ATTRACTIONS_EDGES_FNAME)
    # logging.warning("FILE NAME: "+ settings.ATTRACTIONS_EDGES_FNAME)

    with open(settings.ATTRACTIONS_EDGES_FNAME, 'w') as fout:
        csw = csv.writer(fout)
        csw.writerow(['source', 'source_name', 'target', 'target_name', 'distance_km'])
        cache = {}
        with open(settings.ATTRACTIONS_FNAME) as fin:
            my_attractions_nodes = list(csv.DictReader(fin))

            for r1 in my_attractions_nodes:
                cache[int(r1['id'])] = r1
                for r2 in my_attractions_nodes:

                    if r1['id'] == r2['id']:
                        continue

                    if int(r1['id']) in SW_EXTRAS_CONNECTORS:
                        continue

                    if int(r2['id']) in SW_EXTRAS_CONNECTORS:
                        continue

                    distance = haversine_km(r1['long'], r1['lat'], r2['long'], r2['lat'])
                    if distance <= max_distance:
                        csw.writerow(

                            [r1['id'], r1['name'], r2['id'], r2['name'], distance]

                        )

            for e1, e2 in get_hard_coded_edges():
                r1 = cache[e1]
                r2 = cache[e2]

                # if e1 in SW_EXTRAS_CONNECTORS:
                #     continue
                #
                # if e2 in SW_EXTRAS_CONNECTORS:
                #     continue

                distance = haversine_km(r1['long'], r1['lat'], r2['long'], r2['lat'])
                csw.writerow(

                    [r1['id'], r1['name'], r2['id'], r2['name'], distance]

                )

        # artificial edges
        art_edges = {

            # frontier land
            73113: [60568, 280],

            # critter country
            33970: [714, 43753, 49078],
            # fantasy
            87125: [32605, 280]

        }

        for sw_entrance in art_edges:

            for e1 in art_edges[sw_entrance]:
                for e2 in art_edges[sw_entrance]:

                    if e1 == e2:
                        continue

                    r1 = cache[e1]
                    r2 = cache[e2]
                    sw = cache[sw_entrance]

                    d1 = haversine_km(r1['long'], r1['lat'], sw['long'], sw['lat'])
                    d2 = haversine_km(r2['long'], r2['lat'], sw['long'], sw['lat'])
                    distance = d1 + d2
                    csw.writerow(

                        [r1['id'], r1['name'], r2['id'], r2['name'], distance]

                    )

# generate_edges_file()
