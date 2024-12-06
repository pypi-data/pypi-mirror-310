from typing import List , Any , Optional , Dict 
import heapq
from geopy.distance import geodesic
from .aStar_custom import astar_pathfinding

def astar_pathfind_multi_stop(
    graph: Any,
    route: List[Any]
)-> Optional[List[Any]]:
    '''
    
    Finds the shortest path for a route with multiple stops using the A* algorithm.

    Args:
        graph (networkx.Graph): A graph object representing the road network. 
                                Nodes must have 'x' (longitude) and 'y' (latitude) attributes.
        route (List[Any]): A list of nodes representing the route.
                           The first node is the start, the last is the goal, and 
                           the intermediate nodes are stops.

    Returns:
        List[Any]: A list of nodes representing the shortest path for the entire route.
                   Returns None if any segment of the route is unreachable.
    
    
    '''
    
    # Validate route input 
    
    if len(route) < 2 :
        raise ValueError("Route must include at least a start and a goal node ")
    
    #Combiine paths for each segment 
    complete_path = []
    
    for i in range(len(route)-1):
        start_node = route[i]
        goal_node = route[i+1]
        
        #Find shortest path for this segment --> Making use of the single stop astart function
        segment_path = astar_pathfinding(graph,start_node,goal_node)
        
        if segment_path is None :
            print(f"No path found between {start_node} and {goal_node}")
            return None 
        
        # Append segment path to complete path (avoid duplicating intermediate nodes)
        if i == 0:
            complete_path.extend(segment_path)
        else:
            complete_path.extend(segment_path[1:])
            
    return complete_path