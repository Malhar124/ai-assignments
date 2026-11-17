from collections import deque
import heapq


# =========================================================
# 8-PUZZLE
# =========================================================

# 0 represents the empty cell (#)

N = int(input("Enter puzzle size N (e.g., 3 for 8-puzzle): "))


def read_state(name):

    print(f"Enter the {name} configuration "
          f"({N} rows, {N} space-separated numbers each, 0 = empty):")

    while True:

        state = []

        for i in range(N):

            while True:

                row = input(f"Row {i + 1}: ").split()

                if len(row) == N and all(x.isdigit() for x in row):
                    state.extend(int(x) for x in row)
                    break

                print(f"  Enter exactly {N} numbers, try again.")

        if sorted(state) == list(range(N * N)):
            return tuple(state)

        print(f"  Configuration must contain each number from "
              f"0 to {N * N - 1} exactly once, re-enter.")


initial = read_state("initial")

goal = read_state("goal")


# Parity invariant: inversions (+ blank row when N is even).
# Goal is reachable only if initial and goal have the same parity.

def parity(state):

    tiles = [x for x in state if x != 0]

    inversions = sum(
        1
        for i in range(len(tiles))
        for j in range(i + 1, len(tiles))
        if tiles[i] > tiles[j]
    )

    if N % 2 == 0:
        inversions += state.index(0) // N

    return inversions % 2


if parity(initial) != parity(goal):
    print("\nGoal configuration is not reachable from the initial configuration.")
    raise SystemExit


# =========================================================
# PRINT PUZZLE
# =========================================================

def print_puzzle(state):

    for i in range(0, N * N, N):

        row = state[i:i + N]

        print(
            " ".join(
                "#" if x == 0 else str(x)
                for x in row
            )
        )

    print()


# =========================================================
# GENERATE NEIGHBOURS
# =========================================================

def get_neighbours(state):

    neighbours = []

    empty = state.index(0)

    row = empty // N
    col = empty % N

    # Possible movements of empty cell
    moves = [
        (-1, 0, "Up"),
        (1, 0, "Down"),
        (0, -1, "Left"),
        (0, 1, "Right")
    ]

    for dr, dc, move in moves:

        new_row = row + dr
        new_col = col + dc

        # Check whether new position is inside puzzle
        if 0 <= new_row < N and 0 <= new_col < N:

            new_position = new_row * N + new_col

            new_state = list(state)

            # Swap empty cell with tile
            new_state[empty], new_state[new_position] = \
                new_state[new_position], new_state[empty]

            neighbours.append(
                (tuple(new_state), move)
            )

    return neighbours


# =========================================================
# RECONSTRUCT PATH
# =========================================================

def reconstruct_path(parent, move_taken, goal):

    path = []

    current = goal

    while current is not None:

        path.append(
            (current, move_taken[current])
        )

        current = parent[current]

    path.reverse()

    return path


# =========================================================
# BFS
# =========================================================

def bfs(start, goal):

    queue = deque([start])

    visited = {start}

    parent = {start: None}
    move_taken = {start: "Start"}

    while queue:

        current = queue.popleft()

        if current == goal:

            return reconstruct_path(
                parent,
                move_taken,
                goal
            )

        for neighbour, move in get_neighbours(current):

            if neighbour not in visited:

                visited.add(neighbour)

                parent[neighbour] = current
                move_taken[neighbour] = move

                queue.append(neighbour)

    return None


# =========================================================
# DFS
# =========================================================

def dfs(start, goal):

    stack = [start]

    visited = {start}

    parent = {start: None}
    move_taken = {start: "Start"}

    while stack:

        current = stack.pop()

        if current == goal:

            return reconstruct_path(
                parent,
                move_taken,
                goal
            )

        for neighbour, move in reversed(
            get_neighbours(current)
        ):

            if neighbour not in visited:

                visited.add(neighbour)

                parent[neighbour] = current
                move_taken[neighbour] = move

                stack.append(neighbour)

    return None


# =========================================================
# A* HEURISTIC
# =========================================================

# h(n) = number of mismatched cells
#
# The empty cell (#) is not counted.


def heuristic(state, goal):

    count = 0

    for i in range(N * N):

        if state[i] != 0 and state[i] != goal[i]:

            count += 1

    return count


# =========================================================
# A*
# =========================================================

def a_star(start, goal):

    # g(n) = level of the node
    g = {start: 0}

    parent = {start: None}
    move_taken = {start: "Start"}

    # f(n) = g(n) + h(n)
    h = heuristic(start, goal)

    priority_queue = [
        (g[start] + h, g[start], start)
    ]

    visited = set()

    while priority_queue:

        f_current, current_g, current = \
            heapq.heappop(priority_queue)

        if current in visited:
            continue

        visited.add(current)

        if current == goal:

            return reconstruct_path(
                parent,
                move_taken,
                goal
            )

        for neighbour, move in get_neighbours(current):

            new_g = g[current] + 1

            if neighbour not in g or new_g < g[neighbour]:

                g[neighbour] = new_g

                parent[neighbour] = current
                move_taken[neighbour] = move

                h = heuristic(
                    neighbour,
                    goal
                )

                f = new_g + h

                heapq.heappush(
                    priority_queue,
                    (f, new_g, neighbour)
                )

    return None


# =========================================================
# DISPLAY SOLUTION
# =========================================================

def display_solution(name, solution):

    print("\n")
    print("=" * 50)
    print(name)
    print("=" * 50)

    if solution is None:
        print("No solution found")
        return

    for step, (state, move) in enumerate(solution):

        print("Step:", step)
        print("Move:", move)

        print_puzzle(state)

    print("Total moves:", len(solution) - 1)


# =========================================================
# MAIN
# =========================================================

print("=" * 50)
print("QUESTION 2: 8-PUZZLE")
print("=" * 50)

print("\nInitial Configuration:")
print_puzzle(initial)

print("Goal Configuration:")
print_puzzle(goal)


# ---------------------------------------------------------
# BFS
# ---------------------------------------------------------

bfs_solution = bfs(initial, goal)

display_solution(
    "BFS",
    bfs_solution
)


# ---------------------------------------------------------
# DFS
# ---------------------------------------------------------

dfs_solution = dfs(initial, goal)

display_solution(
    "DFS",
    dfs_solution
)


# ---------------------------------------------------------
# A*
# ---------------------------------------------------------

astar_solution = a_star(initial, goal)

display_solution(
    "A*",
    astar_solution
)