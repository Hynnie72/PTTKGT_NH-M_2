import numpy as np
from typing import List, Tuple, Dict
import heapq

class DeliveryOptimizer:
    """
    Tối ưu hóa lộ trình giao hàng sử dụng thuật toán tham lam (Nearest Neighbor)
    với ràng buộc thời gian
    """
    
    def __init__(self, distances: List[List[float]], time_windows: List[Tuple[int, int]] = None, 
                 service_times: List[float] = None, start_point: int = 0):
        """
        Khởi tạo bài toán giao hàng
        
        Args:
            distances: Ma trận khoảng cách giữa các điểm (N x N)
            time_windows: Khung giờ cho phép giao hàng tại mỗi điểm [(earliest, latest), ...]
                         None nếu không có ràng buộc
            service_times: Thời gian phục vụ tại mỗi điểm (phút)
            start_point: Điểm xuất phát (kho hàng)
        """
        self.distances = distances
        self.n = len(distances)
        self.time_windows = time_windows
        self.service_times = service_times if service_times else [0] * self.n
        self.start_point = start_point
        
    def nearest_neighbor_with_time_constraints(self) -> Tuple[List[int], float, List[float]]:
        """
        Thuật toán Nearest Neighbor có xét ràng buộc thời gian
        
        Returns:
            route: Danh sách các điểm theo thứ tự giao hàng
            total_distance: Tổng quãng đường
            arrival_times: Thời gian đến từng điểm
        """
        unvisited = set(range(self.n))
        unvisited.remove(self.start_point)
        
        route = [self.start_point]
        current = self.start_point
        current_time = 0  # Thời gian hiện tại (phút)
        total_distance = 0
        arrival_times = [0] * self.n
        arrival_times[self.start_point] = 0
        
        while unvisited:
            best_next = None
            best_distance = float('inf')
            
            # Tìm điểm chưa thăm gần nhất thỏa mãn ràng buộc thời gian
            for next_point in unvisited:
                travel_time = self.distances[current][next_point]
                arrival_time = current_time + travel_time + self.service_times[current]
                
                # Kiểm tra ràng buộc khung giờ
                if self.time_windows and self.time_windows[next_point]:
                    earliest, latest = self.time_windows[next_point]
                    # Nếu đến sớm hơn earliest, phải đợi
                    if arrival_time < earliest:
                        arrival_time = earliest
                    # Nếu đến muộn hơn latest, không thể giao
                    if arrival_time > latest:
                        continue
                
                # Chọn điểm gần nhất thỏa mãn
                if self.distances[current][next_point] < best_distance:
                    best_distance = self.distances[current][next_point]
                    best_next = next_point
                    best_arrival_time = arrival_time
            
            if best_next is None:
                # Không tìm được điểm thỏa mãn, kết thúc
                break
                
            # Thêm điểm vào lộ trình
            route.append(best_next)
            total_distance += best_distance
            current_time = best_arrival_time
            arrival_times[best_next] = current_time
            current = best_next
            unvisited.remove(best_next)
        
        # Quay về điểm xuất phát
        return_distance = self.distances[current][self.start_point]
        total_distance += return_distance
        route.append(self.start_point)
        
        return route, total_distance, arrival_times
    
    def nearest_neighbor_with_look_ahead(self) -> Tuple[List[int], float, List[float]]:
        """
        Nearest Neighbor với cải tiến: xét cả 2 bước tiếp theo để tránh kẹt
        """
        unvisited = set(range(self.n))
        unvisited.remove(self.start_point)
        
        route = [self.start_point]
        current = self.start_point
        current_time = 0
        total_distance = 0
        arrival_times = [0] * self.n
        
        while unvisited:
            best_next = None
            best_score = float('inf')
            
            # Đánh giá từng điểm khả thi
            for next_point in unvisited:
                travel_time = self.distances[current][next_point]
                arrival_time = current_time + travel_time + self.service_times[current]
                
                if self.time_windows and self.time_windows[next_point]:
                    earliest, latest = self.time_windows[next_point]
                    if arrival_time < earliest:
                        arrival_time = earliest
                    if arrival_time > latest:
                        continue
                
                # Tính điểm số dựa trên khoảng cách và ảnh hưởng đến các điểm còn lại
                temp_unvisited = unvisited.copy()
                temp_unvisited.remove(next_point)
                
                # Tìm điểm gần nhất từ next_point trong số các điểm còn lại
                if temp_unvisited:
                    min_next_dist = min(self.distances[next_point][p] for p in temp_unvisited)
                    # Điểm số: khoảng cách hiện tại + khoảng cách dự kiến tiếp theo
                    score = self.distances[current][next_point] + 0.5 * min_next_dist
                else:
                    score = self.distances[current][next_point]
                
                if score < best_score:
                    best_score = score
                    best_next = next_point
                    best_arrival_time = arrival_time
            
            if best_next is None:
                break
                
            route.append(best_next)
            total_distance += self.distances[current][best_next]
            current_time = best_arrival_time
            arrival_times[best_next] = current_time
            current = best_next
            unvisited.remove(best_next)
        
        # Quay về điểm xuất phát
        total_distance += self.distances[current][self.start_point]
        route.append(self.start_point)
        
        return route, total_distance, arrival_times
    
    def calculate_route_time(self, route: List[int]) -> Tuple[float, List[float]]:
        """
        Tính thời gian hoàn thành lộ trình
        
        Args:
            route: Lộ trình giao hàng
            
        Returns:
            total_time: Tổng thời gian hoàn thành
            arrival_times: Thời gian đến từng điểm
        """
        current_time = 0
        arrival_times = [0] * self.n
        total_distance = 0
        
        for i in range(len(route) - 1):
            from_point = route[i]
            to_point = route[i + 1]
            
            travel_time = self.distances[from_point][to_point]
            current_time += travel_time
            
            # Nếu có ràng buộc thời gian, phải đợi nếu đến sớm
            if self.time_windows and self.time_windows[to_point]:
                earliest, _ = self.time_windows[to_point]
                if current_time < earliest:
                    current_time = earliest
            
            arrival_times[to_point] = current_time
            current_time += self.service_times[to_point]
            total_distance += travel_time
        
        return current_time, arrival_times
    
    def two_opt_improvement(self, route: List[int]) -> Tuple[List[int], float]:
        """
        Cải thiện lộ trình bằng thuật toán 2-opt (tùy chọn)
        
        Args:
            route: Lộ trình cần cải thiện
            
        Returns:
            improved_route: Lộ trình được cải thiện
            improved_distance: Quãng đường sau cải thiện
        """
        best_route = route[:-1]  # Bỏ điểm quay về
        best_distance = sum(self.distances[best_route[i]][best_route[i+1]] 
                           for i in range(len(best_route)-1))
        improved = True
        
        while improved:
            improved = False
            for i in range(1, len(best_route) - 2):
                for j in range(i + 1, len(best_route) - 1):
                    # Đảo đoạn [i:j]
                    new_route = best_route[:i] + best_route[i:j+1][::-1] + best_route[j+1:]
                    
                    new_distance = sum(self.distances[new_route[k]][new_route[k+1]] 
                                      for k in range(len(new_route)-1))
                    
                    if new_distance < best_distance:
                        best_route = new_route
                        best_distance = new_distance
                        improved = True
                        break
                if improved:
                    break
        
        # Thêm điểm quay về
        best_route.append(self.start_point)
        best_distance += self.distances[best_route[-2]][self.start_point]
        
        return best_route, best_distance

