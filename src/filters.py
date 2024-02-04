""" This module contains the filters to be applied to the vehicles. """
from .filter_functions.national_international import national_international
from .filter_functions.vehicle_expirations import vehicle_expirations
from .filter_functions.check_material import check_material
from .filter_functions.check_truck_type import check_truck_type
from .filter_functions.check_locations_constraints import check_locations_constraints


class Filter:
    """
    Class to represent a filter.
    """

    def __init__(self, name, func):
        """
        Initializes a Filter object.

        Args:
            name (str): The name of the filter.
            func (function): The function to be applied by the filter.
        """
        self.name = name
        self.func = func

    def __call__(self, *args, **kwargs):
        """
        Calls the filter function with the given arguments.

        Returns:
            The result of applying the filter function.
        """
        return self.func(*args, **kwargs)

    def __str__(self):
        """
        Returns a string representation of the filter.

        Returns:
            The name of the filter.
        """
        return self.name

    def __repr__(self):
        """
        Returns a string representation of the filter.

        Returns:
            A formatted string containing the name and function of the filter.
        """
        return f"Filter(name={self.name}, func={self.func})"


def filter_vehicles(order, vehicles, force_clean):
    """Filter the vehicles based on the order and the force_clean flag."""
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
        for filter_function in filters:
            if not filter_function(order=order, vehicle=vehicle):
                print(
                    f"DEUBG: El vehículo {vehicle} no cumple con el filtro {filter_function}")
                break
        else:
            filtered_vehicles.append(vehicle)

    return filtered_vehicles
