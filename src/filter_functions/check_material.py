def check_material(order, vehicle):
    last_order_material = vehicle.get_last_order_material()
    return not last_order_material or last_order_material == order.material