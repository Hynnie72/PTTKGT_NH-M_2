import time

from utils import read_data
from tsp_dp import tsp_dp
from code_tim_duong import solve_tsp
from code_xu_ly import create_distance_from_points


def main():
    print("=== CHUONG TRINH TSP NHOM ===")

    # đọc dữ liệu từ file
    points = read_data("testdp.txt")

    # lấy tọa độ (bỏ id)
    coords = [(p[1], p[2]) for p in points]

    # tạo ma trận khoảng cách
    dist = create_distance_from_points(coords)

    start = time.time()

    # thuật toán 1
    cost1, path1 = tsp_dp(dist)

    # thuật toán 2
    cost2, path2 = solve_tsp(dist)

    end = time.time()

    print("\n--- Ket qua tsp_dp ---")
    print("Chi phi:", cost1)
    print("Duong di:", path1)

    print("\n--- Ket qua code_tim_duong ---")
    print("Chi phi:", cost2)
    print("Duong di:", path2)

    print("\nThoi gian chay:", (end - start)*1000, "ms")


if __name__ == "__main__":
    main()