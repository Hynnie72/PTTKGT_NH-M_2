def solve_tsp(cost):
    n = len(cost)
    INF = 10**9

    dp = [[INF] * n for _ in range(1 << n)]
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
                new_cost = dp[mask][u] + cost[u][v]

                if new_cost < dp[new_mask][v]:
                    dp[new_mask][v] = new_cost
                    parent[new_mask][v] = u

    full_mask = (1 << n) - 1
    min_cost = INF
    last_city = -1

    for i in range(1, n):
        total_cost = dp[full_mask][i] + cost[i][0]
        if total_cost < min_cost:
            min_cost = total_cost
            last_city = i

    # truy vết đường đi
    path = []
    mask = full_mask
    city = last_city

    while city != -1:
        path.append(city)
        temp = parent[mask][city]
        mask ^= (1 << city)
        city = temp

  
    path.reverse()

    return min_cost, path