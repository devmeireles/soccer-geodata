from geopy.geocoders import Nominatim


class GeoData():
    geo_locator = None

    def __init__(self, address):
        self.address = address
        GeoData.set_geo_locator()

    @classmethod
    def set_geo_locator(cls):
        cls.geo_locator = Nominatim(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36")

    def get_lat_long(self):
        location = GeoData.geo_locator.geocode(self.address)
        if location != None:
            return {
                'lat': location.latitude,
                'lon': location.longitude
            }

        return {}