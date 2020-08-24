import unittest
from preprocessing.edges_parser import haversine_km, get_hard_coded_edges, generate_edges_file
from collections import Counter
from unittest.mock import Mock, patch
import settings
import tempfile
import csv


class MyTestCase(unittest.TestCase):
    def test_haversine(self):
        lon1, lat1, lon2, lat2 = -0.116773, 51.510357, -77.009003, 38.889931

        ans = round(5897.658289, 6)
        hav = round(haversine_km(lon1, lat1, lon2, lat2), 6)
        print(ans, hav)
        self.assertTrue(ans == hav)

    def test_check_harc_coded_edges(self):
        edges = get_hard_coded_edges()
        c = Counter(edges)

        # one of each
        all_ones = [v == 1 for k, v in c.items()]
        self.assertTrue(all(all_ones))

        # bi directional

        for k, v in c.items():

            source, target = k

            if (target, source) not in c:
                self.fail(f"not bi directional, missing   {(target, source)} ")

    # @patch("preprocessing.edges_parser.get_hard_coded_edges")
    @patch("preprocessing.edges_parser.settings")
    def test_gen_edge_file(self, mocked_settings):

        mocked_settings.ATTRACTIONS_FNAME = settings.ATTRACTIONS_FNAME
        with tempfile.TemporaryDirectory() as tmpdirname:
            mocked_settings.ATTRACTIONS_EDGES_FNAME = tmpdirname + "/test_gen_edge_file"
            generate_edges_file()

            with open(mocked_settings.ATTRACTIONS_EDGES_FNAME) as fin:
                csvr = csv.reader(fin)

                names = set(next(csvr))
                self.assertTrue(len(names) == 3)
                self.assertTrue(names == {"source", "target", "distance_km"})


