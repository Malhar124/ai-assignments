def solve_q1_plain(variables, domains, neighbors):
    """Standard Backtracking Search without heuristics."""
    stats = {'assignments': 0, 'backtracks': 0}

    def is_valid(var, val, assignment):
        for neighbor in neighbors[var]:
            if neighbor in assignment and assignment[neighbor] == val:
                return False
        return True

    def backtrack(assignment):
        if len(assignment) == len(variables):
            return assignment
        
        # Fixed order selection
        unassigned = [v for v in variables if v not in assignment]
        var = unassigned[0]
        
        for val in domains[var]:
            stats['assignments'] += 1
            if is_valid(var, val, assignment):
                assignment[var] = val
                result = backtrack(assignment)
                if result:
                    return result
                del assignment[var]
                stats['backtracks'] += 1
        return None

    print("=== Question 1: Standard Backtracking ===")
    solution = backtrack({})
    print(f"Solution: {solution}")
    print(f"Total Assignments: {stats['assignments']}, Total Backtracks: {stats['backtracks']}\n")


def solve_q1_mrv(variables, domains, neighbors):
    """Backtracking Search using MRV Heuristic."""
    stats = {'assignments': 0, 'backtracks': 0}

    def is_valid(var, val, assignment):
        for neighbor in neighbors[var]:
            if neighbor in assignment and assignment[neighbor] == val:
                return False
        return True

    def get_remaining_values(var, assignment):
        return [val for val in domains[var] if is_valid(var, val, assignment)]

    def backtrack(assignment):
        if len(assignment) == len(variables):
            return assignment
        
        # Select unassigned variable with Minimum Remaining Values
        unassigned = [v for v in variables if v not in assignment]
        var = min(unassigned, key=lambda v: len(get_remaining_values(v, assignment)))
        
        for val in get_remaining_values(var, assignment):
            stats['assignments'] += 1
            assignment[var] = val
            result = backtrack(assignment)
            if result:
                return result
            del assignment[var]
            stats['backtracks'] += 1
        return None

    print("=== Question 1: MRV Backtracking ===")
    solution = backtrack({})
    print(f"Solution: {solution}")
    print(f"Total Assignments: {stats['assignments']}, Total Backtracks: {stats['backtracks']}\n")


def read_map_from_user():
    variables = input("Enter regions (space-separated, e.g., A B C D E): ").split()
    colors = input("Enter colours (space-separated, e.g., Red Green Blue): ").split()
    domains = {v: list(colors) for v in variables}
    neighbors = {v: [] for v in variables}

    num_edges = int(input("Enter number of adjacent region pairs: "))
    print("Enter each adjacent pair as: region1 region2 (e.g., A B)")
    for i in range(num_edges):
        u, v = input(f"Pair {i+1}: ").split()
        neighbors[u].append(v)
        neighbors[v].append(u)
    print()
    return variables, domains, neighbors


if __name__ == "__main__":
    variables, domains, neighbors = read_map_from_user()
    solve_q1_plain(variables, domains, neighbors)
    solve_q1_mrv(variables, domains, neighbors)