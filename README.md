# Simulador de Tráfego Usando MQTT e Python
Projeto da disciplina de Introdução a Python em Engenharia da Universidade Federal de Pernambuco - UFPE. O projeto consiste em um simulador de tráfego, contendo um mapa de uma cidade fictícia, carros se movendo aleatoriamente ou comandados por uma central e um usuário fazendo requisições de viagem. A comunicação entre os carros e a central, assim como a comunicação entre a central e o usuário é via MQTT através de um broker. O sistema atualiza de forma discreta ao longo do tempo e as posições, velocidades e status dos veículos são enviados para a central que utiliza esses dados e também armazena em arquivos.

----- Inserir gif com a simulação rodando

## Criação do mapa da cidade
Foi utilizada a biblioteca do opencv para criação do mapa e do movimento dos carros de forma visual. Inicialmente, é utilizado uma imagem de fundo totalmente em branco e a partir dela é criado o mapa da cidade com ruas, quarteirões e posições para movimentar os carros. Para criar o mapa é definido alguns parâmetros: a largura da rua é de 30 pixels, contendo duas faixas de 15 pixels cada; o tamanho dos quarteirões são definidos no início do script e a partir do valor dele será definido a quantidade de ruas e o tamanho total do mapa.
—--------inserir imagem do mapa sem os carros
Para criar o mapa é utilizado as linhas imaginárias verticais e horizontais do centro da imagem, para o primeiro quadrante: é deslocado uma faixa de rua para o lado e vai somando o tamanho de um quarteirão e uma rua até que não seja possível colocar mais um conjunto rua + quarteirão. Quando chega no limite é colocado uma rua e uma linha que representa o limite do mapa. É feito a mesma coisa para os outros quadrantes do mapa de forma espelhada. Por fim, é possível obter o mapa da cidade com os limites da cidade definidos e dentro dos limites de tamanho da imagem utilizada.
Foi definido três valores para o tamanho dos quarteirões (60, 120 ou 240), esses valores foram escolhidos por serem múltiplos de 30, que é o tamanho em pixels que o carro pode se deslocar no mapa. O motivo da escolha desses valores também foi devido a lógica do deslocamento dos carros que será explicado mais adiante.
Após construir o mapa foram nomeadas as ruas horizontais e verticais para uma melhor visualização.
Foi criado um objeto chamado de “cidade” que contém listas com coordenadas das ruas horizontais e verticais, lista com os limites superior, inferior, esquerda e direita do mapa, o valor do passo do carro (fixo em 30) e o tamanho do quarteirão.
—--------- imagem com a class cidade

Para facilitar o deslocamento dos carros e o envio de posições para a central, foi criada uma matriz contendo todas as possíveis posições para os carros poderem se deslocar no mapa.
A matriz é criada com valores em forma de tuplas contendo inicialmente o valor (-1,-1). O tamanho da matriz é calculado a partir do tamanho de posições do limite superior ao inferior (X_MAX) e de posições do limite da esquerda ao da direita (Y_MAX). Cada posição fica a uma distância de 30 pixels uma da outra, como o quarteirão é múltiplo de 30 e as ruas contém 30 pixels cada, é possível determinar quantas posições é possível obter.
As tuplas da matriz devem ser as coordenadas horizontais e verticais na imagem. Então a matriz que continha somente valores (-1,-1) será preenchida com as coordenadas do centro da posição na imagem. Como pode ser visto na imagem abaixo, para a posição com x=0 e y=0 da matriz, as coordenadas do centro dela na imagem é de (68,69). 

—--------- inserir imagem com o mapa de matriz de posições

Para preencher os valores corretos das coordenadas e deixando somente os quarteirões com valores (-1,-1), foi deslocado para direita 15 pixels com relação ao limite à esquerda e 15 pixels para baixo com relação ao limite superior, assim obtendo o centro da primeira posição. Assim vai salvando na matriz as tuplas com as posições da faixa de rua da primeira rua Horizontal até chegar ao Y_MAX. Isso é feito nas duas primeiras ruas horizontais e pulado um quarteirão para baixo e vai preencher mais duas ruas até que chegue ao fim da última rua horizontal. Preenchendo o centro das posições de cada linha em verde visto na imagem abaixo.

—--------- inserir imagem com linhas horizontais verdes

Para preencher o que falta é utilizado a mesma lógica, mas agora olhando as faixas de rua verticais e ignorando quem tem valor diferente de (-1,-1). Após obter os centros das posições, a matriz de posições contém também os valores das faixas em azul da imagem abaixo.

—-------- inserir imagem com linhas verticais azuis

Como os carros estarão sempre no centro das posições, é possível saber exatamente onde o carro está, deslocar ele facilmente e impedir que ele entre nos quarteirões sem querer.

## Movimento dos carros

## Protocolo de comunicação
Inicialmente os carros estão em movimento no mapa 

## Usuário

## Referências

## Possíveis melhorias
