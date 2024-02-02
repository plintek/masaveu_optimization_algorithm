def national_international(order, vehicle):
    is_international = order.destination.is_international()
    return is_international and vehicle.can_travel_international() or not is_international and vehicle.can_travel_national()