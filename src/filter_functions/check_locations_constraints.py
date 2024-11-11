"""This module contains the function to check if the vehicle can handle the load type and the height of the order's origin and destination"""


def check_locations_constraints(order, vehicle, check_date, use_pending_orders):
    """Check if the vehicle can handle the load type and the height of the order's origin and destination"""
    return vehicle.truck_type_name == order.origin.load_type and vehicle.truck_type_name == order.destination.load_type and vehicle.height <= order.origin.max_height and vehicle.height <= order.destination.max_height
