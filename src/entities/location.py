"""Location entity"""


class Location:
    """Location entity"""

    # lat lon
    def __init__(
        self,
        lat,
        lon,
        uid=None,
        name=None,
        country=None,
        max_height=None,
        load_type=None
    ):
        self.uid = uid
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

    def to_json(self):
        """Return the location as a JSON representation."""
        return {
            "uid": self.uid,
            "name": self.name,
            "lat": self.lat,
            "lon": self.lon,
            "country": self.country,
            "max_height": self.max_height,
            "load_type": self.load_type
        }

    def __str__(self):
        return f"ID {self.uid} ({self.name}): {self.lat}, {self.lon}"

    def __repr__(self):
        return f"ID {self.uid} ({self.name}): {self.lat}, {self.lon}"

    def is_international(self):
        """Check if the location is international."""
        return self.country != "ES"
