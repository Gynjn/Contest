import cv2
import numpy as np
from torchvision import transforms


def color_filter(image, threshold):
    HSV_frame = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    H, S, V = cv2.split(HSV_frame)

    H_green_lower = 30

    # green
    H_green_condition = (H_green_lower<H) & (H<90)
    S_green_condition = (S>20)
    V_green_condition = V>100
    green_condition = H_green_condition & S_green_condition & V_green_condition
    H[green_condition] = 50
    S[green_condition] = 100
    V[green_condition] = 100
    # white
    # day_evening = 200 #day
    # day_evening = 180 #mid
    # day_evening = 165 #evening


    V_white_condition = V>threshold

    white_condition = V_white_condition
    H[V_white_condition] = 0
    S[V_white_condition] = 0
    V[V_white_condition] = 255
    # gray
    V_gray_condition = (115<V) & (V<=threshold)
    # V_gray_condition = (100 < V) & (V <= threshold)

    # S_gray_condition = S<25
    gray_condition = V_gray_condition  # & S_gray_condition
    H[gray_condition] = 120
    S[gray_condition] = 150
    V[gray_condition] = 150
    # black -> blue (road)
    road_condition = True ^ ((green_condition | V_white_condition) | V_gray_condition)
    H[road_condition] = 120
    S[road_condition] = 150
    V[road_condition] = 150

    HSV_frame[:, :, 0] = H
    HSV_frame[:, :, 1] = S
    HSV_frame[:, :, 2] = V
    frame_filtered = cv2.cvtColor(HSV_frame, cv2.COLOR_HSV2BGR)

    return frame_filtered

def only_stadium(image):  # 경기장 밖 지우는 함수
    HSV_frame = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    H, S, V = cv2.split(HSV_frame)



    H_satisfied = (30< H) & (H < 80)
    S_satisfied = S == 100 + 2
    V_satisfied = V == 100
    satisfied = H_satisfied & S_satisfied & V_satisfied
    satisfied[:, 639] = True
    check_top_green = len(np.where(satisfied[0])[0])

    first_green_x = np.argmax(satisfied, axis=1).reshape(480, 1)
    green_left_x = first_green_x - 20
    # print(first_green_x)
    x = np.linspace(0, 639, 640)
    y = np.linspace(0, 479, 480)
    X, Y = np.meshgrid(x, y)
    if check_top_green == 0:  # 제일 상단 row에 초록색 없음
        green_area = (X > first_green_x) & (first_green_x != 0)
    else:  # 제일 상단 row에 초록색 있음
        green_area = (X > first_green_x)

    white_area = (X <= first_green_x) & (X > green_left_x) & (X < 619)

    HSV_frame[green_area] = [50, 100, 100]
    HSV_frame[white_area] = [0, 0, 255]

    V_white_satisfied = V == 255
    satisfied = V_white_satisfied
    satisfied[:, 639] = True

    first_white_x = np.argmax(satisfied, axis=1).reshape(480, 1)
    white_right_x = first_white_x + 15
    # print(first_green_x)
    x = np.linspace(0, 639, 640)
    y = np.linspace(0, 479, 480)
    X, Y = np.meshgrid(x, y)


    white_area1 = (X > first_white_x) & (X <= white_right_x)
    HSV_frame[white_area1] = [0, 0, 255]

    # white_scene = np.ones((480, 640))
    # # cv2.imshow("satisfied", white_scene)
    #
    # green_points = np.argwhere(satisfied)

    # ---------------------------------------------------------------------------------------------

    frame_stadium = cv2.cvtColor(HSV_frame, cv2.COLOR_HSV2BGR)
    return frame_stadium


def hide_car_head(image):
    HSV_frame = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    H, S, V = cv2.split(HSV_frame)

    x = np.linspace(0, 639, 640)
    y = np.linspace(0, 479, 480)
    X, Y = np.meshgrid(x, y)

    a = 125
    b = 54
    elipse_eq = b * b * (X - 310) * (X - 310) + a * a * (Y - 479) * (Y - 479) < a * a * b * b

    H[elipse_eq] = 120
    S[elipse_eq] = 150
    V[elipse_eq] = 150

    HSV_frame[:, :, 0] = H
    HSV_frame[:, :, 1] = S
    HSV_frame[:, :, 2] = V
    car_hidden_img = cv2.cvtColor(HSV_frame, cv2.COLOR_HSV2BGR)

    return car_hidden_img

def increase_contrast(image, roi):
    # Convert the ROI to grayscale
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # Apply histogram equalization to the ROI
    equalized_roi = cv2.equalizeHist(gray_roi)

    # Convert the equalized ROI back to color
    equalized_roi_color = cv2.cvtColor(equalized_roi, cv2.COLOR_GRAY2BGR)

    # Replace the ROI in the original image with the equalized ROI
    result = image.copy()
    result[:roi.shape[0], :roi.shape[1]] = equalized_roi_color

    return result

def remove_black(image):
    x = np.linspace(0,639,640)
    y = np.linspace(0,479,480)
    X,Y = np.meshgrid(x,y)

    left_bottom = -123*X + 69*Y - 69*354
    left_bottom = left_bottom>0
    right_bottom = 173*(X-639) + 93*Y - 93*304
    right_bottom = right_bottom>0

    B, G, R = cv2.split(image)
    left_color = image[479, 70]
    right_color = image[479, 545]

    B[left_bottom] = left_color[0]
    G[left_bottom] = left_color[1]
    R[left_bottom] = left_color[2]

    B[right_bottom] = right_color[0]
    G[right_bottom] = right_color[1]
    R[right_bottom] = right_color[2]

    image[:,:,0] = B
    image[:,:,1] = G
    image[:,:,2] = R

    return image
def preprocess_img(img, threshold, flag):
    image_blured = cv2.GaussianBlur(img, (0,0), 5)
    image_filtered2 = color_filter(image_blured, threshold)
    if flag == 1:
        image_filtered1 = color_filter(image_blured[:, 300:], threshold-20)
        image_filtered2[:, 300:] = image_filtered1
    elif flag == 2:
        pass
    else:
        image_filtered1 = color_filter(image_blured[:, :280], threshold-20)
        image_filtered2[:, :280] = image_filtered1
    image_no_black = remove_black(image_filtered2)
    image_stadium = only_stadium(image_no_black)
    car_hidden = hide_car_head(image_stadium)


    return car_hidden


def cvt_binary(transform_img):  # input : preprocess image
    gray = cv2.cvtColor(transform_img, cv2.COLOR_BGR2GRAY)
    # img_binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)[1]

    return gray


def preprocess(image, device="cpu"):
    image = transforms.functional.to_tensor(image).to(device)
    # image = transforms.functional.normalize(image, [0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    image = image[None, ...]

    return image