import csv
import unittest
from datetime import datetime
from unittest.mock import patch, Mock

import api


class TestApi(unittest.TestCase):
    def setUp(self):
        self.csvfile = "./orders.csv"

    def test_validate(self):
        with open(self.csvfile, "r") as f:
            #lineas = [l for l in csv.DictReader(f)]
            rows = [row for row in csv.DictReader(f) if api.validate(row)]
        self.assertEqual(len(rows), 14)
        #print(rows)

    def test_validate_order(self):
        invalid_order = {'sku': 'empty', 'size': '', 'created_at': '2021-----12-01 12:11:10', 'seconds': '3600', 'expired_at': '', 'address_line_1': 'calle5', 'postal_code': '12345', 'locality': 'colonia5', 'city': 'ciudad5', 'state': 'estado5', 'country': 'pais5', 'address_line_2': '', 'notes': 'casa roja'}
        res = api.validate_order(invalid_order)
        self.assertEqual(res, False)
        valid_order = {'sku': 'empty', 'size': '', 'created_at': '2021-12-01 12:11:10', 'seconds': '3600', 'expired_at': '', 'address_line_1': 'calle5', 'postal_code': '12345', 'locality': 'colonia5', 'city': 'ciudad5', 'state': 'estado5', 'country': 'pais5', 'address_line_2': '', 'notes': 'casa roja'}
        res = api.validate_order(valid_order)
        self.assertEqual(res, True)

    def test_validate_address(self):
        invalid_address = {'address_line_X': 'calle5', 'postal_code': '12345', 'locality': 'colonia5', 'city': 'ciudad5', 'state': 'estado5', 'country': 'pais5', 'address_line_2': '', 'notes': 'casa roja'}
        res = api.validate_address(invalid_address)
        self.assertEqual(res, False)
        valid_address = {'address_line_1': 'calle5', 'postal_code': '12345', 'locality': 'colonia5', 'city': 'ciudad5', 'state': 'estado5', 'country': 'pais5', 'address_line_2': '', 'notes': 'casa roja'}
        res = api.validate_address(valid_address)
        self.assertEqual(res, True)

    def test_valid_date(self):
        valid_dates = [
            "2022-01-27",
            "2022/01/27",
            "27/01/2022",
            "27-01-2022",
            "2022-01-27 12:11:10",
            "2022/01/27 12:11:10",
            "27/01/2022 12:11:10",
            "27-01-2022 12:11:10",
        ]
        for d in valid_dates:
            res = api.valid_date(d)
            self.assertTrue(res)
        # invalid date
        res = api.valid_date("2022_01_27")
        self.assertFalse(res)

        
    @patch("api.cargamos.datetime")
    def test_main(self, mock_dt):
        mock_dt.now.return_value = datetime(2022, 1, 25, 13, 12, 11)
        res = api.main(self.csvfile)
        # todos los registros no repetidos
        self.assertEqual(len(res), 10)
        # orden con la mayor diferencia entre created_at y expired_at
        self.assertEqual(res[0].alive_time, 3408469)
        self.assertEqual(res[-1].delivered_at, None)
        self.assertEqual(res[5].delivered_at, None)
        # mark as delivered
        res = api.main(self.csvfile, skus_delivered=["sku_one", "1231231123"])
        self.assertEqual(res[-1].delivered_at, datetime(2022, 1, 25, 13, 12, 11))
        # orden expirada
        self.assertEqual(res[5].delivered_at, None)
