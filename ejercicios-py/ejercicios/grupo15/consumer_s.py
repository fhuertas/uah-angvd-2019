import time
from http.server import BaseHTTPRequestHandler, HTTPServer

from confluent_kafka import Consumer, KafkaError

consumer_id = round(time.time() * 1000000)


def consume_sensor(path):
    """

    :rtype: object
    """
    c = Consumer({
        'bootstrap.servers': 'localhost:9092',
        'group.id': consumer_id,
        'auto.offset.reset': 'earliest'
    })

    c.subscribe([path])
    body = ""
    while True:
        msg = c.poll(1.0)
        print(msg)
        if msg is None:
            break
        elif msg.error() and msg.error().code() == KafkaError._PARTITION_EOF:
            print("Fin: {}".format(msg.error()))
            break
        elif msg.error():
            print("Consumer error: {}".format(msg.error()))
            continue
        content = msg.value().decode('utf-8')
        body = "{}\n{}".format(body, content)
    c.close()
    return body


class ServerRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        path = self.path[1:]
        print("Make a request for {}".format(path))

        self.send_header('Content-type', 'text/html')
        self.end_headers()
        print(path)

        body = consume_sensor(path)
        self.wfile.write(bytes(body, "utf8"))
        return


# curl http://localhost:8080/this-is-a-topic

if __name__ == "__main__":
    print('starting server...')

    port = 8080
    server_address = ('127.0.0.1', port)
    httpd = HTTPServer(server_address, ServerRequestHandler)
    print('running server...')
    httpd.serve_forever()
