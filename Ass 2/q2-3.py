import heapq
import random

def get_delivery_grid_from_user():
    print("=== Enter Delivery Grid Configuration ===")
    num_rows = int(input("Enter number of rows (e.g., 10): ").strip())
    num_cols = int(input("Enter number of columns (e.g., 10): ").strip())
    print(f"Enter the {num_rows} rows, each with {num_cols} space-separated characters (S, P, G, R, X):")

    grid = []
    for i in range(num_rows):
        while True:
            row = input(f"Row {i+1}: ").strip().upper().split()
            if len(row) != num_cols:
                print(f"  Row must have exactly {num_cols} cells, try again.")
            elif any(cell not in ('S', 'P', 'G', 'R', 'X') for cell in row):
                print("  Only S, P, G, R, X are allowed, try again.")
            else:
                break
        grid.append(row)
    return grid

def find_locations(grid):
    start = pickup = goal = None
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == 'S': start = (r, c)
            elif grid[r][c] == 'P': pickup = (r, c)
            elif grid[r][c] == 'G': goal = (r, c)
            
    if not start or not pickup or not goal:
        raise ValueError("Grid must contain 'S' (Start), 'P' (Pickup), and 'G' (Goal)!")
    return start, pickup, goal

def get_neighbors(grid, r, c):
    neighbors = []
    for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] != 'X':
            neighbors.append((nr, nc))
    return neighbors

def bfs_shortest_path(grid, start, end):
    queue = [(start, [start])]
    visited = {start}
    
    while queue:
        curr, path = queue.pop(0)
        if curr == end:
            return path
            
        for nxt in get_neighbors(grid, curr[0], curr[1]):
            if nxt not in visited:
                visited.add(nxt)
                queue.append((nxt, path + [nxt]))
    return []

def generate_environment_costs(grid):
    random.seed(10)  # Reproducible random environmental characteristics
    costs = {}
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] != 'X':
                costs[(r, c)] = {
                    'distance': 1,
                    'energy': random.randint(1, 5),
                    'risk': random.randint(1, 5),
                    'traffic': random.randint(1, 5)
                }
    return costs

def calculate_utility(costs, cell, w1=0.4, w2=0.3, w3=0.2, w4=0.1):
    c = costs[cell]
    return (w1 * c['distance']) + (w2 * c['energy']) + (w3 * c['risk']) + (w4 * c['traffic'])

def uniform_cost_search(grid, cell_costs, start, end):
    pq = [(0, start, [start])]
    visited = {}
    
    while pq:
        curr_cost, curr_node, path = heapq.heappop(pq)
        
        if curr_node == end:
            return path, curr_cost
            
        if curr_node in visited and visited[curr_node] <= curr_cost:
            continue
            
        visited[curr_node] = curr_cost
        
        for nxt in get_neighbors(grid, curr_node[0], curr_node[1]):
            nxt_cost = curr_cost + calculate_utility(cell_costs, nxt)
            heapq.heappush(pq, (nxt_cost, nxt, path + [nxt]))
            
    return [], float('inf')

if __name__ == "__main__":
    grid = get_delivery_grid_from_user()
    start, pickup, destination = find_locations(grid)

    # Goal-Based Agent (BFS)
    path_to_p = bfs_shortest_path(grid, start, pickup)
    path_to_g = bfs_shortest_path(grid, pickup, destination)

    moves_p = len(path_to_p) - 1 if path_to_p else 0
    moves_g = len(path_to_g) - 1 if path_to_g else 0

    print("\n--- Goal-Based Agent ---")
    if path_to_p and path_to_g:
        print(f"Route to Package: {path_to_p[0]} -> ... -> {path_to_p[-1]}")
        print(f"Movements to Package: {moves_p}")
        print(f"Route to Destination: {path_to_g[0]} -> ... -> {path_to_g[-1]}")
        print(f"Movements to Destination: {moves_g}")
        print(f"Total Movements: {moves_p + moves_g}")
    else:
        print("No valid route found!")

    # Utility-Based Agent (Uniform Cost Search)
    cell_costs = generate_environment_costs(grid)
    util_path_p, cost_p = uniform_cost_search(grid, cell_costs, start, pickup)
    util_path_g, cost_g = uniform_cost_search(grid, cell_costs, pickup, destination)

    util_moves = (len(util_path_p) - 1) + (len(util_path_g) - 1)
    total_cost = cost_p + cost_g

    print("\n--- Utility-Based Agent ---")
    if util_path_p and util_path_g:
        print(f"Route to Package: {util_path_p[0]} -> ... -> {util_path_p[-1]}")
        print(f"Route to Destination: {util_path_g[0]} -> ... -> {util_path_g[-1]}")
        print(f"Total Movements: {util_moves}")
        print(f"Total Cost: {total_cost:.2f}")
    else:
        print("No valid route found!")