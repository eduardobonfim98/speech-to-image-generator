import json
import os

import yaml

_config = None

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

with open(os.path.join(__location__, 'config.yaml'), 'r') as stream:
    CONFIG = yaml.safe_load(stream)

