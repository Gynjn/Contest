import sys
import numpy as np
from rplidar import RPLidar

import os
from math import floor


# Setup the RPLidar
PORT_NAME = 'COM13'
lidar = RPLidar(PORT_NAME, timeout=3)

# used to scale data to fit on the screen
max_distance = 0

def process_data(data):
    print(data)

scan_data = [0]*360

try:
#    print(lidar.get_info())
    for scan in lidar.iter_scans():
        for (_, angle, distance) in scan:
            if(floor(angle) == 270 or floor(angle) == 271 or floor(angle) == 279):
                print(floor(angle), distance)
        #

except KeyboardInterrupt:
    print('Stopping.')
lidar.stop()
lidar.disconnect()