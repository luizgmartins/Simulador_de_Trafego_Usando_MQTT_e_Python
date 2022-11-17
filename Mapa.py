# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 18:56:22 2022

@author: luizg
"""
# =============================================================================
# Bibliotecas
# =============================================================================
import cv2
from random import randint
import numpy as np

path = r'C:\Workspace\Simulador_de_Trafego_Usando_MQTT_e_Python\Imagens\background_mapa.png'

# =============================================================================
#Criação da cidade, com ruas, quarteirões e limites externos
# =============================================================================
def mapa_cidade(path, quarteirao):
    image = cv2.imread(path)
    image2 = image.copy() - image
    lines = image.shape[0]
    columns = image.shape[1]
    window_name = 'Image'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
    passo=30
    # Blue color in BGR
    color = (0, 0, 0)
    thickness = 2
    aux = 0
    #min = 60 max < menor_valor(((columns/2)-90),((lines/2)-90))
    # quarteirao = 60
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
    image = cv2.line(image, (0, lines - i), (columns, lines - i), (0, 0, 0), thickness)
    limite_superior = i
    limite_inferior = lines - i
    image = cv2.rectangle(image, (0, limite_superior - 1), (limite_esquerda-2, limite_inferior + 1), (255, 255, 255), -1)
    image = cv2.rectangle(image, (limite_direita + 2, limite_superior - 1), (columns, limite_inferior + 1), (255, 255, 255), -1)
    image = cv2.rectangle(image, (limite_esquerda - 1, 0), (limite_direita + 1, limite_superior - 2), (255, 255, 255), -1)
    image = cv2.rectangle(image, (limite_esquerda - 1, limite_inferior + 2), (limite_direita + 1, columns), (255, 255, 255), -1)
    limites = []
    limites.append(limite_direita)
    limites.append(limite_esquerda)
    limites.append(limite_superior)
    limites.append(limite_inferior)
    RuaHorizontal, RuaVertical = nome_ruas(image, limites, meio_lines, meio_columns, quarteirao)
    Cidade1 = cidade(RuaHorizontal, RuaVertical, quarteirao, passo, limites)
    return Cidade1, image, image2, window_name
# =============================================================================
# Nomeando ruas verticais e horizontais
# =============================================================================
def nome_ruas(image, limites, meio_lines, meio_columns, quarteirao):
    k=limites[1] + 30
    aux = 1
    RuaVertical = [] 
    while(k<limites[0]):
        rua = 'Rua Vertical ' + str(aux)
        image = cv2.putText(image, rua, (k, meio_lines-quarteirao), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
        RuaVertical.append(k)
        k+= quarteirao + 60
        aux+=1
    k=limites[2] + 30
    aux2 = 1
    RuaHorizontal = [] 
    while(k<limites[3]):
        rua = 'Rua Horizontal ' + str(aux2)
        image = cv2.putText(image, rua, (meio_columns-quarteirao, k), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
        RuaHorizontal.append(k)
        k+= quarteirao + 60
        aux2+=1
    return RuaHorizontal, RuaVertical
# =============================================================================
# Constantes em um classe
# =============================================================================
class cidade:
    def __init__(self, RuaHorizontal, RuaVertical, quarteirao, passo, limites):
        self.RuaHorizontal = RuaHorizontal
        self.RuaVertical = RuaVertical
        self.quarteirao = quarteirao
        self.passo = passo
        self.limites = limites
# =============================================================================
# Mapeando as posições da cidade em uma matriz
# =============================================================================
def matriz_posicoes(cidade):
    
    RuaHorizontal = cidade.RuaHorizontal
    RuaVertical = cidade.RuaVertical
    quarteirao = cidade.quarteirao
    passo = cidade.passo
    limite_esquerda = cidade.limites[1]
    limite_superior = cidade.limites[2]
    
    Y_MAX = int(((quarteirao/passo)*(len(RuaVertical)-1)) + (len(RuaVertical) * 2))
    X_MAX = int(((quarteirao/passo)*(len(RuaHorizontal)-1)) + (len(RuaHorizontal) * 2))
    matriz_cidade = np.zeros((X_MAX,Y_MAX),dtype=tuple)
    
    for i in range(X_MAX):
        for j in range(Y_MAX):
            matriz_cidade[i,j] = (-1,-1)
    x = 0
    aux = 0
    while((x+quarteirao/30) < X_MAX):
        if(aux<2):
            for y in range(0, Y_MAX):
                matriz_cidade[x,y] = (limite_esquerda + 15 + 30*y, limite_superior + 15 + 30*x)
            aux += 1
            x += 1
        else:
            x = int(x+quarteirao/30)
            aux = 0
    aux = 0
    while(aux<=1):
        for y in range(0, Y_MAX):
            matriz_cidade[x,y] = (limite_esquerda + 15 + 30*y, limite_superior + 15 + 30*x)
        aux += 1
        x += 1
    y = 0
    aux = 0
    while((y+quarteirao/30) < Y_MAX):
        if(aux<2):
            for x in range(0, X_MAX):
                if matriz_cidade[x,y] == (-1,-1):
                    matriz_cidade[x,y] = (limite_esquerda + 15 + 30*y, limite_superior + 15 + 30*x)
            aux += 1
            y += 1
        else:
            y = int(y+quarteirao/30)
            aux = 0
    aux = 0
    while(aux<=1):
        for x in range(0, X_MAX):
            matriz_cidade[x,y] = (limite_esquerda + 15 + 30*y, limite_superior + 15 + 30*x)
        aux += 1
        y += 1
    return matriz_cidade, X_MAX, Y_MAX
# =============================================================================
# Movimento do carro
# =============================================================================
class carro:
    def __init__(self, ID, placa):
        self.ID = ID
        self.placa = placa
    def movimento_carro(self, image2, matriz_cidade, atual, direcao_atual, prox_direcao, velocidade, status, estacionado):
        X_MAX, Y_MAX = np.shape(matriz_cidade)
        anterior = atual
        x = atual[0]
        y = atual[1]
        color = cor(status)
        if status == 2:
            atual, estacionado = estacionar(image2, atual, matriz_cidade, X_MAX, Y_MAX)
            return image2, atual, direcao_atual, prox_direcao, velocidade, estacionado
        elif status == 3:
            image2 = cv2.circle(image2, (matriz_cidade[estacionado[0]][estacionado[1]][0], matriz_cidade[estacionado[0]][estacionado[1]][1]), 10, (0, 0, 0), -1)
        if velocidade == 0:
            velocidade = 0
        #Mover o carro para direita do mapa
        elif(prox_direcao == 0):
            if(x % 2 == 0):
                prox_direcao = 1
                direcao_atual = 0
            elif(y < (Y_MAX - 1)):
                if(direcao_atual == 0):
                    if(matriz_cidade[x,y+1] != (-1,-1)):
                        y+=1
                        atual = (x,y)
                        image2 = direcao(image2, anterior, atual, matriz_cidade, prox_direcao, direcao_atual, color)
                    else:
                        prox_direcao = 2
                        direcao_atual=1
                elif(direcao_atual == 1):
                    if(x >= 2):
                        if((y % 2 == 1) and (matriz_cidade[x-2,y] != (-1,-1))):
                            prox_direcao = 2
                            direcao_atual = 0
                        else:
                            y+=1
                            atual = (x,y)
                            image2 = direcao(image2, anterior, atual, matriz_cidade, prox_direcao, direcao_atual, color)
                    else:
                        if((matriz_cidade[x+1,y] != (-1,-1)) and (y % 2 == 1)):
                            prox_direcao = 2
                            direcao_atual=0
                        else:
                            y+=1
                            atual = (x,y)
                            image2 = direcao(image2, anterior, atual, matriz_cidade, prox_direcao, direcao_atual, color)
                elif(direcao_atual == 2):
                    if(x < (X_MAX - 1)):
                        if((y % 2 == 0 and matriz_cidade[x+1,y] != (-1,-1))):
                            prox_direcao = 3
                            direcao_atual=0
                        elif((matriz_cidade[x,y+1] == (-1,-1))):
                            prox_direcao = 1
                        else: 
                            y+=1
                            atual = (x,y)
                            image2 = direcao(image2, anterior, atual, matriz_cidade, prox_direcao, direcao_atual, color)
                    else:
                        y+=1
                        atual = (x,y)
                        image2 = direcao(image2, anterior, atual, matriz_cidade, prox_direcao, direcao_atual, color)
            elif(y == (Y_MAX - 1)):
                prox_direcao = 2
                direcao_atual = 0
        #Mover o carro para esquerda do mapa
        elif(prox_direcao == 1):
            if(x % 2 == 1):
                prox_direcao = 0
                direcao_atual = 0
            elif(y > 0):
                if(direcao_atual == 0):
                    if(matriz_cidade[x,y-1] != (-1,-1)):
                        y-=1
                        atual = (x,y)
                        image2 = direcao(image2, anterior, atual, matriz_cidade, prox_direcao, direcao_atual, color)
                    else:
                        prox_direcao = 3
                        direcao_atual=2
                elif(direcao_atual == 1):
                    if(x > 0):
                        if((y % 2 == 1 and matriz_cidade[x-1,y] != (-1,-1))):
                            prox_direcao = 1
                            direcao_atual=0
                        elif(matriz_cidade[x,y-1] == (-1,-1)):
                            prox_direcao = 3
                        else: 
                            y-=1
                            atual = (x,y)
                            image2 = direcao(image2, anterior, atual, matriz_cidade, prox_direcao, direcao_atual, color)
                    else:
                        y-=1
                        atual = (x,y)
                        image2 = direcao(image2, anterior, atual, matriz_cidade, prox_direcao, direcao_atual, color)
                elif(direcao_atual == 2):
                    if(x <= (X_MAX-3)):
                        if((y % 2 == 0) and (matriz_cidade[x+2,y] != (-1,-1))):
                            prox_direcao = 3
                            direcao_atual = 0
                        else:
                            y-=1
                            atual = (x,y)
                            image2 = direcao(image2, anterior, atual, matriz_cidade, prox_direcao, direcao_atual, color)
                    else:
                        if((y % 2 == 0) and (matriz_cidade[x-1,y] != (-1,-1))):
                            prox_direcao = 3
                            direcao_atual=0
                        else:
                            y-=1
                            atual = (x,y)
                            image2 = direcao(image2, anterior, atual, matriz_cidade, prox_direcao, direcao_atual, color)
            elif(y == 0):
                prox_direcao = 3
                direcao_atual = 0
        #Mover o carro para cima do mapa
        elif(prox_direcao == 2):
            if(y % 2 == 0):
                prox_direcao = 3
                direcao_atual = 0
            elif(x > 0):
                if(direcao_atual == 0):
                    if(matriz_cidade[x-1,y] != (-1,-1)):
                        x-=1
                        atual = (x,y)
                        image2 = direcao(image2, anterior, atual, matriz_cidade, prox_direcao, direcao_atual, color)
                    else:
                        prox_direcao = 1
                        direcao_atual=1
                elif(direcao_atual == 1):
                    if(y < (Y_MAX-1)):
                        if((x % 2 == 1 and matriz_cidade[x,y+1] != (-1,-1))):
                            prox_direcao = 0
                            direcao_atual=0
                        elif((matriz_cidade[x-1,y] == (-1,-1))):
                            prox_direcao = 1
                        else: 
                            x-=1
                            atual = (x,y)
                            image2 = direcao(image2, anterior, atual, matriz_cidade, prox_direcao, direcao_atual, color)
                    else:
                        x-=1
                        atual = (x,y)
                        image2 = direcao(image2, anterior, atual, matriz_cidade, prox_direcao, direcao_atual, color)
                elif(direcao_atual == 2):
                    if(y <= (Y_MAX-3)):
                        if((x % 2 == 0) and (matriz_cidade[x,y+1] != (-1,-1))):
                            prox_direcao = 1
                            direcao_atual = 0
                        else:
                            x-=1
                            atual = (x,y)
                            image2 = direcao(image2, anterior, atual, matriz_cidade, prox_direcao, direcao_atual, color)
                    else:
                        if((y % 2 == 0) and (matriz_cidade[x,y-2] != (-1,-1))):
                            prox_direcao = 1
                            direcao_atual=0
                        else:
                            x-=1
                            atual = (x,y)
                            image2 = direcao(image2, anterior, atual, matriz_cidade, prox_direcao, direcao_atual, color)
            elif(x == 0):
                prox_direcao = 1
                direcao_atual = 0
        #Mover o carro para baixo do mapa
        elif(prox_direcao == 3):
            if(y % 2 == 1):
                prox_direcao = 2
                direcao_atual = 0
            elif(x < (X_MAX - 1)):
                if(direcao_atual == 0):
                    if(matriz_cidade[x+1,y] != (-1,-1)):
                        x+=1
                        atual = (x,y)
                        image2 = direcao(image2, anterior, atual, matriz_cidade, prox_direcao, direcao_atual, color)
                    else:
                        prox_direcao = 0
                        direcao_atual= 2
                elif(direcao_atual == 1):
                    if(y <= (Y_MAX-3)):
                        if((x % 2 == 1) and (matriz_cidade[x,y+2] != (-1,-1))):
                            prox_direcao = 0
                            direcao_atual = 0
                        else:
                            x+=1
                            atual = (x,y)
                            image2 = direcao(image2, anterior, atual, matriz_cidade, prox_direcao, direcao_atual, color)
                    else:
                        if((matriz_cidade[x,y-1] != (-1,-1)) and (x % 2 == 1)):
                            prox_direcao = 0
                            direcao_atual=0
                        else:
                            x+=1
                            atual = (x,y)
                            image2 = direcao(image2, anterior, atual, matriz_cidade, prox_direcao, direcao_atual, color)
                elif(direcao_atual == 2):
                    if(y > 0):
                        if((x % 2 == 0 and matriz_cidade[x,y-1] != (-1,-1))):
                            prox_direcao = 1
                            direcao_atual=0
                        elif((matriz_cidade[x+1,y] == (-1,-1))):
                            prox_direcao == 1
                        else: 
                            x+=1
                            atual = (x,y)
                            image2 = direcao(image2, anterior, atual, matriz_cidade, prox_direcao, direcao_atual, color)
                    else:
                        x+=1
                        atual = (x,y)
                        image2 = direcao(image2, anterior, atual, matriz_cidade, prox_direcao, direcao_atual, color)
            elif(x == (X_MAX-1)):
                prox_direcao = 0
                direcao_atual = 0
        estacionado = (-1,-1)
        return image2, atual, direcao_atual, prox_direcao, velocidade, estacionado
# =============================================================================
# Movimentar carro no mapa
# =============================================================================
def direcao(image2, anterior, atual, matriz_cidade, prox_direc, direc_atual, color=(255, 255, 255)):
    x_anterior, y_anterior = anterior
    x_atual, y_atual = atual
    image2 = cv2.circle(image2, (matriz_cidade[x_anterior][y_anterior][0], matriz_cidade[x_anterior][y_anterior][1]), 10, (0, 0, 0), -1)
    image2 = cv2.circle(image2, (matriz_cidade[x_atual][y_atual][0], matriz_cidade[x_atual][y_atual][1]), 10, color, -1)
    return image2
# =============================================================================
# Define a cor de acordo com o status do carro
# =============================================================================
def cor(status=0):
    if status == 0:
        color = (255, 255, 255)
    elif status == 1:
        color = (255, 255, 0)
    elif status == 2:
        color = (0, 255, 255)
    elif status == 3:
        color = (255, 0, 255)
    return color
# =============================================================================
# Estaciona carro
# =============================================================================
def estacionar(image2, atual, matriz_cidade, X_MAX, Y_MAX):
    x = atual[0]
    y = atual[1]
    image2 = cv2.circle(image2, (matriz_cidade[x][y][0], matriz_cidade[x][y][1]), 10, (0, 0, 0), -1)
    if x == 0:
        image2 = cv2.circle(image2, (matriz_cidade[x][y][0], matriz_cidade[x][y][1]-30), 10, cor(2), -1)
        estacionado = (matriz_cidade[x][y][0],matriz_cidade[x][y][1]-30)
    elif x == (len(X_MAX)-1):
        image2 = cv2.circle(image2, (matriz_cidade[x][y][0], matriz_cidade[x][y][1]+30), 10, cor(2), -1)
        estacionado = (matriz_cidade[x][y][0],matriz_cidade[x][y][1]+30)
    elif y == 0:
        image2 = cv2.circle(image2, (matriz_cidade[x][y][0]-30, matriz_cidade[x][y][1]), 10, cor(2), -1)
        estacionado = (matriz_cidade[x][y][0]-30,matriz_cidade[x][y][1])
    elif y == (len(Y_MAX)-1):
        image2 = cv2.circle(image2, (matriz_cidade[x][y][0]+30, matriz_cidade[x][y][1]), 10, cor(2), -1)
        estacionado = (matriz_cidade[x][y][0]+30,matriz_cidade[x][y][1])
    else:
        if matriz_cidade[x-1][y] == (-1, -1):
            image2 = cv2.circle(image2, (matriz_cidade[x-1][y][0], matriz_cidade[x-1][y][1]), 10, cor(2), -1)
            estacionado = (matriz_cidade[x-1][y][0],matriz_cidade[x-1][y][1])
        elif matriz_cidade[x][y-1] == (-1, -1):
            image2 = cv2.circle(image2, (matriz_cidade[x][y-1][0], matriz_cidade[x][y-1][1]), 10, cor(2), -1)
            estacionado = (matriz_cidade[x][y-1][0],matriz_cidade[x][y-1][1])
        elif matriz_cidade[x][y+1] == (-1, -1):
            image2 = cv2.circle(image2, (matriz_cidade[x][y+1][0], matriz_cidade[x][y+1][1]), 10, cor(2), -1)
            estacionado = (matriz_cidade[x][y+1][0], matriz_cidade[x][y+1][1])
        elif matriz_cidade[x+1][y] == (-1, -1):
            image2 = cv2.circle(image2, (matriz_cidade[x+1][y][0], matriz_cidade[x+1][y][1]), 10, cor(2), -1)
            estacionado = (matriz_cidade[x+1][y][0], matriz_cidade[x+1][y][1])
        elif matriz_cidade[x-1][y-1] == (-1, -1):
            image2 = cv2.circle(image2, (matriz_cidade[x-1][y-1][0], matriz_cidade[x-1][y-1][1]), 10, cor(2), -1)
            estacionado = (matriz_cidade[x-1][y-1][0], matriz_cidade[x-1][y-1][1])
        elif matriz_cidade[x-1][y+1] == (-1, -1):
            image2 = cv2.circle(image2, (matriz_cidade[x-1][y+1][0], matriz_cidade[x-1][y+1][1]), 10, cor(2), -1)
            estacionado = (matriz_cidade[x-1][y+1][0], matriz_cidade[x-1][y+1][1])
        elif matriz_cidade[x+1][y-1] == (-1, -1):
            image2 = cv2.circle(image2, (matriz_cidade[x+1][y-1][0], matriz_cidade[x+1][y-1][1]), 10, cor(2), -1)
            estacionado = (matriz_cidade[x+1][y-1][0], matriz_cidade[x+1][y-1][1])
        elif matriz_cidade[x+1][y+1] == (-1, -1):
            image2 = cv2.circle(image2, (matriz_cidade[x+1][y+1][0], matriz_cidade[x+1][y+1][1]), 10, cor(2), -1)
            estacionado = (matriz_cidade[x+1][y+1][0], matriz_cidade[x+1][y+1][1])
    return atual, estacionado
# =============================================================================
# Criando carros
# =============================================================================
def cria_carros(X_MAX, Y_MAX, matriz_cidade, quantidade):
    carros = []
    for i in range(quantidade):
        carros.append(carro(i,123)) 
    posicoes = []
    for l in range(len(carros)):
        while 1:
            aux6=0
            x = randint(0, X_MAX-1)
            y = randint(0, Y_MAX-1)
            if matriz_cidade[x][y] != (-1,-1):
                atual = (x,y)
                if(l>0):
                    for k in posicoes:
                        if k == atual:
                            break
                        else:
                            aux6 = 1
                    if aux6 == 1:
                        posicoes.append(atual)
                        break
                else:
                    posicoes.append(atual)
                    break
    return posicoes, carros
# =============================================================================
# Se houver obstáculo o carro para até que possa seguir
# =============================================================================
def proxima(proxima_direcao, posicoes, ID, atual):
    if proxima_direcao == 0:
        for index in range(len(posicoes)):
            if index!=ID and posicoes[index]==(atual[0],atual[1]+1):
                velocidade = 0
                break
            else:
                velocidade = 1
    elif proxima_direcao == 1:
        for index in range(len(posicoes)):
            if index!=ID and posicoes[index]==(atual[0],atual[1]-1):
                velocidade = 0
                break
            else:
                velocidade = 1
    elif proxima_direcao == 2:  
        for index in range(len(posicoes)):
            if index!=ID and posicoes[index]==(atual[0]-1,atual[1]):
                velocidade = 0
                break
            else:
                velocidade = 1
    elif proxima_direcao == 3:    
        for index in range(len(posicoes)):
            if index!=ID and posicoes[index]==(atual[0]+1,atual[1]):
                velocidade = 0
                break
            else:
                velocidade = 1
    return velocidade
# =============================================================================

