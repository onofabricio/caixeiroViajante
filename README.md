# O Problema do Caixeiro Viajante

O problema do caixeiro viajante é um problema do tipo NP-Difícil, que se enuncia da seguinte forma: Dados pontos (cidades), determinar o menor caminho que passe por todos os pontos uma única vez e termine no ponto inicial. Este problema é baseado na necessidade de transportadoras, varejistas e caixeiros viajantes realizarem entregas em várias cidades diferentes optando pelo caminho em que mais economizarão tempo e recursos. Por ter uma abordagem em otimização combinatória, o problema é um excelente meio de testar algoritmos de otimização, como: colônia de formigas, colônia de morcegos, algoritmo genético, simulated annealing, etc.  


![problema_caixeiro_viajante](https://npcompletosite.files.wordpress.com/2015/11/mapa2.gif)


Este projeto consiste em desenvolver o problema em python e analisar o comportamento de cada algoritmo, usando a biblioteca pygame para interface do sistema.


Ao iniciar o programa, 10 pontos serão gerados aleatoriamente (ou o valor que estiver contido na variavel `nr_de_pontos`)

![pontos_aleatorios](/assets/images/pontos_aleatorios.jpg)

### Algoritmo de Força Bruta

No caso trivial, este algoritmo verifica cada caminho possível através da permutação de caminhos, o número das possiveis combinações é n!, sendo n o numero de pontos do problema. Neste caso, temos 10 pontos e 3.628.800 caminhos possiveis. Para as primeiras iterações temos resultados inconvenientes:

![primeiras_iteracoes](/assets/images/primeiras_iteracoes.jpg)

As retas em verde mostram o menor caminho calculado no momento, as retas em branco mostram o caminho que está sendo calculado na atual iteração. Após varias iterações é possivel ver uma solução tomando forma:

![ultimas_iteracoes](/assets/images/ultimas_iteracoes.jpg)

Visto que o número de iterações desse algoritimo é igual ao número de caminhos possiveis do problema, se tivermos um número alto de pontos n, os caminhos serão processados até n!. O que o torna ineficiente e computacionalmente custoso para problemas mais elaborados, apesar de sua simplicidade lógica.

### Algoritmo genético

Em 1975, John H. Holland publicava *Adaptation in natural and artificial systems*, livro pioneiro nos algoritmos genéticos, que se baseiam na teoria neodarwinista para encontrar soluções em problemas de otimização combinatória. A teoria neodarwinista explica como surgem novas espécies através de três pilares:

- Todo ser vivo se reproduz ao alcançar a fase reprodutiva
- Na reprodução, ocorre mutação. (Erro gerado pela combinação de proteínas)
- A seleção natural elimina aqueles que não alcançaram a fase reprodutiva.
    
O algoritmo segue o seguinte esquema:

![fluxograma](./assets/images/fluxogramaAG.jpg)

No caso, cada indivíduo da população inicial representa um caminho aleatório e cada caminho é uma sequencia de pontos. A seleção dos pais depende do calculo de fitness de cada indivíduo da população, ou seja, o quão boa é a solução. Decidi calcular esse fitness como 1/d, sendo d a distância euclidiana do caminho, pois queremos minimizar o caminho percorrido. Após dividir cada fitness pela soma de todos os outros, teremos a probabilidade de cada individuo ser selecionado e gerar outros individuos. 

Após selecionados os pais, devemos realizar o *crossing over*, equivalente à reprodução entre os individuos, mas ao invés de recombinarmos proteínas de fitas de DNA, estaremos recombinando sequencias de pontos de cada caminho (individuo). Experimentei três técnicas de crossover, a primeira técnica consistia em sortear dois pontos em ambos os caminhos selecionados e fazer a permutação entre os intervalos gerados desses pontos. Apesar de ser uma manipulação fácil, a taxa de convergencia para caminhos que se cruzam era muito grande (falarei de caminhos cruzados mais pra frente). Com isso em mente, tentei desenvolver a minha própria técnica de crossover. Diferente da primeira técnica, defini o número de pontos de crossover como variável em função da quantidade de pontos do caminho, e assim permutar todos os intervalos gerados entre os pais. Porém, isso volta a ser um problema O(n!), tornando o tempo de execução inviável. Após uma consulta no artigo *Genetic Algorithms for the Travelling Salesman Problem: A Review of Representations and Operators*[1], notei que o próprio Holland havia criado algumas técnicas de crossover, entre elas, a Simple Inversion Mutation (SIM), em que, sorteados os dois pontos de crossover, inverte-se o intervalo do meio. Isso parecia um forte candidato a "desatar o nó" dos caminhos cruzados. Esta terceira técnica prevaleceu, a ocorrencia de caminhos cruzados diminuiu assim como o tempo para convergencia.

Assim como na natureza, a diversidade genética (Ou, aumento de escopo no dominio de soluções), pode ser obtida através da mutação. A mutação aplicada aqui consiste em sortear dois pontos do caminho e trocá-los de lugar um com o outro. Com efeito, todos os filhos gerados sofrem mutação,  na qual está atrelada uma taxa. Esta taxa carece de método, apenas percebi que quanto maior mais provavel da população divergir. A taxa está a 1% do numero de pontos (o que significa que apenas 1% vão ser sorteados). Quando feita a reprodução e mutação, todos os filhos gerados retornam à população original para que possam competir entre si. A população deve voltar ao tamanho original, então eliminamos os X piores, sendo X a quantidade de filhos gerados.

Na etapa de convergencia, o caminho ótimo com certeza não terá caminhos cruzados (creio que seja condição específica do PCV euclidiano). Por exemplo, seja $P$ um polígono formado pelos vértices $A, B, C, D$. Este polígono $P$ irá representar o caminho percorrendo os vértices na sequência $ACBD$ , como na figura abaixo. 
(Imagem caminho inicial exemplo)

Percebe-se que há um cruzamento entre as arestas $\overline{AC}$ e $\overline{BD}$, em que chamaremos de ponto $Q$
(Imagem adição do ponto Q)

Pela propriedade da desigualdade triangular, $\overline{AQ} + \overline{QB} \le \overline{AB}$, o mesmo se nota em $\overline{CQ} + \overline{QD} \le \overline{CD}$. Portanto, um caminho menor teria que passar pelas retas $\overline{AB}$ e $\overline{CD}$, necessariamente. Assim,  um polígono $P'$ que representa o caminho $ABCD$, seria do tipo:
(Imagem caminho melhorado)

### NOTAS

[1] Larranaga, Pedro & Kuijpers, Cindy & Murga, R. & Inza, I. & Dizdarevic, S.. (1999). Genetic Algorithms for the Travelling Salesman Problem: A Review of Representations and Operators. Artificial Intelligence Review. 13. 129-170. 10.1023/A:1006529012972
