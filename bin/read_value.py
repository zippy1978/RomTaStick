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

# Parse input
args = parser.parse_args()

# Read settings
stgs = Settings()
print(stgs.read(args.section, args.property))

sys.exit(0)
