
""" This module contains the optimization process. """
from src.entities.order import Order
from src.entities.vehicle import Vehicle
from src.filters import filter_vehicles
from src.scorer import score_vehicles


def execute_optimization(data):
    """ Execute the optimization process. """
    order = Order.load_order_from_sinex(data['order_id'])
    force_clean = data['force_clean']

    vehicles = Vehicle.load_from_sinex()

    filtered_vehicles = filter_vehicles(order, vehicles, force_clean)

    scored_vehicles = score_vehicles(order, filtered_vehicles)

    # order by score from lowest to highest
    scored_vehicles.sort(key=lambda vehicle: vehicle.score)
    scored_vehicles.sort(
        key=lambda vehicle: vehicle.will_be_in_geographic_zone, reverse=True)

    if not scored_vehicles:
        print("No vehicles available")
        return

    best_vehicle = scored_vehicles[0]
    print("BEST VEHICLE: ", best_vehicle)
    print("CHOSEN VEHICLES: ", scored_vehicles)
