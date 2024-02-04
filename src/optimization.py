
""" This module contains the optimization process. """
from src.entities.order import Order
from src.entities.vehicle import Vehicle
from src.filters import filter_vehicles
from src.scorer import score_vehicles

from .utils.here_utility import calculate_locations_with_here


def execute_optimization(data):
    """ Execute the optimization process. """
    order = Order.load_order_from_sinex(data['order_id'])
    force_clean = data['forceClean']

    vehicles = Vehicle.load_from_sinex()

    filtered_vehicles = filter_vehicles(order, vehicles, force_clean)

    score_vehicles(order, filtered_vehicles)

    calculate_locations_with_here(order.origin, order.destination)
