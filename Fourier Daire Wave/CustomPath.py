import cv2
import numpy as np
import math
import CircleToWaveModule as ctw

## Double click to create path point
## Press 's' to start simulation
## Press 'd' to recreate your path

def get_line(x1, y1, x2, y2):
    points = []
    issteep = abs(y2-y1) > abs(x2-x1)
    if issteep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    rev = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        rev = True
    deltax = x2 - x1
    deltay = abs(y2-y1)
    error = int(deltax / 2)
    y = y1
    ystep = None
    if y1 < y2:
        ystep = 1
    else:
        ystep = -1
    for x in range(x1, x2 + 1):
        if issteep:
            points.append((y, x))
        else:
            points.append((x, y))
        error -= deltay
        if error < 0:
            y += ystep
            error += deltax
    # Reverse the list if the coordinates were reversed
    if rev:
        points.reverse()
    return points

def customShape(pointList):
    all_points = []
    final_list = []
    for i in range(len(pointList)-1):
        all_points.append(get_line(pointList[i][0], pointList[i][1], pointList[i+1][0], pointList[i+1][1]))
    #all_points.append(get_line(pointList[-1][0], pointList[-1][1], pointList[0][0], pointList[0][1]))
    flat_list = [item for sublist in all_points for item in sublist]
    for j in range(len(flat_list) - 1):
        if flat_list[j] != flat_list[j+1]:
            final_list.append(flat_list[j])
    return final_list

def draw_circle(event, x, y, flags,param):
    global mouseX, mouseY
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(img_tmp, (x, y), 2, (255, 0, 0), -1)
        mouseX, mouseY = x, y
        points.append((mouseX, mouseY))

points = []
height = 700
width = 1200

img = np.zeros((height, width, 3), np.uint8)
img_tmp = img.copy()

cv2.namedWindow('Fourier')
cv2.setMouseCallback('Fourier', draw_circle)

for i in range(150, width, 50):
    cv2.line(img_tmp, (i, 0), (i, height), (25, 25, 25), 2)
for i in range(0, height, 50):
    cv2.line(img_tmp, (150, i), (width, i), (25, 25, 25), 2)
k = img_tmp.copy()
startWorking = False
while True:
    img = img_tmp.copy()
    cv2.putText(img, "Ahmet Yildirim", (1070, 680), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
    if len(points) != 0:
        final = customShape(points)
        for i in final:
            cv2.circle(img, i, 1, (0, 105, 0), -1)

    if startWorking:
        RandomShape1.startProcess(img)

    if cv2.waitKey(1) == ord("s"):
        startWorking = True
        RandomShape1 = ctw.FourierWave("Custom", pointList=points, aperture=150)

    if cv2.waitKey(1) == ord("d"):
        startWorking = False
        img_tmp = k.copy()
        points = []
    cv2.imshow("Fourier", img)
    cv2.waitKey(1)

