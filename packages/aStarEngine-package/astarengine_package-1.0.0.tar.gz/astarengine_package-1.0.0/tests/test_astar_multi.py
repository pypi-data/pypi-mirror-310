import unittest
import networkx as nx
from algorithms.aStar_multi import astar_pathfind_multi_stop


class TestAStarMultiStop(unittest.TestCase):

    def setUp(self):
        """
        Set up a graph with multiple paths and weights for a challenging test case.
        """
        # Create a directed graph
        self.graph = nx.DiGraph()

        # Add nodes with coordinates (for heuristic calculation)
        for i in range(1, 9):  # Nodes 1 through 8
            self.graph.add_node(i, x=i, y=i % 2)  # Zigzag positions

        # Add weighted edges
        self.graph.add_edge(1, 2, weight=5)   # Long route
        self.graph.add_edge(1, 3, weight=2)   # Shorter route
        self.graph.add_edge(2, 4, weight=2)
        self.graph.add_edge(3, 4, weight=4)   # Detour
        self.graph.add_edge(4, 5, weight=1)
        self.graph.add_edge(5, 6, weight=3)
        self.graph.add_edge(6, 7, weight=2)
        self.graph.add_edge(5, 8, weight=5)   # Alternate route to the goal
        self.graph.add_edge(8, 7, weight=1)   # Short cut to the goal

    def test_tricky_multi_stop_route(self):
        """
        Test a multi-stop route with complex paths and weights.
        """
        # Define the route: start, 3 stops, and the goal
        route = [1, 3, 5, 8, 7]

        # Run the multi-stop pathfinding
        result = astar_pathfind_multi_stop(self.graph, route)

        # Expected path considering weights
        # Path segments:
        # 1 → 3 (weight=2), 3 → 5 (via 4, weight=4+1=5), 5 → 8 (weight=5), 8 → 7 (weight=1)
        expected = [1, 3, 4, 5, 8, 7]

        self.assertEqual(result, expected, "Failed to find the correct multi-stop path in a tricky graph.")

    def test_tricky_no_path(self):
        """
        Test when no valid path exists for a tricky route.
        """
        # Remove the edge between stop 8 and goal
        self.graph.remove_edge(8, 7)

        # Define the route: start, 3 stops, and the goal
        route = [1, 3, 5, 8, 7]

        # Run the multi-stop pathfinding
        result = astar_pathfind_multi_stop(self.graph, route)

        self.assertIsNone(result, "Should return None when no path exists in a tricky graph.")

if __name__ == "__main__":
    unittest.main()
