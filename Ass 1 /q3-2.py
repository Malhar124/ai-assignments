from collections import deque

def find_nearest_parking(grid):
    rows = len(grid)
    cols = len(grid[0])
    
    # 1. Locate Entrance 'E'
    entrance = None
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 'E':
                entrance = (r, c)
                break
        if entrance:
            break
            
    if not entrance:
        return "Entrance 'E' not found in grid."

    # BFS Setup
    queue = deque([entrance])
    visited = {entrance}
    parent = {}

    # Movement vectors: Up, Down, Left, Right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    target = None

    # BFS Loop
    while queue:
        curr_r, curr_c = queue.popleft()


        if grid[curr_r][curr_c] == 'A':
            target = (curr_r, curr_c)
            break

        for dr, dc in directions:
            nr, nc = curr_r + dr, curr_c + dc


            if 0 <= nr < rows and 0 <= nc < cols:
                cell = grid[nr][nc]

                if cell in ('R', 'A') and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    parent[(nr, nc)] = (curr_r, curr_c)
                    queue.append((nr, nc))

    if not target:
        return "No available parking space reachable."

    # 4. Reconstruct Path
    path = []
    curr = target
    while curr != entrance:
        path.append(curr)
        curr = parent[curr]
    path.append(entrance)
    path.reverse()

    movements = len(path) - 1

    # 5. Format Output
    route_str = " -> ".join([str(p) for p in path])
    print(f"Nearest available parking space: {target}")
    print(f"Number of movements required: {movements}")
    print(f"Route: {route_str}")


# Demonstration on a 10x10 Grid Example
if __name__ == "__main__":
    parking_grid = [
        ['E', 'R', 'R', 'X', 'A', 'X', 'X', 'R', 'R', 'R'],
        ['X', 'X', 'R', 'X', 'X', 'X', 'X', 'R', 'X', 'R'],
        ['A', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'X', 'R'],
        ['X', 'X', 'X', 'X', 'O', 'X', 'X', 'X', 'X', 'R'],
        ['R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R'],
        ['R', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['R', 'R', 'R', 'O', 'A', 'X', 'R', 'R', 'R', 'R'],
        ['X', 'X', 'R', 'X', 'X', 'X', 'R', 'X', 'X', 'R'],
        ['R', 'R', 'R', 'R', 'R', 'R', 'R', 'X', 'X', 'R'],
        ['A', 'X', 'X', 'O', 'R', 'A', 'R', 'R', 'R', 'A']
    ]

    find_nearest_parking(parking_grid)