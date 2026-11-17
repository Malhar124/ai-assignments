import math
import random

# Location coordinates (filled from user input)
LOCATIONS = {}

DELIVERY_NODES = []

def read_locations():
    """Reads warehouse and delivery point coordinates from the user."""
    wx, wy = map(float, input("Enter warehouse W coordinates (x y): ").split())
    LOCATIONS['W'] = (wx, wy)

    num_points = int(input("Enter number of delivery points (at least 2): "))
    print("Enter each delivery point as: name x y (e.g., A 2 6)")
    for i in range(num_points):
        name, x, y = input(f"Point {i+1}: ").split()
        LOCATIONS[name] = (float(x), float(y))
        DELIVERY_NODES.append(name)

def calculate_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def total_route_cost(route):
    full_route = ['W'] + route + ['W']
    cost = 0.0
    for i in range(len(full_route) - 1):
        cost += calculate_distance(LOCATIONS[full_route[i]], LOCATIONS[full_route[i+1]])
    return cost

def hill_climbing_silent(initial_route):
    current_route = list(initial_route)
    current_cost = total_route_cost(current_route)
    iterations = 0
    
    while True:
        iterations += 1
        best_neighbour = None
        best_neighbour_cost = float('inf')
        
        n = len(current_route)
        for i in range(n):
            for j in range(i + 1, n):
                neighbour = list(current_route)
                neighbour[i], neighbour[j] = neighbour[j], neighbour[i]
                cost = total_route_cost(neighbour)
                
                if cost < best_neighbour_cost:
                    best_neighbour_cost = cost
                    best_neighbour = neighbour
        
        if best_neighbour_cost < current_cost:
            current_route = best_neighbour
            current_cost = best_neighbour_cost
        else:
            break

    return current_cost, iterations

def simulated_annealing_silent(initial_route, T_init=100.0, alpha=0.95, T_min=0.1):
    current_route = list(initial_route)
    current_cost = total_route_cost(current_route)
    best_cost = current_cost
    
    T = T_init
    iterations = 0

    while T >= T_min:
        iterations += 1
        
        i, j = random.sample(range(len(current_route)), 2)
        neighbour = list(current_route)
        neighbour[i], neighbour[j] = neighbour[j], neighbour[i]
        neighbour_cost = total_route_cost(neighbour)
        
        delta_E = neighbour_cost - current_cost
        
        if delta_E < 0 or random.random() < math.exp(-delta_E / T):
            current_route = neighbour
            current_cost = neighbour_cost
            if current_cost < best_cost:
                best_cost = current_cost

        T *= alpha

    return best_cost, iterations

def run_iterations(num_runs=5, T_init=100.0, alpha=0.95, T_min=0.1):
    hc_costs, sa_costs = [], []
    hc_iters, sa_iters = [], []

    print("=" * 65)
    print(f"{'Run':<5} | {'HC Cost':<12} | {'SA Cost':<12} | {'HC Iterations':<13} | {'SA Iterations':<13}")
    print("=" * 65)

    for run in range(1, num_runs + 1):
        init_route = list(DELIVERY_NODES)
        random.shuffle(init_route)
        
        hc_cost, hc_it = hill_climbing_silent(init_route)
        sa_cost, sa_it = simulated_annealing_silent(init_route, T_init, alpha, T_min)
        
        hc_costs.append(hc_cost)
        sa_costs.append(sa_cost)
        hc_iters.append(hc_it)
        sa_iters.append(sa_it)
        
        print(f"{run:<5} | {hc_cost:<12.4f} | {sa_cost:<12.4f} | {hc_it:<13} | {sa_it:<13}")

    print("-" * 65)
    
    # Statistical outputs
    print("\nOVERALL METRICS:")
    print(f"HC -> Best Cost: {min(hc_costs):.4f} | Worst Cost: {max(hc_costs):.4f} | Avg Cost: {sum(hc_costs)/num_runs:.4f} | Avg Iters: {sum(hc_iters)/num_runs:.1f}")
    print(f"SA -> Best Cost: {min(sa_costs):.4f} | Worst Cost: {max(sa_costs):.4f} | Avg Cost: {sum(sa_costs)/num_runs:.4f} | Avg Iters: {sum(sa_iters)/num_runs:.1f}")

if __name__ == "__main__":
    read_locations()
    num_runs = int(input("Enter number of runs (e.g., 5): "))
    T_init = float(input("Enter initial temperature (e.g., 100): "))
    alpha = float(input("Enter cooling rate alpha (0 < alpha < 1, e.g., 0.95): "))
    T_min = float(input("Enter minimum temperature (e.g., 0.1): "))
    run_iterations(num_runs, T_init, alpha, T_min)