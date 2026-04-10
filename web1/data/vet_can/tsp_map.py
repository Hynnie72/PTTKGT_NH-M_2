# ==============================
# MODULE: TÌM TUYẾN TỐI ƯU (Ý)
# ==============================

from all_paths import tsp_bruteforce   # dùng code của Kiên
from cost import calculate_cost       # dùng code của Đức

names = ["Kho", "Quận 1", "Quận 3", "Quận 4", "Quận 5", "Quận 6", "Quận 8", "Quận 10"]


def find_best_route(nodes, dist_matrix):

    print("\n ĐANG TÌM TUYẾN TỐI ƯU...")

    best_path, best_cost = tsp_bruteforce(nodes, dist_matrix)

    return best_path, best_cost


def print_best_route(best_path, dist_matrix):
    """
    In kết quả đẹp hơn
    """

    print("\n=========================")
    print(" TUYẾN ĐƯỜNG TỐI ƯU")

    route_str = " → ".join(names[i] for i in best_path)
    print("Path:", route_str)

    print("\n CHI TIẾT CHI PHÍ:")

    # bỏ kho đầu và cuối
    path_for_cost = best_path[1:-1]

    total_cost = calculate_cost(path_for_cost, dist_matrix)

    print("\n Tổng chi phí:", round(total_cost, 2))

    return total_cost