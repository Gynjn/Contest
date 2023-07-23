import cv2
import numpy as np
import serial
import camera
from time import sleep
from imgpreprocess import *
from birdeye import *
from utility import *
from stopping import *
from control import *
from utility2 import *
from yolov5.models.common import DetectMultiBackend
from yolov5.utils.general import non_max_suppression
from shift import *
import keyboard
detect_net = DetectMultiBackend(weights="./yolo_best_0205_openvino_model")
labels_to_names = {0 : "Crosswalk", 1 : "Green", 2 : "Red", 3 : "Car"}
port = 'COM7'
baudrate = 9600
cnt = 1
ser = serial.Serial(port, baudrate,)  # 아두이노와 시리얼 통신
speed = 100
if ser.is_open:
    ser.close()

ser.open()

threshold = 210
flag = 0
bias1 = 0
bias2 = 0
bias3 = 0
# 카메라 장치 번호에 따라 수정 (0: 기본 카메라, 1: 외부 카메라)
capture = camera.CameraModule(width=640, height=480)
capture.open_cam(1)
if keyboard.read_key() == "z":
    pass
message = message = 'a' + str(0) + 's' + str(speed)
ser.write(message.encode())
while True:
    # if flag == 1:
    #     threshold = 210
    # else:
    #     threshold = 205
    bias1 = 0
    cam1_origin = capture.read()
    cam2_bird = bird_convert(cam1_origin, 'front')
    cam3_hsv = preprocess_img(cam2_bird, threshold, flag)
    ob_cam = cam1_origin[:,80:560].copy()
    ob_img = preprocess(ob_cam, device='cpu')
    pred = detect_net(ob_img)
    pred = non_max_suppression(pred)[0]
    detect, _ = object_detection(pred)

    if detect[0] != None:
        print("traffic")
        cross_box = detect[0]
        if box_center(cross_box)[1] >= 333 and box_center(cross_box)[1] <= 370 and flag == 2:
            print("yes!")
            message = 'a' + str(0) + 's'+str(0)
            ser.write(message.encode())
            if detect[1] != None:
                flag = 3
            else:
                sleep(0.05)
                continue
        else:
            if detect[1] != None:
                angle = box_control(detect[1])
            elif detect[2] != None:
                angle = box_control(detect[2])
            else:
                angle = 0
            message = 'a' + str(angle) + 's' + str(50)
            ser.write(message.encode())
            sleep(0.025)
            continue

    else:
        pass

    if detect[3] != None:
        car_box = detect[3]
        # print(box_center(car_box))
        if box_center(car_box)[1] >= 250 and is_outside(cam3_hsv)== True and flag == 0:
            print("죄측 우회")
            flag = avoidance(1, ser)
        elif box_center(car_box)[1] >= 250 and is_outside(cam3_hsv)== False and flag == 1:
            print("우측 우회")
            flag = avoidance(0, ser)

    binary_img = cvt_binary(cam3_hsv)
    roi_img1 = roi_cutting(binary_img, 230)
    roi_img2 = roi_cutting(binary_img, 130)
    _, bottom_value, image_test2 = dominant_gradient(roi_img1)
    road_gradient, _, image_test = dominant_gradient(roi_img2)
    if (road_gradient == None and bottom_value == None):
        direction = 0
        message = 'a' + str(bias1) + 's' + str(speed)
        ser.write(message.encode())
        continue

    road_direction = return_road_direction(road_gradient)  # gradient에 따른 direction
    final_direction = strengthen_control(road_direction, road_gradient, bottom_value)
    direction = smooth_direction(bias1, bias2, bias3, final_direction)
    message = 'a' + str(direction) + 's' + str(speed)
    if direction <= -3:
        direction = -4
    # print(flag)
    print(direction, final_direction)
    ser.write(message.encode())
    bias1, bias2, bias3 = final_direction, bias1, bias2
    # cv2.imshow("cam_test1", cam1_origin)
    cv2.imshow("cam_test2", cam2_bird)
    cv2.imshow("cam_test5", ob_cam)
    # cv2.imshow("cam_test3", image_test)
    # cv2.imshow("cam_test4", image_test2)
    cv2.imshow("cam_test3", image_test)
    cv2.imshow("cam_test4", image_test2)
    # cnt += 1
    # if (cnt == 10):
    #     cv2.imwrite("center_test.png", ob_cam)
    #     break
    if cv2.waitKey(50) == ord('f'):
        end_message = "a0s0"
        ser.write(end_message.encode())
        ser.close()
        print(end_message)
        capture.close_cam()
        cv2.destroyAllWindows()

        print("Program Finish")

        break


