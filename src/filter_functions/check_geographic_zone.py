"""This module contains the function to check if a vehicle can travel to the order's location."""
from haversine import haversine
from src.entities.order import Order


def check_geographic_zone(vehicle, order):
    """Check if the vehicle can travel to the order's location."""
    max_diff_hours = 24
    max_distance = 50  # in km
    last_order_of_vehicle = Order.get_last_order_of_vehicle(vehicle)
    is_on_the_way_to_origin_pex = False

    if last_order_of_vehicle:
        order_date = order.date
        last_order_delivery_date = last_order_of_vehicle and last_order_of_vehicle.delivery_date
        diff_hours = (
            order_date - last_order_delivery_date).total_seconds() / 3600
        is_on_the_way_to_origin_pex = diff_hours <= max_diff_hours and last_order_of_vehicle.destination.uid == order.origin.uid
        is_assigned_pex_same_as_order_destination = vehicle.assigned_pex == order.destination.uid

        if diff_hours <= max_diff_hours and is_assigned_pex_same_as_order_destination:
            if last_order_of_vehicle.destination.uid == order.origin.uid:
                is_on_the_way_to_origin_pex = True
            else:
                # check if the destination lat and lon is at max 50km from the origin lat and lon
                last_order_destination = (
                    last_order_of_vehicle.destination.lat,
                    last_order_of_vehicle.destination.lon,
                )
                order_origin = (order.origin.lat, order.origin.lon)
                distance = haversine(
                    order_origin,
                    last_order_destination
                )
                if distance <= max_distance:
                    is_on_the_way_to_origin_pex = True

        if is_on_the_way_to_origin_pex:
            vehicle.will_be_in_geographic_zone = True

    return vehicle.assigned_pex == order.origin.uid or is_on_the_way_to_origin_pex
