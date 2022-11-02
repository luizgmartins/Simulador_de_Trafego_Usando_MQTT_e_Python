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
image2 = image.copy() - image
lines = image.shape[0]
columns = image.shape[1]
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
aux = 0
#min = 60 max < menor_valor(((columns/2)-90),((lines/2)-90))
quarteirao = 100

meio_lines = int(lines / 2)       
meio_columns = int(columns / 2)
for i in range(meio_lines-30, 0,-(quarteirao+60)):
    if i>=quarteirao:
        for j in range(meio_columns-30, 0,-(quarteirao+60)):
            if aux == 0:
                aux=1
            if j>=quarteirao:
                #superior esquerda
                image = cv2.rectangle(image, (j, i), (j-quarteirao, i-quarteirao), color, thickness)
                #superior direita
                image = cv2.rectangle(image, (columns - j, i), (columns - j + quarteirao, i - quarteirao), color, thickness)
                #inferior esquerda
                image = cv2.rectangle(image, (j, lines - i), (j-quarteirao, lines - i + quarteirao), color, thickness)
                #inferior direita
                image = cv2.rectangle(image, (columns - j, lines - i), (columns - j + quarteirao, lines - i + quarteirao), color, thickness)
        if aux == 1:
            image = cv2.line(image, (j, 0), (j,lines), (0, 0, 0), thickness)
            limite_esquerda = j
            image = cv2.line(image, (columns - j,0), (columns - j,lines), (0, 0, 0), thickness)
            limite_direita = columns - j
            aux = 2
image = cv2.line(image, (0,i), (columns,i), (0, 0, 0), thickness)
limite_superior = i
image = cv2.line(image, (0, lines - i), (columns, lines - i), (0, 0, 0), thickness)
limite_inferior = lines - i
image = cv2.rectangle(image, (0, limite_superior - 1), (limite_esquerda-2, limite_inferior + 1), (255, 255, 255), -1)
image = cv2.rectangle(image, (limite_direita + 2, limite_superior - 1), (columns, limite_inferior + 1), (255, 255, 255), -1)
image = cv2.rectangle(image, (limite_esquerda - 1, 0), (limite_direita + 1, limite_superior - 2), (255, 255, 255), -1)
image = cv2.rectangle(image, (limite_esquerda - 1, limite_inferior + 2), (limite_direita + 1, columns), (255, 255, 255), -1)
print(limite_esquerda,limite_direita,limite_superior,limite_inferior)

k=limite_esquerda + 30
aux2 = 1
RuaVertical = [] 
while(k<limite_direita):
    rua = 'Rua Vertical ' + str(aux2)
    image = cv2.putText(image, rua, (k, meio_lines-quarteirao), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
    # image = cv2.circle(image, (k , meio_lines-quarteirao), 5, (255, 0, 0), -1)
    RuaVertical.append(k)
    k+= quarteirao + 60
    aux2+=1
print(RuaVertical)
k=limite_superior + 30
aux3 = 1
RuaHorizontal = [] 
print(meio_lines)
while(k<limite_inferior):
    rua = 'Rua Horizontal ' + str(aux3)
    image = cv2.putText(image, rua, (meio_columns-quarteirao, k), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
    # image = cv2.circle(image, (meio_columns-quarteirao, k), 5, (255, 0, 0), -1)
    RuaHorizontal.append(k)
    k+= quarteirao + 60
    aux3+=1

atual=limite_esquerda+15
anterior=atual
atual2=580
anterior2=atual2
passo=15
#max 587
while 1:
    #indo à direita
    image2 = cv2.circle(image2, (anterior, RuaHorizontal[0] + 15), 10, (0, 0, 0), -1)
    image2 = cv2.circle(image2, (atual, RuaHorizontal[0] + 15), 10, (255, 0, 255), -1)
    #image3 =  image - image2
    anterior = atual
    #cv2.imshow(window_name, image3)
    if atual<=(limite_direita):
        atual+=passo*6
    else:
        atual=limite_esquerda+15
    #indo à esquerda
    image2 = cv2.circle(image2, (anterior2, 115), 10, (0, 0, 0), -1)
    image2 = cv2.circle(image2, (atual2, 115), 10, (255, 255, 0), -1)
    anterior2 = atual2
    image3 = image - image2   
    cv2.imshow(window_name, image3)
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
