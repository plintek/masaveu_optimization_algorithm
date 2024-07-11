def check_pending_orders(order, vehicle):
    """Check if the vehicle has any pending orders."""
    return not vehicle.has_pending_orders()