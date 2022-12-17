# Simulador de Tráfego Usando MQTT e Python
Projeto da disciplina de Introdução a Python em Engenharia da Universidade Federal de Pernambuco - UFPE. O projeto consiste em um simulador de tráfego, contendo um mapa de uma cidade fictícia, carros se movendo aleatoriamente ou comandados por uma central e um usuário fazendo requisições de viagem. A comunicação entre os carros e a central, assim como a comunicação entre a central e o usuário é via MQTT através de um broker. O sistema atualiza de forma discreta ao longo do tempo e as posições, velocidades e status dos veículos são enviados para a central que utiliza esses dados e também armazena em arquivos.

<p align="center">
    <img src="https://github.com/luizgmartins/Simulador_de_Trafego_Usando_MQTT_e_Python/blob/main/Imagens/gif_simu.gif"></a>
</p>

OBS.: Não foi implementado programação paralela para executar os scripts em conjunto, portanto é necessário executá-los em terminais separados. De preferência na sequência Carro.py, Central.py e Usuario.py.

OBS2.: O script do usuário nem sempre atualiza os prints das mensagens apesar de está em loop. É necessário pressionar alguma tecla do teclado que não esteja em uso no script para aparecer os prints.

## Criação do mapa da cidade
Foi utilizada a biblioteca do opencv para criação do mapa e do movimento dos carros de forma visual. Inicialmente, é utilizado uma imagem de fundo totalmente em branco e a partir dela é criado o mapa da cidade com ruas, quarteirões e posições para movimentar os carros. Para criar o mapa é definido alguns parâmetros: a largura da rua é de 30 pixels, contendo duas faixas de 15 pixels cada; o tamanho dos quarteirões são definidos no início do script e a partir do valor dele será definido a quantidade de ruas e o tamanho total do mapa.

<p align="center">
    <img src="https://github.com/luizgmartins/Simulador_de_Trafego_Usando_MQTT_e_Python/blob/main/Imagens/mapa_construido(240).png"></a>
</p>

Para criar o mapa é utilizado as linhas imaginárias verticais e horizontais do centro da imagem, para o primeiro quadrante: é deslocado uma faixa de rua para o lado e vai somando o tamanho de um quarteirão e uma rua até que não seja possível colocar mais um conjunto rua + quarteirão. Quando chega no limite é colocado uma rua e uma linha que representa o limite do mapa. É feito a mesma coisa para os outros quadrantes do mapa de forma espelhada. Por fim, é possível obter o mapa da cidade com os limites da cidade definidos e dentro dos limites de tamanho da imagem utilizada.

Foi definido três valores para o tamanho dos quarteirões (60, 120 ou 240), esses valores foram escolhidos por serem múltiplos de 30, que é o tamanho em pixels que o carro pode se deslocar no mapa. O motivo da escolha desses valores também foi devido a lógica do deslocamento dos carros que será explicado mais adiante.
Após construir o mapa foram nomeadas as ruas horizontais e verticais para uma melhor visualização.

Foi criado um objeto chamado de “cidade” que contém listas com coordenadas das ruas horizontais e verticais, lista com os limites superior, inferior, esquerda e direita do mapa, o valor do passo do carro (fixo em 30) e o tamanho do quarteirão.

<p align="center">
    <img src="https://github.com/luizgmartins/Simulador_de_Trafego_Usando_MQTT_e_Python/blob/main/Imagens/class_cidade.png"></a>
</p>

Para facilitar o deslocamento dos carros e o envio de posições para a central, foi criada uma matriz contendo todas as possíveis posições para os carros poderem se deslocar no mapa.

A matriz é criada com valores em forma de tuplas contendo inicialmente o valor (-1,-1). O tamanho da matriz é calculado a partir do tamanho de posições do limite superior ao inferior (X_MAX) e de posições do limite da esquerda ao da direita (Y_MAX). Cada posição fica a uma distância de 30 pixels uma da outra, como o quarteirão é múltiplo de 30 e as ruas contém 30 pixels cada, é possível determinar quantas posições é possível obter.
As tuplas da matriz devem ser as coordenadas horizontais e verticais na imagem. Então a matriz que continha somente valores (-1,-1) será preenchida com as coordenadas do centro da posição na imagem. Como pode ser visto na imagem abaixo, para a posição com x=0 e y=0 da matriz, as coordenadas do centro dela na imagem é de (68,69). 

<p align="center">
    <img src="https://github.com/luizgmartins/Simulador_de_Trafego_Usando_MQTT_e_Python/blob/main/Imagens/Mapa240.jpg"></a>
</p>

