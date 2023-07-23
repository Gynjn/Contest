import camera
import cv2
import numpy as np
import camera
from time import sleep
# capture = camera.CameraModule(width=640, height=480)
# capture.open_cam(1)

def stopping(capture):
# def stopping():
    while True:
        cam_img = capture.read()
        # Convert the image to HSV color space
        hsv_image = cv2.cvtColor(cam_img, cv2.COLOR_BGR2HSV)

        # Define the lower and upper thresholds for the green color
        lower_green = np.array([35, 150, 0])
        upper_green = np.array([90, 255, 255])

        # Apply a mask to the HSV image using the green color range
        green_mask = cv2.inRange(hsv_image, lower_green, upper_green)

        # Apply morphological operations to enhance the circular shape
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_OPEN, kernel)

        # Apply the Hough Circle Transform
        circles = cv2.HoughCircles(green_mask, cv2.HOUGH_GRADIENT, dp=2, minDist=50, param1=50, param2=30, minRadius=10, maxRadius=30)

        # Process the detected circles
        if circles is not None:
            # circles = np.round(circles[0, :]).astype("int")  # Convert the (x, y, r) values to integers
            print("detect!!!")
            break
        else:
            sleep(0.03)
            # continue
        #     for (x, y, radius) in circles:
        #         cv2.circle(cam_img, (x, y), radius, (0, 255, 0), 2)  # Draw a green circle with a thickness of 2
        #
        # # Display the image with detected circles
        # cv2.imshow('Detected Circles', cam_img)
        #
        # if cv2.waitKey(30) & 0xFF == ord('q'):
        #     # print(end_message)
        #     capture.close_cam()
        #     cv2.destroyAllWindows()
        #     break
    return 3


