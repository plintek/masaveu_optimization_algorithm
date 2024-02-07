"""Vehicle entity module"""
import json
from datetime import datetime
from src.entities.location import Location
from src.entities.order import Order


class Vehicle:
    """Vehicle entity class"""

    def __init__(self, uid, vehicle_code, license_plate, card_expiration, permission_expiration, itv_expiration, insurance_expiration, extinguisher_expiration, waste_expiration, pressure_expiration, compressor_expiration, suspension_expiration, tachograph_expiration, active, mileage, hours, gross_vehicle_weight, tare_weight, truck_type_name, assigned_pex, geolocation, last_trimester_order_count, last_trimester_mileage_count, height, can_go_international):
        self.uid = uid
        self.vehicle_code = vehicle_code
        self.license_plate = license_plate
        self.card_expiration = datetime.strptime(
            card_expiration, "%Y-%m-%dT%H:%M:%S.%fZ") if card_expiration else None
        self.permission_expiration = datetime.strptime(
            permission_expiration, "%Y-%m-%dT%H:%M:%S.%fZ") if permission_expiration else None
        self.itv_expiration = datetime.strptime(
            itv_expiration, "%Y-%m-%dT%H:%M:%S.%fZ") if itv_expiration else None
        self.insurance_expiration = datetime.strptime(
            insurance_expiration, "%Y-%m-%dT%H:%M:%S.%fZ") if insurance_expiration else None
        self.extinguisher_expiration = datetime.strptime(
            extinguisher_expiration, "%Y-%m-%dT%H:%M:%S.%fZ") if extinguisher_expiration else None
        self.waste_expiration = datetime.strptime(
            waste_expiration, "%Y-%m-%dT%H:%M:%S.%fZ") if waste_expiration else None
        self.pressure_expiration = datetime.strptime(
            pressure_expiration, "%Y-%m-%dT%H:%M:%S.%fZ") if pressure_expiration else None
        self.compressor_expiration = datetime.strptime(
            compressor_expiration, "%Y-%m-%dT%H:%M:%S.%fZ") if compressor_expiration else None
        self.suspension_expiration = datetime.strptime(
            suspension_expiration, "%Y-%m-%dT%H:%M:%S.%fZ") if suspension_expiration else None
        self.tachograph_expiration = datetime.strptime(
            tachograph_expiration, "%Y-%m-%dT%H:%M:%S.%fZ") if tachograph_expiration else None
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
        return f'{self.uid} con matrícula {self.license_plate}'

    def __repr__(self):
        return f'{self.uid} con matrícula {self.license_plate}: {round(self.score, 4)} points{self.will_be_in_geographic_zone and " GEOGRAPHIC PRIORITY" or ""}'

    # json dumps
    def to_json(self):
        """Returns the vehicle as a dictionary"""
        return {
            "uid": self.uid,
            "vehicle_code": self.vehicle_code,
            "license_plate": self.license_plate,
            "card_expiration": self.card_expiration.strftime("%Y-%m-%dT%H:%M:%S.%fZ") if self.card_expiration else None,
            "permission_expiration": self.permission_expiration.strftime("%Y-%m-%dT%H:%M:%S.%fZ") if self.permission_expiration else None,
            "itv_expiration": self.itv_expiration.strftime("%Y-%m-%dT%H:%M:%S.%fZ") if self.itv_expiration else None,
            "insurance_expiration": self.insurance_expiration.strftime("%Y-%m-%dT%H:%M:%S.%fZ") if self.insurance_expiration else None,
            "extinguisher_expiration": self.extinguisher_expiration.strftime("%Y-%m-%dT%H:%M:%S.%fZ") if self.extinguisher_expiration else None,
            "waste_expiration": self.waste_expiration.strftime("%Y-%m-%dT%H:%M:%S.%fZ") if self.waste_expiration else None,
            "pressure_expiration": self.pressure_expiration.strftime("%Y-%m-%dT%H:%M:%S.%fZ") if self.pressure_expiration else None,
            "compressor_expiration": self.compressor_expiration.strftime("%Y-%m-%dT%H:%M:%S.%fZ") if self.compressor_expiration else None,
            "suspension_expiration": self.suspension_expiration.strftime("%Y-%m-%dT%H:%M:%S.%fZ") if self.suspension_expiration else None,
            "tachograph_expiration": self.tachograph_expiration.strftime("%Y-%m-%dT%H:%M:%S.%fZ") if self.tachograph_expiration else None,
            "active": self.active,
            "mileage": self.mileage,
            "hours": self.hours,
            "gross_vehicle_weight": self.gross_vehicle_weight,
            "tare_weight": self.tare_weight,
            "truck_type_name": self.truck_type_name,
            "assigned_pex": self.assigned_pex,
            "geolocation_lat": self.geolocation["lat"],
            "geolocation_lon": self.geolocation["lon"],
            "last_trimester_order_count": self.last_trimester_order_count,
            "last_trimester_mileage_count": self.last_trimester_mileage_count,
            "height": self.height,
            "can_go_international": self.can_go_international,
            "score": round(self.score, 3)
        }

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
