#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

sys.path.append('../lib')
sys.path.append('/home/pi/RomTaStick/lib')

import argparse
from settings.settings import *

parser = argparse.ArgumentParser(description='Read RomTaStick setting value.')
parser.add_argument('--section', help='Section')
parser.add_argument('--property', help='Property')
parser.add_argument('--value', help='Value')

# Parse input
args = parser.parse_args()

# Read settings
stgs = Settings()
stgs.write(args.section, args.property, args.value)

sys.exit(0)
