from objects.login import LoginSession
from bs4 import BeautifulSoup
from objects.utility import StringModifier, InputValidator
from objects.data import Condos, CondoUnits
import datetime

class ContentScrapper(LoginSession, InputValidator):

    def __init__(self):
        LoginSession.__init__(self)
        InputValidator.__init__(self)
        self.content = None

    def get_content(self, url):

        url = self.validate_input_type(url, str)
        r = self.session.get(url)

        if r.status_code == 200:
            self.content = BeautifulSoup(r.text,'lxml')

class BuildingScrapper(ContentScrapper, StringModifier, InputValidator):

    def __init__(self):
        ContentScrapper.__init__(self)
        StringModifier.__init__(self)
        InputValidator.__init__(self)
        self.buildings = {}
        self.page_count = 1
        self.more_buildings_available = True
        self.content = None

    def get_buildings(self):

        if not self.more_buildings_available:
            return False

        url = self.secrets['search_url'] + '?b_page={page_count}'.format(page_count = self.page_count)
        last_content = self.content
        self.get_content(url)

        building_contents = self.content.find('div',{'id':'building-tab'}).find_all('a', {'class':'no-decro'})

        if last_content:
            last_building_contents = last_content.find('div',{'id':'building-tab'}).find_all('a', {'class':'no-decro'})

            if last_building_contents == building_contents:
                self.more_buildings_available = False
                return False

        for content in building_contents:
            title = content.get('title')
            link = content.get('href')

            if link.startswith('new-development'):
                continue
            else:
                c = Condos()
                c.assign_attribute('name', content.find('img').get('alt'))
                c.assign_attribute('link', link)

                self.buildings[title] = c

        return True

    def building_list(self):
        return list(self.buildings.keys())

    def get_more_buildings(self):
        self.page_count += 1
        self.get_buildings()

    def get_building_detail(self, key):

        key = self.validate_input_type(key, str)
        if key not in self.buildings:
            raise KeyError("{} is not in 'buildings' dict".format(key))

        self.get_content(self.secrets['url'] + self.buildings[key].link)
        self.__get_building_region(key)

    def __get_building_region(self, key):
        building = self.buildings[key]

        regions = self.content.find('h2', {'class':"slide-address"}).find_all('a')
        region_keys = ['neighborhood', 'region', 'city']

        for n, region in enumerate(regions):
            building.assign_attribute(region_keys[n], region.text)

class UnitScrapper(ContentScrapper, StringModifier, InputValidator):

    def __init__(self, building = None):
        ContentScrapper.__init__(self)
        InputValidator.__init__(self)
        StringModifier.__init__(self)
        self.building = building
        self.units = []

    def set_building(self, building_information):
        building_information = self.validate_input_type(building_information, str)

        self.building = building_information
        self.units = []

    def get_history(self, type='sold'):

        self.get_content(self.secrets['url'] + self.building.link)
        all_sales_link = self.content.find('a', {'class':"all_sale_link"}).get('href')
        #get all sales info
        self.get_content(self.secrets['url'] + all_sales_link)
        history_content = self.content.find_all('li', {'type':self.secrets['listing_map'][type]})

        records = []
        for content in history_content:
            unit_detail = self.__get_unit_detail(content)
            unit_detail.assign_attribute('building', self.building.name)
            records.append(unit_detail)

        return records

    def __get_unit_detail(self, content):
        unit = CondoUnits()

        self.__assign_period(unit, content)
        self.__assign_size(unit, content)
        self.__assign_transaction_info(unit, content)
        self.__assign_unit_detail(unit, content)

        return unit

    def __assign_period(self, unit, content):
        period = self.remove_escapes(content.find('time').text)

        if period.strip() == '':
            period = self.last_period
        else:
            self.last_period = period
        date_format = '%b %Y'
        date = datetime.datetime.strptime(period.strip(), date_format).date()

        unit.assign_attribute('period', date.strftime('%Y-%m-%d'))

    def __assign_size(self, unit, content):
        size = self.remove_escapes(content.find('span', {'class':'listing-sqft'}).text)
        if '-' in size:
            size_min, size_max = size.split('-')
        else:
            size_min = size_max = int(size)

        try:
            unit.assign_attribute('min_sqft', int(size_min))
            unit.assign_attribute('max_sqft', int(size_max))
        except:
            pass

    def __assign_transaction_info(self, unit, content):

        unit_content = content.find('span', {'class':'listing-name'}).text
        price_content = content.find('span', {'class':'tag-price'}).text

        unit.assign_attribute('unit', self.remove_escapes(unit_content).replace('Unit ','').strip())
        unit.assign_attribute('price', int(self.remove_escapes(price_content).replace('$','').replace(',','')))

    def __assign_unit_detail(self, unit, content):
        detailed_content = content.find('div', {'class':'listing-bed-bath-div'})

        unit.assign_attribute('dom', self.remove_escapes(detailed_content.text.split(':')[-1]))

        for span in detailed_content.find_all('span'):
            if span.find('img'):
                if span.find('img').get('src') == "application/themes/boot/images/bed.jpg":
                    unit.assign_attribute('bed', self.remove_escapes(span.text))
                elif span.find('img').get('src') == "application/themes/boot/images/shower.jpg":
                    unit.assign_attribute('bath', self.remove_escapes(span.text))
                elif span.find('img').get('src') == "application/themes/boot/images/parking.jpg":
                    unit.assign_attribute('parking', self.remove_escapes(span.text))
