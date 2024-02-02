from .filter_functions.national_international import national_international
from .filter_functions.vehicle_expirations import vehicle_expirations
from .filter_functions.check_material import check_material
from .filter_functions.check_truck_type import check_truck_type
from .filter_functions.check_locations_constraints import check_locations_constraints
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


def filter_vehicles(order, vehicles, force_clean):
    filters = [
        Filter("national_international", national_international),
        Filter("vehicle_expirations", vehicle_expirations),
        Filter("check_truck_type", check_truck_type),
        Filter("check_locations_constraints", check_locations_constraints),
    ]

    if not force_clean:
        filters.append(Filter("check_material", check_material))

    filtered_vehicles = []
    for vehicle in vehicles:
        for filter in filters:
            if not filter(order=order, vehicle=vehicle):
                print(f"DEUBG: El vehículo {vehicle} no cumple con el filtro {filter}")
                break
        else:
            filtered_vehicles.append(vehicle)

    return filtered_vehicles

