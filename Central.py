# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 06:48:40 2022

@author: luizg
"""
# =============================================================================
# Required libraries
# =============================================================================
import paho.mqtt.client as mqtt
import time
import cv2
from datetime import datetime
# =============================================================================
# Global variables
# =============================================================================
path = r'Imagens\central.png'
image = cv2.imread(path)
first = conec = status = x = y = flag = X_MAX = Y_MAX = iniciou = pd = aux = aux1 = ncarros = subs = recebido = 0
disc = velocidade = 1
tipo = 5
carro_em_uso = -1
status = []
cliente = 'central'
id_carro = -2
posicoes = []
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
# Tratamento das mensagens recebidas de início, do carro e do usuário
# =============================================================================
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
    global ncarros
    global recebido
    global posicoes
    if recebido == 0:
         recebido = 1
    msg = mensagem.split('/')
    topic = topico.split('/')
    topic = topic[1]
    aux_msg = topic.split('o')
    if iniciou == 0:
        if aux_msg[0] == 'inici':
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
        if aux_msg[0] == 'matriz':
            msg.pop(-1)
            posicoes = msg
        else:
            x = int(msg[1])
            y = int(msg[2])
            if aux_msg[0] == 'carr':
                cliente = 'carro'
                id_carro = int(aux_msg[1])
                if id_carro != carro_em_uso:
                    status[id_carro] = int(msg[0])
                velocidade = int(msg[3])
                pd = int(msg[4])
            elif aux_msg[0] == 'usuari':
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
    data_e_hora_em_texto = datetime.now().strftime('%d/%m/%Y %H:%M')
    info =  data_e_hora_em_texto + ' ' + mensagem + '\n'
    arquivo.write(info)
    arquivo.close()
# =============================================================================
#  Função que seleciona qual a próxima direção para o carro seguir de acordo
# com a localização enviada pelo usuário
# =============================================================================
def mover_carro(x_viagem, y_viagem, x_atual, y_atual, carro_em_uso):
    global pd
    global flag
    global aux1
    if aux1 == 0:
        if(x_viagem > x_atual):
            if pd == 0:
                direc_atual = 2
            elif pd == 1:
                direc_atual = 2
            elif pd == 2:
                direc_atual = 2
            elif pd == 3:
                direc_atual = 0
            return direc_atual
        elif x_viagem < x_atual:
            if pd == 0:
                direc_atual = 1
            elif pd == 1:
                direc_atual = 1
            elif pd == 2:
                direc_atual = 0
            elif pd == 3:
                direc_atual = 1
            return direc_atual
        if x_atual == x_viagem:
            aux1 = 1
    if aux1 == 1:
        if y_viagem > y_atual:
            if pd == 0:
                direc_atual = 0
            elif pd == 1:
                direc_atual = 2
            elif pd == 2:
                direc_atual = 1
            elif pd == 3:
                direc_atual = 1
            return direc_atual
        elif y_viagem < y_atual:
            if pd == 0:
                direc_atual = 1
            elif pd == 1:
                direc_atual = 0
            elif pd == 2:
                direc_atual = 2
            elif pd == 3:
                direc_atual = 2
            return direc_atual
        if y_atual == y_viagem:    
            aux1 = 0
    if x_atual == x_viagem and y_atual == y_viagem:
        if flag == 2:
            flag = 3
            return 4
        elif flag == 5:
            flag = 6
            return 4
    return 4
# =============================================================================
# Brokers address
# =============================================================================
# broker_address =    'test.mosquitto.org'
broker_address =    'broker.emqx.io'
# =============================================================================
# Conectando a central ao broker
# =============================================================================
client = mqtt.Client("Central1")
client.on_connect = on_connect
client.on_disconnect= on_disconnect
#client.on_log = on_log
client.on_message = on_message
client.connect(broker_address)
client.loop_start()
# =============================================================================
# Faz as subs de cada carro, do usuário, de inicio e da matriz de posições
# =============================================================================
for j in range(10):
    tp = 'transporte/carro' + str(j)
    client.subscribe(tp,1)    
client.subscribe("transporte/usuario0",1)
client.subscribe("transporte/inicio",1)
client.subscribe('transporte/matrizo',1)
# =============================================================================
# Inicia uma janela do opencv
# =============================================================================
cv2.namedWindow('Central', cv2.WINDOW_AUTOSIZE)
# =============================================================================
# Loop principal
# =============================================================================
while 1:
    cv2.imshow('Central', image)
    key = cv2.waitKey(1)
    #Check if you are connected
    if conec == 1:
        # Verifica se o sistema recebeu a mensagem de início dos carros
        if iniciou == 0:
            top = 'transporte/central_carro'
            menssage = '-2/0/0'
            client.publish(top, menssage)
        elif iniciou == 1:
            if subs == 0:
                for j in range(ncarros):
                    tp = 'transporte/carro' + str(j)
                    client.subscribe(tp,1)
            subs = 1
        # Roda a sequência cada vez que a central recebe alguma mensagem
        if recebido == 1:
            recebido = 0
            # Flags são estados que a central processa a viagem
            if flag == 1:
                aux = 0
                verificacao = '(' + str(x_viagem) + ',' + str(y_viagem) + ')'
                # Verifica se a posição (x,y) que o usuário enviou existe no mapa utilizado
                if verificacao in posicoes:
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
                            # Se a tecla 'c' for pressionada, cancela a viagem
                            if key == 99:
                                client.publish("transporte/central_usuario", '4')
                                top = 'transporte/central_carro'
                                menssage = str(carro_em_uso) + '/2/0'
                                client.publish(top, menssage)
                                aux = 1
                                flag = 0
                else:
                    client.publish("transporte/central_usuario", '6')
                    flag = 0
                tipo = 5
            if flag == 2:
                aux = 0
                while aux == 0 :
                    if id_carro == carro_em_uso:
                        if cliente == 'carro':
                            x_atual = x
                            y_atual = y
                            direcao_atual = mover_carro(x_viagem, y_viagem, x_atual, y_atual, carro_em_uso)
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
                    verificacao = '(' + str(x_viagem) + ',' + str(y_viagem) + ')'
                    if verificacao in posicoes:
                    # Verifica se a posição (x,y) que o usuário enviou existe no mapa utilizado
                        client.publish("transporte/central_usuario", '2')
                        flag = 5
                    else:
                        client.publish("transporte/central_usuario", '6')
                        top = 'transporte/central_carro'
                        menssage = str(carro_em_uso) + '/2/0'
                        client.publish(top, menssage)
                        flag = 0
                    tipo = 5
            if flag == 5:
                aux = 0
                while aux == 0:
                    if id_carro == carro_em_uso:
                        if cliente == 'carro':
                            x_atual = x
                            y_atual = y
                            direcao_atual = mover_carro(x_viagem, y_viagem, x_atual, y_atual, carro_em_uso)
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
                # Pressing the 'esc' key ends the connection
                if key == 27:
                    client.publish("transporte/central_usuario", '4')
                    flag = 0
                    break
        # Pressing the 'esc' key ends the connection
        if key == 27:
            client.publish("transporte/central_usuario", '4')
            flag = 0
            break
    time.sleep(0.1)
# =============================================================================
# Encerra a aplicação e desconecta a central    
# =============================================================================
cv2.destroyAllWindows()      
print("Disconnecting Central") 
client.loop_stop()
client.disconnect()
print("Disconnected Central")