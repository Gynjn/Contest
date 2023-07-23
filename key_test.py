import time

import cv2
import numpy as np
import serial
import camera
import keyboard
from time import sleep
from imgpreprocess import *
from birdeye import *
from utility import *
from stopping import *
from control import *
from utility2 import *

# from yolov5.models.common import DetectMultiBackend
# from yolov5.utils.general import non_max_suppression
#
# detect_net = DetectMultiBackend(weights="./yolo_best_0205_openvino_model")
# labels_to_names = {0 : "Crosswalk", 1 : "Green", 2 : "Red", 3 : "Car"}
# port = 'COM7'
# baudrate = 9600
# cnt = 1
# ser = serial.Serial(port, baudrate, )  # 아두이노와 시리얼 통신
speed = 255
# if ser.is_open:
#     ser.close()
#
# ser.open()
# print("ser opened!")
is_key_pressed = False
threshold = 180
flag = 0
bias1 = 0
bias2 = 0
bias3 = 0
# slope_list = np.empty(1)
# 카메라 장치 번호에 따라 수정 (0: 기본 카메라, 1: 외부 카메라)
capture = camera.CameraModule(width=640, height=480)
capture.open_cam(0)
if keyboard.read_key() == "g":
    pass
message = message = 'a' + str(0) + 's' + str(speed)
# ser.write(message.encode())
while True:
    # (1) 원본 cam1_origin
    bias1 = 0
    cam1_origin = capture.read()
    cam2_bird = bird_convert(cam1_origin, 'front')
    # ob_cam = cam1_origin[:,:480].copy()
    cam3_hsv = preprocess_img(cam2_bird, threshold)
    binary_img = cvt_binary(cam3_hsv)
    roi_img1 = roi_cutting(binary_img, 240)
    roi_img2 = roi_cutting(binary_img, 130)
    _, bottom_value, image_test2 = dominant_gradient(roi_img1)
    road_gradient, _, image_test = dominant_gradient(roi_img2)
    print(road_gradient, bottom_value)
    if (road_gradient == None and bottom_value == None):
        direction = 0
        message = 'a' + str(bias1) + 's' + str(speed)
        # ser.write(message.encode())
        continue

    road_direction = return_road_direction(road_gradient)  # gradient에 따른 direction
    final_direction = strengthen_control(road_direction, road_gradient, bottom_value)
    direction = smooth_direction(bias1, bias2, bias3, final_direction)
    if direction <= -3:
        direction = -4
    message = 'a' + str(direction) + 's' + str(speed)
    print(direction, final_direction)
    # ser.write(message.encode())

    bias1, bias2, bias3 = final_direction, bias1, bias2
    cv2.imshow("cam_test1", cam1_origin)
    cv2.imshow("cam_test2", cam2_bird)
    cv2.imshow("cam_test3", image_test)
    cv2.imshow("cam_test4", image_test2)

    # if KeyboardInterrupt:
    #     end_message = "a0s0"
    #     # ser.write(end_message.encode())
    #     # ser.close()
    #     print(end_message)
    #     capture.close_cam()
    #     cv2.destroyAllWindows()
    #
    #     print("Program Finish")
    #
    #     break

    if cv2.waitKey(25) == ord('f'):
        end_message = "a0s0"
        # ser.write(end_message.encode())
        # ser.close()
        print(end_message)
        capture.close_cam()
        cv2.destroyAllWindows()

        print("Program Finish")

        break

    sleep((0.0001))

