# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 06:54:05 2022

@author: luizg
"""
# =============================================================================
# Required libraries
# =============================================================================
import paho.mqtt.client as mqtt
import time
import numpy as np
import cv2
import Mapa as mp
import random as rd
# =============================================================================
# Global variables
# =============================================================================
path = r'Imagens\background_mapa.png'
path2 = r'Imagens\inicio.png'
img = cv2.imread(path2)
first = conec = flag = central_statecar = prox_direc_car = direc_atual = 0
parked = ult_pos = startSimulacao = counter_pd = counter_parked = 0
disc = count = 1
estacionado = (-1,-1)
id_carro = -1
pd = [] #proxima direção
da = [] #direção atual
# =============================================================================
# Inicializa valores da simulação
# =============================================================================
def nothing(x):
    pass
cv2.namedWindow('Inicio', cv2.WINDOW_NORMAL)
cv2.createTrackbar('Q','Inicio',0,2,nothing)
while(1):
    cv2.imshow('Inicio',img)
    k = cv2.waitKey(1) & 0xFF
    # if press n
    if k == 110:
        break
    q = cv2.getTrackbarPos('Q','Inicio')
if k == 27:
    cv2.destroyAllWindows()
else:
    cv2.destroyWindow('Inicio')
    cv2.namedWindow('Inicio', cv2.WINDOW_AUTOSIZE)
    if q == 0:
        quarteirao = 240
        cv2.createTrackbar('Carros','Inicio',0,30,nothing)
    elif q == 1:
        quarteirao = 120
        cv2.createTrackbar('Carros','Inicio',0,40,nothing)
    elif q == 2:
        quarteirao = 60
        cv2.createTrackbar('Carros','Inicio',0,60,nothing)
    k = 0
    img2 = np.zeros((1,200,3), np.uint8)
    while (1):
        cv2.imshow('Inicio',img2)
        k = cv2.waitKey(1) & 0xFF
        nclients = cv2.getTrackbarPos('Carros','Inicio')
        if k == 110:
            break
cv2.destroyAllWindows()
# =============================================================================
# Function to show the log
# =============================================================================
def on_log(client, userdata, level, buf):
    print("log: " + buf)
# =============================================================================
# Function to show you are connected
# =============================================================================
def on_connect(client, userdata, flags, rc):
    global conec
    global disc
    if rc==0:
        conec = 1
        disc = 0
        print("Connected OK")
    else:
        print("Bad connection Returned code= ", rc)
# =============================================================================
# #Function to show you are disconnected
# =============================================================================
def on_disconnect(client, userdata, flags, rc=0):
    global first
    global conec
    global disc
    first = 0
    conec = 0
    disc  = 1
    print("Disconnected OK")
# =============================================================================
# #Function to print the received message
# =============================================================================
def on_message(client, userdata, msg):
    # print("Message received = '", str(msg.payload.decode("utf-8")), "'", "on topic '", msg.topic, "'")
    salva_msg(str(msg.payload.decode("utf-8")), str(msg.topic))
# =============================================================================
# Tratamento das mensagens recebidas da central
# =============================================================================
def salva_msg(mensagem, topico):
    global flag
    global id_carro
    global central_statecar
    global direc_atual
    msg = mensagem.split('/')
    id_carro = int(msg[0])
    central_statecar = int (msg[1])
    direc_atual = int(msg[2])
    if central_statecar > 1 and central_statecar < 4:
        flag = 1
    else:
        flag = 0
# =============================================================================
# Brokers address
# =============================================================================
# broker_address =    'test.mosquitto.org'
broker_address =    'broker.emqx.io'
# =============================================================================
# Conectando os n carros ao broker
# =============================================================================
clients=[]
# nclients= 30
for i  in range(nclients):
    cname="Carros_"+str(i)
    print("Creating new instance for " + cname +"...")
    client= mqtt.Client(cname)
    clients.append(client)
for client in clients:
    client.on_connect = on_connect
    client.on_disconnect= on_disconnect
    #client.on_log = on_log
    client.on_message = on_message
    client.connect(broker_address)
    client.loop_start()
# =============================================================================
# Cria a cidade, a matriz de posições e cria os carros
# =============================================================================
Cidade1, image, image2, window_name = mp.mapa_cidade(path, quarteirao)
matriz_cidade, X_MAX, Y_MAX = mp.matriz_posicoes(Cidade1)
posicoes, carros = mp.cria_carros(X_MAX, Y_MAX, matriz_cidade, quantidade=nclients)
# =============================================================================
# Cria string para enviar as posições, dos carros que são válidas dentro do
# mapa, para a central verificar as coordenadas enviadas pelo usuário
# =============================================================================
usuario_pos = ''
for i in range(X_MAX):
    for j in range(Y_MAX):
        if matriz_cidade[i][j] != (-1,-1):
            usuario_pos += '(' + str(i) + ',' + str(j) + ')' + '/'
# =============================================================================
# Inicia as listas com valores default            
# =============================================================================
for n in range(len(carros)):
    da.append(0)
    pd.append(3)
# =============================================================================
# Seleciona 60% dos carros para colocar estado ocupado
# =============================================================================
aux_status = np.array(range(0,(len(carros))))
rd.shuffle(aux_status)
aux2_status = aux_status[0: int(len(carros)*0.6)] 
# =============================================================================
# Faz a sub da central
# =============================================================================
client.subscribe("transporte/central_carro" ,1)
# =============================================================================
# Loop principal
# =============================================================================
while 1:
    # Se recebeu mensagem de início, envia a confirmação para a central e manda
    # a string com posições válidas para a central verificar as solicitações do
    # usuário
    if id_carro == -2:
        startSimulacao = 1
        id_carro = -1
        msg = str(X_MAX) + '/' + str(Y_MAX) + '/' + str(nclients) + '/0'
        clients[0].publish('transporte/inicio', msg)
        clients[0].publish('transporte/matrizo', usuario_pos)
    # Contador para gerar próximas direções aleatórias para 60% dos carros
    if counter_pd == 15:
        rd.shuffle(aux_status)
        aux2_status = aux_status[0: int(len(carros)*0.6)]
        for q in range(len(pd)):
            if flag == 1 and q == id_carro:
                nda = 1
            else:
                pd[q] = rd.randint(0,3)
        counter_pd = 0
    # Contador para gerar as direções atuais aleatórias dos carros
    if count == 5:
        for p in range(len(da)):
            if da[p] == 0:
                da[p] = rd.randint(0,2)
            else:
                da[p] = rd.randint(0,2)
        count=0
    # Se a simulação iniciar, começa as movimentações no mapa
    if(startSimulacao == 1):
        # A sequência segue para cada carro
        for m in range(len(carros)):
            velocidade = mp.proxima(pd[m], posicoes, m, posicoes[m])
            # Verifica se recebeu mudança de estado
            if flag == 1 and m == id_carro:
                status = central_statecar
                da[m] = direc_atual
            # Se o carro estiver muito tempo estacionado ele retorna ao mapa
            if central_statecar == 2:
                counter_parked +=1
                if counter_parked == 1250:
                    status = 0
                    flag = -1
                    counter_parked = 0
            else:
                counter_parked = 0
            # Verifica se o carro está na lista de carros ocupados e não é o carro utilizado pelo usuário
            if m in aux2_status:
                if m != id_carro:
                    status = 1
            else:
                if m != id_carro:
                    status = 0
            #Se o carro for estacionar pela primeira vez ele estaciona e salva a sua última posição no mapa
            if status == 2:
                if parked == 0:
                    image2, posicoes[m], da[m], pd[m], velocidade, estacionado = carros[m].movimento_carro(image2, matriz_cidade, posicoes[m], da[m], pd[m], velocidade, status, estacionado, flag)
                    ult_pos = posicoes[m]
                    parked = 1
                else:
                    posicoes[m] = (-1,-1)
            else:
                if status == 3:
                    parked = 0
                if posicoes[m] == (-1,-1):
                    posicoes[m] = ult_pos
                    velocidade = mp.proxima(pd[m], posicoes, m, posicoes[m])
                image2, posicoes[m], da[m], pd[m], velocidade = carros[m].movimento_carro(image2, matriz_cidade, posicoes[m], da[m], pd[m], velocidade, status, estacionado, flag)
                if flag == -1:
                    flag = 0
            # Publica as mensagens para a central
            msg = str(status) + '/' + str(posicoes[m][0]) + '/' + str(posicoes[m][1]) + '/' + str(velocidade) + '/' + str(pd[m])
            topico =  'transporte/carro' + str(m)
            clients[m].publish(topico, msg)
    count += 1    
    counter_pd += 1   
    image3 = image - image2   
    cv2.imshow(window_name, image3)
    key = cv2.waitKey(1)
    #Se pressionar 'esc', encerra a aplicação
    if key == 27:
        break
    time.sleep(0.5)
cv2.destroyAllWindows()
# =============================================================================
# Desconecta do broker todos os clientes
# =============================================================================
j = 0
for client in clients:
    # print("Disconnecting Client", j) 
    client.loop_stop()
    client.disconnect()
    print("Disconnected Client", j)
    j+=1