# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 20:29:44 2022

@author: luizg
"""

import numpy as np
import cv2 as cv
def nothing(x):
    pass
path = r'C:\Workspace\Simulador_de_Trafego_Usando_MQTT_e_Python\Novapasta\we.png'
# Create a black image, a window
img = cv.imread(path)
cv.namedWindow('image', cv.WINDOW_NORMAL)
# create trackbars for color change
cv.createTrackbar('Q','image',0,2,nothing)
while(1):
    cv.imshow('image',img)
    k = cv.waitKey(1) & 0xFF
    # if press n
    if k == 110:
        break
    # get current positions of four trackbars
    q = cv.getTrackbarPos('Q','image')
print(q)
if k == 27:
    cv.destroyAllWindows()
else:
    cv.destroyWindow('image')
    cv.namedWindow('image', cv.WINDOW_AUTOSIZE)
    if q == 0:
        cv.createTrackbar('Carros','image',0,30,nothing)
    elif q == 1:
        cv.createTrackbar('Carros','image',0,60,nothing)
    elif q == 2:
        cv.createTrackbar('Carros','image',0,90,nothing)
    k = 0
    img2 = np.zeros((1,200,3), np.uint8)
    while (1):
        cv.imshow('image',img2)
        k = cv.waitKey(1) & 0xFF
        c = cv.getTrackbarPos('Carros','image')
        if k == 110:
            break
cv.destroyAllWindows()

print(q, c)