Para preencher os valores corretos das coordenadas e deixando somente os quarteirões com valores (-1,-1), foi deslocado para direita 15 pixels com relação ao limite à esquerda e 15 pixels para baixo com relação ao limite superior, assim obtendo o centro da primeira posição. Assim vai salvando na matriz as tuplas com as posições da faixa de rua da primeira rua Horizontal até chegar ao Y_MAX. Isso é feito nas duas primeiras ruas horizontais e pulado um quarteirão para baixo e vai preencher mais duas ruas até que chegue ao fim da última rua horizontal. Preenchendo o centro das posições de cada linha em verde visto na imagem abaixo.

<p align="center">
    <img src="https://github.com/luizgmartins/Simulador_de_Trafego_Usando_MQTT_e_Python/blob/main/Imagens/matriz_posicoes_H.jpg"></a>
</p>

Para preencher o que falta é utilizado a mesma lógica, mas agora olhando as faixas de rua verticais e ignorando quem tem valor diferente de (-1,-1). Após obter os centros das posições, a matriz de posições contém também os valores das faixas em azul da imagem abaixo.

<p align="center">
    <img src="https://github.com/luizgmartins/Simulador_de_Trafego_Usando_MQTT_e_Python/blob/main/Imagens/matriz_posicoes_V.jpg"></a>
</p>

Como os carros estarão sempre no centro das posições, é possível saber exatamente onde o carro está, deslocar ele facilmente e impedir que ele entre nos quarteirões sem querer.

## Movimento dos carros
Ao selecionar a quantidade inicial de carros esses serão criados como instâncias e conectados ao broker. No fim da simulação cada carro é desconectado do broker. Cada carro também é criado como um objeto que possui uma ID de identificação e uma placa (Mas a placa não foi implementada com valores diferentes). O objeto carro possui uma função de deslocamento (movimento_carro).

Para colocar os carros no mapa foi necessário criar uma cópia da imagem de fundo que estava em branco no início do script e foi utilizado para criar o mapa, suas cores são invertidas, assim é possível criar uma máscara contendo somente o que foi desenhado nela. No fim a imagem do mapa é subtraído dessa máscara contendo os carros, isso resulta em uma imagem contendo o mapa e os carros. Isso foi necessário para que o movimento dos carros não apagasse as linhas do mapa caso eles pudessem ser desenhados em cima de alguma linha.

A lógica de movimento dos carros consiste em uma próxima direção, em uma direção atual, na velocidade do carro e sua posição anterior. A posição anterior é sempre a atual antes do próximo deslocamento do carro, assim é possível apagar o carro onde ele foi desenhado anteriormente para poder desenhá-lo na próxima posição do mapa. A velocidade do carro é 1 ou 0, caso seja 1 o carro desloca uma posição ou passo (que equivale a 30 pixels) e caso seja 0 ele fica parado. A velocidade é 0 sempre que a próxima direção que o carro irá seguir houver algum obstáculo, seja um carro ou alguma posição que ele não pode ir. As “próximas direções” dos carros possuem valores entre 0 e 3, sendo, próxima direção para direita, para esquerda, para cima e para baixo, respectivamente. As “direções atuais” podem ser valores entre 0 e 2, sendo direção atual igual a 0 para que o carro continue na mesma direção que ele está. Por exemplo, se a próxima direção dele é 0 (para direita) e a direção atual for 0 ele continua seguindo para direita. 

Tanto para próxima direção para direita ou para esquerda, as direções atuais, se tiverem valores 1 ou 2, irão fazer o carro ir para próxima direção para cima ou para baixo, respectivamente. Isto é, se a próxima direção for 1 (para esquerda), mas a direção atual for 1, o carro vai se movimentar para que assim que for possível começar a se deslocar para cima. Tanto para próxima direção para cima ou para baixo, as direções atuais, se tiverem valores 1 ou 2, irão fazer o carro ir para próxima direção para direita ou para esquerda, respectivamente. Isto é, se a próxima direção for 2 (para cima), mas a direção atual for 1, o carro vai se movimentar para que assim que for possível começar a se deslocar para direita.

As restrições de movimento observam se o carro está em uma posição específica, por exemplo, se o carro estiver em uma rua vertical e posição onde seu Y da matriz de posições for ímpar ele só pode ir para cima ou assim que possível ir para direita ou esquerda. Portanto, sempre que Y for ímpar o carro não pode ir para baixo. Isso limita alguns valores para os quarteirões no início da aplicação, pois é necessário que a divisão do quarteirão por 30 seja igual a um número par, caso contrário a posição de Y sendo ímpar o carro não poderia ir para cima. Isso foi utilizado para que os carros não andem na contramão das ruas.

O movimento do carro também verifica se chegou aos limites do mapa ou se o carro irá entrar em um quarteirão. Nesses casos o carro deve ir para uma outra direção válida.

