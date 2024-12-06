import unittest
import networkx as nx
from algorithms.aStar_custom import astar_pathfinding, heuristic_distance

class TestAstarAlgorithm(unittest.TestCase):
    
    def setUp(self):
        """
        Set up a simple graph for testing.
        """
        # Create a simple test graph
        self.graph = nx.DiGraph()
        self.graph.add_node(1, x=0, y=0)  # Start node
        self.graph.add_node(2, x=0, y=1)
        self.graph.add_node(3, x=1, y=1)
        self.graph.add_node(4, x=1, y=0)  # Goal node

        # Add weighted edges
        self.graph.add_edge(1, 2, weight=1)
        self.graph.add_edge(2, 3, weight=1)
        self.graph.add_edge(3, 4, weight=1)
        self.graph.add_edge(1, 4, weight=10)  # Direct but expensive route

        
    def test_astar_pathfinding(self):
        '''
        
        Test the A* algorithm for a valid shortest path
        
        '''
        path = astar_pathfinding(self.graph, start_node = 1, goal_node=4)        
        # Expected shortest path
        expected_path = [1,4]
        
        
        self.assertEqual(path,expected_path,"A* failed to find the shortest path")
        
    def test_heuristic_distance(self):
        '''
        
        Test the heuristic function for accuracy
        
        '''
        distance = heuristic_distance(self.graph, 1 ,4)
        expected_dsitance = 111319 # Approx straight-line distance in metres
        self.assertAlmostEqual(distance,expected_dsitance, delta = 150 , msg="Heuristic Distance is incorrect")
        
    
    def test_no_path(self):
        '''
        Test the behavior when there is no path between nodes.
        '''
        # Remove all edges
        self.graph.remove_edges_from(list(self.graph.edges))
        
        # Run A* pathfinding
        path = astar_pathfinding(self.graph, start_node=1, goal_node=4)
        
        self.assertIsNone(path, "A* did not return None for an unreachable goal.")

if __name__ == "__main__":
    unittest.main()