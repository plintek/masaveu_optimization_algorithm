"""Filter function to check if a vehicle can travel to the destination of an order."""


def national_international(order, vehicle, check_date):
    """Filter function to check if a vehicle can travel to the destination of an order."""
    is_international = order.destination.is_international()
    return is_international and vehicle.can_travel_international() or not is_international and vehicle.can_travel_national()
