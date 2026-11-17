from collections import deque

def water_jug_bfs():
    start_state = (0, 0)
    queue = deque([(start_state, [])])
    visited = {start_state}

    while queue:
        (j4, j3), path = queue.popleft()

        # Goal State: 2 Liters in the 4-liter jug
        if j4 == 2:
            return path + [(j4, j3)]
        ## Check all possible moves
        moves = [
            ((4, j3), "Fill 4L Jug"),                      # Fill 4L
            ((j4, 3), "Fill 3L Jug"),                      # Fill 3L
            ((0, j3), "Empty 4L Jug"),                     # Empty 4L
            ((j4, 0), "Empty 3L Jug"),                     # Empty 3L
            # Pour 3L -> 4L
            ((min(4, j4 + j3), j3 - (min(4, j4 + j3) - j4)), "Pour 3L -> 4L"),
            # Pour 4L -> 3L
            ((j4 - (min(3, j4 + j3) - j3), min(3, j4 + j3)), "Pour 4L -> 3L")
        ]
        ## Check for visited state
        for next_state, action in moves:
            if next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, path + [(j4, j3)]))

    return None

path = water_jug_bfs()
print("Steps to solve Water Jug Problem:")
for step_num, state in enumerate(path):
    print(f"Step {step_num}: 4L Jug = {state[0]}L, 3L Jug = {state[1]}L")