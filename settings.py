
def get_ride_id(hex):
    return int(hex, 16)%100000


ATTRACTIONS_FNAME = "data/disneyland_attractions.csv"
ATTRACTIONS_EDGES_FNAME = "data/attractions_edges.csv"



RAIL_ROAD_ENTRANCE_ID = get_ride_id("0BF5D5A0A713B6B6A081")
MINNIES_HOUSE_ID = get_ride_id("0D8D702F9D13A7C3A0D4")
RAIL_ROAD_TOMORROWLAND_ID = get_ride_id("005DCC8A8413B6B56EFF")

SW_LAUNCH_BAY = get_ride_id("0CEB5828ED13A7C449E7")
SPACE_MOUNTAIN_ID = get_ride_id("06B1424A4613A7C17094")
SW_TOURS = get_ride_id("08F6B05F6813A7C4734D")


FORTUNE_TELLER_MST_ID = get_ride_id("0AB31AE41D13B6BB8A9A")
TIKI_ROOM_ID = get_ride_id("024911581213A7A7887A")
CASTLE_ID = get_ride_id("0ED9128B2213C25E7840")
ASTRO_ORBITOR_ID = get_ride_id("01A126989313B0A7AA52")

BUZZ_RIDE = get_ride_id("0E8EB1CD7613A7C4569F")


WINNIE_POOH = get_ride_id("0A8B71CAD913A7BD8AA9")
SW_ENTRANCE_ADV_LAND = get_ride_id("0B76231CE813D58AA419")
SW_ENTRANCE_FANTASY_LAND = get_ride_id("045BFCC4E813D58E7955")
SW_ENTRANCE_FRONTIER_LAND = get_ride_id("02E9209DE313D58F29B2")
DAVY_CROC = get_ride_id("0CC239AEC813B172106A")

RISE_RESISTANCE = get_ride_id("00E1B5429A13C260BC96")
SMUGGLERS_RUN = get_ride_id("00C399D54913C25A1A98")

STORY_BOOK = get_ride_id("0F27749CE713A7C2EBF6")
SMALL_WORLD = get_ride_id("0600C026F613A7C19D77")
SMALL_WORLD_HOLIDAY = get_ride_id("0B4FDB258813BC04D88B")

MATTERHORN = get_ride_id("0BDDD94EB613A7C20841")
NEMO = get_ride_id("0B73DF4CAC13A7C403A6")
## website lists 55 attractions
# -1 holiday decoration is outside park, discarded
# +1 fortune teller has 2 locations
# +3 there are 4 railroad stations
# -1 datapad is mobile app game
# +3 SW entrances


# total 5
TOTAL_ROWS = (55 - 1 + 1 + 3 - 1 + 3)