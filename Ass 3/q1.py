def get_blank_pos(state):
    n = len(state)
    for r in range(n):
        for c in range(n):
            if state[r][c] == 0:
                return r, c

def get_neighbors(state):
    n = len(state)
    r, c = get_blank_pos(state)
    moves = [('Up', -1, 0), ('Down', 1, 0), ('Left', 0, -1), ('Right', 0, 1)]
    neighbors = []
    
    for move_name, dr, dc in moves:
        nr, nc = r + dr, c + dc
        if 0 <= nr < n and 0 <= nc < n:
            new_state = [list(row) for row in state]
            new_state[r][c], new_state[nr][nc] = new_state[nr][nc], new_state[r][c]
            neighbors.append((move_name, tuple(tuple(row) for row in new_state)))
            
    return neighbors

def dls_8_puzzle(start_state, goal_state, max_depth):
    start_tuple = tuple(tuple(row) for row in start_state)
    goal_tuple = tuple(tuple(row) for row in goal_state)
    
    nodes_generated = 1
    visited = set()

    def recursive_dls(current_state, path, depth):
        nonlocal nodes_generated
        if current_state == goal_tuple:
            return path
        if depth == max_depth:
            return None
        
        visited.add((current_state, depth))
        
        for move, neighbor in get_neighbors(current_state):
            nodes_generated += 1
            if (neighbor, depth + 1) not in visited:
                result = recursive_dls(neighbor, path + [move], depth + 1)
                if result is not None:
                    return result
        return None

    solution_path = recursive_dls(start_tuple, [], 0)
    return solution_path, nodes_generated

def read_state(name, n):
    print(f"Enter the {name} state ({n} rows, {n} space-separated numbers each, 0 = blank):")
    while True:
        state = []
        for i in range(n):
            while True:
                row = input(f"Row {i+1}: ").split()
                if len(row) == n and all(x.isdigit() for x in row):
                    state.append([int(x) for x in row])
                    break
                print(f"  Enter exactly {n} numbers, try again.")
        if sorted(x for row in state for x in row) == list(range(n * n)):
            return state
        print(f"  State must contain each number from 0 to {n * n - 1} exactly once, re-enter.")

size = int(input("Enter puzzle size N: "))
starting_state = read_state("starting", size)
goal_state = read_state("goal", size)
depth_limit = int(input("Enter depth limit: "))

moves_seq, nodes_count = dls_8_puzzle(starting_state, goal_state, depth_limit)

print("Whether goal is found within depth limit:", "Yes" if moves_seq is not None else "No")
print("Sequence of moves:", moves_seq)
print("Total nodes generated:", nodes_count)