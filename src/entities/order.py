from .container import Container
from datetime import datetime
import json
from .location import Location

class Order:
    def __init__(self, id, order_number, date, quantity, container, assignedTruck, truckType, material, origin, destination):
        self.id = id
        self.order_number = order_number
        self.date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        self.quantity = quantity
        self.container = Container.from_json(container)
        self.assignedTruck = assignedTruck
        self.truckType = truckType
        self.material = material
        self.origin = Location.from_json(origin)
        self.destination = Location.from_json(destination)

    def __str__(self):
        return f'{self.id} {self.order_number} {self.date} {self.quantity} {self.container}'

    def __repr__(self):
        return f'{self.id} {self.order_number} {self.date} {self.quantity} {self.container}'

    @staticmethod
    def from_json(order):
        return Order(order['id'], order['order_number'], order['date'], order['quantity'], order['container'], order['assignedTruck'], order['truckType'], order['material'], order['origin'], order['destination'])

    @staticmethod
    def load_all_orders():
        with open(f'src/data/orders.json', 'r') as file:
            order_json = json.load(file)
        orders = []
        for order in order_json:
            orders.append(Order.from_json(order))
        return orders

    @staticmethod
    def load_order_from_sinex(order_id):
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
        orders = Order.load_all_orders()
        found_orders = []
        for order in orders:
            if order.assignedTruck == vehicle.licensePlate:
                found_orders.append(order)

        return found_orders

    @staticmethod
    def get_last_order_of_vehicle(vehicle):
        orders = Order.get_order_of_vehicle(vehicle)
        if not orders:
            return None

        return max(orders, key=lambda x: x.date)