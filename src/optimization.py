from .entities.order import Order
from .entities.location import Location
from .entities.vehicle import Vehicle
from .filters import filter_vehicles
from .scorer import score_vehicles

from .utils.here_utility import calculate_locations_with_here

def execute_optimization(data):
    order = Order.load_from_sinex(data['order_id'])
    origin = Location.from_json(data['origin'])
    destination = Location.from_json(data['destination'])

    vehicles = Vehicle.load_from_sinex()

    filtered_vehicles = filter_vehicles(order, vehicles, origin, destination)

    scored_vehicles = score_vehicles(order, filtered_vehicles, origin, destination)

    route = calculate_locations_with_here(origin, destination)