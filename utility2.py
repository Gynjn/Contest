import numpy as np
import cv2
import sys
import os

def center_point(left_idx, right_idx):
    if left_idx == None or right_idx == None:
        return None
    else:
        return (left_idx + right_idx) / 2

def find_nearest(array, value=290):
    array = np.asarray(array)
    left_val = array[np.max(np.where(array <= value)[0])] if len(np.where(array <= value)[0]) != 0 else None
    right_val = array[np.min(np.where(array > value)[0])] if len(np.where(array > value)[0]) != 0 else None

    return left_val, right_val


def return_road_direction(road_gradient):
    f = lambda x: 7 / 64000 * (x ** 3)
    ret_direction = round(f(road_gradient))

    ret_direction = 7 if ret_direction >= 7 else ret_direction
    ret_direction = -7 if ret_direction <= -7 else ret_direction

    return ret_direction


def dominant_gradient(image):  # 흑백 이미지에서 gradient 값, 차선 하단 값 추출

    image_original = image.copy()

    ##Canny
    # img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    try:
        img_blur = cv2.GaussianBlur(image_original, (0, 0), 1)
        # img_blur = image
        img_edge = cv2.Canny(img_blur, 110, 180)
    except Exception as e:
        _, _, tb = sys.exc_info()
        print("image preprocess(gradient) error = {}, error line = {}".format(e, tb.tb_lineno))

        exception_image_path = "./exception_image/"
        try:
            if not os.path.exists(exception_image_path):
                os.mkdir(exception_image_path)
        except OSError:
            print('Error: Creating dirctory. ' + exception_image_path)

        # cv2.imwrite(os.path.join(exception_image_path, "exception_image--{}.png".format(datetime.now())), pre_image)
        return None, None

    try:
        # lines = cv2.HoughLines(img_edge, 1, np.pi / 180, 30)
        lines = cv2.HoughLines(img_edge, 1, np.pi / 180, 25)
        angles = []
        bottom_flag = np.zeros((640,))
        bottom_idx = 280

        if (not isinstance(lines, type(None))):

            for line in lines:
                for rho, theta in line:
                    a = np.cos(theta)
                    b = np.sin(theta)
                    x0 = a * rho
                    y0 = b * rho
                    x1 = int(x0 + 1000 * (-b))
                    y1 = int(y0 + 1000 * (a))
                    x2 = int(x0 - 1000 * (-b))
                    y2 = int(y0 - 1000 * (a))

                    if y1 > 120 or y2 > 120:
                        flag_idx = int((x1 - x2) / (y1 - y2) * (bottom_idx - 1 - y1) + x1)
                        if flag_idx < 0 or flag_idx >= 640:
                            continue
                        bottom_flag[flag_idx] = 1
                    cv2.line(image_original, (x1, y1), (x2, y2), (0, 0, 255), 1)
                    if (theta < 1.87 and theta > 1.27):
                        continue
                    else:
                        if y1 == y2:
                            angle = 'inf'
                        else:
                            angle = np.arctan((x2 - x1) / (y1 - y2)) * 180 / np.pi
                        angles.append(angle)
        result_idx = np.where(bottom_flag == 1)[0]
        if len(angles) == 0:
            result = 0
        else:
            result = np.median(angles)



        # print(angles)
        return result, result_idx, image_original

    except Exception as e:
        _, _, tb = sys.exc_info()
        print("gradient detection error = {}, error line = {}".format(e, tb.tb_lineno))
        exception_image_path = "./exception_image/"
        try:
            if not os.path.exists(exception_image_path):
                os.mkdir(exception_image_path)
        except OSError:
            print('Error: Creating dirctory. ' + exception_image_path)
        # cv2.imwrite(os.path.join(exception_image_path, "exception_image--{}.png".format(str(uuid.uuid1()))), pre_image)
        return None, None