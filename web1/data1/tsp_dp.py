# giải TSP bằng quy hoạch động (bitmask)
def tsp_dp(dist):
    n = len(dist)

    INF = 10**9

    # tạo bảng dp
    dp = []
    parent = []

    for i in range(1 << n):
        dp.append([INF]*n)
        parent.append([-1]*n)

    # bắt đầu từ điểm 0
    dp[1][0] = 0

    # duyệt tất cả trạng thái
    for mask in range(1 << n):
        for u in range(n):

            # nếu u chưa đi qua thì bỏ
            if (mask & (1 << u)) == 0:
                continue

            # thử đi tiếp đến v
            for v in range(n):

                # nếu v đã đi rồi thì bỏ
                if (mask & (1 << v)) != 0:
                    continue

                new_mask = mask | (1 << v)

                new_cost = dp[mask][u] + dist[u][v]

                # nếu tốt hơn thì cập nhật
                if new_cost < dp[new_mask][v]:
                    dp[new_mask][v] = new_cost
                    parent[new_mask][v] = u

    # tìm kết quả cuối
    full_mask = (1 << n) - 1

    best = INF
    last = -1

    for i in range(1, n):
        cost = dp[full_mask][i] + dist[i][0]
        if cost < best:
            best = cost
            last = i

    # =====================
    # truy vết đường đi
    # =====================
    path = []
    mask = full_mask

    while last != -1:
        path.append(last)
        temp = parent[mask][last]
        mask = mask ^ (1 << last)
        last = temp

    path.reverse()

    return best, path