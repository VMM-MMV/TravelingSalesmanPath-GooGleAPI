from typing import List, Tuple
import numpy as np
import requests

def solve_tsp(distances: np.ndarray) -> Tuple[int, List[int]]:
    n = distances.shape[0]
    path = np.zeros(n, dtype=int)
    best_path = np.arange(n)
    best_weight = np.inf
    
    def tsp_recursive(mask: np.ndarray, curr_weight: int, level: int) -> int:
        nonlocal best_weight
        
        if curr_weight >= best_weight:
            return curr_weight
        
        if level == n:
            if curr_weight + distances[path[-1]][path[0]] < best_weight:
                best_weight = curr_weight + distances[path[-1]][path[0]]
                best_path[:] = path[:]
            return curr_weight
        
        for i in range(n):
            if not mask[i]:
                mask_next = np.copy(mask)
                mask_next[i] = True
                path[level] = i
                tsp_recursive(mask_next, curr_weight + distances[path[level-1]][i], level+1)
    
    tsp_recursive(np.zeros(n, dtype=bool), 0, 0)
    
    return best_weight, list(best_path)

nodes = ["str.Studentilor 9","Strada 31 August 1989 161, Chișinău 2004","Strada Calea Orheiului 36, Chișinău", "str.Igor vieru 14", "malldova", "gara feroviara", "colonita", "aeroport Chisinau"]

list_nodes = []

been_there = []
times = []

for i in range(len(nodes)):
    temp = []
    for j in range(len(nodes)):
        if (nodes[i] != nodes[j]) and ({nodes[i],nodes[j]} not in been_there):
            been_there.append({nodes[i],nodes[j]})
            url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={nodes[i]}&destinations={nodes[j]}&departure_time=now&units=metric&key=key_here"

            response = requests.request("GET", url, headers={}, data={})
            print(nodes[i],nodes[j])
            print(response.json())

            #distance = response.json()["rows"][0]["elements"][0]["distance"]["text"]
            duration = response.json()["rows"][0]["elements"][0]["duration_in_traffic"]["text"]

            temp.append(int(duration.replace(" min", "").replace("s","")))
            times.append(int(duration.replace(" min", "").replace("s","")))
        elif nodes[i] == nodes[j]:
            temp.append(0)
        elif {nodes[i],nodes[j]} in been_there:
            temp.append(times[been_there.index({nodes[i],nodes[j]})])

    list_nodes.append(temp)


distances = np.array(list_nodes)

# Solve the TSP problem using the branch and bound algorithm
min_weight, best_path = solve_tsp(distances)

#print("Minimum weight:", min_weight)
print("Best path:", best_path)

for i in best_path:
    print(nodes[i])

