def check_material(order, vehicle, check_date, use_pending_orders):
    """Check if the vehicle can carry the material of the order. If the vehicle has no last order, it can carry the material. If the vehicle has a last order, it can carry the material if the material of the last order is the same as the material of the order. If the vehicle has a last order and the material of the last order is different from the material of the order, the vehicle cannot carry the material."""
    last_order_material = vehicle.get_last_order_material()
    return not last_order_material or last_order_material == order.material
