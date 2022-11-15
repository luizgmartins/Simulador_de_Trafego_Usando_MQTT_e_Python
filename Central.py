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
tipo = 0

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
    global status
    global x
    global y
    global velocidade
    global tipo
    msg = mensagem.split('/')
    topic = topico.split('/')
    topic = topic[1]
    aux = topic.split('o')
    x = msg[1]
    y = msg[2]
    if aux[0] == 'carr':   
        status = msg[0]
        velocidade = msg[3]
    elif aux[0] == 'usuari':
        tipo = msg[0]
    arq_name = 'Historico/' + str(topic) + '.txt'
    arquivo = open(arq_name,'a')
    arquivo.write(mensagem + "\n")
    arquivo.close()
    
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

i = 0
for j in range(10):
    tp = 'transporte/carro' + str(j)
    client.subscribe(tp,1)
client.subscribe("transporte/usuario0",1)
while 1:
    #Check if you are connected
    if conec == 1:
        #Checks if the 'p' button for Pub was pressed and if it is not disconnected, if so it makes pub
        if (keyboard.read_key() == "p") and (disc == 0):
            #print("Publishing message to topic","transporte/carro/teste2")
            client.publish("transporte/carro0", "Solicitação " + str(i))
            client.publish("transporte/usuario0", "Confirmação " + str(i))
            i+=1
        #Pressing the d key ends the connection
        if keyboard.read_key() == "d":
            break
        
print("Disconnecting Central") 
client.loop_stop()
client.disconnect()
print("Disconnected Central")
time.sleep(2)