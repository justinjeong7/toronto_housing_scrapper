from objects import BuildingScrapper, UnitScrapper
from objects import Condos, CondoUnits
import argparse
import os


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Provide condo building to scrape')
    parser.add_argument('--condo-key',  help = "Condo building key", default = None)
    args = parser.parse_args()

    s = BuildingScrapper()
    s.load_cred('.secret.yaml')
    s.login()

    condos = Condos()
    condos.set_dir('data/')

    if os.path.exists(condos.fullpath):
        for c in condos.load():
            s.buildings[c.name] = c

    else:
        s.get_buildings()
        while s.more_buildings_available:
            s.get_more_buildings()

        for key, building in s.buildings.items():
            s.get_building_detail(key)
            building.set_dir('data/')
            building.generate_record()
            building.write()

    u = UnitScrapper()
    u.session = s.session
    u.secrets = s.secrets

    counts = 0
    if args.condo_key:
        u.set_building(s.buildings[args.condo_key])
        units = u.get_history()

        for unit in units:
            unit.set_dir('data/')
            unit.generate_record()
            unit.write()

    else:
        for k, v  in s.buildings.items():
            u.set_building(v)
            units = u.get_history()

            for unit in units:
                unit.set_dir('data/')
                unit.generate_record()
                unit.write()

            counts += 1
            print("{n}/{total} buildings scrapped".format(n=counts, total = len(s.buildings)))
