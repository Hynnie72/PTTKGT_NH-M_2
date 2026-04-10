import math

# TÍNH KHOẢNG CÁCH HAVERSINE (km)
def haversine_distance(node1, node2):
    R = 6371  # bán kính Trái Đất (km)

    lat1 = math.radians(node1.x)
    lon1 = math.radians(node1.y)
    lat2 = math.radians(node2.x)
    lon2 = math.radians(node2.y)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c  # km


# MA TRẬN KHOẢNG CÁCH
def create_distance_matrix(nodes):
    n = len(nodes)
    dist_matrix = [[0]*n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            dist_matrix[i][j] = haversine_distance(nodes[i], nodes[j])

    return dist_matrix


# IN MA TRẬN
def print_distance_matrix(matrix):
    print("Distance Matrix (km):")
    for row in matrix:
        for val in row:
            print(f"{val:.2f}", end="\t")
        print()