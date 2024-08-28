import heapq

class Node:
    def __init__(self, name, x, y, safety_points):
        self.name = name
        self.x = x
        self.y = y
        self.safety_points = safety_points
        self.adjacent = {}

    def add_edge(self, neighbor, distance):
        self.adjacent[neighbor] = distance

    def __lt__(self, other):
        return self.name < other.name

def heuristic(node1, node2):
    return ((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2) ** 0.5

def a_star(start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            return reconstruct_path(came_from, current)

        for neighbor, distance in current.adjacent.items():
            tentative_g_score = g_score[current] + distance - neighbor.safety_points

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                if neighbor not in [i[1] for i in open_set]:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None

def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

if __name__ == "__main__":
    start = Node('Start', 0, 0, 0)
    nodeA = Node('A', 1, 2, 5)
    nodeB = Node('B', 2, 3, 10)
    goal = Node('Goal', 4, 4, 15)

    start.add_edge(nodeA, 2)
    start.add_edge(nodeB, 5)
    nodeA.add_edge(nodeB, 1)
    nodeA.add_edge(goal, 3)
    nodeB.add_edge(goal, 1)

    path = a_star(start, goal)
    if path:
        print("Path found:")
        for node in path:
            print(node.name)
    else:
        print("No path found.")