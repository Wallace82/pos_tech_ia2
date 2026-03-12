# Solucionador de TSP usando Algoritmo Genético

Este repositório contém uma implementação em Python de um solucionador para o Problema do Caixeiro Viajante (Traveling Salesman Problem - TSP) utilizando um Algoritmo Genético (GA).

O TSP é um problema clássico da área de otimização combinatória, onde o objetivo é encontrar a menor rota possível que visite um conjunto de cidades exatamente uma vez e retorne à cidade de origem.

## Visão Geral

O solucionador de TSP utiliza um Algoritmo Genético para evoluir iterativamente uma população de soluções candidatas até encontrar uma solução ótima ou próxima do ótimo.

O algoritmo genético funciona imitando o processo de seleção natural, no qual indivíduos com maior aptidão (fitness) — neste caso, rotas com menor distância total — têm maior probabilidade de sobreviver e gerar descendentes.

## Arquivos

** genetic_algorithm.py **
Contém a implementação do Algoritmo Genético, incluindo funções para:

gerar populações aleatórias

calcular o fitness

realizar operações de crossover (cruzamento)

realizar mutação

ordenar populações com base no fitness.

** tsp.py ** 
Implementa o solucionador principal do TSP, utilizando Pygame para visualização.
Ele:

inicializa o problema

cria a população inicial

evolui a população iterativamente

mostra visualmente a melhor solução encontrada até o momento.

** draw_functions.py ** 
Fornece funções para desenhar cidades, caminhos e gráficos utilizando Pygame.

## Uso

Para executar o solucionador de TSP, execute o script tsp.py utilizando Python.

O programa permite escolher entre diferentes tipos de problemas:

Cidades geradas aleatoriamente

Problemas pré-definidos com 10, 12 ou 15 cidades

Conjunto de dados de benchmark att48 (descomente o código correspondente em tsp.py)

Você também pode personalizar parâmetros diretamente no arquivo tsp.py, como:

tamanho da população

número de gerações

probabilidade de mutação

## Dependências

Python 3.x

Pygame (para visualização)

Certifique-se de que o Pygame esteja instalado antes de executar o programa.

Você pode instalar utilizando:

pip install pygame

Este solucionador de TSP foi desenvolvido como projeto de aprendizado e se baseia em diversos recursos online e materiais acadêmicos sobre Algoritmos Genéticos e o Problema do Caixeiro Viajante.

Licença

Este projeto está licenciado sob a Licença MIT.
