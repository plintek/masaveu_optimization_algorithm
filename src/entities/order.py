from .container import Container
from datetime import datetime

class Order:
    def __init__(self, id, order_number, date, quantity, container):
        self.id = id
        self.order_number = order_number
        self.date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        self.quantity = quantity
        self.container = Container.from_json(container)

    def __str__(self):
        return f'{self.id} {self.order_number} {self.date} {self.quantity} {self.container}'

    def __repr__(self):
        return f'{self.id} {self.order_number} {self.date} {self.quantity} {self.container}'

    @staticmethod
    def from_json(order):
        return Order(order['id'], order['order_number'], order['date'], order['quantity'], order['container'])

    @staticmethod
    def load_from_sinex(order_id):
        return Order.from_json({
            "id": "89F07B0D-E424-4FC4-9135-FFE85FAC5AAF",
            "order_number": 1,
            "date": "2024-01-01 00:00:00",
            "quantity": 25000,
            "container": {
                "sacos": 1000,
                "pales": 1,
                "fardos": 0,
                "fundas": 0,
                "laminas": 0,
                "bigBags": 0
            }
        })