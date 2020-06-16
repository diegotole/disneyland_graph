import xmltodict, csv

file_name = "Disneyland Graph.kml"

with open(file_name) as xml_file:
    data_dict = xmltodict.parse(xml_file.read())

with open("disneyland_attractions.csv", 'w') as fout:
    csv_writer = csv.writer(fout)
    csv_writer.writerow(['place_id', 'name', 'lat', 'long'])
    rows = []
    for idx, placemark in enumerate(data_dict['kml']['Document']['Placemark']):
        # print(placemark)
        lat, long = placemark["LookAt"]['latitude'], placemark['LookAt']['longitude']
        name = placemark['name']
        place_id = placemark['@id']
        rows.append(
            [place_id,
             name.lower(),
             lat,
             long]

        )

    rows.sort(key=lambda x: x[1])

    csv_writer.writerows(rows)

## website lists 55 attractions
# -1 holiday decoration is outside park, discarded
# +1 fortune teller has 2 locations
# +3 there are 4 railroad stations
# -1 datapad is mobile app game
# +3 SW entrances

print(len(rows))
# total 5
total_rows = (55 - 1 + 1 + 3 - 1 + 3)
assert len(rows) == total_rows

# no repeats
coords = [(x[-1], x[-2]) for x in rows]
assert len(coords) == len(set(tuple(coords)))
