"""Vehicle entity module"""
import json
from datetime import datetime
from src.entities.location import Location
from src.entities.order import Order


class Vehicle:
    """Vehicle entity class"""
    @classmethod
    def _check_keys(cls, vehicle):
        required_keys = ['oid', 'vehicle_code', 'license_plate', 'card__expiration', 'permission__expiration', 'itv__expiration', 'insurance_expiration', 'extinguisher_expiration', 'waste_expiration', 'pressure_expiration', 'compressor_expiration',
                         'suspension__expiration', 'tachograph_expiration', 'active', 'mileage', 'hours', 'gross_vehicle_weight', 'tare_weight', 'truck_type_name', 'assigned_ex', 'geolocation', 'last_trimester_order_count', 'last_trimester_mileage_count']

        if not all(key in vehicle for key in required_keys):
            raise ValueError("Missing required keys in vehicle dictionary")

    def __init__(self, oid, vehicle_code, license_plate, card__expiration, permission__expiration, itv__expiration, insurance_expiration, extinguisher_expiration, waste_expiration, pressure_expiration, compressor_expiration, suspension__expiration, tachograph_expiration, active, mileage, hours, gross_vehicle_weight, tare_weight, truck_type_name, assigned_ex, geolocation, last_trimester_order_count, last_trimester_mileage_count):
        self.oid = oid
        self.vehicle_code = vehicle_code
        self.license_plate = license_plate
        self.card__expiration = datetime.strptime(
            card__expiration, "%Y-%m-%d %H:%M:%S")
        self.permission__expiration = datetime.strptime(
            permission__expiration, "%Y-%m-%d %H:%M:%S")
        self.itv__expiration = datetime.strptime(
            itv__expiration, "%Y-%m-%d %H:%M:%S")
        self.insurance_expiration = datetime.strptime(
            insurance_expiration, "%Y-%m-%d %H:%M:%S")
        self.extinguisher_expiration = datetime.strptime(
            extinguisher_expiration, "%Y-%m-%d %H:%M:%S")
        self.waste_expiration = datetime.strptime(
            waste_expiration, "%Y-%m-%d %H:%M:%S")
        self.pressure_expiration = datetime.strptime(
            pressure_expiration, "%Y-%m-%d %H:%M:%S")
        self.compressor_expiration = datetime.strptime(
            compressor_expiration, "%Y-%m-%d %H:%M:%S")
        self.suspension__expiration = datetime.strptime(
            suspension__expiration, "%Y-%m-%d %H:%M:%S")
        self.tachograph_expiration = datetime.strptime(
            tachograph_expiration, "%Y-%m-%d %H:%M:%S")
        self.active = active
        self.mileage = mileage
        self.hours = hours
        self.gross_vehicle_weight = gross_vehicle_weight
        self.tare_weight = tare_weight
        self.truck_type_name = truck_type_name
        self.assigned_ex = assigned_ex
        self.geolocation = geolocation
        self.last_trimester_order_count = last_trimester_order_count
        self.last_trimester_mileage_count = last_trimester_mileage_count

        self.score = 0

    def __str__(self):
        return f'{self.license_plate}'

    def __repr__(self):
        return f'{self.license_plate}: {round(self.score, 4)} points'

    @staticmethod
    def from_json(vehicle):
        """Creates a Vehicle object from a dictionary"""
        return Vehicle(**vehicle)

    @staticmethod
    def load_from_sinex():
        """Loads vehicles from a json file and returns a list of Vehicle objects"""
        with open('src/data/vehicles.json', 'r', encoding='utf-8') as file:
            vehicle_json = json.load(file)
        vehicles = []
        for vehicle in vehicle_json:
            vehicles.append(Vehicle.from_json(vehicle))
        return vehicles

    # TODO: Implement fields
    def can_travel_international(self):
        """Returns True if the vehicle can travel internationally, False otherwise."""
        return True

    # TODO: Implement fields
    def can_travel_national(self):
        """Returns True if the vehicle can travel nationally, False otherwise."""
        return True

    def check__expirations(self, date):
        """Returns True if all the vehicle's _expirations are valid, False otherwise."""
        if self.active is False:
            return False

        attributes_to_check = ['card__expiration', 'permission__expiration', 'itv__expiration', 'insurance_expiration', 'extinguisher_expiration',
                               'waste_expiration', 'pressure_expiration', 'compressor_expiration', 'suspension_expiration', 'tachograph_expiration']

        is_valid = True
        for attribute in attributes_to_check:
            _expiration = getattr(self, attribute)
            if _expiration is not None and date >= _expiration:
                is_valid = False
                print(f"DEUBG: {attribute} del vehiculo {self} ha expirado")

        return is_valid

    def add_score(self, score):
        """Adds score to the vehicle's score."""
        self.score += score

    def get_last_order_material(self):
        """Returns the material of the last order of the vehicle."""
        last_vehicle_order = Order.get_last_order_of_vehicle(self)
        return last_vehicle_order and last_vehicle_order.material

    def get_location(self):
        """Returns the vehicle's location as a Location object."""
        return Location(lat=self.geolocation['lat'], lon=self.geolocation['lon'])
