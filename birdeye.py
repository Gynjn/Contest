import cv2
import numpy as np
import matplotlib.pyplot as plt
import pickle
import os

direction_div = 12

def src_mat(camera_type):
    dic_param = {}
    if camera_type == 'front':
        path_perspect = os.path.dirname(os.path.abspath(__file__))
        with open(path_perspect + "/test_c.pkl", 'rb') as f:
            dic_param = pickle.load(f)
    if camera_type == 'back':
        path_perspect = os.path.dirname(os.path.abspath(__file__))
        with open(path_perspect + "/test_c.pkl", 'rb') as f:
            dic_param = pickle.load(f)
    if len(dic_param) != 0:
        return dic_param['pts_src']
    else:
        return None

def wrapping(image, pts_src, camera_type):
    (h, w) = (image.shape[0], image.shape[1])

    if camera_type == 'front':
        destination = np.float32(
            # [[round(w * 0.8), round(h * 0.0)], [round(w * 0.8), round(h * 0.0)],
            #  [round(w * 0.2), h], [round(w * 0.2), h]]
            [[round(w * 0.3), round(h * 0.0)], [round(w * 0.7), round(h * 0.0)],
             [round(w * 0.7), h], [round(w * 0.3), h]]
        )
    if camera_type == 'back':
        destination = np.float32(
            # [[round(w * 0.8), round(h * 0.0)], [round(w * 0.8), round(h * 0.0)],
            #  [round(w * 0.2), h], [round(w * 0.2), h]]
            [[round(w * 0.3), round(h * 0.0)], [round(w * 0.7), round(h * 0.0)],
             [round(w * 0.7), h], [round(w * 0.3), h]]
        )

    transform_matrix = cv2.getPerspectiveTransform(pts_src, destination)
    minv = cv2.getPerspectiveTransform(destination, pts_src)
    _image = cv2.warpPerspective(image, transform_matrix, (w,h))

    return _image, minv

def bird_convert(img, camera_type):
    srcmat = src_mat(camera_type)
    img_warpped, minverse = wrapping(img, srcmat, camera_type)

    return img_warpped