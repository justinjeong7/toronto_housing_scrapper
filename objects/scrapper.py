from login import LoginSession
from bs4 import BeautifulSoup
from utility import StringModifier

class Scrapper(LoginSession, StringModifier):

    def __init__(self):
        LoginSession.__init__(self)
        StringModifier.__init__(self)

    def __get_content(self, url):
        r = self.session.get(url)

        if r.status_code == 200:
            self.content = BeautifulSoup(r.text,'lxml')

    def get_buildings(self):
        self.__get_content(self.secrets['search_url'])

        building_contents = self.content.find('div',{'id':'building-tab'}).find_all('a', {'class':'no-decro'})
        buildings = []
        for content in building_contents:

            detail = {
                'link':content.get('href'),
                'title' : content.get('title')
            }

            if detail['link'].startswith('new-development'):
                continue
            buildings.append(detail)
        return buildings

    def __get_more_buildings(self):
        pass

    def get_history(self, building, type='sold'):

        self.__get_content(self.secrets['url'] + building['link'])
        all_sales_link = self.content.find('a', {'class':"all_sale_link"}).get('href')
        #get all sales info
        self.__get_content(self.secrets['url'] + all_sales_link)
        history_content = self.content.find_all('li', {'type':self.secrets['listing_map'][type]})

        records = []
        for content in history_content:
            records.append(self.__get_unit_detail(content))
        return records

    def __get_unit_detail(self, content):
        info = {
            'period': self.remove_escapes(content.find('time').text),
            'unit': self.remove_escapes(content.find('span', {'class':'listing-name'}).text),
            'size': self.remove_escapes(content.find('span', {'class':'listing-sqft'}).text),
            'price': self.remove_escapes(content.find('span', {'class':'tag-price'}).text)
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
