import cv2
import numpy as np

def roi_cutting(image, cutting_idx = 200):
    image = image[cutting_idx:]
    return image

def box_center(box):
    if box == None:
        return None

    p1, p2 = (int(box[0]), int(box[1])), (int(box[2]), int(box[3]))
    return (int((p1[0] + p2[0]) / 2), int((p1[1] + p2[1]) / 2))


def box_area(box):
    if box == None:
        return 0
    p1, p2 = (int(box[0]), int(box[1])), (int(box[2]), int(box[3]))
    box_area = (p2[0] - p1[0]) * (p2[1] - p1[1])
    return box_area


def show_bounding_box(image, pred):
    labels_to_names = {0: "Crosswalk", 1: "Green", 2: "Red", 3: "Car"}

    for *box, cf, cls in pred:
        cf = cf.item()
        cls = int(cls.item())
        p1, p2 = (int(box[0]), int(box[1])), (int(box[2]), int(box[3]))
        # if (cls == 3):
            # print(box_center(box), box_area(box))
        caption = "{}: {:.4f}".format(labels_to_names[cls], cf)

        cv2.rectangle(image, p1, p2, color=(0, 255, 0), thickness=2)
        cv2.putText(image, caption, (p1[0], p1[1] - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), thickness=1)

    return image


def center_inside(center, xmin=130, xmax=400, ymin=150):
    x = center[0]
    y = center[1]

    if xmin < x and x < xmax and y > ymin:
        return True
    else:
        return False


def center_inside2(center):
    x = center[0]
    y = center[1]

    if 40 < x and x < 440 and y > 150:
        return True
    else:
        return False


def object_detection(pred):  # pred 중 class별로 가장 큰 bbox return
    flag = 0
    pred_array = [None, None, None, None]  # 0:Crosswalk, 1:Green, 2:Red, 3:Car
    bbox_threshold = [15000, 5000, 5000, 13000]  # bbox area

    for *box, cf, cls in pred:
        bbox_area = box_area(box)

        cls = int(cls)

        # print("bbox area of {}: {}".format(cls, bbox_area))
        if cls == 0:
            # print("cross walk points : ", box)
            y2_crosswalk = int(box[3])
            # print("y2_cw : ", y2_crosswalk)
        if bbox_area > bbox_threshold[cls] and cls != 3:  # find object
            if pred_array[cls] != None and box_area(pred_array[cls]) > bbox_area:
                pass
            else:
                pred_array[cls] = box

        elif (cls == 3 and center_inside(box_center(box)) and
              box_area(box) > bbox_threshold[cls]):  # find object(car)
            pred_array[cls] = box
    if pred_array[3] != None:
        flag = 1
    # if (pred_array[0] != None) and (pred_array[2] != None) and (y2_crosswalk > 430):  # and y2_crosswalk > 300
    #     order_flag = 0
    #     # print("over 430")
    # elif pred_array[3] != None:
    #     order_flag = 2
    # else:
    #     order_flag = 1
    # if (pred_array[0] != None) and (y2_crosswalk > 330):
    #     is_crosswalk = True
    # else:
    #     is_crosswalk = False
    # # print("order flag: ", order_flag)
    return pred_array, flag
    # return pred_array, order_flag, is_crosswalk

def is_outside(image): # Is current line outside?
    HSV_frame = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    H,S,V = cv2.split(HSV_frame)

    # bottom_green_x = -1
    # top_green_x = -1
    # up_start_time = time.time()

    H_satisfied = (30 < H) & (H<80)
    S_satisfied = S==100+2
    V_satisfied = V==100
    satisfied = H_satisfied & S_satisfied & V_satisfied
    satisfied[:,639] = True
    check_top_green = len(np.where(satisfied[0])[0])
    first_green_x = np.argmax(satisfied, axis = 1).reshape(480, 1)
    if np.percentile(first_green_x,5) == 639:
        return 0

    else:
        return 1