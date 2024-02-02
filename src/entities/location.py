class Location:
    # lat lon
    def __init__(self, lat, lon, id=None, name=None, country=None, maxHeight=None, loadType=None):
        self.id = id
        self.name = name
        self.lat = lat
        self.lon = lon
        self.country = country
        self.maxHeight = maxHeight
        self.loadType = loadType

    @staticmethod
    def from_json(location):
        return Location(**location)

    def __str__(self):
        return f'ID {self.id} ({self.name}): {self.lat}, {self.lon}'

    def __repr__(self):
        return f'ID {self.id} ({self.name}): {self.lat}, {self.lon}'


    def is_international(self):
        return self.country != "ES"