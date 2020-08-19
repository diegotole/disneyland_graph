import unittest
from preprocessing.edges_parser import haversine_km


class MyTestCase(unittest.TestCase):
    def test_haversine(self):
        lon1, lat1, lon2, lat2 = -0.116773, 51.510357, -77.009003, 38.889931

        ans = round(5897.658289, 6)
        hav = round(haversine_km(lon1, lat1, lon2, lat2), 6)
        print(ans, hav)
        self.assertTrue(ans == hav)


if __name__ == '__main__':
    unittest.main()
