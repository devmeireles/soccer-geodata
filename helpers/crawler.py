import requests
import re
import os
from datetime import datetime
from dotenv import load_dotenv
from bs4 import BeautifulSoup as bs
from helpers.database import Database
from helpers.geo_data import GeoData
from helpers.treat_data import TreatData

load_dotenv(verbose=True)


class Crawler():
    """
    A class to get an specific data

    Attributes
    ----------
    url: str
        the url to be crawled

    url: int
        the id of the team

    Methods
    -------
    extract_data(self)
        Return the data from page
    """

    def __init__(self, url, id):
        self.url = url
        self.id = id

    def extract_data(self):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}

            resp = requests.get(self.url, headers=headers)

            if resp.status_code == 200:
                soup = bs(resp.content, "html.parser")

                content = soup.select("div.content-column")[0]

                if content:
                    team_name = soup.select('#subheading > h1')[0].text
                    team_data_box = content.select('.first-element')[0]
                    stadium_data = content.select('.second-element')[0]

                    stadium_data_content = stadium_data.select(
                        '.redesign > .block_team_venue-wrapper > .content > .block_team_venue > .fully-padded')[0]

                    team_data_content = team_data_box.select(
                        '.redesign > .block_team_info-wrapper > .content > .block_team_info > .fully-padded')[0]

                    logo = team_data_content.select('.logo > img')[0]['src']
                    stadium_img = stadium_data.select('a > img')[0]['src']

                    team_dict = self.set_team_values(team_data_content)
                    stadium_dict = self.set_team_values(stadium_data_content)

                    team_dict['team_name'] = team_name
                    team_dict['logo'] = logo
                    stadium_dict['img'] = stadium_img

                    return {
                        'club': team_dict,
                        'stadium': stadium_dict
                    }
        except Exception:
            return None

    @staticmethod
    def set_team_values(data):
        data_key = data.find_all('dt')
        data_value = data.find_all('dd')

        keys = []
        values = []
        data = {}

        for key in data_key:
            keys.append(key.string.lower())

        for value in data_value:
            item_value = value.text
            item_value = re.sub(r'[\ \n]{2,}', ' ', item_value)
            values.append(item_value)

        for i in range(len(keys)):
            data[keys[i]] = values[i]

        return data

    def save_data(self):
        try:
            mongo_address = os.getenv('MONGO_ADDRESS')
            db_name = os.getenv('DATABASE_NAME')
            collection = 'clubs'

            database = Database(mongo_address, db_name)

            data = Crawler.extract_data(self)

            if data != None:
                data['club_id'] = self.id
                data['club']['slug'] = TreatData.slugify(data['club']['team_name'])

                now = datetime.now()
                now = now.strftime("%Y-%m-%d %H:%M:%S")
                data['created_at'] = now

                # if data['club']['address']:
                if 'address' in data['club'].keys():
                    club_geo_data = GeoData(data['club']['address'])
                    data['club']['geo_data'] = club_geo_data.get_lat_long()

                if 'name' in data['stadium'].keys():
                    stadium_geo_data = GeoData(data['stadium']['name'])
                    data['stadium']['geo_data'] = stadium_geo_data.get_lat_long()

                return database.save_not_exists(data, collection)
        except Exception:
            return None
