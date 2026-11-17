import copy
import random

def get_grid_from_user():
    print("Enter Grid Configuration: ")
    num_rows = int(input("Enter number of rows (e.g., 10): ").strip())
    num_cols = int(input("Enter number of columns (e.g., 10): ").strip())
    print(f"Enter the {num_rows} rows, each with {num_cols} space-separated characters (S, C, D, X):")

    grid = []
    for i in range(num_rows):
        while True:
            row = input(f"Row {i+1}: ").strip().upper().split()
            if len(row) != num_cols:
                print(f"  Row must have exactly {num_cols} cells, try again.")
            elif any(cell not in ('S', 'C', 'D', 'X') for cell in row):
                print("  Only S, C, D, X are allowed, try again.")
            else:
                break
        grid.append(row)
    return grid

def get_start_and_reachable_dirty(grid):
    start = None
    rows, cols = len(grid), len(grid[0])
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 'S':
                start = (r, c)
    
    if not start:
        raise ValueError("Starting position 'S' not found in grid!")

    # BFS to identify reachable dirty cells
    queue = [start]
    visited = {start}
    reachable_dirty = 0
    directions = [(-1,0), (1,0), (0,-1), (0,1)]
    
    while queue:
        r, c = queue.pop(0)
        if grid[r][c] == 'D':
            reachable_dirty += 1
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != 'X' and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append((nr, nc))
                
    return start, reachable_dirty

def get_valid_neighbors(grid, r, c):
    neighbors = []
    directions = [(-1,0), (1,0), (0,-1), (0,1)]  # Up, Down, Left, Right
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] != 'X':
            neighbors.append((nr, nc))
    return neighbors

def run_simple_reflex_agent(initial_grid):
    grid = copy.deepcopy(initial_grid)
    start, total_dirty = get_start_and_reachable_dirty(grid)
    
    pos = start
    cleaned = 0
    movements = 0
    actions = 0
    visit_counts = {}
    repeated_visits = 0
    
    random.seed(42)  # For reproducible random moves
    max_steps = 10000  # Safety limit for random walk
    
    while cleaned < total_dirty and actions < max_steps:
        r, c = pos
        visit_counts[(r, c)] = visit_counts.get((r, c), 0) + 1
        
        # Current percept check
        if grid[r][c] == 'D':
            grid[r][c] = 'C'
            cleaned += 1
            actions += 1
        else:
            # Memoryless move to a random valid neighbor
            neighbors = get_valid_neighbors(grid, r, c)
            if not neighbors:
                break
            pos = random.choice(neighbors)
            movements += 1
            actions += 1
            
            if visit_counts.get(pos, 0) > 0:
                repeated_visits += 1

    print("\n--- Simple Reflex Agent ---")
    print(f"Dirty cells cleaned: {cleaned}/{total_dirty}")
    print(f"Movements: {movements}")
    print(f"Total actions: {actions}")
    print(f"Repeated visits: {repeated_visits}")

def run_model_based_agent(initial_grid):
    grid = copy.deepcopy(initial_grid)
    start, total_dirty = get_start_and_reachable_dirty(grid)
    
    pos = start
    cleaned = 0
    movements = 0
    actions = 0
    repeated_visits = 0
    
    visited = {pos}
    stack = []
    
    while cleaned < total_dirty:
        r, c = pos
        
        if grid[r][c] == 'D':
            grid[r][c] = 'C'
            cleaned += 1
            actions += 1
            if cleaned == total_dirty:
                break
                
        neighbors = get_valid_neighbors(grid, r, c)
        unvisited = [n for n in neighbors if n not in visited]
        
        if unvisited:
            stack.append(pos)
            pos = unvisited[0]
            visited.add(pos)
            movements += 1
            actions += 1
        else:
            if stack:
                pos = stack.pop()
                movements += 1
                actions += 1
                repeated_visits += 1
            else:
                break  # Fully explored

    print("\n--- Model-Based Reflex Agent ---")
    print(f"Dirty cells cleaned: {cleaned}/{total_dirty}")
    print(f"Movements: {movements}")
    print(f"Total actions: {actions}")
    print(f"Repeated visits: {repeated_visits}")

if __name__ == "__main__":
    user_grid = get_grid_from_user()
    run_simple_reflex_agent(user_grid)
    run_model_based_agent(user_grid)