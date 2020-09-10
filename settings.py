def get_ride_id(hex):
    return int(hex, 16) % 100000


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

CONNECTION_SW_ADV_LAND = {SW_ENTRANCE_ADV_LAND, }
CONNECTION_SW_FRONTIER = {SW_ENTRANCE_FRONTIER_LAND, }
CONNECTION_SW_FANTASY = {SW_ENTRANCE_FANTASY_LAND, }

FANTASY_LAND = {
    "029CF4E7CE13A7C139C8",
    "030606F92B13A7C1D1E1",
    "05DE65A65813B16F4EF9",
    "0600C026F613A7C19D77",
    "066915218D13A7BFF593",
    "079ACFAD3413A7C301E8",
    "08186403BC13B0A688CA",
    "0B4FDB258813BC04D88B",
    "0BDDD94EB613A7C20841",
    "0D12A6B8D013A7BFE61D",
    "0E2A31BD5613B0A3295B",
    "0ED9128B2213C25E7840",
    "0F27749CE713A7C2EBF6",
    "0FD9BE9B7513A7C00B76"

}
FANTASY_LAND = {get_ride_id(i) for i in FANTASY_LAND}

TOMORROW_LAND = {
    "005DCC8A8413B6B56EFF",
    "01A126989313B0A7AA52",
    "06B1424A4613A7C17094",
    "08F6B05F6813A7C4734D",
    "0B73DF4CAC13A7C403A6",
    "0CEB5828ED13A7C449E7",
    "0E8EB1CD7613A7C4569F",
    "0EF77D74B213A7C4392B",
    "0F6CE8437413B1780353",

}
TOMORROW_LAND = {get_ride_id(i) for i in TOMORROW_LAND}

MAIN_STREET = {
    "0122F0529313BC07DDD6",
    "05339F3E7F13B1740ECE",
    "086C7A03AC13BC08F3B2",
    "0881FBFB6613B1743A40",
    "0AB31AE41D13B6BB8A9A",
    "0BF5D5A0A713B6B6A081",
    "0EA01CB54313BC0B7CAA",

}
MAIN_STREET = {get_ride_id(i) for i in MAIN_STREET}

ADVENTURE_LAND = {
    "007D6F8B3313A7A71F44",
    "024911581213A7A7887A",
    "04A79152A813A7A76D39",
    "0AAA11A5E113C261ADD1",

}

ADVENTURE_LAND = {get_ride_id(i) for i in ADVENTURE_LAND}

FRONTIER_LAND = {
    "0577C24E6013A7C2AF38",
    "05B39FBDCE13A7C502CC",
    "087200FCCF13A7BEBED5",
    "09BD79D7C213B6C0CB0F",
    "0A6050D15A13C25D55ED",

}
FRONTIER_LAND = {get_ride_id(i) for i in FRONTIER_LAND}

NEW_ORLEANS_SQUARE = {
    "00EEAF10C213B0A14102",
    "01AE7B50D113B6BEB8F5",
    "040392B74F13A7A75353",
    "076CF89D1113B6B412F0",
    "0D0C230FA613BBFDF428",

}
NEW_ORLEANS_SQUARE = {get_ride_id(i) for i in NEW_ORLEANS_SQUARE}

CRITTER_COUNTRY = {
    "0875E1562513A7BD59AB",
    "0A8B71CAD913A7BD8AA9",
    "0CC239AEC813B172106A",

}
CRITTER_COUNTRY = {get_ride_id(i) for i in CRITTER_COUNTRY}

TOON_TOWN = {
    "0005A7BFDB13B09F848E",
    "016CB3B30A13A7C38243",
    "01CF75336813B6B8962F",
    "01DB559F0913A7C3C41C",
    "05FF91A9C713A7C3901D",
    "06362FB21B13A7C34C64",
    "0CE037331013B6B264D4",
    "0D8D702F9D13A7C3A0D4",

}
TOON_TOWN = {get_ride_id(i) for i in TOON_TOWN}

STAR_WARS_GALAXY_EDGE = {
    "00C399D54913C25A1A98",
    "00E1B5429A13C260BC96",

}

STAR_WARS_GALAXY_EDGE = {get_ride_id(i) for i in STAR_WARS_GALAXY_EDGE}

# total 5
TOTAL_ROWS = (55 - 1 + 1 + 3 - 1 + 3)
C_REGIONS_SETS = STAR_WARS_GALAXY_EDGE | TOON_TOWN | CRITTER_COUNTRY | NEW_ORLEANS_SQUARE | FRONTIER_LAND | ADVENTURE_LAND | MAIN_STREET | TOMORROW_LAND | FANTASY_LAND
EXTRAS_CONNECTORS = CONNECTION_SW_ADV_LAND | CONNECTION_SW_FRONTIER | CONNECTION_SW_FANTASY
ALL_SETS =  EXTRAS_CONNECTORS | C_REGIONS_SETS
REGIONS_LIST = [
    (STAR_WARS_GALAXY_EDGE, "STAR_WARS_GALAXY_EDGE"),
    (TOON_TOWN, "TOON_TOWN"),
    (CRITTER_COUNTRY, "CRITTER_COUNTRY"),
    (NEW_ORLEANS_SQUARE, "NEW_ORLEANS_SQUARE"),
    (FRONTIER_LAND, "FRONTIER_LAND"),
    (ADVENTURE_LAND, "ADVENTURE_LAND"),
    (MAIN_STREET, "MAIN_STREET"),
    (TOMORROW_LAND, "TOMORROW_LAND"),
    (FANTASY_LAND, "FANTASY_LAND")

]

assert TOTAL_ROWS == len(ALL_SETS)
