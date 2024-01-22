def national_international(order, vehicle, origin, destination):
    is_international = destination.is_international(destination)
    return is_international and vehicle.can_travel_international() or not is_international and vehicle.can_travel_national()