#!/usr/bin/env python

import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from confluent_kafka import Consumer


def genera_diccionario(lectura):
    segmentado = lectura.split(sep=",")
    return {"temperatura": segmentado[0], "location": {"latitud": segmentado[1], "longitud": segmentado[2]}}


def acumular_lecturas(path):
    c = Consumer({
        'bootstrap.servers': 'localhost:9092',
        'group.id': 1000,
        'auto.offset.reset': 'earliest'
    })  # El grupo se fija para hacer que una vez se leen no se relean en posteriores invocaciones

    c.subscribe([path])

    hay_pendientes = True
    lista_lecturas = []

    while hay_pendientes:
        # Traer mensaje del topic
        msg = c.poll(1.0)

        if msg is None:
            hay_pendientes = False
        elif msg.error():
            print("Consumer error: {}".format(msg.error()))
            hay_pendientes = False
        elif hay_pendientes:
            lista_lecturas.append(genera_diccionario(msg.value().decode('utf-8')))
    c.close()
    return json.dumps(lista_lecturas)


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
        message = acumular_lecturas(str(path))
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return


if __name__ == "__main__":
    print('starting server...')
    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = ('127.0.0.1', 8080)
    httpd = HTTPServer(server_address, ServerRequestHandler)
    print('running server...')
    httpd.serve_forever()
