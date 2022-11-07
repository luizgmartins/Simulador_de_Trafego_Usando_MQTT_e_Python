"""
Created on Tue Oct 25 18:56:22 2022

@author: luizg
"""

import cv2
import time
from random import randint
path = r'C:\Users\luizg\Desktop\casas.png'

image = cv2.imread(path)
image2 = image.copy() - image
lines = image.shape[0]
columns = image.shape[1]
window_name = 'Image'
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)

# Blue color in BGR
color = (0, 0, 0)
thickness = 2
aux = 0
#min = 60 max < menor_valor(((columns/2)-90),((lines/2)-90))
quarteirao = 90
meio_lines = int(lines / 2)       
meio_columns = int(columns / 2)

# =============================================================================
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
image = cv2.line(image, (0, lines - i), (columns, lines - i), (0, 0, 0), thickness)
limite_superior = i
limite_inferior = lines - i
image = cv2.rectangle(image, (0, limite_superior - 1), (limite_esquerda-2, limite_inferior + 1), (255, 255, 255), -1)
image = cv2.rectangle(image, (limite_direita + 2, limite_superior - 1), (columns, limite_inferior + 1), (255, 255, 255), -1)
image = cv2.rectangle(image, (limite_esquerda - 1, 0), (limite_direita + 1, limite_superior - 2), (255, 255, 255), -1)
image = cv2.rectangle(image, (limite_esquerda - 1, limite_inferior + 2), (limite_direita + 1, columns), (255, 255, 255), -1)
# =============================================================================

print('esq:',limite_esquerda, 'dir:', limite_direita, 'sup:', limite_superior, 'inf:', limite_inferior)

