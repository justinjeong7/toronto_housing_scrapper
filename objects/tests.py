import unittest
import sys
sys.path.append('../')
from login import LoginSession
from scrapper import BuildingScrapper, UnitScrapper
from persistance import Persist
from objects.data import Condos, CondoUnits
import os
import shutil
import logging

class CondoModelTests(unittest.TestCase):

    def setUp(self):
        self.condo = Condos()
        self.condo.set_dir('data/')

    def test_attribute_generation(self):

        self.condo.generate_attributes()

        for attr in self.condo.attributes_default:
            self.assertTrue(attr in self.condo.__dict__)

    def test_assign_attribute(self):

        self.condo.assign_attribute('name', 'test')

        with self.assertRaises(AttributeError) as context:
            self.condo.assign_attribute('test', 'test')

        self.assertEqual(self.condo.name, 'test')
        self.assertTrue('test' not in self.condo.__dict__)

    def test_save(self):
        self.condo.generate_record()
        self.condo.write()

    def test_load(self):
        self.condo.generate_record()
        self.condo.write()

        self.condo.assign_attribute('name', "test")
        self.condo.generate_record()
        self.condo.write()

        data = self.condo.load()

        self.assertEqual(data[0].name, '')
        self.assertEqual(data[1].name, "test")

    def tearDown(self):

        if os.path.exists(self.condo.fullpath):
            os.remove(self.condo.fullpath)

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

class BuildingScrapperTests(unittest.TestCase):

    def setUp(self):
        self.s = BuildingScrapper()
        self.filename = '../.secret.yaml'
        self.s.load_cred(self.filename)
        self.s.login()

    def test_get_buildings(self):
        self.s.get_buildings()
        self.assertIsInstance(self.s.buildings, dict)

        buildings = iter(self.s.buildings)
        building = next(buildings)

        self.assertEqual(self.s.buildings[building].__class__, Condos)

    def test_get_more_buildings(self):
        self.s.get_buildings()
        building_count_0 = len(self.s.buildings)
        self.s.get_more_buildings()
        building_count_1 = len(self.s.buildings)
        self.assertEqual(building_count_1>building_count_0,True)

    def test_get_more_buildings_limit(self):
        self.s.get_buildings()
        self.s.page_count = 55
        while self.s.more_buildings_available:
            self.s.get_more_buildings()

        self.assertTrue(self.s.page_count>1)
        self.assertFalse(self.s.more_buildings_available)

    def test_get_building_list(self):

        self.assertIsInstance(self.s.building_list(), list)

    def test_building_region(self):
        self.s.get_buildings()

        test_cases = {
        'Four Winds Condos Condos in Toronto':'York University Heights',
        'Ice Condos | Ice Condos II Condos in Toronto': 'The Core'
        }

        for test_building, expected_value in test_cases.items():
            self.s.get_building_detail(test_building)
            self.assertEqual(self.s.buildings[test_building].neighborhood, expected_value)

class UnitScrapperTests(unittest.TestCase):

    def setUp(self):
        self.s = BuildingScrapper()
        self.filename = '../.secret.yaml'
        self.s.load_cred(self.filename)
        self.s.login()
        _ = self.s.get_buildings()

        building_keys = iter(self.s.buildings)
        building_key = next(building_keys)

        self.u = UnitScrapper()
        self.u.load_cred(self.filename)
        self.u.login()
        self.u.set_building(self.s.buildings[building_key])

    def test_get_sold_units(self):

        units = self.u.get_history()
        self.assertIsInstance(units, list)
        self.assertEqual(units[0].__class__, CondoUnits)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
