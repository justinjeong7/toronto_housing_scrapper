from objects.login import LoginSession
from bs4 import BeautifulSoup
from objects.utility import StringModifier
from objects.persistance import Persist
import datetime

class Scrapper(LoginSession, StringModifier, Persist):

    def __init__(self):
        LoginSession.__init__(self)
        StringModifier.__init__(self)
        Persist.__init__(self)
        self.buildings = {}
        self.page_count = 1
        self.more_buildings_available = True
        self.content = None

    def __get_content(self, url):
        r = self.session.get(url)

        if r.status_code == 200:
            self.content = BeautifulSoup(r.text,'lxml')

    def get_buildings(self):

        if not self.more_buildings_available:
            return False

        url = self.secrets['search_url'] + '?b_page={page_count}'.format(page_count = self.page_count)
        last_content = self.content
        self.__get_content(url)

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
                self.buildings[title] = link

        return True

    def get_more_buildings(self):
        self.page_count += 1
        self.get_buildings()

    def get_history(self, building_key, type='sold'):

        self.__get_content(self.secrets['url'] + self.buildings[building_key])
        all_sales_link = self.content.find('a', {'class':"all_sale_link"}).get('href')
        #get all sales info
        self.__get_content(self.secrets['url'] + all_sales_link)
        history_content = self.content.find_all('li', {'type':self.secrets['listing_map'][type]})

        records = []
        for content in history_content:
            unit_detail = self.__get_unit_detail(content)
            unit_detail['building'] = building_key
            records.append(unit_detail)
        return records

    def __get_unit_detail(self, content):
        period = self.remove_escapes(content.find('time').text)

        #in order to retain period information
        if period.strip() == '':
            period = self.last_period
        else:
            self.last_period = period

        size = self.remove_escapes(content.find('span', {'class':'listing-sqft'}).text)
        if '-' in size:
            size_min, size_max = size.split('-')
        else:
            size_min = size_max = int(size)

        date_format = '%b %Y'

        info = {
            'period': datetime.datetime.strptime(period.strip(), date_format).date(),
            'unit': int(self.remove_escapes(content.find('span', {'class':'listing-name'}).text).replace('Unit ','')),
            'size_min': int(size_min),
            'size_max': int(size_max),
            'price': int(self.remove_escapes(content.find('span', {'class':'tag-price'}).text).replace('$','').replace(',',''))
        }

        more_info = content.find('div', {'class':'listing-bed-bath-div'})
        info['dom'] = self.remove_escapes(more_info.text.split(':')[-1])

        for n, span in enumerate(more_info.find_all('span')):
            if span.find('img'):
                if span.find('img').get('src') == "application/themes/boot/images/bed.jpg":
                    info['bed'] = self.remove_escapes(span.text)
                elif span.find('img').get('src') == "application/themes/boot/images/shower.jpg":
                    info['baths'] = self.remove_escapes(span.text)
                elif span.find('img').get('src') == "application/themes/boot/images/parking.jpg":
                    info['parking'] = self.remove_escapes(span.text)
        return info