Para estacionar o carro quando ele chega a uma posição de destino ele observa se está em alguma das faixas próximas aos limites do mapa e estaciona fora do mapa. Caso ele esteja próximo a um quarteirão, ele vai procurar o primeiro lugar ao redor dele que tem coordenada (-1,-1) e parar lá. A última posição válida dele no mapa é salva para quando ele retornar ao mapa e sua posição de estacionado também é salva para que seja possível apagar ela quando o carro retornar ao mapa.

Os carros possuem 4 estados (valores de 0 a 3), estando livres, ocupados, estacionados ou em uso pela central. Cada um desses estados faz com que o carro assuma uma cor diferente no mapa. Então, as cores utilizadas para os estados foram, preto, vermelho, azul e verde, respectivamente.

Os carros possuem inicialmente uma posição aleatória no mapa e as próximas direções e direções atuais são geradas aleatoriamente para os carros que não estão em uso pela central. O status do carro é definido inicialmente para 60% dos carros estiverem ocupados e 40% livres para uso da central. A cada certa quantidade de iterações no mapa esses 60% dos carros são escolhidos novamente de forma aleatória e carros que estavam livres podem ficar ocupados ou vice-versa. Os valores aleatórios só não influenciam os carros que estão em uso pela central ou estacionados. A cada certa quantidade de iterações as próximas direções e direções atuais também são escolhidas novamente de forma aleatória, isso evita que os carros fiquem sempre parados quando não puderem avançar em uma mesma direção.

Como a central sabe todos os status dos carros, é possível selecionar um carro que esteja livre (status 0) para movimentar ele no mapa. A central vai enviar as novas direções atuais para movimentar o carro. Esse movimento consiste em observar se o carro está na posição com x e y iguais ao que o usuário fez a requisição, se estiver acima ela deve deslocar o carro para baixo, se tiver abaixo da posição ela deve deslocar o carro para cima. Ao chegar no mesmo x, porém com y diferente, a central vai fazer o carro se deslocar para esquerda ou direita para fazer o carro ir para o destino certo. Se ao observar y, o carro tiver que passar do x que ele deveria estar, a central vai observar novamente o x. Essa mudança de observação fica alterando enquanto o carro não chega no destino. Isso foi necessário, pois o carro poderia chegar ao x de destino e não poder deslocar o y para esquerda ou direita por conta dos quarteirões.



## Protocolo de comunicação
### Comunicação entre carro e central
Existem três tipos de mensagem enviadas para a central. A primeira mensagem é a mensagem de início que possui o formato visto na imagem abaixo e serve para indicar a central que o script dos carros já iniciou e que a central pode começar a rodar o seu loop. Essa mensagem é publicada no tópico “transporte/inicio”.

<p align="center">
    <img src="https://github.com/luizgmartins/Simulador_de_Trafego_Usando_MQTT_e_Python/blob/main/Imagens/mensagem_inicio.png"></a>
</p>

A segunda mensagem é uma string com todas as posições válidas contidas na matriz de posições. São posições que o usuário pode requisitar e que os carros podem se mexer no mapa. Essa mensagem é publicada no tópico “transporte/matrizo”

Na outra mensagem os carros publicam no tópico “transporte/carroX” sendo X o número ID de cada carro. Esse ID é único para cada carro. Esse tipo de mensagem tem o formato que pode ser visto na imagem abaixo.

<p align="center">
    <img src="https://github.com/luizgmartins/Simulador_de_Trafego_Usando_MQTT_e_Python/blob/main/Imagens/mensagem_carros.png"></a>
</p>

O script dos carros está inscrito no sub “transporte/central_carro” que recebe as mensagens da central.

### Comunicação entre central e carros
A central recebe e trata as mensagens vindas dos carros e envia uma mensagem para o script dos carros. O formato das mensagens é o mesmo e pode ser visto na imagem abaixo. A central é inscrita nas subs “transporte/inicio”, “transporte/matrizo” e “transporte/carroX”, sendo X o número ID de cada carro. A mensagem enviada pela central é publicada no tópico “transporte/central_carro”.

<p align="center">
    <img src="https://github.com/luizgmartins/Simulador_de_Trafego_Usando_MQTT_e_Python/blob/main/Imagens/mensagem_central_carro.png"></a>
</p>

### Comunicação entre usuário e central
O usuário faz as requisições de viagem seguindo o tipo de mensagem visto na imagem abaixo.

<p align="center">
    <img src="https://github.com/luizgmartins/Simulador_de_Trafego_Usando_MQTT_e_Python/blob/main/Imagens/mensagem_usuario.png"></a>
</p>

### Comunicação entre central e usuário
A central envia as respostas das mensagens do usuário. O formato dessas mensagens podem ser vistos na imagem abaixo.

