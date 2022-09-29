# O Problema do Caixeiro Viajante

O problema do caixeiro viajante é um problema do tipo NP-Difícil. Que se enuncia da seguinte forma: Dados pontos (cidades), determinar o menor caminho que passe por todos os pontos uma única vez e termine no ponto inicial. Por ter uma abordagem em otimização combinatória, o problema é um excelente meio de testar algoritmos de otimização, como: colonia de formigas, colonia de morcegos, algoritmo genético, annealing ...  


Este projeto consiste em desenvolver o problema em python e analisar o comportamento de cada algoritmo, usando a biblioteca pygame para interface do sistema.


Ao iniciar o programa, 10 pontos serão gerados aleatoriamente (ou o valor que estiver contido na variavel `nr_de_pontos`)

![pontos_aleatorios](/assets/images/pontos_aleatorios.jpg)

### Algoritmo de Força Bruta

No caso trivial, este algoritmo verifica cada caminho possivel através da permutação de caminhos, o numero das possiveis combinações é n!, sendo n o numero de pontos do problema. Neste caso, temos 10 pontos e 3.628.800 caminhos possiveis. Para as primeiras iterações temos resultados incovenientes:

![primeiras_iteracoes](/assets/images/primeiras_iteracoes.jpg)

As retas em verde mostram o menor caminho calculado no momento, as retas em branco mostram o caminho que está sendo calculado na atual iteração. Após varias iterações é possivel ver uma solução tomando forma:

![ultimas_iteracoes](/assets/images/ultimas_iteracoes.jpg)

Visto que o numero de iterações desse algoritimo é igual ao numero de caminhos possiveis do problema, se tivermos um numero alto de pontos n, os caminhos serão processados indefinidamente até n!. O que o torna ineficiente e computacionalmente custoso para problemas mais elaborados, apesar de sua simplicidade lógica.
