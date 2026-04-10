import itertools
names = ["Kho", "Quận 1", "Quận 3", "Quận 4", "Quận 5", "Quận 6", "Quận 8", "Quận 10"]
def calculate_route(nodes, dist_matrix, path):
    time = 0
    total_distance = 0

    for i in range(len(path) - 1):
        current = nodes[path[i]]
        next_node = nodes[path[i+1]]

        travel_time = dist_matrix[current.id][next_node.id]
        time += travel_time

        if time < next_node.earliest:
            time = next_node.earliest

        # if time > next_node.latest:
        #     return float('inf')

        time += next_node.service_time
        total_distance += travel_time

    return total_distance


def tsp_bruteforce(nodes, dist_matrix):
    n = len(nodes)
    all_nodes = list(range(n))

    start = 0
    other_nodes = all_nodes[1:]

    best_cost = float('inf')
    best_path = None

    print("\n Một số tuyến đường:")

    max_print = 10   # 👉 giới hạn số tuyến in
    count = 0

    for perm in itertools.permutations(other_nodes):
        path = [start] + list(perm) + [start]

        cost = calculate_route(nodes, dist_matrix, path)

        if cost != float('inf'):
            #  chỉ in một số tuyến đầu
            if count < max_print:
                route_str = " → ".join(names[i] for i in path)
                print(f"Path: {route_str}")
                count += 1

        # vẫn tính tối ưu bình thường
        if cost < best_cost:
            best_cost = cost
            best_path = path

    return best_path, best_cost