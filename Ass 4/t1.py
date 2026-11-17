import heapq


# ---------------------------------------------------------
# Graph
# ---------------------------------------------------------

nodes = input("Enter node names (space-separated, e.g., a b c d e f): ").split()
graph = {node: {} for node in nodes}

num_edges = int(input("Enter number of edges: "))
print("Enter each edge as: node1 node2 cost (e.g., a b 5)")
for i in range(num_edges):
    u, v, w = input(f"Edge {i+1}: ").split()
    graph[u][v] = int(w)
    graph[v][u] = int(w)


# Heuristic values h(n) for each node
heuristic = {}
for node in nodes:
    heuristic[node] = int(input(f"Enter heuristic value of {node}: "))

start_node = input("Enter start node: ").strip()
goal_node = input("Enter goal node: ").strip()


# ---------------------------------------------------------
# Dijkstra's Algorithm
# ---------------------------------------------------------

def dijkstra(graph, start, goal):

    distance = {node: float('inf') for node in graph}
    distance[start] = 0

    parent = {node: None for node in graph}

    priority_queue = [(0, start)]

    while priority_queue:

        current_distance, current = heapq.heappop(priority_queue)

        if current_distance > distance[current]:
            continue

        if current == goal:
            break

        for neighbour, weight in graph[current].items():

            new_distance = current_distance + weight

            if new_distance < distance[neighbour]:

                distance[neighbour] = new_distance
                parent[neighbour] = current

                heapq.heappush(
                    priority_queue,
                    (new_distance, neighbour)
                )

    # Construct path
    path = []
    current = goal

    while current is not None:
        path.append(current)
        current = parent[current]

    path.reverse()

    return path, distance[goal]


# ---------------------------------------------------------
# A* Algorithm
# ---------------------------------------------------------

def a_star(graph, heuristic, start, goal):

    # g(n) = actual cost from start
    g = {node: float('inf') for node in graph}
    g[start] = 0

    parent = {node: None for node in graph}

    # f(n) = g(n) + h(n)
    priority_queue = [
        (heuristic[start], start)
    ]

    while priority_queue:

        f_current, current = heapq.heappop(priority_queue)

        if current == goal:
            break

        for neighbour, weight in graph[current].items():

            new_g = g[current] + weight

            if new_g < g[neighbour]:

                g[neighbour] = new_g
                parent[neighbour] = current

                f = new_g + heuristic[neighbour]

                heapq.heappush(
                    priority_queue,
                    (f, neighbour)
                )

    # Construct path
    path = []
    current = goal

    while current is not None:
        path.append(current)
        current = parent[current]

    path.reverse()

    return path, g[goal]


# =========================================================
# MAIN
# =========================================================

print("=" * 50)
print("QUESTION 1")
print("=" * 50)


# ---------------- Dijkstra ----------------

path, cost = dijkstra(graph, start_node, goal_node)

print("\nDijkstra's Algorithm")
print("--------------------")
print("Path :", " -> ".join(path))
print("Cost :", cost)


# ---------------- A* ----------------

path, cost = a_star(
    graph,
    heuristic,
    start_node,
    goal_node
)

print("\nA* Algorithm")
print("------------")
print("Path :", " -> ".join(path))
print("Cost :", cost)