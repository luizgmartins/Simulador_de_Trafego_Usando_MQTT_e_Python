# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 07:44:07 2022

@author: luizg
"""
# =============================================================================
# Required libraries
# =============================================================================
import paho.mqtt.client as mqtt
import keyboard
import time
# =============================================================================
# Global variables
# =============================================================================
first = conec = recebido = 0
disc  = 1
viagem =  'n'
status = 5
topico = 'transporte/usuario0'
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
# Function to show you are disconnected
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
# Function to print the received message
# =============================================================================
def on_message(client, userdata, msg):
    # print("Message received = '", str(msg.payload.decode("utf-8")), "'", "on topic '", msg.topic, "'")
    salva_msg(str(msg.payload.decode("utf-8")), str(msg.topic))
# =============================================================================
# Tratamento das mensagens recebidas da central
# =============================================================================
def salva_msg(mensagem, topico):
    global status
    global recebido
    if recebido == 0:
         recebido = 1
    status = int(mensagem)
# =============================================================================
# #Brokers address
# =============================================================================
# broker_address =    'test.mosquitto.org'
broker_address =    'broker.emqx.io'
# =============================================================================
# Conectando o Usuário ao broker
# =============================================================================
client = mqtt.Client("Usuario2")
client.on_connect = on_connect
client.on_disconnect= on_disconnect
#client.on_log = on_log
client.on_message = on_message
client.connect(broker_address)
client.loop_start()
    
time.sleep(2)
# =============================================================================
# Faz o sub da central
# =============================================================================
client.subscribe("transporte/central_usuario",1)
# =============================================================================
# Loop principal
# =============================================================================
while 1:
    flag = 0
    #Check if you are connected
    if conec == 1:
        # Pressione 'y' para iniciar uma viagem
        if keyboard.read_key() == "y":
            viagem = input('Gostaria de solicitar uma viagem?[y/n]')
            if viagem == 'y':
                print('Envie qual o seu local: ')
                x = int(input('x: '))
                y = int(input('y: '))
                msg = str(0) + '/' + str(x) + '/' + str(y)
                client.publish(topico, msg)
                viagem = 'aguardando'
            elif viagem != 'n':
                print('Parâmetro inválido')
        # Aguarda mensagens da central
        while viagem == 'aguardando':
            if recebido == 1:
                recebido = 0
                if flag == 0:
                    print('Aguardando retorno da central...')
                    flag = 1
                # Pressione 's' cancela a viagem
                if keyboard.read_key() == "s":
                    print('Cancelamento de viagem solicitado')
                    msg = '2/0/0'
                    client.publish(topico, msg)
                else:
                    if status == 4:
                        print('Viagem cancelada')
                        status = 5
                        viagem = 'n'
                        break
                    elif status == 6:
                        print('Parâmetro inválido')
                        print('Viagem cancelada')
                        status = 5
                        viagem = 'n'
                        break
                    elif status == 0:
                        if flag == 1:
                            print('Viagem confirmada pela central')
                            print('Aguarde no local de partida')
                            flag = 2
                            status = 5
                    elif status == 1:
                        print('Carro chegou no local de partida')
                        print('Envie o local de destino: ')
                        x = int(input('x: '))
                        y = int(input('y: '))
                        msg = str(1) + '/' + str(x) + '/' + str(y)
                        client.publish(topico, msg)
                        flag = 0
                        status = 5
                    elif status == 2:
                        print('Destino confirmado pela central')
                        flag = 0
                        status = 5
                    elif status == 3:
                        print('Você chegou ao seu destino')
                        viagem = 'n'
                        break
                        status = 5
        # Se pressionar 'esc', encerra a aplicação
        if keyboard.read_key() == "esc":        
            break
# =============================================================================
# Encerra a aplicação e desconecta a central    
# =============================================================================        
print("Disconnecting Usuario") 
client.loop_stop()
client.disconnect()
print("Disconnected Usuario")
time.sleep(2)