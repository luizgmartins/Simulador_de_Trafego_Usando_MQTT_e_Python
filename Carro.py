# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 06:54:05 2022

@author: luizg
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 06:48:40 2022

@author: luizg
"""

#Required libraries
import paho.mqtt.client as mqtt
# import keyboard
import time
import numpy as np
import cv2
import Mapa as mp
import random as rd

path = r'Imagens\background_mapa.png'

#Global variables
first = 0
conec = 0
disc  = 1
flag = 0
central_statecar = 0
prox_direc_car = 0
estacionado = (-1,-1)

#Function to show the log
def on_log(client, userdata, level, buf):
    print("log: " + buf)
    
#Function to show you are connected
def on_connect(client, userdata, flags, rc):
    global conec
    global disc
    if rc==0:
        conec = 1
        disc = 0
        print("Connected OK")
    else:
        print("Bad connection Returned code= ", rc)

#Function to show you are disconnected
def on_disconnect(client, userdata, flags, rc=0):
    global first
    global conec
    global disc
    first = 0
    conec = 0
    disc  = 1
    print("Disconnected OK")

#Function to print the received message
def on_message(client, userdata, msg):
    # print("Message received = '", str(msg.payload.decode("utf-8")), "'", "on topic '", msg.topic, "'")
    salva_msg(str(msg.payload.decode("utf-8")), str(msg.topic))

def salva_msg(mensagem, topico):
    global flag
    global id_carro
    global central_statecar
    global prox_direc_car
    msg = mensagem.split('/')
    id_carro = msg[0]
    central_statecar = msg[1]
    prox_direc_car = msg[2]
    if int(central_statecar) > 1 and int(central_statecar) < 4:
        flag = 1
    else:
        flag = 0
        

#Brokers address
# broker_address =    'test.mosquitto.org'
broker_address =    'broker.emqx.io'
clients=[]
nclients= 10
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
    
# time.sleep(2)

i = 0

Cidade1, image, image2, window_name = mp.mapa_cidade(path, quarteirao=240)
matriz_cidade, X_MAX, Y_MAX = mp.matriz_posicoes(Cidade1)
posicoes, carros = mp.cria_carros(X_MAX, Y_MAX, matriz_cidade, quantidade=nclients)
aux = 1
da = []
pd = []
for n in range(len(carros)):
    da.append(0)
    pd.append(3)
teste = 1
tempo = 0.05
aux7 = 0
aux4 = 0
aux2 = np.array(range(0,(len(carros))))
rd.shuffle(aux2)
aux3 = aux2[0: int(len(carros)*0.6)] 

client.subscribe("transporte/central_carro" ,1)
msg = str(X_MAX) + '/' + str(Y_MAX) + '/0/0'
clients[0].publish('transporte/inicio', msg)

while 1:
    if aux7 == 15:
        rd.shuffle(aux2)
        aux3 = aux2[0: int(len(carros)*0.6)]
        for q in range(len(pd)):
            pd[q] = rd.randint(0,3)
        aux7=0
    if aux == 5:
        for p in range(len(da)):
            if da[p] == 0:
                da[p] = rd.randint(0,2)
            else:
                da[p] = rd.randint(0,2)
        aux=0
    if(teste == 1):
        for m in range(len(carros)):
            velocidade = mp.proxima(pd[m], posicoes, m, posicoes[m])
            if m in aux3:
                status = 1
            else:
                status = 0
            if flag == 1 and m == id_carro:
                status = central_statecar
                pd[m] = prox_direc_car
            if central_statecar == 2:
                aux4 +=1
                if aux4 == 10:
                    status = 0
                    flag = 0
                    aux4 = 0
            image2, posicoes[m], da[m], pd[m], velocidade, estacionado = carros[m].movimento_carro(image2, matriz_cidade, posicoes[m], da[m], pd[m], velocidade, status, estacionado)
            msg = str(status) + '/' + str(posicoes[m][0]) + '/' + str(posicoes[m][1]) + '/' + str(velocidade)
            topico =  'transporte/carro' + str(m)
            clients[m].publish(topico, msg)
    aux+=1    
    aux7+=1   
    image3 = image - image2   
    cv2.imshow(window_name, image3)
    key = cv2.waitKey(1)
    if key == 27:
        break
    elif key == 97:
        if tempo > 0.01:
            tempo -= 0.01
    elif key == 98:
        tempo += 0.01
    elif key == 99:
        if teste == 1:
            teste = 0
        else:
            teste = 1
    time.sleep(0.2)
cv2.destroyAllWindows()
j = 0
for client in clients:
    # print("Disconnecting Client", j) 
    client.loop_stop()
    client.disconnect()
    print("Disconnected Client", j)
    j+=1
# time.sleep(2)