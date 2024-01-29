import json
from datetime import datetime

class Vehicle:
    @classmethod
    def _check_keys(cls, vehicle):
        required_keys = ['oid', 'vehicleCode', 'licensePlate', 'cardExpiration', 'permissionExpiration', 'itvExpiration', 'insuranceExpiration', 'extinguisherExpiration', 'wasteExpiration', 'pressureExpiration', 'compressorExpiration', 'suspensionExpiration', 'active', 'company', 'cardType', 'truckType', 'tachographExpiration', 'loadCapacity', 'authorizedWeight', 'delegation', 'mileage', 'hours', 'grossVehicleWeight', 'tareWeight', 'operationalStatus', 'vehicleClassification', 'usualLoadingPoint']
        
        if not all(key in vehicle for key in required_keys):
            raise ValueError("Missing required keys in vehicle dictionary")

    def __init__(self, **kwargs):
        self._check_keys(kwargs)
        for key, value in kwargs.items():
            if 'Expiration' in key and value is not None:
                value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            setattr(self, key, value)

        self.score = 0

    def __str__(self):
        return f'{self.licensePlate}'

    def __repr__(self):
        return f'{self.licensePlate}: {self.score} points'

    @staticmethod
    def from_json(vehicle):
        return Vehicle(**vehicle)

    @staticmethod
    def load_from_sinex():
        with open(f'src/data/vehicles.json', 'r') as file:
            vehicle_json = json.load(file)
        vehicles = []
        for vehicle in vehicle_json:
            vehicles.append(Vehicle.from_json(vehicle))
        return vehicles
         
    # TODO: Implement fields
    def can_travel_international(self):
        return True

    # TODO: Implement fields
    def can_travel_national(self):
        return True

    def check_expirations(self, date):
        if self.active == False:
            return False

        attributes_to_check = ['cardExpiration', 'permissionExpiration', 'itvExpiration', 'insuranceExpiration', 'extinguisherExpiration', 'wasteExpiration', 'pressureExpiration', 'compressorExpiration', 'suspensionExpiration', 'tachographExpiration']
        
        is_valid = True
        for attribute in attributes_to_check:
            expiration = getattr(self, attribute)
            if expiration is not None and date >= expiration:
                is_valid = False
                print(f"DEUBG: {attribute} del vehiculo {self} ha expirado")

        return is_valid

    def add_score(self, score):
        self.score += score