from collections import deque

def bidirectional_search(graph, source, goal):
    if source == goal:
        return [source], source, [source], [goal]
    
    fwd_queue = deque([(source, [source])])
    bwd_queue = deque([(goal, [goal])])
    
    fwd_visited = {source: [source]}
    bwd_visited = {goal: [goal]}
    
    meeting_point = None
    final_path = []
    
    while fwd_queue and bwd_queue:
        # Forward BFS Step
        curr_fwd, path_fwd = fwd_queue.popleft()
        for neighbor in graph.get(curr_fwd, []):
            if neighbor not in fwd_visited:
                new_path = path_fwd + [neighbor]
                fwd_visited[neighbor] = new_path
                fwd_queue.append((neighbor, new_path))
                
                if neighbor in bwd_visited:
                    meeting_point = neighbor
                    final_path = new_path + bwd_visited[neighbor][:-1][::-1]
                    break
        if meeting_point:
            break
            
        # Backward BFS Step
        curr_bwd, path_bwd = bwd_queue.popleft()
        for neighbor in graph.get(curr_bwd, []):
            if neighbor not in bwd_visited:
                new_path = path_bwd + [neighbor]
                bwd_visited[neighbor] = new_path
                bwd_queue.append((neighbor, new_path))
                
                if neighbor in fwd_visited:
                    meeting_point = neighbor
                    final_path = fwd_visited[neighbor] + new_path[:-1][::-1]
                    break
        if meeting_point:
            break
            
    return final_path, meeting_point, list(fwd_visited.keys()), list(bwd_visited.keys())

num_nodes = int(input("Enter number of nodes: "))
print("For each node, enter the node followed by its neighbours (e.g., B A D E):")
city_map = {}
for i in range(num_nodes):
    tokens = input(f"Node {i+1}: ").split()
    city_map[tokens[0]] = tokens[1:]

source = input("Enter source node: ").strip()
goal = input("Enter goal node: ").strip()

path, meeting_pt, visited_fwd, visited_bwd = bidirectional_search(city_map, source, goal)

if path:
    print("Path:", " → ".join(path))
else:
    print("Path: No path found")
print("Meeting point:", meeting_pt)
print("Nodes visited from source direction:", visited_fwd)
print("Nodes visited from goal direction:", visited_bwd)