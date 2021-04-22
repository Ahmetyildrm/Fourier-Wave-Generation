import cv2
import numpy as np
import math

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
def linspace(a, b, n):
    return [a + (b - a) / (n - 1) * i for i in range(n)]
def full(n, x):
    return n * [x]
def square(center, l, n):
    top_left = (center[0] - l // 2, center[1] + l // 2)
    top = np.stack(
        [np.linspace(top_left[0], top_left[0] + l, n//4 + 1),
         np.full(n//4 + 1, top_left[1])],
         axis=1
    )[:-1]
    left = np.stack(
        [np.full(n//4 + 1, top_left[0]),
         np.linspace(top_left[1], top_left[1] - l, n//4 + 1)],
         axis=1
    )[:-1]
    right = left.copy()
    right[:, 0] += l
    bottom = top.copy()
    bottom[:, 1] -= l
    return np.concatenate([top[::-1], left, bottom, right[::-1]]) ##Saat yönünde
    #return left[::-1] + top + right + bottom[::-1] # Saat yönü tersine
def triangle(center, l):
    distance = l / math.sqrt(3)
    leftCorner = (int(center[0] - distance), int(center[1] + distance//2))
    rightCorner = (int(center[0] + distance), int(center[1] + distance//2))
    top = (center[0], int(center[1] - (l * math.sqrt(3)/2 - distance//2)))
    bottomEdge = get_line(leftCorner[0], leftCorner[1], rightCorner[0], rightCorner[1])
    rightEdge = get_line(rightCorner[0], rightCorner[1], top[0], top[1])
    leftEdge = get_line(top[0], top[1], leftCorner[0], leftCorner[1])
    return np.concatenate([leftEdge[::-1], rightEdge[::-1], bottomEdge[::-1]])
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

class FourierWave():
    def __init__(self, shape, length=1, center=(0, 0), frequencyRatio=1.0, aperture=50, name="", pointList=[]):
        self.shape = shape
        self.length = length
        self.center = center
        self.frequencyRatio = frequencyRatio
        self.aperture = aperture
        if self.shape == "Circle":
            self.numofpointsOnShape = int(math.pi * 2 * self.length)
            self.pointLooper = self.numofpointsOnShape // 4
            self.ShapePoints = [(self.center[0] + math.cos(2 * math.pi / self.numofpointsOnShape * x) * self.length, self.center[1] +
                     math.sin(2 * math.pi / self.numofpointsOnShape * x) * self.length) for x in range(0, self.numofpointsOnShape + 1)]
        if self.shape == "Square":
            self.numofpointsOnShape = self.length*4
            self.pointLooper = 0
            self.ShapePoints = square(self.center, self.length, self.numofpointsOnShape)
        if self.shape == "Triangle":
            #self.numofpointsOnShape = self.length*4
            self.pointLooper = 0
            self.ShapePoints = triangle(self.center, self.length)
        if self.shape == "Custom":
            self.pointLooper = 0
            self.ShapePoints = customShape(pointList)
        self.turnCounter = 0
        self.Heights = []
        self.lengthIncrease = 0
        self.lengthChangeStep = 0
        self.ShapeColor = (105, 105, 105)
        self.WaveColor = (0, 255, 0)
        self.Name = name

    def drawCircle(self, img):
        cv2.circle(img, self.center, self.length, self.ShapeColor, -1)
        cv2.putText(img, str(self.Name), (self.center[0] - 40, self.center[1] - 10), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 0), 2)
        cv2.putText(img, "length: " + str(self.length), (self.center[0] - 64, self.center[1] + self.length + 20), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2)
        cv2.putText(img, "rate: " + str(self.frequencyRatio), (self.center[0] - 50, self.center[1] + self.length + 40), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2)
        cv2.putText(img, "turn: " + str(self.turnCounter), (self.center[0] - 50, self.center[1] + self.length + 60), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2)

    def drawSquare(self, img):
        cv2.rectangle(img, (self.center[0] - self.length//2, self.center[1] - self.length//2), (self.center[0] + self.length//2, self.center[1] + self.length//2), self.ShapeColor, 3)
        cv2.putText(img, str(self.Name), (self.center[0] - self.length//2, self.center[1] + self.length//2), cv2.FONT_HERSHEY_PLAIN, 1.5,
                    (0, 0, 0), 2)
        cv2.putText(img, "length: " + str(self.length), (self.center[0] - self.length//2, self.center[1] + self.length//2 + 20),
                    cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2)
        cv2.putText(img, "rate: " + str(self.frequencyRatio), (self.center[0] - self.length//2, self.center[1] + self.length//2 + 40),
                    cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2)
        cv2.putText(img, "turn: " + str(self.turnCounter), (self.center[0] - self.length//2, self.center[1] + self.length//2 + 60),
                    cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2)

    def drawTriangle(self, img):
        points = triangle(self.center, self.length)
        for i in points:
            cv2.circle(img, tuple(i), 3, self.ShapeColor, -1)
        cv2.putText(img, str(self.Name), (self.center[0] - 40, self.center[1] - 10), cv2.FONT_HERSHEY_PLAIN, 1.5,
                   (0, 0, 0), 2)
        cv2.putText(img, "length: " + str(self.length), (self.center[0] - 50, self.center[1] + self.length//2),
                    cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2)
        cv2.putText(img, "rate: " + str(self.frequencyRatio), (self.center[0] - 50, self.center[1] + self.length//2+20),
                    cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2)
        cv2.putText(img, "turn: " + str(self.turnCounter), (self.center[0] - 50, self.center[1] + self.length//2 + 40),
                    cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2)

    def startProcess(self, img):
        if self.shape == "Circle":
            self.drawCircle(img)
        if self.shape == "Square":
            self.drawSquare(img)
        if self.shape == "Triangle":
            self.drawTriangle(img)
        if self.shape == "Custom":
            for i in (customShape(self.ShapePoints)):
                cv2.circle(img, i, 1, self.ShapeColor, -1)
        pointOnCircle = (int(self.ShapePoints[0][0]), int(self.ShapePoints[0][1]))
        # if int(self.pointLooper) == len(self.CirclePoints) - 1:
        #     self.pointLooper = 0
        #     self.turnCounter += 1
        #     if self.lengthChangeStep != 0:
        #         if self.turnCounter % self.lengthChangeStep == 0:
        #             self.length += self.lengthIncrease

        self.pointLooper += self.frequencyRatio
        try:
            pointOnCircle = (int(self.ShapePoints[int(self.pointLooper)][0]), int(self.ShapePoints[int(self.pointLooper)][1]))
            self.Heights.append(pointOnCircle[1])
        except:
            self.pointLooper = 0
            self.turnCounter += 1
            if self.lengthChangeStep != 0:
                if self.turnCounter % self.lengthChangeStep == 0:
                    self.length += self.lengthIncrease

        if self.shape == "Circle":
            cv2.line(img, self.center, pointOnCircle, (0, 0, 0), 2)

        cnt = 2 * self.length + self.aperture
        if len(self.Heights) > 1100:
            del self.Heights[:10]
        for i in reversed(self.Heights):
            cnt += 1
            cv2.circle(img, (cnt, i), 1, self.WaveColor, -1)


        cv2.line(img, (2 * self.length + self.aperture, pointOnCircle[1]), pointOnCircle, self.WaveColor, 2)
        cv2.circle(img, (2 * self.length + self.aperture, pointOnCircle[1]), 8, self.WaveColor, -1)
        cv2.circle(img, pointOnCircle, 6, (0, 0, 255), -1)
        return img

    def setlengthChange(self, value, step):
        self.lengthIncrease = value
        self.lengthChangeStep = step
        self.ShapePoints = [
            (self.center[0] + math.cos(2 * math.pi / self.numofpointsOnShape * x) * self.length, self.center[1] +
             math.sin(2 * math.pi / self.numofpointsOnShape * x) * self.length) for x in
            range(0, self.numofpointsOnShape + 1)]

    def setShapeColor(self, color):
        self.ShapeColor = color

    def setWaveColor(self, color):
        self.WaveColor = color

    def setName(self, name):
        self.Name = name

    def setShapePoints(self, CoordinateList):
        self.ShapePoints = CoordinateList




