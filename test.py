import cv2
import numpy as np

frameWidth = 640
frameHeight = 480

cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

while True:
    success, img = cap.read()
    blurred_img = cv2.GaussianBlur(img, (5, 5), 0)
    hsv = cv2.cvtColor(blurred_img, cv2.COLOR_BGR2HSV)

    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    centre = 0
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for contour in contours:
        area = cv2.contourArea(contour)

        # compute the center of the contour
        if area > 1000:
            M = cv2.moments(contour)
            contourX = int(M["m10"] / M["m00"])
            contourY = int(M["m01"] / M["m00"])
            cv2.drawContours(img, contour, -1, (0, 255, 0), 3)
            cv2.circle(img, (contourX, contourY), 7, (255, 255, 255), -1)
            centre += 1

            if centre == 1:
                centreX1 = contourX
                centreY1 = contourY
            if centre == 2:
                centreX2 = contourX
                centreY2 = contourY
                cv2.line(img, (centreX1, centreY1), (centreX2, centreY2), (0, 0, 255), 5)


    cv2.imshow("Frame", img)
    cv2.imshow("Mask", mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
