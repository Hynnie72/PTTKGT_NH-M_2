import math

# đọc dữ liệu từ file
def read_data(filename):
    points = []

    f = open(filename, "r")
    n = int(f.readline())

    for i in range(n):
        line = f.readline().split()
        id = int(line[0])
        x = float(line[1])
        y = float(line[2])

        points.append((id, x, y))

    f.close()
    return points


# tính khoảng cách giữa 2 điểm
def calc_distance(a, b):
    x1 = a[1]
    y1 = a[2]

    x2 = b[1]
    y2 = b[2]

    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)


# tạo ma trận khoảng cách
def create_matrix(points):
    n = len(points)

    dist = []
    for i in range(n):
        row = []
        for j in range(n):
            d = calc_distance(points[i], points[j])
            row.append(d)
        dist.append(row)

    return dist