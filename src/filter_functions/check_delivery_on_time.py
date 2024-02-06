""" This module contains the distance score function. It calculates the distance between the vehicle and the order's origin. """
from datetime import datetime, timedelta
from src.utils.here_utility import calculate_locations_with_here


def check_delivery_on_time(order, vehicle):
    """ This function calculates the distance between the vehicle and the order's origin."""
    route_from_vehicle_to_origin = calculate_locations_with_here(
        vehicle.get_location(), order.origin)
    route_order = calculate_locations_with_here(
        order.origin, order.destination)

    duration_from_vehicle_to_origin = route_from_vehicle_to_origin[
        'routes'][0]['sections'][0]['summary']['duration'] / 60
    duration_order = route_order['routes'][0]['sections'][0]['summary']['duration'] / 60
    total_route_time = duration_from_vehicle_to_origin + duration_order

    total_rest_time = vehicle.get_total_rest_time(total_route_time)
    load_duration = order.load_duration

    total_time_minutes = total_route_time + total_rest_time + load_duration

    # TODO: Tenemos el tiempo total de ruta pero no sabemos si usar el tiempo actual o otro tiempo para ver si llega a tiempo

    # now = datetime.now()
    now = datetime.strptime("2024-01-01T00:00:00.000Z",
                            "%Y-%m-%dT%H:%M:%S.%fZ")
    deadline_date = order.deadline_date

    condition = now + timedelta(minutes=total_time_minutes) <= deadline_date
    return condition
