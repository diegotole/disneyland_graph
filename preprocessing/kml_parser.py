import xmltodict, csv
import utils


def transform_kml_into_dict():
    file_name = "data/Disneyland Graph.kml"
    with open(file_name) as xml_file:
        data_dict = xmltodict.parse(xml_file.read())

    return data_dict

def parse_kml():

    data_dict = transform_kml_into_dict()

    with open("data/disneyland_attractions.csv", 'w') as fout:
        csv_writer = csv.writer(fout)
        csv_writer.writerow(['id', 'gearth_id', 'name', 'lat', 'long'])
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
                    long]

            )

        rows.sort(key=lambda x: x[1])

        csv_writer.writerows(rows)
        return rows


