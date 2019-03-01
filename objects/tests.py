
import unittest
import sys
sys.path.append('../')
from login import LoginSession
from scrapper import Scrapper
from persistance import Persist
import os
import shutil
import logging


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
        self.assertIsInstance(self.s.buildings, dict)

    def test_get_sold_units(self):
        self.s.get_buildings()
        building_keys = iter(self.s.buildings)
        building_key = next(building_keys)

        units = self.s.get_history(building_key)
        while len(units) ==0:
            building_key = next(building_keys)
            units = self.s.get_history(building_key)

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

class PersistTests(unittest.TestCase):

    def setUp(self):
        self.p = Persist()

    def test_set_filename(self):

        self.p.set_filename('test.json')
        self.assertEqual(self.p.filename, 'test.json')
        self.assertEqual(self.p.format, 'json')
        self.assertEqual(self.p.fullpath, None)

        self.p.set_filename('/test.csv')
        self.assertEqual(self.p.filename, 'test.csv')
        self.assertEqual(self.p.format, 'csv')
        self.assertEqual(self.p.fullpath, None)

    def test_set_dir(self):
        self.p.set_dir('../test/')
        self.assertEqual(self.p.dir, '../test/')
        self.assertEqual(os.path.exists('../test/'), True)

        shutil.rmtree('../test/')
        self.p.set_dir('../test')
        self.assertEqual(self.p.dir, '../test/')
        self.assertEqual(os.path.exists('../test/'), True)

    def test_write(self):
        self.p.set_dir('../test/')
        self.p.set_filename('test.csv')

        record = {'header1':5, 'header2':10}
        self.p.write(record)

        with open(self.p.fullpath, 'r') as f :
            output = f.read()

        self.assertEqual(len(output.split('\n')),3)

    def tearDown(self):
        self.p.dir = None
        self.p.filename = None
        if os.path.exists('../test/'):
            shutil.rmtree('../test/')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
