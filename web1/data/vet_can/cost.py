# =========================
# MODULE: COST 
# =========================
names = ["Kho", "Quận 1", "Quận 3", "Quận 4", "Quận 5", "Quận 6", "Quận 8", "Quận 10"]

def calculate_cost(path, dist_matrix):
    if not path:
        return 0

    total_cost = 0
    prev = 0  # bắt đầu từ kho

    print("Chi tiết tuyến đường:")

    # đi qua từng điểm
    for node in path:
        cost = dist_matrix[prev][node]
        print(f"{names[prev]} → {names[node]} = {cost:.2f}")

        total_cost += cost
        prev = node

    # quay về kho
    cost = dist_matrix[prev][0]
    print(f"{names[prev]} → {names[0]} = {cost:.2f}")

    total_cost += cost

    print(f"Tổng quãng đường: {total_cost:.2f}")

    return total_cost