import unittest
from unittest.mock import patch, Mock, MagicMock
import networkx as nx
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from src.utils.routing import Routing
import osmnx as ox
import json


class TestRouting(unittest.TestCase):
    
    @classmethod
    def setUp(self) -> None:
        self.graph_path = "../data/LA_road_network.graphml"
        self.road_network = ox.load_graphml(self.graph_path)
        self.router = Routing(self.graph_path)

    
    @patch('requests.get')
    def test_get_coordinates(self,mock_get):
        # All that this function does is do a HTTP GET 
        #Take a base url and pass certain things to it 
        # But only takes the location as string 
        
        #What we need to check is 
        # Is the HTTP response going through ?
        # Is the data fine , does it match
        mock_response = Mock()
        exp_lat,exp_lon = '33.99518','-118.46849'
        
        response_dict = {"lat": "33.99518" , "lon":"-118.46849"}
        
        mock_response.json.return_value = [response_dict]
        
        mock_get.return_value.status_code = 200
        
        mock_get.return_value = mock_response
        
        lat,lon = self.router.get_coordinates('Venice Beach')
        self.assertEqual(lat,33.99518)
        self.assertEqual(lon,-118.46849)
        
        mock_get.assert_called_once_with(
            url="https://nominatim.openstreetmap.org/search",
            params={'q': "Venice Beach", 'format': 'json'},
            headers={'User-Agent': 'Map_Engine/1.0 (sathya05@vt.edu)'}
        )
        
    @patch("osmnx.distance.nearest_nodes")
    @patch("src.algorithms.astar_pathfind_multi_stop")
    @patch("src.utils.routing.Routing.get_coordinates")
    def test_get_route(self, mock_get_coordinates, mock_astar, mock_nearest_nodes):
        # Mock `get_coordinates` to return predefined coordinates
        mock_get_coordinates.side_effect = [
            (33.99518, -118.46849),  # Venice Beach
            (34.04302, -118.26728),  # Staples Center
            (34.13672, -118.29436),  # Griffith Observatory
        ]

        # Mock `nearest_nodes` to return predefined node IDs
        mock_nearest_nodes.side_effect = [1, 2, 3]  # Mock node IDs for the locations

        # Mock `astar_pathfind_multi_stop` to return a predefined route
        mock_astar.return_value = [1, 4, 5, 2, 6, 3]

        # Test routing function
        locations = ["Venice Beach", "Staples Center", "Griffith Observatory"]
        expected_route = [1, 4, 5, 2, 6, 3]
        actual_route = self.router.get_route(locations)

        # Assert the mocked output
        self.assertEqual(actual_route, expected_route, "The route does not match the expected output.")

        # Assert that all mocked methods were called with the correct arguments
        mock_get_coordinates.assert_has_calls([
            unittest.mock.call("Venice Beach"),
            unittest.mock.call("Staples Center"),
            unittest.mock.call("Griffith Observatory"),
        ])
        mock_nearest_nodes.assert_has_calls([
            unittest.mock.call(self.router.road_network, X=-118.46849, Y=33.99518),
            unittest.mock.call(self.router.road_network, X=-118.26728, Y=34.04302),
            unittest.mock.call(self.router.road_network, X=-118.29436, Y=34.13672),
        ])
        mock_astar.assert_called_once_with(self.router.road_network, [1, 2, 3])

    @patch("osmnx.load_graphml")
    def test_init_graph_loading(self, mock_load_graphml):
        # Mock `ox.load_graphml` to return a fake graph object
        mock_graph = MagicMock()
        mock_load_graphml.return_value = mock_graph

        # Initialize the `Routing` object
        router = Routing(self.graph_path)

        # Assert that the graph was loaded correctly
        self.assertEqual(router.road_network, mock_graph)
        mock_load_graphml.assert_called_once_with(self.graph_path)

if __name__ == '__main__':
    unittest.main()