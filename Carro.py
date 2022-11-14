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
import keyboard
import time
import numpy as np
import cv2
import Mapa as mp
from random import randint

path = r'Imagens\background_mapa.png'

#Global variables
first = 0
conec = 0
disc  = 1

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
    print("Message received = '", str(msg.payload.decode("utf-8")), "'", "on topic '", msg.topic, "'")

#Brokers address
broker_address =    'test.mosquitto.org'

clients=[]
nclients=2
for i  in range(nclients):
    cname="Carro1"+str(i)
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

Cidade1, image, image2, window_name = mp.mapa_cidade(path, quarteirao=60)
matriz_cidade, X_MAX, Y_MAX = mp.matriz_posicoes(Cidade1)
posicoes, carros = mp.cria_carros(X_MAX, Y_MAX, matriz_cidade, quantidade=50)
aux = 1
da = []
pd = []
for n in range(len(carros)):
    da.append(0)
    pd.append(3)
teste = 1
tempo = 0.05
aux7 = 0

while 1:
    if(teste == 1):
        for m in range(len(carros)):
            velocidade = mp.proxima(pd[m], posicoes, m, posicoes[m])
            image2, posicoes[m], da[m], pd[m], velocidade = carros[m].movimento_carro(image2, matriz_cidade, posicoes[m], da[m], pd[m], velocidade)
            if(m==0):
                clients[0].publish("transporte/carro0/central", str(posicoes[0]))
            if(m==1):
                clients[1].publish("transporte/carro1/central", str(posicoes[1]))
    if aux == 5:
        for p in range(len(da)):
            if da[p] == 0:
                da[p] = randint(0,2)
            else:
                da[p] = randint(0,2)
        aux=0
    aux+=1    
    if aux7 == 15:
        for q in range(len(pd)):
            pd[q] = randint(0,3)

        aux7=0
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
    time.sleep(1)
    
    # for i in range(len(clients)):
    #     string = 'transporte/central/carro'+str(i)
    #     clients[i].subscribe(string,1)
    
    # #Check if you are connected
    # if conec == 1:
    #     #Checks if the 'p' button for Pub was pressed and if it is not disconnected, if so it makes pub
    #     if (keyboard.read_key() == "c") and (disc == 0):
    #         #print("Publishing message to topic","transporte/carro/teste1")
    #         clients[0].publish("transporte/carro/central", "Confirmação OK" + str(i))
    #         i+=1
    #     #Pressing the d key ends the connection
    #     if keyboard.read_key() == "d":
    #         break
cv2.destroyAllWindows()
j = 0
for client in clients:
    print("Disconnecting Client", j) 
    client.loop_stop()
    client.disconnect()
    print("Disconnected Client", j)
    j+=1
time.sleep(2)