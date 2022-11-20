# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 06:48:40 2022

@author: luizg
"""

#Required libraries
import paho.mqtt.client as mqtt
# import keyboard
import time
import cv2

path = r'Imagens\central.png'
image = cv2.imread(path)
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
carro_em_uso = -1
status = []
iniciou = 0
pd = 0
cliente = 'central'
aux = 0

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
    # if id_carro == carro_em_uso:
    #     print("Message received = '", str(msg.payload.decode("utf-8")), "'", "on topic '", msg.topic, "'")
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
    global iniciou
    global pd
    global cliente
    msg = mensagem.split('/')
    topic = topico.split('/')
    topic = topic[1]
    aux = topic.split('o')
    if iniciou == 0:
        if aux[0] == 'inici':
            X_MAX = int(msg[0])
            Y_MAX = int(msg[1])
            ncarros = int(msg[2])
            for i in range(0,ncarros):
                status.append(0)
            print('Recebeu inicio')
            iniciou = 1
            flag = 0
        else:
            flag = 7
    elif iniciou == 1:
        x = int(msg[1])
        y = int(msg[2])
        if aux[0] == 'carr':
            cliente = 'carro'
            id_carro = int(aux[1])
            if id_carro != carro_em_uso:
                status[id_carro] = int(msg[0])
            velocidade = int(msg[3])
            pd = int(msg[4])
        elif aux[0] == 'usuari':
            cliente = 'usuario'
            tipo = int(msg[0])
        if cliente == 'usuario':
            if tipo == 0:
                x_viagem = int(x)
                y_viagem = int(y)
                flag = 1
                tipo = 5
            elif tipo == 1:
                x_viagem = int(x)
                y_viagem = int(y)
            elif tipo == 2:
                client.publish("transporte/central_usuario", '4')
                top = 'transporte/central_carro'
                menssage = str(carro_em_uso) + '/2/0'
                client.publish(top, menssage)
                flag = 0
                tipo = 5
            
    arq_name = 'Historico/' + str(topic) + '.txt'
    arquivo = open(arq_name,'a')
    arquivo.write(mensagem + "\n")
    arquivo.close()
 
def mover_carro(x_viagem, y_viagem, x_atual, y_atual):
    global pd
    global flag
    if x_viagem % 2 == 0:
        if(x_atual < x_viagem):
            if pd <=1:
                direc_atual = 2
            elif pd == 2:
                direc_atual = 2
            elif pd == 3:
                direc_atual = 0
        elif x_atual > x_viagem:
            if pd <=1:
                direc_atual = 1
            elif pd == 2:
                direc_atual = 0
            elif pd == 3:
                direc_atual = 1
        elif y_atual < y_viagem:
            if pd == 0:
                direc_atual = 0
            elif pd == 1:
                direc_atual = 3
            elif pd >= 2:
                direc_atual = 1
        elif y_atual > y_viagem:
            if pd == 0:
                direc_atual = 1
            elif pd == 1:
                direc_atual = 0
            elif pd >= 2:
                direc_atual = 2
    elif x_viagem % 2 == 1:
        print('aqui')
        if y_atual < y_viagem:
            if pd == 0:
                direc_atual = 0
            elif pd == 1:
                direc_atual = 3
            elif pd >= 2:
                direc_atual = 1
        elif y_atual > y_viagem:
            if pd == 0:
                direc_atual = 1
            elif pd == 1:
                direc_atual = 0
            elif pd >= 2:
                direc_atual = 2
        elif(x_atual < x_viagem):
            if pd <=1:
                direc_atual = 2
            elif pd == 2:
                direc_atual = 2
            elif pd == 3:
                direc_atual = 0
        elif x_atual > x_viagem:
            if pd <=1:
                direc_atual = 1
            elif pd == 2:
                direc_atual = 0
            elif pd == 3:
                direc_atual = 1
    if x_atual == x_viagem and y_atual == y_viagem:
        if flag == 2:
            flag = 3
            return 4
        elif flag == 5:
            flag = 6
            return 4
    return direc_atual

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
    
# time.sleep(2)
cv2.namedWindow('Central', cv2.WINDOW_AUTOSIZE)
for j in range(10):
    tp = 'transporte/carro' + str(j)
    client.subscribe(tp,1)
client.subscribe("transporte/usuario0",1)
client.subscribe("transporte/inicio",1)
while 1:
    cv2.imshow('Central', image)
    key = cv2.waitKey(1)
    client.subscribe("transporte/usuario0",1)
    #Check if you are connected
    if conec == 1:
        if iniciou == 0:
            top = 'transporte/central_carro'
            menssage = '-2/0/0'
            client.publish(top, menssage)
        if flag == 1:
            aux = 0
            if x_viagem < X_MAX and y_viagem < Y_MAX:
                for j in range(0, len(status)):
                    if status[j] == 0:
                        carro_em_uso = j
                        break
                while aux == 0:
                    if id_carro == carro_em_uso:
                        if cliente == 'carro':
                            x_atual = x
                            y_atual = y
                            client.publish("transporte/central_usuario", '0')
                            top = 'transporte/central_carro'
                            menssage = str(carro_em_uso) + '/2/0'
                            client.publish(top, menssage)
                            flag = 2
                            aux = 1
                    else:
                        # if keyboard.read_key() == "m":
                        if key == 109:
                            client.publish("transporte/central_usuario", '4')
                            top = 'transporte/central_carro'
                            menssage = str(carro_em_uso) + '/2/0'
                            client.publish(top, menssage)
                            aux = 1
            tipo = 5
        if flag == 2:
            aux = 0
            while aux == 0 :
                if id_carro == carro_em_uso:
                    if cliente == 'carro':
                        x_atual = x
                        y_atual = y
                        direcao_atual = mover_carro(x_viagem, y_viagem, x_atual, y_atual)
                        top = 'transporte/central_carro'
                        menssage = str(carro_em_uso) + '/3/' + str(direcao_atual)
                        client.publish(top, menssage)
                        aux = 1
        if flag == 3:
            client.publish("transporte/central_usuario", '1')
            top = 'transporte/central_carro'
            menssage = str(carro_em_uso) + '/2/0'
            client.publish(top, menssage)
            flag = 4
        if flag == 4:
            if tipo == 1:
                if x_viagem < X_MAX and y_viagem < Y_MAX:
                    client.publish("transporte/central_usuario", '2')
                else:
                    client.publish("transporte/central_usuario", '4')
                    top = 'transporte/central_carro'
                    menssage = str(carro_em_uso) + '/2/0'
                    client.publish(top, menssage)
                tipo = 5
                flag = 5
        if flag == 5:
            aux = 0
            while aux == 0:
                if id_carro == carro_em_uso:
                    if cliente == 'carro':
                        x_atual = x
                        y_atual = y
                        direcao_atual = mover_carro(x_viagem, y_viagem, x_atual, y_atual)
                        top = 'transporte/central_carro'
                        menssage = str(carro_em_uso) + '/3/' + str(direcao_atual)
                        client.publish(top, menssage)
                        aux = 1
        if flag == 6:
            client.publish("transporte/central_usuario", '3')
            top = 'transporte/central_carro'
            menssage = str(carro_em_uso) + '/2/0'
            client.publish(top, menssage)
            flag = 0
        if flag == 7:
            # if (keyboard.read_key() == "e"):
            if key == 101:
                break
        # Checks if the 'p' button for Pub was pressed and if it is not disconnected, if so it makes pub
        # if (keyboard.read_key() == "p"):
        if key == 112:
            # client.publish("transporte/carro0", "Solicitação " + str(i))
            estado = input('Manda o estado aí doidão: ')
            client.publish("transporte/central_usuario", estado)
        # Pressing the d key ends the connection
        # if keyboard.read_key() == "d":
        if key == 100:
            client.publish("transporte/central_usuario", '4')
            break
        
    time.sleep(0.4)
        
cv2.destroyAllWindows()      
print("Disconnecting Central") 
client.loop_stop()
client.disconnect()
print("Disconnected Central")
