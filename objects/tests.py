
import unittest
import sys
sys.path.append('../')
from login import LoginSession
from scrapper import Scrapper

class loginTest(unittest.TestCase):

    def setUp(self):
        self.l = LoginSession()
        self.filename = '../.secret.yaml'
        self.l.load_cred(self.filename)

    def test_load_cred(self):
        self.assertNotEqual(self.l.secrets['url'], None)
        self.assertIsInstance(self.l.secrets['cred_data'], dict)

    def test_login(self):
        self.l.login()
        self.assertEqual(self.l.logged_in, True)

class ScrapperTests(unittest.TestCase):

    def setUp(self):
        self.s = Scrapper()
        self.filename = '../.secret.yaml'
        self.s.load_cred(self.filename)
        self.s.login()

    def test_get_buildings(self):
        buildings = self.s.get_buildings()

        self.assertIsInstance(buildings, list)
        self.assertIsInstance(buildings[0], dict)

    def test_get_sold_units(self):
        buildings = self.s.get_buildings()

        units = self.s.get_history(buildings[0])
        self.assertIsInstance(units, list)
        self.assertIsInstance(units[0], dict)


if __name__ == '__main__':
    unittest.main()
