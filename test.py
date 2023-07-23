import cv2
import numpy as np
import serial
import middle
import camera

width = 640
height = 480

p1 = [130., 240.]  # 좌상
p2 = [480., 240.]  # 우상
p3 = [602., 480.]  # 우하
p4 = [38., 480.]  # 좌하

image_p1 = [round(width * 0.2), round(height * 0.0)]
image_p2 = [round(width * 0.8), round(height * 0.0)]
image_p3 = [round(width * 0.8), height]
image_p4 = [round(width * 0.2), height]

capture = camera.CameraModule(width=640, height=480)
capture.open_cam(1)

while True:
    # (1) 원본 cam1_origin
    cam1_origin = capture.read()
    # captured_frame = capture2.read()
    # output_frame = captured_frame.copy()
    bias1 = 0
    bias2 = 0
    # (2) Bird Eye View 변환
    corner_points_arr = np.float32([p1, p2, p3, p4])
    image_params = np.float32([image_p1, image_p2, image_p3, image_p4])
    mat = cv2.getPerspectiveTransform(corner_points_arr, image_params)
    cam2_bird = cv2.warpPerspective(cam1_origin, mat, (width, height))

    cv2.imshow("cam_test1", cam1_origin)
    cv2.imshow("cam_test2", cam2_bird)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

capture.release()
# capture2.release()
cv2.destroyAllWindows()