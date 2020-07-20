import sys
from loguru import logger


import os

path = '/home/pi/logs-rpi/logs'

logger.add(sys.stderr, format="{time} {level} {message}")
logger.add(path, rotation='100 MB')    # Once the file is too old, it's rotated
