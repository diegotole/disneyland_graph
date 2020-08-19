import unittest
from preprocessing import kml_parser
from unittest.mock import patch
from settings import TOTAL_ROWS
import xmltodict


@patch("preprocessing.kml_parser.transform_kml_into_dict")
@patch("preprocessing.kml_parser.open")
class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        file_name = "data/Disneyland Graph.kml"
        with open(file_name) as xml_file:
            data_dict = xmltodict.parse(xml_file.read())

        self.data_dict = data_dict

    def test_data_integrity(self, mock_open, transform_kml_into_dict):
        transform_kml_into_dict.return_value = self.data_dict

        rows = kml_parser.parse_kml()
        self.assertTrue(len(rows) == TOTAL_ROWS)

        # no repeats
        coords = [(x[-1], x[-2]) for x in rows]
        self.assertTrue(len(coords) == len(set(tuple(coords))))

    def test_right_schema(self, mock_csv, transform_kml_into_dict):
        transform_kml_into_dict.return_value = self.data_dict

        rows = kml_parser.parse_kml()

        self.assertTrue(len(rows[0]) == 5)
        self.assertTrue(type(rows[0][0]) == type(1))


