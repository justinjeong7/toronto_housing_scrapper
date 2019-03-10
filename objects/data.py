from objects.persistance import Persist

class DataModel(Persist):

    def __init__(self):
        Persist.__init__(self)

    def generate_attributes(self):

        for attribute, value in self.attributes_default.items():
            if attribute not in self.__dict__:
                setattr(self, attribute, value)

    def assign_attribute(self, name, value):

        if name not in self.attributes_default.keys():
            raise AttributeError("'{attr}' is not a valid attribute for the data.".format(attr=name))
        else:
            setattr(self, name, value)

    def generate_record(self):
        self.generate_attributes()
        self.record = {}

        for k, v in self.__dict__.items():
            if k in self.attributes_default:
                self.record[k] = v


class Condos(DataModel):

    tablename = 'buildings'
    attributes_default = {
        'name':None,
        'link':None,
        'neighborhood':None,
        'region':None,
        'city': 'Toronto'
    }

    def __init__(self):
        DataModel.__init__(self)

class CondoUnits(DataModel):

    tablename = "condo_units"
    attributes_default = {
        'unit':None,
        'period':None,
        'price':None,
        'bed': 0,
        'bath': 0,
        'min_sqft': 0,
        'max_sqft': 0,
        'parking': 0,
        'dom': 0,
        'building': None
    }

    def __init__(self):
        DataModel.__init__(self)
