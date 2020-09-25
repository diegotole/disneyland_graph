
from preprocessing import edges_parser
from preprocessing import kml_parser
import os



kml_parser.parse_kml()
# print(os.getcwd())
edges_parser.generate_edges_file()

print("all files generated")