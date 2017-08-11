from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import threading
import logging
import requests
import json
import sys

from events.events import *

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

class RequestHandler(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

    def do_GET(self):
        self._set_headers()

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):

        options = {
           '/stop' : self._stop_server,
           '/event' : self._inject_event
        }

        self._set_headers()
        options[self.path]()

    def _stop_server(self):
        logging.info('Stopping RomTaStick service...')
        assassin = threading.Thread(target=self.server.shutdown)
        assassin.daemon = True
        assassin.start()

    def _inject_event(self):
        content_len = int(self.headers.getheader('content-length', 0))
        post_body = self.rfile.read(content_len)
        json_data = json.loads(post_body)
        e = Event(json_data['type'], json_data['data'])
        notify_event_receivers(e)

class HTTPService(object):

    port = 7777
    _httpd = None

    def __init__(self):
        pass

    def start(self):
        logging.info('Starting RomTaStick service...')
        self._httpd = HTTPServer(('127.0.0.1', self.port), RequestHandler)
        logging.info('Done.')
        self._httpd.serve_forever()

    def stop(self):
        requests.post(('http://localhost:%s/stop' % self.port), data = {})
