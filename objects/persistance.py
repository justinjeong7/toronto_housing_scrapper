import os
import csv
import json
import copy

class Persist:

    def __init__(self, dir = None):
        self.__set_filename()
        self.dir = self.set_dir(dir)
        self.fullpath = None
        self.format = 'csv'

    def __set_filename(self):
        self.filename = self.tablename +'.csv'

    def __define_format(self):
        if not self.filename:
            pass
        elif self.filename.endswith('.csv'):
            self.format='csv'
        elif self.filename.endswith('.json'):
            self.format = 'json'
        else:
            raise ValueError("'filename' must have .csv or .json extension")

    def set_dir(self, dirname):
        if isinstance(dirname, str):
            if not dirname.endswith('/'):
                dirname = dirname + '/'

            if not os.path.exists(dirname):
                os.makedirs(dirname)

        self.dir = dirname
        self.__filename()

    def __filename(self):
        if self.filename and self.dir:
            self.fullpath = self.dir + self.filename

    def write(self):
        if not self.fullpath:
            raise ValueError("'filename' and 'dir' values must be set")

        if not os.path.exists(self.fullpath):
            mode = 'w'
        else:
            mode = 'a'

        with open(self.fullpath, mode) as f:
            if self.format == 'csv':
                writer = csv.DictWriter(f, fieldnames = self.record.keys())
                if mode == 'w':
                    writer.writeheader()
                writer.writerow(self.record)
            else:
                json.dump(record, f)

    def load(self):
        with open(self.fullpath, 'r') as f:

            if self.format == 'json':
                data = json.load(f)
            else:
                reader = csv.DictReader(f, delimiter=',')
                data = []
                for row in reader:
                    _obj = copy.deepcopy(self)
                    _obj.__dict__.update(row)
                    data.append(_obj)
        return data
