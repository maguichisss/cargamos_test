import unittest
from unittest.mock import patch, Mock
from datetime import datetime, timedelta
import cargamos


class TestPackage(unittest.TestCase):
    @patch("cargamos.datetime")
    def setUp(self, mock_dt):
        mock_dt.now.return_value = datetime(2022, 1, 27, 20, 40, 30)
        self.package = cargamos.Package()

    def test_attrs(self):
        self.assertTrue(self.package.SKU)
        self.assertEqual(self.package.size, 1)
        self.assertEqual(self.package.total_instances, 2) # one more from TestOrder
        self.assertEqual(self.package.expired_at, datetime(2022, 1, 27, 20, 42, 30))
        self.assertEqual(self.package._Package__created_at, datetime(2022, 1, 27, 20, 40, 30))

    @patch("cargamos.datetime")
    def test_time_to_expire(self, mock_dt):
        # faltan 3 minutos
        mock_dt.now.return_value = datetime(2022, 1, 27, 20, 39, 30)
        res = self.package.time_to_expire()
        self.assertEqual(res, 180)
        # seconds false
        res = self.package.time_to_expire(seconds=False)
        self.assertEqual(res, timedelta(seconds=180))

    @patch("cargamos.datetime")
    def test_has_expired(self, mock_dt):
        # expiro hace 1 segundo
        mock_dt.now.return_value = datetime(2022, 1, 27, 20, 42, 31)
        res = self.package.has_expired()
        self.assertEqual(res, True)
        res = self.package.time_to_expire()
        self.assertEqual(res, -1)
        # 5 segundos para que expire
        mock_dt.now.return_value = datetime(2022, 1, 27, 20, 42, 25)
        res = self.package.has_expired()
        self.assertEqual(res, False)
        res = self.package.time_to_expire()
        self.assertEqual(res, 5)

    @patch("cargamos.datetime")
    def test_time_since_created(self, mock_dt):
        # 3 minutos desde que se creo
        mock_dt.now.return_value = datetime(2022, 1, 27, 20, 43, 30)
        res = self.package.time_since_created()
        self.assertEqual(res, 180)
        # seconds false
        res = self.package.time_since_created(seconds=False)
        self.assertEqual(res, timedelta(seconds=180))

    def test_total_instances(self):
        # una instancia por cada metodo en esta clase
        # ya que setUp se ejecuta al incio de cada uno
        p = cargamos.Package()
        self.assertEqual(p.total_instances, 7)
        self.assertEqual(self.package.total_instances, 7)

class TestAddress(unittest.TestCase):
    def setUp(self):
        self.address = cargamos.Address(
            "Evergreen terrace",
            "48007",
            "Springfield",
            "Springfield",
            "Nevada",
            "USA",
            address_line_2="742",
            notes="Simpson's house",
        )

    def test_attrs(self):
        self.assertEqual(self.address.address_line_1, "Evergreen terrace")
        self.assertEqual(self.address.postal_code, "48007")
        self.assertEqual(self.address.locality, "Springfield")
        self.assertEqual(self.address.city, "Springfield")
        self.assertEqual(self.address.state, "Nevada")
        self.assertEqual(self.address.country, "USA")
        self.assertEqual(self.address.address_line_2, "742")
        self.assertEqual(self.address.notes, "Simpson's house")

    def test_get_full_address(self):
        res = self.address.get_full_address()
        dir_ = "Evergreen terrace, 742, Springfield, Springfield, Nevada, USA - Simpson's house"
        self.assertEqual(res, dir_)

class TestOrder(unittest.TestCase):
    @patch("cargamos.datetime")
    def setUp(self, mock_dt):
        args = ["Evergreen terrace","48007","Springfield","Springfield","Nevada","USA",]
        kwargs = dict(address_line_2="742", notes="Simpson's house", sku="order_1")
        mock_dt.now.return_value = datetime(2022, 1, 27, 20, 50, 00)
        self.order = cargamos.Order(*args, **kwargs)

    def test_attrs(self):
        # atributos
        self.assertTrue(self.order.SKU)
        self.assertEqual(self.order.size, 1)
        self.assertEqual(self.order.total_instances, 1)
        self.assertEqual(self.order.expired_at, datetime(2022, 1, 27, 20, 52, 00))
        self.assertEqual(self.order._Package__created_at, datetime(2022, 1, 27, 20, 50, 00))
        self.assertEqual(self.order.delivered_at, None)
        self.assertIsInstance(self.order.delivery_address, cargamos.Address)

    @patch("cargamos.datetime")
    def test_time_to_expire(self, mock_dt):
        # orden expirada
        mock_dt.now.return_value = self.order.expired_at + timedelta(seconds=1)
        with self.assertRaisesRegex(Exception, r"La orden 'order_1' ha expirado") as ex:
            self.order.mark_as_delivered()

        # orden cerrada 5 segundos antes de expirar
        mock_dt.now.return_value = self.order.expired_at - timedelta(seconds=5)
        _ = self.order.mark_as_delivered()
        self.assertEqual(self.order.delivered_at, datetime(2022, 1, 27, 20, 51, 55))
        #print(self.order.delivery_address)