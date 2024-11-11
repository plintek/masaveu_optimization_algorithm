"""Module providing a function printing python version."""

import json
from datetime import datetime

from src.entities.container import Container
from src.entities.location import Location


class Order:
    """Represents an order with an ID, order number, quantity, container, assigned truck, truck type, material, origin, and destination."""
    all_orders = []

    def __init__(
        self,
        uid,
        status,
        quantity,
        # container,
        assigned_truck,
        is_external,
        truck_type,
        material,
        origin,
        destination,
        deadline_date=None,
        load_duration=0,
    ):
        """
        Initializes an Order object.

        Args:
            uid (int): The ID of the order.
            date (str): The date of the order in the format "%Y-%m-%dT%H:%M:%S.%fZ".
            quantity (int): The quantity of the order.
            container (dict): The container information in JSON format.
            assigned_truck (str): The assigned truck for the order.
            truck_type (str): The type of truck for the order.
            material (str): The material of the order.
            origin (dict): The origin location information in JSON format.
            destination (dict): The destination location information in JSON format.
        """
        self.uid = uid

        self.quantity = quantity
        self.status = status
        # self.container = Container.from_json(container)
        self.assigned_truck = assigned_truck
        self.is_external = is_external
        self.truck_type = truck_type
        self.material = material
        self.origin = Location.from_json(origin)
        self.destination = Location.from_json(destination)
       
        self.deadline_date = (
            datetime.strptime(deadline_date, "%Y-%m-%dT%H:%M:%S.%fZ")
            if deadline_date
            else None
        )

        self.load_duration = load_duration
        self.route = None

    def __str__(self):
        return f"{self.uid} {self.deadline_date} {self.quantity} {self.status}"

    def __repr__(self):
        return f"{self.uid} {self.deadline_date} {self.quantity} {self.status}"

    @staticmethod
    def from_json(order):
        """Create an order from a json object."""
        return Order(
            order["uid"],
            order["status"],
            order["quantity"],
            # order["container"],
            order["assigned_truck"] if "assigned_truck" in order else None,
            order["is_external"] if "is_external" in order else False,
            order["truck_type"],
            order["material"],
            order["origin"],
            order["destination"],
            order["deadline_date"] if "deadline_date" in order else None,
            order["load_duration"] if "load_duration" in order else 0,
        )

    def to_json(self):
        """Return the order as a json object."""
        return {
            "uid": self.uid,
            "quantity": self.quantity,
            "status": self.status,
            "assigned_truck": self.assigned_truck,
            "is_external": self.is_external,
            "truck_type": self.truck_type,
            "material": self.material,
            "origin": self.origin.to_json(),
            "destination": self.destination.to_json(),
            "deadline_date": self.deadline_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            if self.deadline_date
            else None,
            "load_duration": self.load_duration,
            "route": json.dumps(self.route) if self.route else None,
        }

    @staticmethod
    def load_order_from_sinex(order_id):
        """Load an order from the sinex file."""
        found_order = None
        for order in Order.all_orders:
            if order.uid == order_id:
                found_order = order
                break

        if found_order is None:
            raise ValueError(f"Order with id {order_id} not found")

        return found_order

    @staticmethod
    def get_orders_of_vehicle(vehicle, status):
        """Get all orders of a vehicle."""
        found_orders = []
        for order in Order.all_orders:
            if order.assigned_truck == vehicle.license_plate and (not status or order.status == status):
                found_orders.append(order)

        return found_orders

    @staticmethod
    def get_last_order_of_vehicle(vehicle, status=None):
        """Get the last order of a vehicle."""
        orders = Order.get_orders_of_vehicle(vehicle, status)
        if not orders:
            return None

        print(max(orders, key=lambda x: x.deadline_date))

        return max(orders, key=lambda x: x.deadline_date)
    
    @staticmethod
    def update_order(order, vehicle):
        """Update the order with the vehicle."""
        index = 0
        # for order in Order.all_orders:
        #     if order.uid == order.uid:
        #         order.assigned_truck = vehicle.license_plate
            #     Order.all_orders[index] = order

            # index = index + 1
