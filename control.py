from utility2 import *
import numpy as np

def strengthen_control(road_direction, road_gradient, bottom_value): # 차선에 너무 근접한 경우 방향 수정값 증가
    # right_threshold = (370, 450, 530) ## threshold 값을 4등분해서 각 구간에 들어가면 weight값에 따라 방향 보정
    # left_threshold = (100, 150, 250, )
    middle_lane_offset = 293
    middle_threshold = (-60, -30, -10, -5, +5, +10, +30, +60)
    middle_threshold = np.array(middle_threshold)
    middle_threshold += middle_lane_offset


    road_bias = (-4, -3, -2, -1, 0, 1, 2, 3, 4)

    # middle_threshold = (250, 280, 300, 310, 330, 340, 360, 390)
    road_weight = 1 - abs(road_direction) * 0.1
    left_idx, right_idx = find_nearest(bottom_value, middle_lane_offset)
    # print("left_idx : ", left_idx)
    # print("right_idx : ", right_idx)
    if left_idx == None or right_idx == None:
        if road_gradient < 0:
            direction = -7
        else:
            direction = 7
    else:
        middle_lane = center_point(left_idx, right_idx)
        # print("middle lane : ",middle_lane)

        if middle_threshold[0] > middle_lane:
            direction = road_direction + road_bias[0] * road_weight
        elif middle_threshold[0] <= middle_lane and middle_lane < middle_threshold[1]:
            direction = road_direction + road_bias[1] * road_weight
        elif middle_threshold[1] <= middle_lane and middle_lane < middle_threshold[2]:
            direction = road_direction + road_bias[2] * road_weight
        elif middle_threshold[2] <= middle_lane and middle_lane < middle_threshold[3]:
            direction = road_direction + road_bias[3] * road_weight
        elif middle_threshold[3] <= middle_lane and middle_lane < middle_threshold[4]:
            direction = road_direction + road_bias[4] * road_weight
        elif middle_threshold[4] <= middle_lane and middle_lane < middle_threshold[5]:
            direction = road_direction + road_bias[5] * road_weight
        elif middle_threshold[5] <= middle_lane and middle_lane < middle_threshold[6]:
            direction = road_direction + road_bias[6] * road_weight
        elif middle_threshold[6] <= middle_lane and middle_lane < middle_threshold[7]:
            direction = road_direction + road_bias[7] * road_weight
        elif middle_threshold[7] <= middle_lane:
            direction = road_direction + road_bias[8] * road_weight


    # print("gradient_direction : ", road_direction)
    # print("bias_direction : ", direction - road_direction)


    direction = 7 if direction >= 7 else direction
    direction = -7 if direction <= -7 else direction

    return round(direction)

# from def total_control(road_direction, model_direction, bottom_value, road_gradient):
#     road_direction = strengthen_control(road_direction, road_gradient, bottom_value)
#     final_direction = control_correction(road_direction, model_direction)
#     print("model_direction : ",model_direction)
#     print("final_direction:", final_direction)
#     return road_direction

def smooth_direction(bef1, bef2, bef3, cur):
    # if abs(bef3) + abs(cur) >= 8:
    #     cur = cur * 0.8
    if cur > 0:
        average = bef3 * 0.05 + bef2 * 0.15 + bef1 * 0.20 + cur * 0.60
    else:
        average = bef3 * 0.05 + bef2 * 0.15 + bef1*0.20 + cur * 0.60
    # average = bef3 * 0.05 + bef2 * 0.15 + bef1*0.25 + cur * 0.55
    return round(average)


def box_control(box):
    bottom_x = box[2].item()
    bottom_x + 80
    base_bottom_x = 310
    direction_bias = (bottom_x - base_bottom_x) * 7 / 160
    # print("direction bias :", direction_bias)

    direction = int(direction_bias)
    direction = 7 if direction >= 7 else direction
    direction = -7 if direction <= -7 else direction
    print(direction + 3)
    return direction+3