import json
import time
from src.optimization import execute_optimization
from http.server import BaseHTTPRequestHandler, HTTPServer


def check_post_data(post_data):
    fields = ['order_id', 'origin', 'destination']
    if not all(field in post_data for field in fields):
        raise ValueError("Missing required fields in post data")

    fields = ['lat', 'lon', 'id', 'name']
    if not all(field in post_data['origin'] for field in fields):
        raise ValueError("Missing required fields in origin")

    if not all(field in post_data['destination'] for field in fields):
        raise ValueError("Missing required fields in destination")

def execute_post(post_data):
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
    # As json
    def do_POST(self):
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
    host_name = '0.0.0.0'
    server_port = 5757

    my_server = HTTPServer((host_name, server_port), Server)
    print(time.asctime(), "Server Starts - %s:%s" % (host_name, server_port))

    # example
    execute_optimization({
        "order_id": "89F07B0D-E424-4FC4-9135-FFE85FAC5AAF",
        "origin": {
            "id": "1",
            "name": "Origin",
            "lat": 41.3851,
            "lon": 2.1734,
            "country": "ES"
        },
        "destination": {
            "id": "2",
            "name": "Destination",
            "lat": 41.3851,
            "lon": 2.1734,
            "country": "ES"
        }
    })

    try:
        my_server.serve_forever()
    except KeyboardInterrupt:
        pass

    my_server.server_close()
    print(time.asctime(), "Server Stops - %s:%s" % (host_name, server_port))
