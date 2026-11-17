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
    """Calculates Euclidean distance between two points."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def total_route_cost(route):
    """Calculates total route distance starting and ending at Warehouse W."""
    full_route = ['W'] + route + ['W']
    cost = 0.0
    for i in range(len(full_route) - 1):
        cost += calculate_distance(LOCATIONS[full_route[i]], LOCATIONS[full_route[i+1]])
    return cost

def simulated_annealing(initial_route, T_init=100.0, alpha=0.95, T_min=0.1):
    current_route = list(initial_route)
    current_cost = total_route_cost(current_route)
    
    best_route = list(current_route)
    best_cost = current_cost
    
    T = T_init
    iterations = 0
    
    print("--- SIMULATED ANNEALING SEARCH ---")
    print(f"Initial Route: W -> {' -> '.join(current_route)} -> W | Cost: {current_cost:.4f}\n")

    while T >= T_min:
        iterations += 1
        
        # Randomly select two indices to swap
        i, j = random.sample(range(len(current_route)), 2)
        neighbour = list(current_route)
        neighbour[i], neighbour[j] = neighbour[j], neighbour[i]
        neighbour_cost = total_route_cost(neighbour)
        
        delta_E = neighbour_cost - current_cost
        accepted = False
        
        if delta_E < 0:
            accepted = True
        else:
            prob = math.exp(-delta_E / T)
            if random.random() < prob:
                accepted = True
                
        if accepted:
            current_route = neighbour
            current_cost = neighbour_cost
            if current_cost < best_cost:
                best_cost = current_cost
                best_route = list(current_route)

        status = "Accepted" if accepted else "Rejected"
        print(f"Iter {iterations:3d} | Temp: {T:6.2f} | Current Cost: {current_cost:.4f} | Status: {status}")

        # Cool down
        T *= alpha

    print(f"\nFinal Best Route: W -> {' -> '.join(best_route)} -> W")
    print(f"Final Best Cost: {best_cost:.4f}")
    print(f"Total Iterations: {iterations}")

if __name__ == "__main__":
    read_locations()
    T_init = float(input("Enter initial temperature (e.g., 100): "))
    alpha = float(input("Enter cooling rate alpha (0 < alpha < 1, e.g., 0.95): "))
    T_min = float(input("Enter minimum temperature (e.g., 0.1): "))

    # Random initial route
    initial_route = list(DELIVERY_NODES)
    random.shuffle(initial_route)
    
    simulated_annealing(initial_route, T_init, alpha, T_min)