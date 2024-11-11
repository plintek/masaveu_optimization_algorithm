""" This module contains the distance score function. It calculates the distance between the vehicle and the order's origin. """
from datetime import datetime, timedelta

from src.utils.here_utility import calculate_locations_with_here


def check_delivery_on_time(order, vehicle, check_date):
    """ This function calculates the distance between the vehicle and the order's origin."""
    route_from_vehicle_to_origin = calculate_locations_with_here(
        vehicle.get_location(), order.origin)

    vehicle.route_to_origin = route_from_vehicle_to_origin
    route_order = order.route

    duration_from_vehicle_to_origin = route_from_vehicle_to_origin[
        'routes'][0]['sections'][0]['summary']['duration'] / 60
    duration_order = route_order['routes'][0]['sections'][0]['summary']['duration'] / 60

    last_occupation_date = vehicle.get_last_ocupation_date()
    if not last_occupation_date:
        last_occupation_date = check_date

    deadline_date = order.deadline_date
    load_duration = order.load_duration
    total_order_time = duration_from_vehicle_to_origin + duration_order + load_duration
    total_rest_time = vehicle.get_total_rest_time(total_order_time)
    if last_occupation_date + timedelta(minutes=total_order_time + total_rest_time) > deadline_date:
        return False

    return True
