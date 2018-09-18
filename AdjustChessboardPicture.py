import cv2
import numpy as np
from random import randint

width = 800
height = 600
heightafter = 400

def find_random_parameters(gray):
    p1 = randint(80,100)
    p2 = randint(80,100)
    p3 = randint(100,400)
    p4 = randint(100,400)
    edges = cv2.Canny(gray,p1,p2,apertureSize = 3)
    lines = cv2.HoughLines(edges,1,np.pi/p3,p4)
    print(f'Parameters selected: {p1} {p1} {p3} {p4}')
    return lines

def calculateLineParameters(rho, theta):
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))
    return (x1,y1,x2,y2)

def addLineToImage(img, rho, theta, color):
    (x1,y1,x2,y2) = calculateLineParameters(rho, theta)
    cv2.line(img,(x1,y1),(x2,y2),color ,2)

def find_lines_on_chessboard(img):    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    number_of_lines = 0

    lines = []
    while number_of_lines < 50 or number_of_lines > 80:
        lines = find_random_parameters(gray)
        number_of_lines = len(lines) if lines is not None else 0
        print(f'Looking for right number of lines: {number_of_lines}')    

    print(f'Done -----------------------------------------------------------------------------------') 
    return lines

def find_limit_lines_on_chessboard(img):
    lines = find_lines_on_chessboard(img)

    yMin = height
    yMax = 0
    xMin = height
    xMax = 0

    xMinLine = (0,0)
    xMaxLine = (0,0)
    yMinLine = (0,0)
    yMaxLine = (0,0)


    for line in lines:
        for rho,theta in line:                         
            (x1,y1,x2,y2) = calculateLineParameters(rho, theta)
            if  theta < 0.7 or theta > 2.5 :
                if min(x1,x2) < xMin:
                    xMin = min(x1,x2)
                    xMinLine = rho, theta
                if max(x1,x2) > xMax:
                    xMax = max(x1,x2) 
                    xMaxLine = rho, theta
            if  theta > 1.55 and theta < 1.58 :               
                if min(y1,y2) < yMin:
                    yMin = min(y1,y2)
                    yMinLine = rho, theta
                if max(y1,y2) > yMax:
                    yMax = max(y1,y2)
                    yMaxLine = rho, theta 

    print(f'xMin {xMin} yMin {yMin} xMax {xMax} yMax {yMax}')
    return (xMinLine, xMaxLine, yMinLine, yMaxLine)

def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    if x < 0:
        x = 0
    if x > width:
        x = width
    if y < 0:
        y = 0
    if y > height:
        y = height
    return x, y

def get_corners(xMinLine, xMaxLine, yMinLine, yMaxLine):
    line1 = np.zeros((2,2))
    line2 = np.zeros((2,2))
    (line1[0][0],line1[0][1],line1[1][0],line1[1][1]) = calculateLineParameters(xMinLine[0], xMinLine[1])
    (line2[0][0],line2[0][1],line2[1][0],line2[1][1]) = calculateLineParameters(yMinLine[0], yMinLine[1])
    (x1,y1) = line_intersection(line1, line2)

    (line1[0][0],line1[0][1],line1[1][0],line1[1][1]) = calculateLineParameters(xMaxLine[0], xMaxLine[1])
    (line2[0][0],line2[0][1],line2[1][0],line2[1][1]) = calculateLineParameters(yMinLine[0], yMinLine[1])
    (x2,y2) = line_intersection(line1, line2)

    (line1[0][0],line1[0][1],line1[1][0],line1[1][1]) = calculateLineParameters(xMinLine[0], xMinLine[1])
    (line2[0][0],line2[0][1],line2[1][0],line2[1][1]) = calculateLineParameters(yMaxLine[0], yMaxLine[1])
    (x3,y3) = line_intersection(line1, line2)

    (line1[0][0],line1[0][1],line1[1][0],line1[1][1]) = calculateLineParameters(xMaxLine[0], xMaxLine[1])
    (line2[0][0],line2[0][1],line2[1][0],line2[1][1]) = calculateLineParameters(yMaxLine[0], yMaxLine[1])
    (x4,y4) = line_intersection(line1, line2)

    print(f'corners {x1},{y1}  {x2},{y2}  {x3},{y3}  {x4},{y4}  ')
    return ([x1 - 15,y1-15],[x2 + 15,y2 - 15],[x3 - 15,y3 + 15],[x4 + 15,y4 + 15])
    #return ([x1 ,y1],[x2,y2],[x3,y3],[x4,y4])

img = cv2.imread('tst_r_0.png')
img = cv2.resize(img, (width,height))
(xMinLine, xMaxLine, yMinLine, yMaxLine) = find_limit_lines_on_chessboard(img)
corners = get_corners(xMinLine, xMaxLine, yMinLine, yMaxLine)
pts1 = np.float32([corners[0],corners[1],corners[2],corners[3]])
pts2 = np.float32([[0,0],[width,0],[0,heightafter],[width,heightafter]])

M = cv2.getPerspectiveTransform(pts1,pts2)
dst = cv2.warpPerspective(img,M,(width,heightafter))

cv2.imshow('Corner', dst)

img = cv2.imread('tst_0.png')
img = cv2.resize(img, (width,height))
(xMinLine, xMaxLine, yMinLine, yMaxLine) = find_limit_lines_on_chessboard(img)
corners = get_corners(xMinLine, xMaxLine, yMinLine, yMaxLine)
pts1 = np.float32([corners[0],corners[1],corners[2],corners[3]])
pts2 = np.float32([[0,0],[width,0],[0,heightafter],[width,heightafter]])

M = cv2.getPerspectiveTransform(pts1,pts2)
dst = cv2.warpPerspective(img,M,(width,heightafter))

gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)

cv2.imshow('Corner1', dst)

cv2.waitKey(0)

