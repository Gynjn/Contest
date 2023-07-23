import cv2
import os
import numpy as np
import serial
from device.camera import  import *


class Run:

    def __init__(self, args):
        self.mode = args.mode
        self.cam1 = args.cam1
        self.cam2 = args.cam2
        self.speed = args.speed
        self.serial = serial.Serial()
        self.serial_port = args.serial_port
        self.serial.baudrate = args.baudrate
        self.lidar_port = args.serial_port
        self.speed = int(self.speed)

    def serial_open(self):
        try:

        except:

    def camera_open(self):

    def lidar_open(self):



