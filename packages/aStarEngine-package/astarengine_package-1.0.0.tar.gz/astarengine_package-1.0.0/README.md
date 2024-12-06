# map_engine


map_engine is a Python package designed to calculate the shortest route between a start and end location, with support for up to 5 additional stops. It leverages the A* algorithm for efficient pathfinding and is ideal for applications requiring custom routing logic over a road network.

Features

Single-destination routing: Quickly calculate the shortest path between two locations.
Multi-stop routing: Add up to 5 additional stops to your route.
Flexible inputs: Provide locations as an ordered list of addresses or coordinates.
Modular design: Well-structured modules for algorithms, utilities, and visualizations.
Integration-ready: Easily integrate with frontend applications, providing optimized routes.

Use following code to start using the pkg 
```python

from aStarEngine_package.algorithms.aStar_multi import astar_pathfind_multi_stop

from aStarEngine_package.utils.routing import Routing 

# Load the road network
graph_path = "data/LA_road_network.graphml"
router = Routing(graph_path)

# Multi-stop route
locations = ["Venice Beach", "Staples Center", "Griffith Observatory"]
route = router.get_route(locations)
print("Multi-stop path:", route)


```