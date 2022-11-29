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
Ao selecionar a quantidade inicial de carros esses serão criados como instâncias e conectados ao broker. No fim da simulação cada carro é desconectado ao broker. Cada carro também é criado como um objeto que possui uma ID de identificação e uma placa (Mas a placa não foi implementada com valores diferentes). O objeto carro possui uma função de deslocamento (movimento_carro).
Para colocar os carros no mapa foi necessário criar uma cópia da imagem de fundo que estava em branco no início do script e foi utilizado para criar o mapa e suas cores são invertidas, assim é possível criar uma máscara contendo somente o que foi desenhado nela. No fim a imagem do mapa é subtraído dessa máscara contendo os carros, isso resulta em uma imagem contendo o mapa e os carros. Isso foi necessário para que o movimento dos carros não apagasse as linhas do mapa caso eles pudessem ser desenhados em cima de alguma linha.
A lógica de movimento dos carros consiste em uma próxima direção, na direção atual, na velocidade do carro e sua posição anterior. A posição anterior é sempre a atual antes do próximo deslocamento do carro, assim é possível apagar o carro onde ele foi desenhado anteriormente para poder desenhá-lo na próxima posição do mapa. A velocidade do carro é 1 ou 0, caso seja 1 o carro desloca uma posição ou passo (que equivale a 30 pixels) e caso seja 0 ele fica parado. A velocidade é 0 sempre que a próxima direção que o carro irá seguir houver algum obstáculo, seja um carro ou alguma posição que ele não pode ir. As “próximas direções” dos carros possuem valores entre 0 e 3, sendo, próxima direção para direita, para esquerda, para cima e para baixo, respectivamente. As “direções atuais” podem ser valores entre 0 e 2, sendo direção atual igual a 0 para que o carro continue na mesma direção que ele está. Por exemplo, se a próxima direção dele é 0 (para direita) e a direção atual for 0 ele continua seguindo para direita. Tanto para próxima direção para direita ou para esquerda, as direções atuais, se tiverem valores 1 ou 2, irão fazer o carro ir para próxima direção para cima ou para baixo, respectivamente. Isto é, se a próxima direção for 1 (para esquerda), mas a direção atual for 1, o carro vai se movimentar para que assim que for possível começar a se deslocar para cima. 

Tanto para próxima direção para cima ou para baixo as direções atuais, se tiverem valores 1 ou 2, irão fazer o carro ir para próxima direção para direita ou para esquerda, respectivamente. Isto é, se a próxima direção for 2 (para cima), mas a direção atual for 1, o carro vai se movimentar para que assim que for possível começar a se deslocar para direita.

O movimento do carro também verifica se chegou aos limites do mapa ou se o carro irá entrar em um quarteirão. Nesses casos o carro deve ir para uma outra direção válida.

Para estacionar o carro quando ele chega a uma posição de destino ele observa se está em alguma das faixas próximas aos limites do mapa e estaciona fora do mapa. Caso ele esteja próximo a um quarteirão, ele vai procurar o primeiro lugar ao redor dele que tem coordenada (-1,-1) e parar lá. A última posição válida dele no mapa é salva para quando ele retornar ao mapa e sua posição de estacionado também é salva para que seja possível apagar ela quando o carro retornar ao mapa.

Os carros possuem 4 estados (valores de 0 a 3), estando livres, ocupados, estacionados ou em uso pela central. Cada um desses estados faz com que o carro assuma uma cor diferente no mapa. Então, as cores utilizadas para os estados foram, preto, vermelho, azul e verde, respectivamente.

Os carros possuem inicialmente uma posição aleatória no mapa e as próximas direções e direções atuais são geradas aleatoriamente para os carros que não estão em uso pela central. O status do carro é definido inicialmente para 60% dos carros estiverem ocupados e 40% livres para uso da central. A cada certa quantidade de iterações no mapa esses 60% dos carros são escolhidos novamente de forma aleatória e carros que estavam livres podem ficar ocupados ou vice-versa. Os valores aleatórios só não influenciam os carros que estão em uso pela central ou estacionados. A cada certa quantidade de iterações as próximas direções e direções atuais também são escolhidas novamente de forma aleatória, isso evita que os carros fiquem sempre parados quando não puderem avançar em uma mesma direção.

Como a central sabe todos os status dos carros, é possível selecionar um carro que esteja livre (status 0) para movimentar ele no mapa. A central vai enviar as novas direções atuais para movimentar o carro. Esse movimento consiste em observar se o carro está na posição com x e y iguais ao que o usuário fez a requisição, se estiver acima ela deve deslocar o carro para baixo, se tiver abaixo da posição ela deve deslocar o carro para cima. Ao chegar no mesmo x, porém com y diferente, a central vai fazer o carro se deslocar para esquerda ou direita para fazer o carro ir para o destino certo. Se ao observar y, o carro tiver que passar do x que ele deveria estar, a central vai observar novamente o x. Essa mudança de observação fica alterando enquanto o carro não chega no destino. Isso foi necessário, pois o carro poderia chegar ao x de destino e não poder deslocar o y para esquerda ou direita por conta dos quarteirões.



## Protocolo de comunicação
Inicialmente os carros estão em movimento no mapa 

## Central

## Usuário

## Referências

## Possíveis melhorias
