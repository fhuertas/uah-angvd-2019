#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer
import sys


# HTTPRequestHandler class
class ServerRequestHandler(BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        print("Make request for topic {}".format(sys.argv[2]))
        # Send response status code
        self.send_response(200)
        path = self.path[1:]
        print("Make a request for {}".format(path))

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Send message back to client
        message = "Hello world!"
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return


if __name__ == "__main__":
    print('starting server...')
    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = ('127.0.0.1', int(sys.argv[1]))
    httpd = HTTPServer(server_address, ServerRequestHandler)
    print('running server...')
    httpd.serve_forever()
