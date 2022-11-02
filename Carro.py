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
nclients=1
for i  in range(nclients):
    cname="Carro"+str(i)
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
    
time.sleep(2)

i = 0

while 1:
    clients[0].subscribe("transporte/central/carro",1)
    
    #Check if you are connected
    if conec == 1:
        #Checks if the 'p' button for Pub was pressed and if it is not disconnected, if so it makes pub
        if (keyboard.read_key() == "c") and (disc == 0):
            #print("Publishing message to topic","transporte/carro/teste1")
            clients[0].publish("transporte/carro/central", "Confirmação OK" + str(i))
            i+=1
        #Pressing the d key ends the connection
        if keyboard.read_key() == "d":
            break
j = 0
for client in clients:
    print("Disconnecting Client", j) 
    client.loop_stop()
    client.disconnect()
    print("Disconnected Client", j)
    j+=1
time.sleep(2)