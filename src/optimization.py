from .entities.order import Order
from .entities.location import Location
from .entities.vehicle import Vehicle
from .filters import filter_vehicles
from .scorer import score_vehicles

from .utils.here_utility import calculate_locations_with_here

def execute_optimization(data):
    order = Order.load_order_from_sinex(data['order_id'])
    force_clean = data['forceClean']

    vehicles = Vehicle.load_from_sinex()

    filtered_vehicles = filter_vehicles(order, vehicles, force_clean)

    scored_vehicles = score_vehicles(order, filtered_vehicles)

    route = calculate_locations_with_here(order.origin, order.destination)