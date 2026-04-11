import math

# --- HÀM BỔ TRỢ: Tính khoảng cách giữa 2 tọa độ GPS (Haversine) ---
def haversine_distance(p1, p2):
    """Tính khoảng cách thực tế giữa 2 điểm tọa độ GPS (đơn vị: km)"""
    # p1, p2 có thể là object DonHang hoặc tuple (lat, lng)
    lat1 = p1.lat if hasattr(p1, 'lat') else p1[0]
    lng1 = p1.lng if hasattr(p1, 'lng') else p1[1]
    lat2 = p2.lat if hasattr(p2, 'lat') else p2[0]
    lng2 = p2.lng if hasattr(p2, 'lng') else p2[1]
    
    # Công thức Haversine để tính km chuẩn trên mặt cầu
    R = 6371  # Bán kính Trái Đất tính bằng km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lng2 - lng1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R * c

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
        # #### CHỈNH SỬA: Sử dụng haversine_distance để tính km thực tế ####
        closest_order = min(unvisited, key=lambda x: haversine_distance(current_pos, x))
        dist = haversine_distance(current_pos, closest_order)
        
        total_dist += dist
        route.append(closest_order)
        
        # Cập nhật vị trí hiện tại là đơn hàng vừa chọn
        # #### CHỈNH SỬA: Đổi toa_do_y -> lat, toa_do_x -> lng ####
        current_pos = (closest_order.lat, closest_order.lng)
        unvisited.remove(closest_order)
        
    # #### THÊM MỚI: Tính quãng đường từ điểm cuối quay về kho ####
    dist_back = haversine_distance(current_pos, depot)
    total_dist += dist_back
        
    return route, total_dist