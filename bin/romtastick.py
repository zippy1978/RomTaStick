#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import sys

sys.path.append('../lib')
sys.path.append('/home/pi/RomTaStick/lib')

from service.bootstrap import *

parser = argparse.ArgumentParser(description='Control RomTaStick service.')
parser.add_argument('--action', help='Action to perform among : start, stop', type=str, required=True)

# Parse input
args = parser.parse_args()

# Start or stop server
if args.action == 'start':
    start_server()

elif args.action == 'stop':
    stop_server()
