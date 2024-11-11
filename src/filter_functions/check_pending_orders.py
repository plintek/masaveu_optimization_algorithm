def check_pending_orders(order, vehicle, check_date):
    """Check if the vehicle has any pending orders."""
    return not vehicle.has_pending_orders()