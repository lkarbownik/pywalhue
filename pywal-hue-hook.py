#! /usr/bin/env python3

from __future__ import print_function

import json
import logging
import math
import os
import re
import sys

import phue
from rgbxy import Converter, GamutC


BRIDGE_IP = '192.168.1.56'
LIGHTS = ['Hue lightstrip plus 1']


converter = Converter(GamutC)

if len(sys.argv) > 1:
    rgb_hex = sys.argv[1]
    if not re.compile(r'[a-fA-F0-9]{6}$').match(rgb_hex):
        raise ValueError('Argument must be a valid hex color')

    xy = converter.hex_to_xy(sys.argv[1])
else:
    colors_file_path = os.path.expanduser('~/.cache/wal/colors.json')
    if not os.path.isfile(colors_file_path):
        print('colors.json not found in pywal cache directory', file=sys.stderr)
        sys.exit(1)

    file = open(colors_file_path, 'r')
    colors = json.load(file)
    rgb_hex = colors['special']['background'][1:]
    xy = converter.hex_to_xy(rgb_hex)

try:
    bridge = phue.Bridge(BRIDGE_IP)
except:
    print(
        'Cannot connect to Hue Bridge. Provide correct IP address',
        file=sys.stderr,
    )
    sys.exit(1)

bridge.connect()

rgb_ints = [
    int(rgb_hex[x:x+2], 16)
    for x in range(1, len(rgb_hex), 2)
]

bri = 254

# Luminance
# bri = math.trunc(0.2126 * rgb_ints[0] + 0.7152 * rgb_ints[1] + 0.0722 * rgb_ints[2])

# Perceived luminance
# bri = math.trunc(0.299 * rgb_ints[0] + 0.587 * rgb_ints[1] + 0.114 * rgb_ints[2])

state = {
    'xy': xy,
    'bri': bri
}

bridge.set_light(LIGHTS, state)
