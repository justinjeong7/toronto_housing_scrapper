import os
import csv
import json

class Persist:

    def __init__(self, filename = None, dir = None):
        pass
        self.filename = self.set_filename(filename)
        self.dir = self.set_dir(dir)
        self.fullpath = None
        self.format = 'csv'

    def set_filename(self, filename):
        if isinstance(filename, str):
            if '/' in filename:

                if filename.startswith('/'):
                    filename = filename[1:]
                else:
                    self.set_dir('/'.join(filename.split('/')[:-1]))

        self.filename = filename
        self.__filename()
        self.__define_format()

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

    def write(self, record):
        if not self.fullpath:
            raise ValueError("'filename' and 'dir' values must be set")

        if not os.path.exists(self.fullpath):
            mode = 'w'
        else:
            mode = 'a'

        with open(self.fullpath, mode) as f:
            if self.format == 'csv':
                writer = csv.DictWriter(f, fieldnames = record.keys())
                if mode == 'w':
                    writer.writeheader()
                writer.writerow(record)
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
                    data.append(row)
        return data
