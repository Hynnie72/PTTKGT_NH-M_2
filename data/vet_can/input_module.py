# =========================
# MODEL
# =========================
class Node:
    def __init__(self, node_id, x, y, earliest, latest, service_time):
        self.id = node_id
        self.x = x
        self.y = y
        self.earliest = earliest
        self.latest = latest
        self.service_time = service_time

    def __repr__(self):
        return f"Node({self.id}, x={self.x}, y={self.y}, TW=[{self.earliest},{self.latest}], service={self.service_time})"


# =========================
# INPUT MODULE
# =========================
def read_input(filename):
    nodes = []
    
    try:
        with open(filename, "r") as file:
            n = int(file.readline().strip())

            for i in range(n):
                x, y, e, l, s = file.readline().split()
                node = Node(i, float(x), float(y), float(e), float(l), float(s))
                nodes.append(node)

    except FileNotFoundError:
        print("❌ Không tìm thấy file")
    except Exception as e:
        print("❌ Lỗi:", e)

    return nodes

