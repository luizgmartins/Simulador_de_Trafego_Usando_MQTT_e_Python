# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 18:56:25 2022

@author: luizg
"""

# Python program to explain cv2.rectangle() method

# importing cv2
import cv2
import time
# path
path = r'C:\Users\luizg\Desktop\casas.png'

# Reading an image in default mode
image = cv2.imread(path)
lines = image.shape[0]
columns = image.shape[1]
print(lines, columns)
# Window name in which image is displayed
window_name = 'Image'
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
# Start coordinate, here (5, 5)
# represents the top left corner of rectangle
start_point = (0, 0)

# Ending coordinate, here (220, 220)
# represents the bottom right corner of rectangle
end_point = (100, 100)

# Blue color in BGR
color = (0, 0, 0)

# Line thickness of 2 px
thickness = 2

# Using cv2.rectangle() method
# Draw a rectangle with blue line borders of thickness of 2 px

meio_lines = int(lines / 2)
for i in range(meio_lines-30, 0,-160):
    print(i)
    if i>=100:
        if i==meio_lines-30:
            image = cv2.line(image, (0,meio_lines), (columns,meio_lines), (0, 255, 255), thickness)
        #superior
        image = cv2.rectangle(image, (0, i), (100, i - 100), color, thickness)
        #inferior
        image = cv2.rectangle(image, (0, lines - i), (100, lines - i + 100), color, thickness)
        #faixas
        image = cv2.line(image, (0, i - 130), (columns, i - 130), (0, 255, 255), thickness)
        image = cv2.line(image, (0, lines - i + 130), (columns, lines - i + 130), (0, 255, 255), thickness)
    else:
        #top
        image = cv2.line(image, (0,i), (columns,i), (0, 0, 0), thickness)
        limite_superior = i
        image = cv2.line(image, (0, lines - i), (columns, lines - i), (0, 0, 0), thickness)
        limite_inferior = lines - i

meio_columns = int(columns / 2)
for i in range(meio_columns-30, 0,-160):
    if i>=100:
        if i==meio_columns-30:
            image = cv2.line(image, (meio_columns, limite_superior), (meio_columns,limite_inferior), (0, 255, 255), thickness)
        #esquerda
        #image = cv2.rectangle(image, (i, 0), (i-100, 100), color, thickness)
        #direita
        #image = cv2.rectangle(image, (columns - i, 0), (columns - i + 100, 100), color, thickness)
        #faixas
        image = cv2.line(image, (i - 130,limite_superior), (i - 130,limite_inferior), (0, 255, 255), thickness)
        image = cv2.line(image, (columns - i + 130,limite_superior), (columns - i + 130,limite_inferior), (0, 255, 255), thickness)
    else:
        image = cv2.line(image, (i,limite_superior), (i,limite_inferior), (0, 0, 0), thickness)
        limite_esquerda = i
        image = cv2.line(image, (columns - i,limite_superior), (columns - i,limite_inferior), (0, 0, 0), thickness)
        limite_direita = columns - i
        
        image = cv2.rectangle(image, (0, limite_superior - 1), (i-2, limite_inferior + 1), (255, 255, 255), -1)
        image = cv2.rectangle(image, (columns - i + 2, limite_superior - 1), (columns, limite_inferior + 1), (255, 255, 255), -1)

#primeiro quarteirão
#image = cv2.rectangle(image, (0, 0), (100, 100), color, thickness)
#segundo quarteirão
#image = cv2.rectangle(image, (0, 160), (100, 250), color, thickness)
#image = cv2.line(image, (0,130), (columns,130), (0, 255, 255), thickness)
atual=10
anterior=atual
atual2=580
anterior2=atual2
passo=50
#max 587
while 1:
    #indo à direita
    image = cv2.circle(image, (anterior, 145), 10, (255, 255, 255), -1)
    image = cv2.circle(image, (atual, 145), 10, (0, 255, 0), -1)
    anterior = atual
    cv2.imshow(window_name, image)
    if atual<=(587-passo):
        atual+=passo
    else:
        atual=10
    #indo à esquerda
    image = cv2.circle(image, (anterior2, 115), 10, (255, 255, 255), -1)
    image = cv2.circle(image, (atual2, 115), 10, (0, 255, 0), -1)
    anterior2 = atual2
    cv2.imshow(window_name, image)
    if atual2>=(passo):
        atual2-=passo
    else:
        atual2=580   
    
    key = cv2.waitKey(1)
    if key == 27:
        break
    time.sleep(1)

# Displaying the image
#cv2.imshow(window_name, image)
#cv2.waitKey(0)
cv2.destroyAllWindows()
