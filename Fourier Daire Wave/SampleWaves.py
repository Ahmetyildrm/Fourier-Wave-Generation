import cv2
import numpy as np
import math
import CircleToWaveModule as ctw

Triangle1 = ctw.FourierWave("Triangle", 50, (100, 60), 3.0, 100)  # Create Triangle
Square1 = ctw.FourierWave("Square", 100, (100, 300), 1.0, 0)  # Create Square
Circle1 = ctw.FourierWave("Circle", 50, (100, 500), 1.0, 100)  # Create Circle

height = 700
width = 1200

img = np.zeros((height, width, 3), np.uint8)
img_tmp = img.copy()


for i in range(200, width, 50):
    cv2.line(img_tmp, (i, 0), (i, height), (25, 25, 25), 2)
for i in range(0, height, 50):
    cv2.line(img_tmp, (200, i), (width, i), (25, 25, 25), 2)

while True:
    img = img_tmp.copy()
    cv2.putText(img, "Ahmet Yildirim", (1070, 680), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)

    Triangle1.setWaveColor((255, 0, 0))
    Triangle1.startProcess(img)

    Square1.setWaveColor((0, 0, 255))
    Square1.startProcess(img)

    Circle1.setWaveColor((255, 0, 255))
    Circle1.setShapeColor((200, 100, 150))
    Circle1.startProcess(img)

    cv2.imshow("Fourier", img)
    cv2.waitKey(1)

