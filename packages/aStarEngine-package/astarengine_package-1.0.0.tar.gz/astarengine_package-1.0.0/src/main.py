import os
import logging
from aStarEngine_package.utils.routing import Routing 

def main():
    # Configure logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    # Load graph and create Routing instance
    graph_path = os.path.abspath("../../data/LA_road_network.graphml")
    router = Routing(graph_path)

    # Define locations
    locations = ["Venice Beach, Los Angeles", "Staples Center, Los Angeles", "Griffith Park, Los Angeles"]

    # Get route
    try:
        route = router.get_route(locations)
        logging.info("Route found: %s", route)
    except FileNotFoundError as fnf_error:
        logging.error("Graph file not found: %s", fnf_error)
    except ValueError as value_error:
        logging.error("Error with locations or routing: %s", value_error)
    except Exception as e:
        logging.error("An unexpected error occurred: %s", e)

if __name__ == "__main__":
    main()




# [tool.setuptools]
# packages = { find = { where = ["src"] } }
# package-dir = {"" = "src"}

