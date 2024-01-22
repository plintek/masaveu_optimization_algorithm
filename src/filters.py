from .filters.national_international import national_international
from .filters.vehicle_expirations import vehicle_expirations

class Filter:
    def __init__(self, name, func):
        self.name = name
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Filter(name={self.name}, func={self.func})"


def filter_vehicles(order, vehicles, origin, destination):
    filters = [
        Filter("national_international", national_international),
        Filter("vehicle_expirations", vehicle_expirations)
    ]

    filtered_vehicles = []
    for vehicle in vehicles:
        if all(filter(order=order, vehicle=vehicle, origin=origin, destination=destination) for filter in filters):
            filtered_vehicles.append(vehicle)

    return filtered_vehicles

