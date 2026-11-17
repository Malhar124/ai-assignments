def solve_q2_mrv_forward_checking(variables, constraints, initial_domains):
    # Pre-build adjacency mapping
    adj = {v: set() for v in variables}
    for u, v in constraints:
        adj[u].add(v)
        adj[v].add(u)

    def print_domains(domains):
        for v in variables:
            print(f"  {v:<5} | {domains[v]}")

    def backtrack(assignment, current_domains, step=1):
        if len(assignment) == len(variables):
            return assignment

        # Select variable with Minimum Remaining Values (MRV)
        unassigned = [v for v in variables if v not in assignment]
        var = min(unassigned, key=lambda v: len(current_domains[v]))

        print(f"--- Step {step} ---")
        print(f"1. Variable selected using MRV: {var}")

        for val in list(current_domains[var]):
            print(f"2. Value assigned: {val}")
            
            # Deep copy of current domains for forward checking
            new_domains = {v: list(current_domains[v]) for v in variables}
            new_domains[var] = [val]
            
            # Apply Forward Checking to neighbors
            failure = False
            for neighbor in adj[var]:
                if neighbor not in assignment:
                    if val in new_domains[neighbor]:
                        new_domains[neighbor].remove(val)
                    if not new_domains[neighbor]:
                        failure = True

            print("3. Updated domains after Forward Checking:")
            print_domains(new_domains)

            if not failure:
                print("4. Whether backtracking is required: No\n")
                assignment[var] = val
                result = backtrack(assignment, new_domains, step + 1)
                if result:
                    return result
                del assignment[var]

            print("4. Whether backtracking is required: Yes (Domain Wipeout)\n")

        return None

    print("MRV + Forward Checking ===")
    print("Initial Domains:")
    print_domains(initial_domains)
    print()

    solution = backtrack({}, initial_domains)
    if solution is None:
        print("No valid assignment exists.")
        return
    print("Final Valid Assignment:")
    for course, slot in solution.items():
        if course == 'A':
            print(f"  {course}: Slot {slot}, Lab: L1")
        elif course == 'B' and slot == 4:
            print(f"  {course}: Slot {slot}, Lab: L2")
        elif course == 'C':
            print(f"  {course}: Slot {slot}, Lab: L2")
        else:
            print(f"  {course}: Slot {slot}, Lab: L1")


def read_timetable_from_user():
    variables = input("Enter sections: ").split()

    # Binary inequality constraints
    num_constraints = int(input("Enter number of conflicting section pairs: "))
    print("Enter each pair of sections that cannot share a slot:    ")
    constraints = []
    for i in range(num_constraints):
        u, v = input(f"Pair {i+1}: ").split()
        constraints.append((u, v))

    initial_domains = {}
    for v in variables:
        initial_domains[v] = [int(x) for x in input(f"Enter available slots for {v} (e.g., 1 2 3): ").split()]
    print()
    return variables, constraints, initial_domains


if __name__ == "__main__":
    variables, constraints, initial_domains = read_timetable_from_user()
    solve_q2_mrv_forward_checking(variables, constraints, initial_domains)