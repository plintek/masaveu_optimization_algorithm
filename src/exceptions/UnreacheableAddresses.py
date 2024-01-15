# UnreacheableAddressException

class UnreacheableAddressesException(Exception):
    def __init__(self, to_locations, from_location):
        super().__init__("La dirección no es alcanzable")
        self.from_location = from_location
        self.to_locations = to_locations

    def __str__(self):
        location_string = ""
        for location in self.to_locations:
            location_string += f'- {location} \n'

        return f'Las siguientes localizaciones no fueron alcanzables desde {self.from_location}: \n {location_string}'
