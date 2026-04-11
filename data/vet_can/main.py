from input_module import read_input
from distance_module import create_distance_matrix, print_distance_matrix
from cost import calculate_cost
from tsp_map import find_best_route, print_best_route

def main():
    names = ["Kho",  "Quận 1", "Quận 3", "Quận 4", "Quận 5", "Quận 6",  "Quận 8", "Quận 10"]

    # -------------------------
    # MODULE INPUT
    # -------------------------
    nodes = read_input("data.txt")

    print("\n===== DANH SÁCH ĐỊA ĐIỂM =====")
    print(f"{'Địa điểm':<10} | {'Tọa độ (lat, lon)':<25} | {'Time Window':<15} | {'Service'}")
    print("-"*70)

    for node in nodes:
        coord = f"({node.x:.5f}, {node.y:.5f})"
        time_window = f"[{node.earliest}, {node.latest}]"
        service = f"{node.service_time}"

        print(f"{names[node.id]:<10} | {coord:<25} | {time_window:<15} | {service}")

    # -------------------------
    # MODULE DISTANCE
    # -------------------------
    matrix = create_distance_matrix(nodes)

    print("\n===== MA TRẬN KHOẢNG CÁCH =====")
    print_distance_matrix(matrix)


    best_path, best_cost = find_best_route(nodes, matrix)

    print_best_route(best_path, matrix)




if __name__ == "__main__":
    main()