class Location:
    # lat lon
    def __init__(self, id, name, lat, lon, country):
        self.id = id
        self.name = name
        self.lat = lat
        self.lon = lon
        self.country = country

    @staticmethod
    def from_json(location):
        return Location(location['id'], location['name'], location['lat'], location['lon'], location['country'])

    def __str__(self):
        return f'ID {self.id} ({self.name}): {self.lat}, {self.lon}'

    def __repr__(self):
        return f'ID {self.id} ({self.name}): {self.lat}, {self.lon}'

    def is_international(self):
        return self.country != "ES"