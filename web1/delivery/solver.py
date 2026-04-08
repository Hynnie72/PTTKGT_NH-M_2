import math

def calculate_distance(p1, p2):
    """Tính khoảng cách Euclide giữa 2 điểm tọa độ GPS"""
    # p1, p2 có thể là object DonHang hoặc tuple (lat, lng)
    lat1 = p1.toa_do_y if hasattr(p1, 'toa_do_y') else p1[0]
    lng1 = p1.toa_do_x if hasattr(p1, 'toa_do_x') else p1[1]
    lat2 = p2.toa_do_y if hasattr(p2, 'toa_do_y') else p2[0]
    lng2 = p2.toa_do_x if hasattr(p2, 'toa_do_x') else p2[1]
    
    return math.sqrt((lat2 - lat1)**2 + (lng2 - lng1)**2)

def solve_greedy(orders):
    """
    Thuật toán Tham lam (Nearest Neighbor):
    Luôn chọn điểm gần vị trí hiện tại nhất để đi tiếp.
    """
    if not orders:
        return [], 0
    
    # #### THÊM MỚI: Tọa độ Kho mặc định tại Võ Oanh ####
    depot = (10.802, 106.713)
    current_pos = depot
    unvisited = list(orders)
    route = []
    total_dist = 0
    
    while unvisited:
        # Tìm đơn hàng gần vị trí hiện tại nhất
        closest_order = min(unvisited, key=lambda x: calculate_distance(current_pos, x))
        dist = calculate_distance(current_pos, closest_order)
        
        total_dist += dist
        route.append(closest_order)
        # Cập nhật vị trí hiện tại là đơn hàng vừa chọn
        current_pos = (closest_order.toa_do_y, closest_order.toa_do_x)
        unvisited.remove(closest_order)
        
    return route, total_dist