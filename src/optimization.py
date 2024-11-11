
""" This module contains the optimization process. """
from datetime import datetime

from src.entities.order import Order
from src.entities.vehicle import Vehicle
from src.filters import filter_vehicles
from src.scorer import score_vehicles
from src.utils.here_utility import calculate_locations_with_here


def execute_order_optimization(order, vehicles, force_clean, date, use_pending_orders=False):
    route_order = calculate_locations_with_here(order.origin, order.destination)
    order.route = route_order

    filtered_vehicles = filter_vehicles(order, vehicles, force_clean, check_date=date, use_pending_orders=use_pending_orders)
    scored_vehicles = score_vehicles(order, filtered_vehicles)

    # order by score from lowest to highest
    scored_vehicles.sort(key=lambda vehicle: vehicle.score)
    scored_vehicles.sort(
        key=lambda vehicle: vehicle.will_be_in_geographic_zone, reverse=True)
      
    return scored_vehicles

def execute_optimization(data):
    try:
        """ Execute the optimization process. """
        force_clean = data['input']['force_clean']
        date = datetime.strptime(data['input']['date'], "%Y-%m-%d")
        vehicles = [Vehicle.from_json(vehicle) for vehicle in data['vehicles']]
        orders = []
        for order in data['orders']:
            order_object = Order.from_json(order)
            orders.append(order_object)

        Order.all_orders = orders

        result = []
        pending_orders = filter(lambda order: order.status == "pending" and order_object.deadline_date is not None and order_object.deadline_date.day == date.day and order_object.deadline_date.month == date.month and order_object.deadline_date.year == date.year, orders)
        sorted_pending_orders = sorted(pending_orders, key=lambda order: (not order.is_external))
        for order in sorted_pending_orders:
            Vehicle.reset_all_total_distance(vehicles)
            scored_vehicles = execute_order_optimization(order, vehicles, force_clean, date)
            
            if not scored_vehicles:
                Vehicle.reset_all_total_distance(vehicles)
                scored_vehicles = execute_order_optimization(order, vehicles, force_clean, date, use_pending_orders=True)

            if not scored_vehicles:
                print("No vehicles available")
                result_json = order.to_json()
                result_json['best_vehicle'] = None
                result_json['vehicles'] = []
                result.append(result_json)
                continue

            best_vehicle = scored_vehicles[0]

            order.assigned_truck = best_vehicle.license_plate
            result_json = order.to_json()
            result_json['best_vehicle'] = best_vehicle.to_json()
            result_json['vehicles'] = [vehicle.to_json() for vehicle in scored_vehicles]
            result.append(result_json)

            best_vehicle.last_trimester_order_count += 1
            best_vehicle.last_trimester_mileage_count += best_vehicle.total_distance

        
        return result

    except Exception as e:
        print(e)
        return {
            "error": "Error in the optimization process. Please check the input data."
        }
