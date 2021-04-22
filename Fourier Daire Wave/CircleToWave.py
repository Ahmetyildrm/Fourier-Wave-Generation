import cv2
import numpy as np
import math


def PointsInCircum(r, n, centerX, centerY): # Çemberin çeperinin koordinatlarını verir
    return [(centerX + math.cos(2*math.pi/n*x)*r, centerY + math.sin(2*math.pi/n*x)*r) for x in range(0, n+1)]

radius = 10
bg = np.zeros((1000, 1800, 3), np.uint8)
h, w, c = bg.shape
center = (radius+5, h//2)
cv2.circle(bg, center, radius, (255, 255, 255), -1)
numofpointsOnCircle = 1000
CirclePoints = PointsInCircum(radius, numofpointsOnCircle, center[0], center[1])
pointLooper = numofpointsOnCircle//4
Heights = []
pointOnCircle = center
aperture = 50 #  Aperture between point on circle and wave beginning

font = cv2.FONT_HERSHEY_PLAIN
frequencyRatio = 18.0
circleCounter = 0

while True:
    center = (radius + 5, h // 2)
    cv2.circle(bg, center, radius, (255, 255, 255), -1)
    numofpointsOnCircle = 1000
    CirclePoints = PointsInCircum(radius, numofpointsOnCircle, center[0], center[1])
    bg = np.zeros((1000, 1800, 3), np.uint8)
    cv2.putText(bg, "Radius: " + str(radius), (20, 20), font, 1.5, (255, 0, 0), 2)
    #cv2.putText(bg, "Frequency Ratio: " + str(frequencyRatio), (w-500, 50), font, 1.5, (255, 0, 0), 2)

    cv2.circle(bg, center, radius, (255, 255, 255), -1)
    if int(pointLooper) >= len(CirclePoints) - 1:
        pointLooper = 0
        circleCounter += 1
        if circleCounter % 2 == 0:
            radius += 5

    pointLooper += frequencyRatio
    try:
        if round(pointLooper, 2).is_integer():
            pointOnCircle = (int(CirclePoints[int(pointLooper)][0]), int(CirclePoints[int(pointLooper)][1]))
            Heights.append(pointOnCircle[1])
    except : pass

    cv2.line(bg, center, pointOnCircle, (0, 0, 0), 2)

    cnt = 2*radius+aperture
    for i in reversed(Heights):
        cnt += 1
        cv2.circle(bg, (cnt, i), 2, (0, 255, 0), -1)
    cv2.line(bg, (2*radius+aperture, pointOnCircle[1]), pointOnCircle, (255, 0, 0), 2)
    cv2.circle(bg, (2*radius+aperture, pointOnCircle[1]), 8, (255, 0, 0), -1)
    cv2.circle(bg, pointOnCircle, 6, (0, 0, 255), -1)

    cv2.imshow("Window", bg)
    cv2.waitKey(1)