from confluent_kafka import Consumer
from http.server import BaseHTTPRequestHandler, HTTPServer
import time

def consume_sensor(path):
    """

    :rtype: object
    """
    c = Consumer({
        'bootstrap.servers': 'localhost:9092',
        'group.id': round(time.time() * 1000000),
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

        print('Received message: {}'.format(msg.value().decode('utf-8')))

    c.close()



class ServerRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        path = self.path[1:]
        print("Make a request for {}".format(path))

        self.send_header('Content-type', 'text/html')
        self.end_headers()
        print(path)
        
        consume_sensor(path)


#curl http://localhost:8080/this-is-a-topic

if __name__ == "__main__":

    print('starting server...')

    port = 8080
    server_address = ('127.0.0.1', port)
    httpd = HTTPServer(server_address, ServerRequestHandler)
    print('running server...')
    httpd.serve_forever()
