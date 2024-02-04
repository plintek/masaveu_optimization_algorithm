"""This module contains the function to check if the truck type of the vehicle is the same as the order's truck type
"""


def check_truck_type(order, vehicle):
    """Check if the truck type of the vehicle is the same as the order's truck type"""
    return vehicle.truck_type_name == order.truck_type
