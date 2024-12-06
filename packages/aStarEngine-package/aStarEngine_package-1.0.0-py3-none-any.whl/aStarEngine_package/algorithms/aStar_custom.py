import heapq
from geopy.distance import geodesic
from typing import Dict, List, Optional, Any

def astar_pathfinding(
    graph: Any,
    start_node: Any,
    goal_node: Any
) -> Optional[List[Any]]:
    """
    Finds the shortest path between two nodes in a graph using the A* algorithm.

    Args:
        graph (networkx.Graph): A graph object representing the road network. 
                                Nodes must have 'x' (longitude) and 'y' (latitude) attributes.
        start_node (Any): The starting node for the pathfinding.
        
        goal_node (Any): The target node for the pathfinding.

    Returns:
        List[Any]: A list of nodes representing the shortest path from start to goal.
                   Returns None if no path is found.
    """
    # Priority queue for nodes to be evaluated (open set)
    open_set = []
    heapq.heappush(open_set, (0, start_node))  # (f_score, node)

    # Maps to track scores
    g_score: Dict[Any, float] = {node: float('inf') for node in graph.nodes}
    g_score[start_node] = 0

    f_score: Dict[Any, float] = {node: float('inf') for node in graph.nodes}
    f_score[start_node] = heuristic_distance(graph, start_node, goal_node)

    # Parent mapping to reconstruct the path
    parent_map: Dict[Any, Any] = {}

    while open_set:
        # Get the node with the lowest f_score
        _, current_node = heapq.heappop(open_set)

        # If goal is reached, reconstruct and return the path
        if current_node == goal_node:
            return reconstruct_path(parent_map, current_node)

        # Explore neighbors of the current node
        for neighbor in graph.neighbors(current_node):
            # Calculate the tentative g_score
            tentative_g_score = g_score[current_node] + graph[current_node][neighbor].get('weight', 1)

            # If a better path is found
            if tentative_g_score < g_score[neighbor]:
                parent_map[neighbor] = current_node
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic_distance(graph, neighbor, goal_node)

                # Add the neighbor to the priority queue
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    # If no path is found
    return None


def heuristic_distance(graph: Any, node: Any, goal: Any) -> float:
    """
    Calculates the heuristic distance between two nodes using the Haversine formula.

    Args:
        graph (networkx.Graph): A graph object where nodes have 'x' (longitude) and 'y' (latitude) attributes.
        node (Any): The current node.
        goal (Any): The target node.

    Returns:
        float: The straight-line distance (in meters) between the current node and the goal.
    """
    node_coords = (graph.nodes[node]['y'], graph.nodes[node]['x'])
    goal_coords = (graph.nodes[goal]['y'], graph.nodes[goal]['x'])
    return geodesic(node_coords, goal_coords).meters


def reconstruct_path(parent_map: Dict[Any, Any], current_node: Any) -> List[Any]:
    """
    Reconstructs the shortest path from the parent mapping.

    Args:
        parent_map (Dict[Any, Any]): A mapping of each node to its parent node in the path.
        current_node (Any): The goal node from which to start the reconstruction.

    Returns:
        List[Any]: A list of nodes representing the shortest path, from start to goal.
    """
    path = [current_node]
    while current_node in parent_map:
        current_node = parent_map[current_node]
        path.append(current_node)
    return path[::-1]  # Reverse the path to get start to goal
