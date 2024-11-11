"""This module contains the function to check if a vehicle can travel to the order's location."""
from haversine import haversine


def check_geographic_zone(vehicle, order, check_date, use_pending_orders):
    """Check if the vehicle can travel to the order's location."""
    max_distance = 50  # in km
    is_on_the_way_to_origin_pex = False

    # check if the destination lat and lon is at max 50km from the origin lat and lon
    vehicle_location = (
        vehicle.geolocation["lat"], vehicle.geolocation["lon"])
    order_origin = (order.origin.lat, order.origin.lon)
    distance = haversine(
        order_origin,
        vehicle_location
    )
    if distance <= max_distance and vehicle.assigned_pex == order.destination.uid:
        is_on_the_way_to_origin_pex = True
        vehicle.will_be_in_geographic_zone = True

    return vehicle.assigned_pex == order.origin.uid or is_on_the_way_to_origin_pex
