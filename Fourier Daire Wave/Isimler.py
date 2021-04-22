import cv2
import numpy as np
import math
import CircleToWaveModule as ctw


def magnify(list, scale):
    return [(int(scale*x), int(scale*y)) for x, y in list]

Ahmet = [(13, 45), (22, 25), (31, 45), (28, 38), (16, 38), (28, 38), (31, 45), (40, 45), (40, 25), (40, 35), (57, 35), (57, 25), (57, 45), (67, 45), (67, 25), (77, 43), (87, 25), (87, 45), (111, 45), (99, 45), (99, 35), (107, 35), (99, 35), (99, 25), (111, 25), (132, 25), (122, 25), (122, 47)]
Huseyin = [(15, 25), (15, 45), (15, 35), (31, 35), (31, 25), (31, 45), (43, 45), (43, 25), (43, 45), (60, 45), (60, 25), (80, 25), (68, 25), (68, 35), (80, 35), (80, 45), (68, 45), (80, 45), (105, 45), (93, 45), (93, 35), (100, 35), (93, 35), (93, 25), (105, 25), (110, 25), (115, 35), (115, 45), (115, 35), (120, 25), (125, 25), (125, 45), (135, 45), (135, 25), (145, 45), (145, 25)]
Besgen = [(40, 7), (63, 25), (55, 53), (25, 53), (17, 25), (40, 7)]
Yildiz4 = [(48, 9), (53, 28), (72, 34), (53, 39), (48, 59), (41, 39), (24, 34), (41, 28), (48, 9)]
Yildiz5 = [(46, 14), (51, 31), (71, 31), (55, 39), (61, 55), (47, 44), (32, 56), (38 ,39), (23, 30), (42, 30), (46, 14)]
Kalp = [(52, 23), (57, 15), (64, 9), (75, 9), (78, 21), (77, 37), (71, 45), (65, 52), (52, 58), (46, 54), (33, 44), (28, 34), (26, 21), (30, 12), (38, 9), (43, 11), (50, 17), (52, 23)]

Ahmet1 = magnify(Ahmet, 1)
AhmetShape = ctw.FourierWave("Custom", pointList=Kalp, aperture=150, frequencyRatio=1.0)

height = 700
width = 1200

img = np.zeros((height, width, 3), np.uint8)
img_tmp = img.copy()


while True:
    img = img_tmp.copy()
    cv2.putText(img, "Ahmet Yildirim", (1070, 680), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)

    AhmetShape.startProcess(img)


    cv2.imshow("Fourier", img)
    cv2.waitKey(1)