def print_route(route: List[int], total_distance: float, arrival_times: List[float]):
    """In lộ trình và thông tin chi tiết"""
    print(f"{'Điểm':<6} {'Thời gian đến':<15} {'Khoảng cách tích lũy':<20}")
    print("-" * 50)
    
    cumulative_dist = 0
    for i in range(len(route) - 1):
        current = route[i]
        next_point = route[i + 1]
        dist = distances[current][next_point]
        cumulative_dist += dist
        
        time_str = f"{arrival_times[next_point]:.2f}" if next_point < len(arrival_times) else "N/A"
        print(f"{next_point:<6} {time_str:<15} {cumulative_dist:<20.2f}")
    
    print(f"\nTổng quãng đường: {total_distance:.2f} đơn vị")
    print(f"Số điểm giao hàng: {len(set(route)) - 1}")

# ============ VÍ DỤ SỬ DỤNG ============

if __name__ == "__main__":
    # Tạo ma trận khoảng cách mẫu (6 điểm: 0 là kho, 1-5 là điểm giao)
    # Khoảng cách ngẫu nhiên trong khoảng 10-50 đơn vị
    np.random.seed(42)
    n_points = 6
    distances = np.random.randint(10, 50, size=(n_points, n_points))
    distances = (distances + distances.T) // 2  # Đối xứng hóa
    np.fill_diagonal(distances, 0)
    
    # Ràng buộc khung giờ (phút từ thời điểm bắt đầu)
    # [earliest, latest] cho mỗi điểm
    time_windows = [
        (0, 200),      # Điểm 0: kho hàng
        (10, 60),      # Điểm 1: 10-60 phút
        (20, 80),      # Điểm 2: 20-80 phút
        (30, 100),     # Điểm 3: 30-100 phút
        (50, 150),     # Điểm 4: 50-150 phút
        (60, 180)      # Điểm 5: 60-180 phút
    ]
    
    # Thời gian phục vụ tại mỗi điểm (phút)
    service_times = [0, 5, 5, 8, 6, 4]
    
    print("=== MA TRẬN KHOẢNG CÁCH ===")
    print(distances)
    print("\n=== KHUNG GIỜ GIAO HÀNG ===")
    for i, (e, l) in enumerate(time_windows):
        print(f"Điểm {i}: {e} - {l} phút")
    
    # Khởi tạo optimizer
    optimizer = DeliveryOptimizer(distances, time_windows, service_times, start_point=0)
    
    # 1. Nearest Neighbor cơ bản
    print("\n" + "="*50)
    print("1. THUẬT TOÁN NEAREST NEIGHBOR CƠ BẢN")
    print("="*50)
    route1, total_dist1, arrival_times1 = optimizer.nearest_neighbor_with_time_constraints()
    print_route(route1, total_dist1, arrival_times1)
    
    # 2. Nearest Neighbor với look-ahead
    print("\n" + "="*50)
    print("2. THUẬT TOÁN NEAREST NEIGHBOR VỚI LOOK-AHEAD")
    print("="*50)
    route2, total_dist2, arrival_times2 = optimizer.nearest_neighbor_with_look_ahead()
    print_route(route2, total_dist2, arrival_times2)
    
    # 3. Cải thiện bằng 2-opt
    print("\n" + "="*50)
    print("3. CẢI THIỆN LỘ TRÌNH BẰNG 2-OPT")
    print("="*50)
    improved_route, improved_dist = optimizer.two_opt_improvement(route1)
    # Tính lại thời gian đến cho lộ trình cải thiện
    _, improved_times = optimizer.calculate_route_time(improved_route)
    print_route(improved_route, improved_dist, improved_times)
    
    # So sánh kết quả
    print("\n=== SO SÁNH KẾT QUẢ ===")
    print(f"Nearest Neighbor cơ bản: {total_dist1:.2f}")
    print(f"Nearest Neighbor look-ahead: {total_dist2:.2f}")
    print(f"Sau 2-opt: {improved_dist:.2f}")
    improvement = ((total_dist1 - improved_dist) / total_dist1) * 100
    print(f"Cải thiện: {improvement:.2f}%")#   U p d a t e   o n   0 4 / 1 0 / 2 0 2 6   2 2 : 1 5 : 4 9  
 