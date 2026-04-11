import itertools
import math
import time

# ==============================
# 1. DATA: TỌA ĐỘ THẬT (TP.HCM)
# ==============================
# 0: Kho hàng (Bình Thạnh)
# 1: Quận 1
# 2: Quận 3
# 3: Phú Nhuận

locations = [
    (10.800000, 106.700000),  # Kho (Bình Thạnh)
    (10.776889, 106.700806),  # Q1
    (10.782222, 106.695000),  # Q3
    (10.799000, 106.680000)   # Phú Nhuận
]

# ==============================
# 2. HÀM TÍNH KHOẢNG CÁCH
# ==============================
def distance(a, b):
    R = 6371  # km
    lat1, lon1 = a
    lat2, lon2 = b

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    x = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2

    return 2 * R * math.asin(math.sqrt(x))

# ==============================
# 3. TẠO MA TRẬN KHOẢNG CÁCH
# ==============================
n = len(locations)
dist = [[0]*n for _ in range(n)]

for i in range(n):
    for j in range(n):
        if i != j:
            dist[i][j] = round(distance(locations[i], locations[j]), 2)

# ==============================
# 4. HÀM TÍNH COST
# ==============================
def calculate_cost(path):
    cost = 0
    cost += dist[0][path[0]]

    for i in range(len(path)-1):
        cost += dist[path[i]][path[i+1]]

    cost += dist[path[-1]][0]
    return cost

# ==============================
# 5. THUẬT TOÁN VÉT CẠN
# ==============================
start = time.time()

points = list(range(1, n))
min_cost = float('inf')
best_path = []

print("Tat ca cac tuyen duong:")

for perm in itertools.permutations(points):
    cost = calculate_cost(perm)

    print("0 ->", " -> ".join(map(str, perm)), "-> 0 | Cost =", cost)

    if cost < min_cost:
        min_cost = cost
        best_path = perm

end = time.time()

# ==============================
# 6. KẾT QUẢ
# ==============================
print("\n===== TUYEN TOI UU =====")
print("Duong di: 0 ->", " -> ".join(map(str, best_path)), "-> 0")
print("Chi phi nho nhat:", round(min_cost, 2))
print("Thoi gian chay:", round(end - start, 5), "giay")

# ==============================
# 7. GHI FILE OUTPUT
# ==============================
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("Tat ca cac tuyen duong:\n")

    for perm in itertools.permutations(points):
        cost = calculate_cost(perm)
        f.write(f"0 -> {' -> '.join(map(str, perm))} -> 0 | Cost = {cost}\n")

    f.write("\n===== TUYEN TOI UU =====\n")
    f.write(f"Duong di: 0 -> {' -> '.join(map(str, best_path))} -> 0\n")
    f.write(f"Chi phi nho nhat: {round(min_cost,2)}\n")