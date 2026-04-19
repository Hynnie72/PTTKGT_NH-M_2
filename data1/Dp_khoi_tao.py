import sys
import io

INF = sys.maxsize   # Giá trị vô cùng lớn

def init_data():


    n = int(input().strip())                    # Số địa điểm (n <= 20)
    
    # Đọc ma trận khoảng cách dist[n][n]
    dist = []
    for _ in range(n):
        row = list(map(int, input().strip().split()))
        dist.append(row)
    
    # Tạo bảng DP: dp[1<<n][n]
    dp = [[INF] * n for _ in range(1 << n)]
    
    # Khởi tạo trạng thái ban đầu
    dp[1 << 0][0] = 0
    
    return n, dist, dp
