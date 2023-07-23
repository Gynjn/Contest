import cv2
import numpy as np

width = 640
height = 480

def left_right(array, value=310):
    array = np.asarray(array)
    left_val = array[np.max(np.where(array <= value)[0])] if len(np.where(array <= value)[0]) != 0 else None
    right_val = array[np.min(np.where(array > value)[0])] if len(np.where(array > value)[0]) != 0 else None
    return left_val, right_val

def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, (255, 255, 255))  # 흰색으로 표시 (255,255,255)
    masked_img = cv2.bitwise_and(img, mask)
    return masked_img

def get_middle(left, right):
    if left == None or right == None:
        return None
    return int((left+right))/2

def correction(angle, left, right, center):
    bias = 320
    if left == None:
        #왼쪽으로 확
        return 27.0
    elif right == None:
        #오른쪽으로 확
        return -27.0
    else:
        diff = bias - center
        if abs(diff) > 10 :
            result = angle + diff / 3
        else:
            result = angle + diff / 4
        if result < -27:
            return -27.0
        elif result > 27:
            return 27.0
        else :
            return result