import cv2
import numpy as np
import serial
import middle
import camera
from time import sleep
from imgpreprocess import *
from birdeye import *
from utility import *
from stopping import *
# from yolov5.models.common import DetectMultiBackend
# from yolov5.utils.general import non_max_suppression

# detect_net = DetectMultiBackend(weights="./yolo_best_0205_openvino_model")
# labels_to_names = {0 : "Crosswalk", 1 : "Green", 2 : "Red", 3 : "Car"}
# port = 'COM14'
# baudrate = 9600
# ser = serial.Serial(port, baudrate, )  # 아두이노와 시리얼 통신
# speed = 255
# if ser.is_open:
#     ser.close()
#
# ser.open()

# ROI 검출할 영역 설정하는 함수
def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, (255, 255, 255))  # 흰색으로 표시 (255,255,255)
    masked_img = cv2.bitwise_and(img, mask)
    return masked_img

width = 640
height = 480
slope_list = np.empty(1)
# 카메라 장치 번호에 따라 수정 (0: 기본 카메라, 1: 외부 카메라)
capture = camera.CameraModule(width=640, height=480)
capture.open_cam(0)
while True:
    # (1) 원본 cam1_origin
    cam1_origin = capture.read()
    bias1 = 0
    bias2 = 0
    cam2_bird = bird_convert(cam1_origin, 'front')
    ob_cam = cam1_origin[:,:480].copy()
    threshold = 180
    cam3_hsv = preprocess_img(cam2_bird, threshold)

    # (4) ROI 설정 : 양쪽 잘라냄 >> 넓게 보고 앞쪽을 자르는걸로 변경하기
    height, width = cam3_hsv.shape[:2]
    roi_vertices = np.array([[(width * 0 / 7, height),
                              (width * 0 / 7, height*0.3),
                              (width * 7 / 7, height*0.3),
                              (width * 7 / 7, height)]], dtype=np.int32)
    cam4_roi = region_of_interest(cam3_hsv, roi_vertices)
    # (5) HoughLines로 차선 직선 검출하기
    cam5_hough = cam4_roi
    gray = cv2.cvtColor(cam5_hough, cv2.COLOR_BGR2GRAY)
    # gray = cvt_binary(cam5_hough)
    ob_img = preprocess(ob_cam, device='cpu')
    # pred = detect_net(ob_img)
    # pred = non_max_suppression(pred)[0]
    # detect, _ = object_detection(pred)
    # if detect[0] != None:
    #     cross_box = detect[0]
    #     if box_center(cross_box)[1] >= 380:
    #         # message = 'a' + str(60) + 's'+str(0)
    #         # ser.write(message.encode())
    #         ser.write(b'H')
    #         stopping(capture)
    # if detect[3] != None:
    #     car_box = detect[3]
    #     if box_center(car_box)[1] >= 0 and is_outside(cam3_hsv)==True:
    #         # message = 'a' + str(120) + 's'+str(-1)
    #         # ser.write(message.encode())
    #         ser.write(b'L')
    #     elif box_center(car_box)[1] >= 0 and is_outside(cam3_hsv)==False:
    #         # message = 'a' + str(0) + 's'+str(-1)
    #         # ser.write(message.encode())
    #         ser.write(b'R')
    # ob_cam = show_bounding_box(ob_cam, pred)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    edges = cv2.Canny(blurred, 30, 100)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 60)
    x_coord = np.zeros((640,))
    y_idx = 350
    slope_list = np.empty(0)
    if (not isinstance(lines, type(None))):
        for line in lines:
            # print(len(lines)) # Line 개수 출력
            rho, theta = line[0]
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            if (theta < 1.87 and theta > 1.27):
                continue
            cv2.line(gray, (x1, y1), (x2, y2), (0, 0, 255), 1)
            if (y1- y2) == 0:
                continue
            slope = np.arctan((x2-x1)/(y1-y2))*180/np.pi
            intercept = int((x1-x2)/(y1-y2) * (y_idx - y1) + x1)
            if intercept < 0 or intercept > 639:
                continue
            x_coord[intercept] = 1

            if slope > -22 and slope < 22:
                slope_list = np.append(slope_list, slope)
        # 중간값 처리

    if(len(slope_list)!=0):
        median_val = np.median(slope_list)
        angle = -median_val
        result = np.where(x_coord == 1)[0]
        left, right = middle.left_right(result)
        # print(left, right)
        center = middle.get_middle(left, right)
        corrected_angle = middle.correction(angle, left, right, center)
        # print("Serial write : ", -corrected_angle)
        # corrected_angle: -27 ~ 27
        angle = (corrected_angle + 27) * 120 / 54
        # angle: 0 ~ 120
        angle = bias1*0.2 + angle*0.8
        bias1 = angle
        angle = int(angle)
        angle = chr(angle)
        # print(angle)
        # message = 'a' + str(angle) + 's' + str(speed)
        # ser.write(message.encode())
        # ser.write(angle.encode())
    # cv2.imshow("cam_test1", cam1_origin)
    # cv2.imshow("cam_test2", cam2_bird)
    # cv2.imshow("cam_test3", gray)
    # cv2.imshow("cam_test4", ob_cam)
    # cv2.imshow("cam_test5", cam2_bird)
    sleep(0.05)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        # ser.close()
        break

capture.release()
# capture2.release()
cv2.destroyAllWindows()