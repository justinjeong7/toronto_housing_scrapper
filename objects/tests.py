
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
        self.s.get_buildings()
        self.assertIsInstance(self.s.buildings, list)
        self.assertIsInstance(self.s.buildings[0], dict)

    def test_get_sold_units(self):
        self.s.get_buildings()
        units = self.s.get_history(self.s.buildings[0])
        self.assertIsInstance(units, list)
        self.assertIsInstance(units[0], dict)

    def test_get_more_buildings(self):
        self.s.get_buildings()
        building_count_0 = len(self.s.buildings)
        self.s.get_more_buildings()
        building_count_1 = len(self.s.buildings)
        self.assertEqual(building_count_1>building_count_0,True)

    def test_get_more_buildings_limit(self):
        self.s.get_buildings()

        while self.s.more_buildings_available:
            self.s.get_more_buildings()

        self.assertEqual(self.s.page_count>1, True)


if __name__ == '__main__':
    unittest.main()
