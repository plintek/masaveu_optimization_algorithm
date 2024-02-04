"""Vehicle entity module"""
import json
from datetime import datetime
from src.entities.location import Location
from src.entities.order import Order


class Vehicle:
    """Vehicle entity class"""

    def __init__(self, oid, vehicle_code, license_plate, card_expiration, permission_expiration, itv_expiration, insurance_expiration, extinguisher_expiration, waste_expiration, pressure_expiration, compressor_expiration, suspension_expiration, tachograph_expiration, active, mileage, hours, gross_vehicle_weight, tare_weight, truck_type_name, assigned_pex, geolocation, last_trimester_order_count, last_trimester_mileage_count, height, can_go_international):
        self.oid = oid
        self.vehicle_code = vehicle_code
        self.license_plate = license_plate
        self.card_expiration = datetime.strptime(
            card_expiration, "%Y-%m-%d %H:%M:%S") if card_expiration else None
        self.permission_expiration = datetime.strptime(
            permission_expiration, "%Y-%m-%d %H:%M:%S") if permission_expiration else None
        self.itv_expiration = datetime.strptime(
            itv_expiration, "%Y-%m-%d %H:%M:%S") if itv_expiration else None
        self.insurance_expiration = datetime.strptime(
            insurance_expiration, "%Y-%m-%d %H:%M:%S") if insurance_expiration else None
        self.extinguisher_expiration = datetime.strptime(
            extinguisher_expiration, "%Y-%m-%d %H:%M:%S") if extinguisher_expiration else None
        self.waste_expiration = datetime.strptime(
            waste_expiration, "%Y-%m-%d %H:%M:%S") if waste_expiration else None
        self.pressure_expiration = datetime.strptime(
            pressure_expiration, "%Y-%m-%d %H:%M:%S") if pressure_expiration else None
        self.compressor_expiration = datetime.strptime(
            compressor_expiration, "%Y-%m-%d %H:%M:%S") if compressor_expiration else None
        self.suspension_expiration = datetime.strptime(
            suspension_expiration, "%Y-%m-%d %H:%M:%S") if suspension_expiration else None
        self.tachograph_expiration = datetime.strptime(
            tachograph_expiration, "%Y-%m-%d %H:%M:%S") if tachograph_expiration else None
        self.active = active
        self.mileage = mileage
        self.hours = hours
        self.gross_vehicle_weight = gross_vehicle_weight
        self.tare_weight = tare_weight
        self.truck_type_name = truck_type_name
        self.assigned_pex = assigned_pex
        self.geolocation = geolocation
        self.last_trimester_order_count = last_trimester_order_count
        self.last_trimester_mileage_count = last_trimester_mileage_count
        self.height = height
        self.can_go_international = can_go_international

        self.score = 0
        self.will_be_in_geographic_zone = False

    def __str__(self):
        return f'{self.oid} con matrícula {self.license_plate}'

    def __repr__(self):
        return f'{self.oid} con matrícula {self.license_plate}: {round(self.score, 4)} points{self.will_be_in_geographic_zone and " GEOGRAPHIC PRIORITY" or ""}'

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

    def can_travel_international(self):
        """Returns True if the vehicle can travel internationally, False otherwise."""
        return self.can_go_international

    def can_travel_national(self):
        """Returns True if the vehicle can travel nationally, False otherwise."""
        return True

    def check_expirations(self, date):
        """Returns True if all the vehicle's _expirations are valid, False otherwise."""
        if self.active is False:
            return False

        attributes_to_check = ['card_expiration', 'permission_expiration', 'itv_expiration', 'insurance_expiration', 'extinguisher_expiration',
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

    @staticmethod
    def get_total_rest_time(road_minutes):
        """Returns the total rest time in minutes based on the road minutes."""
        return round(road_minutes / (4.5*60) * 45, 0)
