from .filter_functions.national_international import national_international
from .filter_functions.vehicle_expirations import vehicle_expirations

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
        for filter in filters:
            if not filter(order=order, vehicle=vehicle, origin=origin, destination=destination):
                print(f"DEUBG: El vehículo {vehicle} no cumple con el filtro {filter}")
                break
        else:
            filtered_vehicles.append(vehicle)

    return filtered_vehicles

