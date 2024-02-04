""" This module contains the distance score function. It calculates the distance between the vehicle and the order's origin. """
from src.utils.here_utility import calculate_locations_with_here


def distance(order, vehicle):
    """ This function calculates the distance between the vehicle and the order's origin."""
    route = calculate_locations_with_here(vehicle.get_location(), order.origin)
    distance_value = route['routes'][0]['sections'][0]['summary']['length']

    return distance_value / 1000
