# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 06:48:40 2022

@author: luizg
"""

#Required libraries
import paho.mqtt.client as mqtt
import keyboard
import time

#Global variables
first = 0
conec = 0
disc  = 1
status = 0
velocidade = 1
x = 0
y = 0
tipo = 5
flag = 0
X_MAX = 0
Y_MAX = 0

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
    salva_msg(str(msg.payload.decode("utf-8")), str(msg.topic))

def salva_msg(mensagem, topico):
    global status
    global x
    global y
    global velocidade
    global tipo
    global id_carro
    global X_MAX
    global Y_MAX
    global flag
    global x_viagem
    global y_viagem
    msg = mensagem.split('/')
    topic = topico.split('/')
    topic = topic[1]
    aux = topic.split('o')
    if aux[0] == 'inic':
        X_MAX = int(msg[0])
        Y_MAX = int(msg[1])
    else:
        x = int(msg[1])
        y = int(msg[2])
        if aux[0] == 'carr':   
            status = int(msg[0])
            velocidade = int(msg[3])
            id_carro = int(aux[1])
        elif aux[0] == 'usuari':
            tipo = int(msg[0])
        if tipo == 0:
            x_viagem = int(x)
            y_viagem = int(y)
            status = 5
            flag = 1
    arq_name = 'Historico/' + str(topic) + '.txt'
    arquivo = open(arq_name,'a')
    arquivo.write(mensagem + "\n")
    arquivo.close()
 
def mover_carro(x_viagem, y_viagem, x_atual, y_atual):
    global flag
    if(x_atual < x_viagem):
        prox_direcao = 3
    elif x_atual > x_viagem:
        prox_direcao = 2
    elif y_atual < x_viagem:
        prox_direcao = 0
    elif y_atual > x_viagem:
        prox_direcao = 1
    elif x_atual == x_viagem and y_atual == y_viagem:
        if flag == 2:
            flag = 3
        elif flag == 4:
            flag = 5
    return prox_direcao

#Brokers address
broker_address =    'test.mosquitto.org'
broker_address =    'broker.emqx.io'

client = mqtt.Client("Central")
client.on_connect = on_connect
client.on_disconnect= on_disconnect
#client.on_log = on_log
client.on_message = on_message
client.connect(broker_address)
client.loop_start()
    
time.sleep(2)

for j in range(10):
    tp = 'transporte/carro' + str(j)
    client.subscribe(tp,1)
client.subscribe("transporte/usuario0",1)
client.subscribe("transporte/inicio",1)
while 1:
    client.subscribe("transporte/usuario0",1)
    #Check if you are connected
    if conec == 1:
        if flag == 1:
            if x_viagem < X_MAX and y_viagem < Y_MAX and x_viagem > 0 and y_viagem>0:
                if int(status) == 0:
                    carro_em_uso = id_carro
                    x_atual = x
                    y_atual = y
                    client.publish("transporte/central_usuario", '0')
                    top = 'transporte/carro' + str(carro_em_uso)
                    menssage = str(carro_em_uso) + '/2/0'
                    client.publish(top, menssage)
                    flag = 2
            else:
                client.publish("transporte/central_usuario", '4')
                top = 'transporte/carro' + str(carro_em_uso)
                menssage = str(carro_em_uso) + '/2/0'
                client.publish(top, menssage)
            tipo = 5
        if flag == 2:
            if id_carro == carro_em_uso:
                x_atual = x
                y_atual = y
                prox_direcao = mover_carro(x_viagem, y_viagem, x_atual, y_atual)
                top = 'transporte/carro' + str(carro_em_uso)
                menssage = str(carro_em_uso) + '/3/' + str(prox_direcao)
                client.publish(top, menssage)
        if flag == 3:
            client.publish("transporte/central_usuario", '1')
            top = 'transporte/carro' + str(carro_em_uso)
            menssage = str(carro_em_uso) + '/2/0'
            client.publish(top, menssage)
            if x_viagem < X_MAX and y_viagem < Y_MAX and x_viagem > 0 and y_viagem>0:
                flag = 4
                client.publish("transporte/central_usuario", '2')
            else:
                client.publish("transporte/central_usuario", '4')
                top = 'transporte/carro' + str(carro_em_uso)
                menssage = str(carro_em_uso) + '/2/0'
                client.publish(top, menssage)
        if flag == 4:
            if id_carro == carro_em_uso:
                x_atual = x
                y_atual = y
                prox_direcao = mover_carro(x_viagem, y_viagem, x_atual, y_atual)
                top = 'transporte/carro' + str(carro_em_uso)
                menssage = str(carro_em_uso) + '/3/' + str(prox_direcao)
                client.publish(top, menssage)
        if flag == 5:
            client.publish("transporte/central_usuario", '3')
            top = 'transporte/carro' + str(carro_em_uso)
            menssage = str(carro_em_uso) + '/2/' + str(prox_direcao)
            client.publish(top, menssage)
            flag = 0
        if tipo == 2:    
            client.publish("transporte/central_usuario", '4')
            
        #Checks if the 'p' button for Pub was pressed and if it is not disconnected, if so it makes pub
        if (keyboard.read_key() == "p"):
            # client.publish("transporte/carro0", "Solicitação " + str(i))
            estado = input('Manda o estado aí doidão: ')
            client.publish("transporte/central_usuario", estado)
        #Pressing the d key ends the connection
        if keyboard.read_key() == "d":
            break
        
print("Disconnecting Central") 
client.loop_stop()
client.disconnect()
print("Disconnected Central")
time.sleep(2)