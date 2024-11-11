# TODO: Check date
"""Check if the vehicle has any expirations."""


def vehicle_expirations(order, vehicle, check_date):
    """Check if the vehicle has any expirations."""
    return vehicle.check_expirations(order.deadline_date)
