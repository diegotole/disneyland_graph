import xmltodict, csv
import utils
import settings

def transform_kml_into_dict():
    file_name = "data/Disneyland Graph.kml"
    with open(file_name) as xml_file:
        data_dict = xmltodict.parse(xml_file.read())

    return data_dict


def get_ride_region(id):

    id = int(id)
    resp = None
    for region_list, region_name in settings.REGIONS_LIST:
        if id in region_list:
            resp = region_name
            break

    if resp is None:
        if id in settings.SW_EXTRAS_CONNECTORS:
            resp = "noregion"
        else:
            raise Exception(f"no region found {id}")

    return resp

def parse_kml():

    data_dict = transform_kml_into_dict()

    with open("data/disneyland_attractions.csv", 'w') as fout:
        csv_writer = csv.writer(fout)
        csv_writer.writerow(['id', 'gearth_id', 'name', 'lat', 'long', 'region'])
        rows = []
        for idx, placemark in enumerate(data_dict['kml']['Document']['Placemark']):
            lat, long = placemark["LookAt"]['latitude'], placemark['LookAt']['longitude']
            name = placemark['name']
            place_id = placemark['@id']
            ride_id = utils.get_ride_id(place_id)




            rows.append(
                [
                    ride_id,
                    place_id,
                    name.lower(),
                    lat,
                    long,
                    get_ride_region(ride_id)
                ]

            )

        rows.sort(key=lambda x: x[1])

        csv_writer.writerows(rows)
        return rows


