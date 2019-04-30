#!/usr/bin/env python

import json
import sys
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

from confluent_kafka import Consumer


def consumer(topic):
    c = Consumer({
        'bootstrap.servers': 'localhost:9092',
        'group.id': round(time.time() * 1000),
        'auto.offset.reset': 'earliest'
    })
    c.subscribe([topic])

    result = {'messages': []}

    msg = c.poll(10.0)
    while msg:
        if msg.error():
            print("error{}".format(msg.error()))
            break
        msg = msg.value().decode('utf-8').split(",")
        result['messages'].append({
            "t": msg[0],
            "location": {"lat": msg[1], "long": msg[2]}
        })
        msg = c.poll(0.5)

    print(result)
    with open('data.json', 'w') as salida:
        json.dump(result, salida, indent=4)

    c.close()


# HTTPRequestHandler class
class ServerRequestHandler(BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        # Send response status code
        self.send_response(200)
        path = self.path[1:]
        print("Make a request for {}".format(path))

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Send message back to client
        consumer(path)
        return


if __name__ == "__main__":
    print('starting server...')
    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = ('127.0.0.1', int(sys.argv[1]))
    httpd = HTTPServer(server_address, ServerRequestHandler)
    print('running server...')
    httpd.serve_forever()
