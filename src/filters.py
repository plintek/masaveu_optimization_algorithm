""" This module contains the filters to be applied to the vehicles. """
from src.filter_functions.check_delivery_on_time import check_delivery_on_time
from src.filter_functions.check_geographic_zone import check_geographic_zone
from src.filter_functions.check_locations_constraints import check_locations_constraints
from src.filter_functions.check_material import check_material
from src.filter_functions.check_pending_orders import check_pending_orders
from src.filter_functions.check_truck_type import check_truck_type
from src.filter_functions.national_international import national_international
from src.filter_functions.vehicle_expirations import vehicle_expirations


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


def filter_vehicles(order, vehicles, force_clean, check_date):
    """Filter the vehicles based on the order and the force_clean flag."""
    filters = [
        Filter("check_pending_orders", check_pending_orders),
        Filter("national_international", national_international),
        Filter("vehicle_expirations", vehicle_expirations),
        Filter("check_truck_type", check_truck_type),
        Filter("check_locations_constraints", check_locations_constraints),
        Filter("check_geographic_zone", check_geographic_zone),
    ]

    if not force_clean:
        filters.append(Filter("check_material", check_material))

    filters.append(Filter("check_delivery_on_time", check_delivery_on_time))

    filtered_vehicles = []
    for vehicle in vehicles:
        for filter_function in filters:
            if not filter_function(order=order, vehicle=vehicle, check_date=check_date):
                print(
                    f"DEUBG: El vehículo {vehicle} no cumple con el filtro {filter_function}")
                break
        else:
            filtered_vehicles.append(vehicle)

    return filtered_vehicles
