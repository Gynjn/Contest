import cv2
import numpy as np
import serial
import middle
import camera
from time import sleep
from imgpreprocess import *
from birdeye import *
from utility import *
from rplidar import RPLidar
from stopping import *
import time
import os
from math import floor

# from yolov5.models.common import DetectMultiBackend
# from yolov5.utils.general import non_max_suppression

# detect_net = DetectMultiBackend(weights="./yolo_best_0205_openvino_model")
# labels_to_names = {0 : "Crosswalk", 1 : "Green", 2 : "Red", 3 : "Car"}
port = 'COM7'
PORT_NAME = 'COM20'
lidar = RPLidar(PORT_NAME, timeout=3)
baudrate = 9600
ser = serial.Serial(port, baudrate, )

if ser.is_open:
    ser.close()

ser.open()
width = 640
height = 480
slope_list = np.empty(1)
stage = 0
capture = camera.CameraModule(width=640, height=480)
capture.open_cam(0)
while True:
    try:
        if (stage == 0):
            start_time = time.time()
            end_time = start_time + 2
            while time.time() < end_time:
                message = 'a' + str(0) + 's' + str(75)
                ser.write(message.encode())
                time.sleep(0.025)
            stage = 1
        if (stage == 1):
            for scan in lidar.iter_scans():
                for (_, angle, distance) in scan:
                    if (floor(angle) == 90 or floor(angle) == 91 or floor(angle) == 89):
                        print(floor(angle), distance)
                        if (500<distance and distance < 1300):
                            message = 'a' + str(0) + 's' + str(0)
                            ser.write(message.encode())
                            stage = 2
                            break
                        else:
                            message = 'a' + str(0) + 's' + str(75)
                            ser.write(message.encode())
                if (stage == 2):
                    break
        if (stage == 2):
            start_time = time.time()
            end_time = start_time + 3
            while time.time() < end_time:
                message = 'a' + str(0) + 's' + str(75)
                ser.write(message.encode())
                time.sleep(0.025)
            stage = 3
        if (stage == 3):
            start_time = time.time()
            end_time = start_time + 5.5
            while time.time() < end_time:
                message = 'a' + str(-6) + 's' + str(75)
                ser.write(message.encode())
                time.sleep(0.025)
            stage = 4
        if (stage == 4):
            start_time = time.time()
            end_time = start_time + 8
            while time.time() < end_time:
                message = 'a' + str(10) + 's' + str(-75)
                ser.write(message.encode())
                time.sleep(0.025)
            stage = 5
        if (stage == 5):
            start_time = time.time()
            end_time = start_time + 3
            while time.time() < end_time:
                message = 'a' + str(1) + 's' + str(-50)
                ser.write(message.encode())
                time.sleep(0.025)
            stage = 6
        if (stage == 6):
            start_time = time.time()
            end_time = start_time + 4
            while time.time() < end_time:
                message = 'a' + str(0) + 's' + str(0)
                ser.write(message.encode())
                time.sleep(0.025)
            # sleep(5)
            stage = 7
        if (stage == 7):
            start_time = time.time()
            end_time = start_time + 2
            while time.time() < end_time:
                message = 'a' + str(1) + 's' + str(50)
                ser.write(message.encode())
                time.sleep(0.025)
            stage = 8
        if (stage == 8):
            start_time = time.time()
            end_time = start_time + 15
            while time.time() < end_time:
                message = 'a' + str(-10) + 's' + str(50)
                ser.write(message.encode())
                time.sleep(0.025)
            stage = 9
        if (stage == 9):
            start_time = time.time()
            end_time = start_time + 20
            while time.time() < end_time:
                message = 'a' + str(0) + 's' + str(70)
                ser.write(message.encode())
                time.sleep(0.025)
            stage = 10
            break
        if (stage == 10):
            start_time = time.time()
            end_time = start_time + 6
            while time.time() < end_time:
                message = 'a' + str(0) + 's' + str(75)
                ser.write(message.encode())
                time.sleep(0.025)
            stage = 10
        if (stage == 10):
            start_time = time.time()
            end_time = start_time + 4
            while time.time() < end_time:
                message = 'a' + str(5) + 's' + str(75)
                ser.write(message.encode())
                time.sleep(0.025)
            stage = 11
        if (stage == 11):
            start_time = time.time()
            end_time = start_time + 30
            while time.time() < end_time:
                message = 'a' + str(0) + 's' + str(75)
                ser.write(message.encode())
                time.sleep(0.025)
            break
    except KeyboardInterrupt:
        print('Stopping.')
        break
    if cv2.waitKey(10) & 0xFF == ord('q'):
        ser.close()
        break

lidar.stop()
lidar.disconnect()
capture.release()
# capture2.release()
cv2.destroyAllWindows()