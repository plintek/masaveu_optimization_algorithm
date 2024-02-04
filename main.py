""" Main file for the optimization server. """
import json
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from src.optimization import execute_optimization

# Example locations (latitude, longitude) along the route
# locations = [
#     (37.7749, -122.4194),  # San Francisco
#     (34.0522, -118.2437)   # Los Angeles
#     # Add more waypoints as needed
# ]

# # Retrieve elevations
# elevation.clip(bounds=(12.35, 41.8, 12.65, 42), output='Rome-DEM.tif')
#  # clean up stale temporary files and fix the cache in the event of a server error
# elevation.clean()

# if elevations:
#     for i, elevation in enumerate(elevations):
#         print(f"Waypoint {i + 1}: Elevation = {elevation} meters")


def check_post_data(post_data):
    """Check if the post data contains all the required fields."""
    fields = ['order_id']
    if not all(field in post_data for field in fields):
        raise ValueError("Missing required fields in post data")


def execute_post(post_data):
    """Execute the optimization based on the post data."""
    try:
        # Start timer
        start_time = time.time()

        check_post_data(post_data)

        execute_optimization(post_data)

        # End timer
        end_time = time.time()
        print('Time elapsed: {}s'.format(end_time - start_time))

    except Exception as e:
        print(e)


class Server(BaseHTTPRequestHandler):
    """Server class for handling requests."""
    # As json

    def do_post(self):
        """Handle POST requests."""
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        post_data = json.loads(post_data.decode("utf-8"))
        return_data = {"message": "Optimization added to queue"}

        execute_post(post_data)

        return_data_bytes = json.dumps(return_data).encode("utf-8")
        self.wfile.write(return_data_bytes)


if __name__ == '__main__':

    HOST_NAME = '0.0.0.0'
    SERVER_PORT = 5758

    my_server = HTTPServer((HOST_NAME, SERVER_PORT), Server)
    print(time.asctime(), f"Server Starts - {HOST_NAME}:{SERVER_PORT}")

    # example
    with open('src/data/input.json', 'r', encoding="utf-8") as file:
        execute_optimization(json.load(file))

    try:
        my_server.serve_forever()
    except KeyboardInterrupt:
        pass

    my_server.server_close()
    print(time.asctime(), f"Server Stops - {HOST_NAME}:{SERVER_PORT}")
