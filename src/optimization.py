
""" This module contains the optimization process. """
from src.entities.order import Order
from src.entities.vehicle import Vehicle
from src.filters import filter_vehicles
from src.scorer import score_vehicles


def execute_optimization(data):
    """ Execute the optimization process. """
    orders = [Order.from_json(order) for order in data['orders']]
    Order.all_orders = orders

    order = Order.load_order_from_sinex(
        data['input']['order_id'])

    force_clean = data['input']['force_clean']

    vehicles = [Vehicle.from_json(vehicle) for vehicle in data['vehicles']]

    filtered_vehicles = filter_vehicles(order, vehicles, force_clean)

    scored_vehicles = score_vehicles(order, filtered_vehicles)

    # order by score from lowest to highest
    scored_vehicles.sort(key=lambda vehicle: vehicle.score)
    scored_vehicles.sort(
        key=lambda vehicle: vehicle.will_be_in_geographic_zone, reverse=True)

    if not scored_vehicles:
        print("No vehicles available")
        return {
            "vehicle_list": [],
            "best_vehicle": None,
            'order': order.to_json()
        }

    best_vehicle = scored_vehicles[0]

    return {
        "vehicle_list": [vehicle.to_json() for vehicle in scored_vehicles],
        "best_vehicle": best_vehicle.to_json(),
        'order': order.to_json()
    }
