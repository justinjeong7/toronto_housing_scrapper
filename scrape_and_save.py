from objects import Scrapper
from objects import Persist
import argparse
import os


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Provide condo building to scrape')
    parser.add_argument('--condo-key',  help = "Condo building key", default = None)
    args = parser.parse_args()

    s = Scrapper()
    s.load_cred('.secret.yaml')
    s.login()

    p = Persist()
    p.set_dir('data/')
    p.set_filename('building_records.json')


    if os.path.exists(p.fullpath):
        s.buildings = p.load()

    else:
        s.get_buildings()
        while s.more_buildings_available:
            s.get_more_buildings()

    p.set_filename('all_sales_data.csv')

    if args.condo_key:
        units = s.get_history(args.condo_key)

        for unit in units:
            p.write(unit)

    else:
        for building in s.buildings:
            units = s.get_history(building)
            for unit in units:
                p.write(unit)
