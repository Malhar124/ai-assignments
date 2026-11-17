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

def hill_climbing(initial_route):
    current_route = list(initial_route)
    current_cost = total_route_cost(current_route)
    iterations = 0
    
    print("--- HILL CLIMBING SEARCH ---")
    print(f"Initial Route: W -> {' -> '.join(current_route)} -> W | Cost: {current_cost:.4f}\n")
    
    while True:
        iterations += 1
        best_neighbour = None
        best_neighbour_cost = float('inf')
        
        # Generate all n*(n-1)/2 possible swap neighbours
        n = len(current_route)
        for i in range(n):
            for j in range(i + 1, n):
                neighbour = list(current_route)
                neighbour[i], neighbour[j] = neighbour[j], neighbour[i]
                cost = total_route_cost(neighbour)
                
                if cost < best_neighbour_cost:
                    best_neighbour_cost = cost
                    best_neighbour = neighbour
        
        # Move to neighbour if strictly better
        if best_neighbour_cost < current_cost:
            current_route = best_neighbour
            current_cost = best_neighbour_cost
            print(f"Iteration {iterations}: Best Route = W -> {' -> '.join(current_route)} -> W | Cost = {current_cost:.4f}")
        else:
            # Stop if no neighbouring solution gives an improvement
            break

    print(f"\nFinal Route: W -> {' -> '.join(current_route)} -> W")
    print(f"Final Route Cost: {current_cost:.4f}")
    print(f"Total Iterations: {iterations}")

if __name__ == "__main__":
    read_locations()

    # Random initial route
    initial_route = list(DELIVERY_NODES)
    random.shuffle(initial_route)
    
    hill_climbing(initial_route)