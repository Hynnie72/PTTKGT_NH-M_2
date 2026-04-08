import math

def create_distance_from_points(coords):
    n = len(coords)

    dist = [[0]*n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            x1, y1 = coords[i]
            x2, y2 = coords[j]

            dist[i][j] = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

    return dist