<p align="center">
    <img src="https://github.com/luizgmartins/Simulador_de_Trafego_Usando_MQTT_e_Python/blob/main/Imagens/mensagem_central_usuario.png"></a>
</p>


## Central
Primeiramente, a central recebe a mensagem de início e a matriz de posições. Essas mensagens são tratadas, no caso da primeira é utilizada para iniciar o loop da central, receber os valores de X_MAX, Y_MAX e o número de carros. Já a matriz de posições é transformada em uma lista contendo as possíveis posições de x e y que o usuário poderá solicitar como destino válido. A central também cria uma lista contendo todos os status dos carros. Essa lista vai sendo atualizada na medida que recebe os status de cada carro no decorrer da simulação.

As mensagens recebidas pela central são salvas em arquivos de texto contendo a data e hora e a mensagem recebida. É criado um novo arquivo de texto para cada tópico que a central está inscrita.

Após receber a mensagem de início a central retorna uma mensagem de confirmação para os carros e assim o script dos carros pode iniciar a simulação. 

Caso receba mensagem de solicitação do usuário, terá que verificar se o valor de x e y recebidos são válidos, se forem, a central envia uma mensagem de confirmação para o usuário. Caso sejam inválidos, a central envia mensagem para o usuário cancelando a viagem e envia para o carro mandando estacionar.

A central seleciona um dos carros livres para mover no mapa e envia uma mensagem para estacionar o carro. Como a central já validou as posições x e y recebidas do usuário, já encaminha uma mensagem para o carro selecionado e faz ele se mover no mapa até a posição que o usuário requisitou como início da viagem.

Após chegar ao local da partida, ela comunica ao usuário confirmando que o carro já chegou ao local e envia ao carro em uso para estacionar. A central aguarda a mensagem do usuário com a localização de destino final, verifica se a localização é válida e, se for, manda mensagem de confirmação para o usuário.

Logo após, começa a deslocar o carro novamente para a direção do destino final e quando o carro chega no local manda mensagem para ele estacionar e manda mensagem para o usuário confirmando que chegou ao destino.

Durante a viagem o usuário pode solicitar o cancelamento da mesma, fazendo com que a central envie a confirmação de cancelamento para o usuário e manda o carro em uso estacionar. 

## Usuário
O usuário faz as solicitações de viagem à central e solicitações de cancelamento e trata as confirmações recebidas pela central. Ficando a maior parte do tempo aguardando mensagens de confirmação.

## Comandos do teclado para utilização da simulação
Ao iniciar o script do Carro.py vai aparecer a janela para selecionar o quarteirão e o número de carros, após selecionar os valores com o mouse, pressionar a tecla "n" para setar o valor. Obs.: Evitar colocar o número de carros iguais a 0.

Para encerrar o script do Carro.py deve pressionar a tecla "esc" na janela do mapa.

Para encerrar o script da Central.py deve pressionar a tecla "esc" na janela da central.

Para fazer solicitações de viagem no script do usuário deve pressionar a tecla "y" e pressionar "enter" para envio dos valores. Para cancelar viagens pressionar a tecla "s". Para encerrar o script do Usuário.py basta pressionar a tecla "esc".

## Referências
* Notas de aula
* https://www.emqx.com/en/blog/how-to-use-mqtt-in-python
* https://www.youtube.com/watch?v=QAaXNt0oqSI&ab_channel=SteveCope
* https://docs.opencv.org/4.x/dc/d4d/tutorial_py_table_of_contents_gui.html

## Possíveis melhorias
* Fazer com que o script da central rode em paralelo com o dos carros logo após a conexão dos carros ao broker MQTT. (Essa parte seria feita para facilitar o início da simulação, pois se fosse um sistema real a central seria executada em um sistema diferente dos carros, assim como o usuário. A única conexão entre eles deve ser  via MQTT)

* A interface do usuário foi improvisada, porém deveria ser um tipo de app ou site que o usuário fizesse as requisições para uma rua específica e um número representando uma posição na rua. O usuário teria as ruas disponíveis no próprio app ou site de acordo com a configuração da simulação.

* A central poderia ter um servidor html para exibir os dados históricos de posição, velocidade e as requisições dos usuários.

* Poderia melhorar o código para que vários usuários pudessem se conectar ao mesmo tempo.
Boa parte do código foi feita utilizando nomes e identificações genéricos, poderia criar um sistema com nomes de ruas de verdade e mais identificações dos carros como placas em formato real, modelo do carro e etc.

* Alguns possíveis bugs no movimento dos carros poderiam ser melhorados para evitar que o carro fique muito tempo parado na rua. Assim como implementar velocidades maiores que 1.
