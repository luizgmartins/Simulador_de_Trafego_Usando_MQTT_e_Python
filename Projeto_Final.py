# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 16:21:21 2022

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
#broker_address =    'iot.eclipse.org'
broker_address =    'test.mosquitto.org'
#broker_address =    'broker.hivemq.com'
#broker_address =    '192.168.1.184'

clients=[]
nclients=1
mqtt.Client.connected_flag=False
for i  in range(nclients):
    cname="Client"+str(i)
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


#Create a client instance
#print("Creating new instance...")
#client = mqtt.Client("P1")
#print("Creating new instance...")
#client = mqtt.Client("P2")
time.sleep(2)

#Activates connection, disconnection, log and incoming message functions
#client.on_connect = on_connect
#client.on_disconnect= on_disconnect
#client.on_log = on_log
#client.on_message = on_message

#Connect to broker and start loop
#print("Connecting to broker " + broker_address + '...')
#client.connect(broker_address)
#time.sleep(2)
#client.loop_start()

i = 0

while 1:
    #Check if you are connected
    if conec == 1:
        #Check if you were already connected, otherwise subscribe to the topic
        if (first == 0):
            clients[0].subscribe("transporte/carro1/teste1",1)
            first = 1
        #Checks if the 'p' button for Pub was pressed and if it is not disconnected, if so it makes pub
        if (keyboard.read_key() == "p") and (disc == 0):
            #client.subscribe([("house/sensor1/teste1",0), ("house/sensor1/teste1",1)])
            print("Publishing message to topic","house/sensor1/teste2")
            clients[0].subscribe("house/sensor1/teste1",1)
            clients[0].publish("house/sensor1/teste1", "Vamo testar " + str(i))
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
