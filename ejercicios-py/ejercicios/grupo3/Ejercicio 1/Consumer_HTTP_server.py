from http.server import BaseHTTPRequestHandler, HTTPServer
from confluent_kafka import Consumer
import time
import json


def get_reading_json(msg):

    data = msg.split(",")

    reading = {
        "temperature": int(data[0]),
        "location": {
            "latitude": float(data[1]),
            "longitude": float(data[2])
        }
    }

    return reading


class ServerRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        # Send response status code
        self.send_response(200)
        path = self.path[1:]

        print("Make a request for {}".format(path))

        # Send headers
        self.send_header('Content-type', 'application/json')
        self.send_header('Accept-Charset', 'UTF-8')
        self.send_response(200)
        self.end_headers()

        c = Consumer({
            'bootstrap.servers': 'localhost:9092',
            'group.id': round(time.time() * 1000),
            'auto.offset.reset': 'earliest'
        })

        c.subscribe([path])

        while True:

            msg = c.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue

            message = get_reading_json(msg.value().decode('utf-8'))

            print('Received message: ', json.dumps(message))

            # Send message back to client

            self.wfile.write(bytes(json.dumps(message) + '\n', "utf8"))

        c.close()


if __name__ == "__main__":

    print('starting server...')
    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access

    PORT = 8080
    server_address = ('127.0.0.1', PORT)
    httpd = HTTPServer(server_address, ServerRequestHandler)
    sa = httpd.socket.getsockname()
    print("Serving HTTP on", sa[0], "port", sa[1], "...")
    print('Running Server...')
    httpd.serve_forever()
