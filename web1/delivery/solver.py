import math
import itertools


# ==============================
# HÀM TÍNH KHOẢNG CÁCH HAVERSINE
# ==============================
def haversine_distance(p1, p2):
    lat1 = p1.lat if hasattr(p1, 'lat') else p1[0]
    lng1 = p1.lng if hasattr(p1, 'lng') else p1[1]

    lat2 = p2.lat if hasattr(p2, 'lat') else p2[0]
    lng2 = p2.lng if hasattr(p2, 'lng') else p2[1]

    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)

    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlng / 2) ** 2

    c = 2 * math.asin(math.sqrt(a))

    return R * c


# ==============================
# THUẬT TOÁN THAM LAM
# ==============================
def solve_greedy(orders):
    if not orders:
        return [], 0

    depot = (10.802, 106.713)

    current_pos = depot
    unvisited = list(orders)

    route = []
    total_dist = 0

    while unvisited:
        closest = min(unvisited, key=lambda x: haversine_distance(current_pos, x))

        dist = haversine_distance(current_pos, closest)

        total_dist += dist
        route.append(closest)

        current_pos = (closest.lat, closest.lng)

        unvisited.remove(closest)

    total_dist += haversine_distance(current_pos, depot)

    return route, round(total_dist, 2)


# ==============================
# BRUTE FORCE
# ==============================
def solve_bruteforce(orders):
    if not orders:
        return [], 0

    depot = (10.802, 106.713)

    best_route = None
    best_dist = float('inf')

    for perm in itertools.permutations(orders):
        dist = 0
        current = depot

        for order in perm:
            dist += haversine_distance(current, order)
            current = (order.lat, order.lng)

        dist += haversine_distance(current, depot)

        if dist < best_dist:
            best_dist = dist
            best_route = perm

    return list(best_route), round(best_dist, 2)


# ==============================
# BITMASK DP
# ==============================
def solve_bitmask(orders):
    if not orders:
        return [], 0

    depot = (10.802, 106.713)

    points = [depot] + [(o.lat, o.lng) for o in orders]

    n = len(points)

    dist = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            dist[i][j] = haversine_distance(points[i], points[j])

    dp = [[float('inf')] * n for _ in range(1 << n)]

    parent = [[-1] * n for _ in range(1 << n)]

    dp[1][0] = 0

    for mask in range(1 << n):
        for u in range(n):
            if not (mask & (1 << u)):
                continue

            for v in range(n):
                if mask & (1 << v):
                    continue

                new_mask = mask | (1 << v)

                new_cost = dp[mask][u] + dist[u][v]

                if new_cost < dp[new_mask][v]:
                    dp[new_mask][v] = new_cost
                    parent[new_mask][v] = u

    full_mask = (1 << n) - 1

    best_cost = float('inf')
    last = -1

    for i in range(1, n):
        cost = dp[full_mask][i] + dist[i][0]

        if cost < best_cost:
            best_cost = cost
            last = i

    path = []

    mask = full_mask

    while last != -1:
        path.append(last)

        temp = parent[mask][last]

        mask ^= (1 << last)

        last = temp

    path.reverse()

    route = [orders[i - 1] for i in path if i != 0]

    return route, round(best_cost, 2)