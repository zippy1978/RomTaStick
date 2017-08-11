#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import json
import requests

sys.path.append('../lib')
sys.path.append('/home/pi/RomTaStick/lib')

from service.http_service import *

parser = argparse.ArgumentParser(description='Push external event to service.')
parser.add_argument('--type', help='Event type', type=str, required=True)
parser.add_argument('--data', help='Event data as JSON', type=str, required=False)

# Parse input
args = parser.parse_args()

# Post
server = HTTPService()
try:
    # Decode JSON data
    data = None
    if args.data != None:
            data = json.loads(args.data)
    # Prepare JSON message
    json_data = {}
    json_data['data'] = data
    json_data['type'] = args.type
    requests.post(('http://localhost:%s/event' % server.port), data=json.dumps(json_data))
except ValueError:
    print('Failed to parse data')
    sys.exit(1)
except:
    print('Failed to push event')
    sys.exit(1)
