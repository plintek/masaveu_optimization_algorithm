"""Module providing a function printing python version."""

import json
from datetime import datetime
from src.entities.container import Container
from src.entities.location import Location


class Order:
    def __init__(
        self,
        id,
        order_number,
        date,
        quantity,
        container,
        assigned_truck,
        truck_type,
        material,
        origin,
        destination,
    ):
        """
        Initializes an Order object.

        Args:
            id (int): The ID of the order.
            order_number (str): The order number.
            date (str): The date of the order in the format "%Y-%m-%d %H:%M:%S".
            quantity (int): The quantity of the order.
            container (dict): The container information in JSON format.
            assigned_truck (str): The assigned truck for the order.
            truck_type (str): The type of truck for the order.
            material (str): The material of the order.
            origin (dict): The origin location information in JSON format.
            destination (dict): The destination location information in JSON format.
        """
        self.id = id
        self.order_number = order_number
        self.date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        self.quantity = quantity
        self.container = Container.from_json(container)
        self.assigned_truck = assigned_truck
        self.truck_type = truck_type
        self.material = material
        self.origin = Location.from_json(origin)
        self.destination = Location.from_json(destination)

    def __str__(self):
        return f"{self.id} {self.order_number} {self.date} {self.quantity} {self.container}"

    def __repr__(self):
        return f"{self.id} {self.order_number} {self.date} {self.quantity} {self.container}"

    @staticmethod
    def from_json(order):
        """Create an order from a json object."""
        return Order(
            order["id"],
            order["order_number"],
            order["date"],
            order["quantity"],
            order["container"],
            order["assigned_truck"],
            order["truck_type"],
            order["material"],
            order["origin"],
            order["destination"],
        )

    @staticmethod
    def load_all_orders():
        """Load all orders from the json file."""
        with open("src/data/orders.json", "r", encoding="utf-8") as file:
            order_json = json.load(file)
        orders = []
        for order in order_json:
            orders.append(Order.from_json(order))
        return orders

    @staticmethod
    def load_order_from_sinex(order_id):
        """Load an order from the sinex file."""
        orders = Order.load_all_orders()
        found_order = None
        for order in orders:
            if order.id == order_id:
                found_order = order
                break

        if found_order is None:
            raise ValueError(f"Order with id {order_id} not found")

        return found_order

    @staticmethod
    def get_order_of_vehicle(vehicle):
        """Get all orders of a vehicle."""
        orders = Order.load_all_orders()
        found_orders = []
        for order in orders:
            if order.assigned_truck == vehicle.licensePlate:
                found_orders.append(order)

        return found_orders

    @staticmethod
    def get_last_order_of_vehicle(vehicle):
        """Get the last order of a vehicle."""
        orders = Order.get_order_of_vehicle(vehicle)
        if not orders:
            return None

        return max(orders, key=lambda x: x.date)
