"""Location entity"""


class Location:
    """Location entity"""

    # lat lon
    def __init__(
        self,
        lat,
        lon,
        id=None,
        name=None,
        country=None,
        max_height=None,
        load_type=None,
    ):
        self.id = id
        self.name = name
        self.lat = lat
        self.lon = lon
        self.country = country
        self.max_height = max_height
        self.load_type = load_type

    @staticmethod
    def from_json(location):
        """Create a Location object from a JSON representation."""
        return Location(**location)

    def __str__(self):
        return f"ID {self.id} ({self.name}): {self.lat}, {self.lon}"

    def __repr__(self):
        return f"ID {self.id} ({self.name}): {self.lat}, {self.lon}"

    def is_international(self):
        """Check if the location is international."""
        return self.country != "ES"