# =============================================================================
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
k=limite_superior + 30
aux3 = 1
RuaHorizontal = [] 
while(k<limite_inferior):
    rua = 'Rua Horizontal ' + str(aux3)
    image = cv2.putText(image, rua, (meio_columns-quarteirao, k), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
    # image = cv2.circle(image, (meio_columns-quarteirao, k), 5, (255, 0, 0), -1)
    RuaHorizontal.append(k)
    k+= quarteirao + 60
    aux3+=1
# =============================================================================
limites = []
limites.append(limite_direita)
limites.append(limite_esquerda)
limites.append(limite_superior)
limites.append(limite_inferior)


atual=limite_esquerda+15
anterior=atual
atual2=limite_direita-15
anterior2=atual2
passo=30
#max 587
direcao = 2
sentido = -1
velocidade = 1
aux4 = 1

# =============================================================================
def movimento_carro(image2, RuaHorizontal, RuaVertical, quarteirao, atual, direcao_atual, prox_direcao, passo, velocidade, x, y, i, j, limites):
    X_MAX = ((quarteirao/passo)*(len(RuaVertical)-1)) + (len(RuaVertical) * 2) -1
    Y_MAX = ((quarteirao/passo)*(len(RuaHorizontal)-1)) + (len(RuaHorizontal) * 2)-1
    print(X_MAX)
    anterior = atual
    #Mover o carro para direita do mapa
    if(prox_direcao == 0):
        if(x < X_MAX):
            print(RuaHorizontal[len(RuaHorizontal)-1])
            if((atual+(passo*velocidade)) < (RuaVertical[i])):
                atual += (passo*velocidade)
                image2 = direcao_Horizontal(image2, anterior, atual, RuaHorizontal, j, z=1)
                x += velocidade
                if(velocidade<5):velocidade+=1
            else:
                if(direcao_atual == 0):
                    if((atual + (passo*velocidade)) > limites[0]):
                        for index in range(1,6):
                            if(((atual + (passo*velocidade)) < limites[0]) or (velocidade == 1)): break
                            else: velocidade-=1
                        atual += (passo*velocidade)
                        image2 = direcao_Horizontal(image2, anterior, atual, RuaHorizontal, j, z=1)
                        x += velocidade
                    else:
                        atual += (passo*velocidade)
                        image2 = direcao_Horizontal(image2, anterior, atual, RuaHorizontal, j, z=1)
                        x += velocidade
                        if(i<(len(RuaVertical)-1)):
                            i+=1
                elif(direcao_atual == 1):
                    if((atual + (passo*velocidade)) > limites[0]):
                        for index in range(1,6):
                            if(((atual + (passo*velocidade)) < limites[0]) or (velocidade == 1)): break
                            else: velocidade-=1
                        atual += (passo*velocidade)
                        image2 = direcao_Horizontal(image2, anterior, atual, RuaHorizontal, j, z=1)
                        x += velocidade
                        atual = RuaHorizontal[j] + 15
                        prox_direcao = 2
                        direcao_atual = 0
                    elif((atual + (passo*velocidade)) > (RuaVertical[i] + passo)):
                        for index in range(1,6):
                            if(((atual + (passo*velocidade)) < (RuaVertical[i] + passo) or velocidade == 1)): break
                            else: velocidade-=1
                        atual += (passo*velocidade)
                        image2 = direcao_Horizontal(image2, anterior, atual, RuaHorizontal, j, z=1)
                        x += velocidade
                        i+=1
                        atual = RuaHorizontal[j] + 15
                        prox_direcao = 2
                        direcao_atual = 0
                    else:
                        atual += (passo*velocidade)
                        image2 = direcao_Horizontal(image2, anterior, atual, RuaHorizontal, j, z=1)
                        x += velocidade
                        atual = RuaHorizontal[j] + 15
                        prox_direcao = 2
                        direcao_atual = 0
                elif(direcao_atual == 2):
                    if(RuaHorizontal[j] == RuaHorizontal[len(RuaHorizontal)-1]):
                        if(((atual + (passo*velocidade)) > limites[0])):
                            for index in range(1,6):
                                if(((atual + (passo*velocidade)) < limites[0]) or (velocidade == 1)): break
                                else: velocidade-=1
                        direcao_atual = 0
                        atual += (passo*velocidade)
                        image2 = direcao_Horizontal(image2, anterior, atual, RuaHorizontal, j, z=1)
                        x += velocidade
                        if i < len(RuaVertical)-1:
                            i+=1
                    elif((atual + 15) == RuaVertical[i]):
                        atual = RuaHorizontal[j] + 15
                        prox_direcao = 3
                        direcao_atual = 0
                    elif((atual + (passo*velocidade)) > RuaVertical[i]):
                        for index in range(1,6):
                            if(((atual + (passo*velocidade)) < (RuaVertical[i]) or velocidade == 1)): break
                            else: velocidade-=1
                        atual += (passo*velocidade)
                        image2 = direcao_Horizontal(image2, anterior, atual, RuaHorizontal, j, z=1)
                        x += velocidade
                        atual = RuaHorizontal[j] + 15
                        prox_direcao = 3
                        direcao_atual = 0
        elif(x == X_MAX):
            prox_direcao = 2
            direcao_atual = 0
            atual = RuaHorizontal[j] + 15
    #Mover o carro para esquerda do mapa
    elif(prox_direcao == 1):
        if(x > 0):
            if( (atual - (passo*velocidade)) > (RuaVertical[i])):
                atual -= (passo*velocidade)
                image2 = direcao_Horizontal(image2, anterior, atual, RuaHorizontal, j, z=-1)
                x -= velocidade
                if(velocidade<5):velocidade+=1
            else:
                if(direcao_atual == 0):
                    if((atual - (passo*velocidade)) < limites[1]):
                        for index in range(1,6):
                            if(((atual - (passo*velocidade)) > limites[1]) or (velocidade == 1)): break
                            else: velocidade-=1
                        atual -= (passo*velocidade)
                        image2 = direcao_Horizontal(image2, anterior, atual, RuaHorizontal, j, z=-1)
                        x -= velocidade
                    else:
                        atual -= (passo*velocidade)
                        image2 = direcao_Horizontal(image2, anterior, atual, RuaHorizontal, j, z=-1)
                        x -= velocidade
                        if(i>0):
                            i-=1
                elif(direcao_atual == 1):
                    if(RuaHorizontal[j] == RuaHorizontal[0]):
                        if(((atual - (passo*velocidade)) < limites[1])):
                            for index in range(1,6):
                                if(((atual - (passo*velocidade)) > limites[1]) or (velocidade == 1)): break
                                else: velocidade-=1
                        direcao_atual = 0
                        atual -= (passo*velocidade)
                        image2 = direcao_Horizontal(image2, anterior, atual, RuaHorizontal, j, z=-1)
                        x -= velocidade
                        if i > 0:
                            i-=1
                    elif((atual - 15) == RuaVertical[i]):
                        atual = RuaHorizontal[j] - 15
                        prox_direcao = 2
                        direcao_atual = 0
                    elif((atual - (passo*velocidade)) < RuaVertical[i]):
                        for index in range(1,6):
                            if(((atual - (passo*velocidade)) > (RuaVertical[i]) or velocidade == 1)): break
                            else: velocidade-=1
                        atual -= (passo*velocidade)
                        image2 = direcao_Horizontal(image2, anterior, atual, RuaHorizontal, j, z=-1)
                        x -= velocidade
                        atual = RuaHorizontal[j] - 15
                        prox_direcao = 2
                        direcao_atual = 0
                elif(direcao_atual == 2):
                    if((atual - (passo*velocidade)) < limites[1]):
                        for index in range(1,6):
                            if(((atual + (passo*velocidade)) > limites[1]) or (velocidade == 1)): break
                            else: velocidade-=1
                        atual -= (passo*velocidade)
                        image2 = direcao_Horizontal(image2, anterior, atual, RuaHorizontal, j, z=-1)
                        x-= velocidade
                        atual = RuaHorizontal[j] - 15
                        prox_direcao = 3
                        direcao_atual = 0
                    elif((atual - (passo*velocidade)) < (RuaVertical[i] - passo)):
                        for index in range(1,6):
                            if(((atual - (passo*velocidade)) > (RuaVertical[i] - passo) or velocidade == 1)): break
                            else: velocidade-=1
                        atual -= (passo*velocidade)
                        image2 = direcao_Horizontal(image2, anterior, atual, RuaHorizontal, j, z=-1)
                        x -= velocidade
                        i-=1
                        atual = RuaHorizontal[j] - 15
                        prox_direcao = 3
                        direcao_atual = 0
                    else:
                        atual -= (passo*velocidade)
                        image2 = direcao_Horizontal(image2, anterior, atual, RuaHorizontal, j, z=-1)
                        x -= velocidade
                        atual = RuaHorizontal[j] - 15
                        prox_direcao = 3
                        direcao_atual = 0
        elif(x == 0):
            prox_direcao = 3
            direcao_atual = 0
            atual = RuaHorizontal[j] - 15
    #Mover o carro para cima do mapa
    elif(prox_direcao == 2):
        if(y > 0):
            if((atual-(passo*velocidade)) > (RuaHorizontal[j])):
                atual -= (passo*velocidade)
                image2 = direcao_Vertical(image2, anterior, atual, RuaVertical, i, z=1)
                y -= velocidade
                if(velocidade<5):velocidade+=1
            else:
                if(direcao_atual == 0):
                    if((atual - (passo*velocidade)) < limites[2]):
                        for index in range(1,6):
                            if(((atual - (passo*velocidade)) > limites[2]) or (velocidade == 1)): break
                            else: velocidade-=1
                        atual -= (passo*velocidade)
                        image2 = direcao_Vertical(image2, anterior, atual, RuaVertical, i, z=1)
                        y -= velocidade
                    else:
                        atual -= (passo*velocidade)
                        image2 = direcao_Vertical(image2, anterior, atual, RuaVertical, i, z=1)
                        y -= velocidade
                        if(j > 0):
                            j-=1
                elif(direcao_atual == 1):
                    if(RuaVertical[i] == RuaVertical[len(RuaVertical)-1]):
                        if(((atual - (passo*velocidade)) < limites[2])):
                            for index in range(1,6):
                                if(((atual - (passo*velocidade)) > limites[2]) or (velocidade == 1)): break
                                else: velocidade-=1
                        direcao_atual = 0
                        atual -= (passo*velocidade)
                        image2 = direcao_Vertical(image2, anterior, atual, RuaVertical, i, z=1)
                        y -= velocidade
                        if j > 0:
                            j-=1
                    elif((atual - 15) == RuaHorizontal[j]):
                        atual = RuaVertical[i] + 15
                        prox_direcao = 0
                        direcao_atual = 0
                    elif((atual - (passo*velocidade)) < RuaHorizontal[j]):
                        for index in range(1,6):
                            if(((atual - (passo*velocidade)) > (RuaHorizontal[j]) or velocidade == 1)): break
                            else: velocidade-=1
                        atual -= (passo*velocidade)
                        image2 = direcao_Vertical(image2, anterior, atual, RuaVertical, i, z=1)
                        y -= velocidade
                        atual = RuaVertical[i] + 15
                        prox_direcao = 0
                        direcao_atual = 0
                    else:
                        atual -= (passo*velocidade)
                        image2 = direcao_Vertical(image2, anterior, atual, RuaVertical, i, z=1)
                        y -= velocidade
                        atual = RuaVertical[i] + 15
                        prox_direcao = 0
                        direcao_atual = 0
                elif(direcao_atual == 2):
                    if((atual - (passo*velocidade)) < limites[2]):
                        for index in range(1,6):
                            if(((atual + (passo*velocidade)) > limites[2]) or (velocidade == 1)): break
                            else: velocidade-=1
                        atual -= (passo*velocidade)
                        image2 = direcao_Vertical(image2, anterior, atual, RuaVertical, i, z=1)
                        y -= velocidade
                        atual = RuaVertical[i] + 15
                        prox_direcao = 1
                        direcao_atual = 0
                    elif((atual - (passo*velocidade)) < (RuaHorizontal[j] - passo)):
                        for index in range(1,6):
                            if(((atual - (passo*velocidade)) > (RuaVertical[i] - passo) or velocidade == 1)): break
                            else: velocidade-=1
                        atual -= (passo*velocidade)
                        image2 = direcao_Vertical(image2, anterior, atual, RuaVertical, i, z=1)
                        y -= velocidade
                        j-=1
                        atual = RuaVertical[i] + 15
                        prox_direcao = 1
                        direcao_atual = 0
                    else:
                        atual -= (passo*velocidade)
                        image2 = direcao_Vertical(image2, anterior, atual, RuaVertical, i, z=1)
                        y -= velocidade
                        atual = RuaVertical[i] + 15
                        prox_direcao = 1
                        direcao_atual = 0
        elif(y == 0):
            prox_direcao = 1
            direcao_atual = 0
            atual = RuaVertical[i] + 15
    #Mover o carro para baixo do mapa
    elif(prox_direcao == 3):
        if(y < Y_MAX):
            if((atual+(passo*velocidade)) < (RuaHorizontal[j])):
                atual += (passo*velocidade)
                image2 = direcao_Vertical(image2, anterior, atual, RuaVertical, i, z=-1)
                y += velocidade
                if(velocidade<5):velocidade+=1
            else:
                if(direcao_atual == 0):
                    if((atual + (passo*velocidade)) > limites[3]):
                        for index in range(1,6):
                            if(((atual + (passo*velocidade)) < limites[3]) or (velocidade == 1)): break
                            else: velocidade-=1
                        atual += (passo*velocidade)
                        image2 = direcao_Vertical(image2, anterior, atual, RuaVertical, i, z=-1)
                        y += velocidade
                    else:
                        atual += (passo*velocidade)
                        image2 = direcao_Vertical(image2, anterior, atual, RuaVertical, i, z=-1)
                        y += velocidade
                        if(j<(len(RuaHorizontal)-1)):
                            j+=1
                elif(direcao_atual == 1):
                    if((atual + (passo*velocidade)) > limites[3]):
                        for index in range(1,6):
                            if(((atual + (passo*velocidade)) < limites[3]) or (velocidade == 1)): break
                            else: velocidade-=1
                        atual += (passo*velocidade)
                        image2 = direcao_Vertical(image2, anterior, atual, RuaVertical, i, z=-1)
                        y += velocidade
                        atual = RuaVertical[i] - 15
                        prox_direcao = 0
                        direcao_atual = 0
                    elif((atual + (passo*velocidade)) > (RuaHorizontal[j] + passo)):
                        for index in range(1,6):
                            if(((atual + (passo*velocidade)) < (RuaVertical[i] + passo) or velocidade == 1)): break
                            else: velocidade-=1
                        atual += (passo*velocidade)
                        image2 = direcao_Vertical(image2, anterior, atual, RuaVertical, i, z=-1)
                        y += velocidade
                        j+=1
                        atual = RuaVertical[i] - 15
                        prox_direcao = 0
                        direcao_atual = 0
                    else:
                        atual += (passo*velocidade)
                        image2 = direcao_Vertical(image2, anterior, atual, RuaVertical, i, z=-1)
                        y += velocidade
                        atual = RuaVertical[i] - 15
                        prox_direcao = 0
                        direcao_atual = 0
                elif(direcao_atual == 2):
                    if(RuaVertical[i] == RuaVertical[0]):
                        if(((atual + (passo*velocidade)) > limites[3])):
                            for index in range(1,6):
                                if(((atual + (passo*velocidade)) < limites[0]) or (velocidade == 1)): break
                                else: velocidade-=1
                        direcao_atual = 0
                        atual += (passo*velocidade)
                        image2 = direcao_Vertical(image2, anterior, atual, RuaVertical, i, z=-1)
                        y += velocidade
                        if j < len(RuaHorizontal)-1:
                            j+=1
                    elif((atual + 15) == RuaHorizontal[j]):
                        atual = RuaVertical[i] - 15
                        prox_direcao = 1
                        direcao_atual = 0
                    elif((atual + (passo*velocidade)) > RuaHorizontal[j]):
                        for index in range(1,6):
                            if(((atual + (passo*velocidade)) < (RuaHorizontal[j]) or velocidade == 1)): break
                            else: velocidade-=1
                        atual += (passo*velocidade)
                        image2 = direcao_Vertical(image2, anterior, atual, RuaVertical, i, z=-1)
                        y += velocidade
                        atual = RuaVertical[i] - 15
                        prox_direcao = 1
                        direcao_atual = 0
        elif(y == Y_MAX):
            atual = RuaVertical[i] - 15
            prox_direcao = 0
            direcao_atual = 0
    return image2, atual, direcao_atual, x, y, i, j, prox_direcao
 
def direcao_Horizontal(image2, anterior, atual, RuaHorizontal, j, z):
    image2 = cv2.circle(image2, (anterior, RuaHorizontal[j] + (15*z)), 10, (0, 0, 0), -1)
    image2 = cv2.circle(image2, (atual, RuaHorizontal[j] +(15*z)), 10, (255, 0, 255), -1)
    return image2
def direcao_Vertical(image2, anterior, atual, RuaVertical, i, z):
    image2 = cv2.circle(image2, (RuaVertical[i] + (15*z), anterior), 10, (0, 0, 0), -1)
    image2 = cv2.circle(image2, (RuaVertical[i] + (15*z), atual), 10, (255, 0, 255), -1)
    anterior = atual
    return image2
# =============================================================================
atual = limites[2] - 15
direcao_atual = 0
prox_direcao = 3
x = 0
y = -1
i=0
j=0
print(len(RuaVertical))
teste = 0
while 1:

    
    if(teste == 1):
        print('i=',i,'j=', j, 'x=', x, 'y=', y, atual, prox_direcao, direcao_atual)
        image2, atual, direcao_atual, x, y, i, j , prox_direcao = movimento_carro(image2, RuaHorizontal, RuaVertical, quarteirao, atual, direcao_atual, prox_direcao, passo, velocidade, x, y, i, j, limites)
    if aux4 == 10:
        if direcao_atual == 0:
            direcao_atual = randint(0,2)
        else:
            direcao_atual = 0
        aux4=0
    aux4+=1
    
    image3 = image - image2   
    cv2.imshow(window_name, image3)
    key = cv2.waitKey(1)
    if key == 27:
        break
    elif key == 97:
        if direcao_atual == 1:
            direcao_atual = 0
        else:
            direcao_atual = 1
    elif key == 98:
        if direcao_atual == 2:
            direcao_atual = 0
        else:
            direcao_atual = 2
    elif key == 99:
        if teste == 1:
            teste = 0
        else:
            teste = 1
    time.sleep(0.1)

cv2.destroyAllWindows()
