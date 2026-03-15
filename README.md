# Sistema de Otimização de Rotas para Atendimento Especializado à Saúde da Mulher

## Descrição do Projeto

Este projeto implementa um sistema de simulação para **otimização de rotas de atendimento especializado voltados à saúde da mulher no Distrito Federal**.

O sistema utiliza como base o **Problema do Caixeiro Viajante (TSP - Traveling Salesman Problem)** e posteriormente evolui para um **Problema de Roteirização de Veículos (VRP)** com restrições específicas do contexto do Tech Challenge.

A aplicação simula atendimentos especializados em diferentes pontos do território do Distrito Federal utilizando um **mapa real como base visual**.

Os pontos de atendimento são gerados aleatoriamente dentro do mapa e representam situações como:

- Emergências obstétricas
- Casos de violência doméstica
- Entrega de medicamentos hormonais
- Atendimento pós-parto

O sistema também apresenta visualmente a **rota de atendimento em tempo real**, juntamente com uma lista detalhada das prioridades.

---

# Objetivo

Desenvolver um sistema que permita **simular e otimizar rotas de atendimento especializado à mulher**, considerando fatores como:

- prioridade de atendimento
- tipo de serviço
- janelas de horário
- demanda de suprimentos

O objetivo é demonstrar como **algoritmos de otimização podem apoiar sistemas de saúde pública**.

---

# Tecnologias Utilizadas

| Tecnologia | Função |
|--------|--------|
| Python | Linguagem principal |
| Pygame | Interface gráfica e visualização do mapa |
| Algoritmos Genéticos | Otimização das rotas |
| NumPy | Manipulação de dados numéricos |

---

# Estrutura do Projeto
pos_tech_ia2/
│
├── assets/
│ └── Mapa_DF.png
│
├── main.py
├── mapa_utils.py
├── pontos.py
├── renderer.py
│
├── requirements.txt
└── README.md


### Descrição dos arquivos

**main.py**

Arquivo principal do sistema.  
Responsável por:

- inicializar o Pygame
- carregar o mapa
- gerar pontos de atendimento
- executar o loop principal da aplicação

---

**genetic_algorithm.py**

Contém a implementação central do algoritmo genético.

Funções principais:

- `calculate_fitness`: Avalia a qualidade de uma rota com base na distância e em um sistema de penalidades.
- `evolve_population`: Orquestra a evolução da população a cada geração, aplicando seleção, crossover e mutação.
- `selection_by_tournament`: Implementa o método de seleção por torneio.
- `order_crossover`: Realiza o cruzamento de dois pais para gerar um novo indivíduo.
- `mutate`: Aplica operadores de mutação para introduzir diversidade.

---

**pontos.py**

Define as estruturas de dados utilizadas no sistema.

Contém a classe principal:
ServicePoint

Essa classe representa um ponto de atendimento com atributos como:

- posição no mapa
- tipo de atendimento
- prioridade
- demanda
- janela de horário

---

**mapa_utils.py**

Responsável pela lógica relacionada ao mapa.

Funções principais:

- carregar e redimensionar o mapa
- identificar áreas válidas para criação de pontos
- gerar pontos de atendimento aleatórios
- definir janelas de atendimento

---

**renderer.py**

Responsável pela renderização gráfica.

Funções principais:

- desenhar o mapa
- desenhar os pontos de atendimento
- desenhar as rotas
- renderizar o painel lateral com a lista de atendimentos

---

**assets/Mapa_DF.png**

Imagem base do mapa do Distrito Federal utilizada para posicionamento dos pontos.

---

# Funcionamento do Sistema

## 1. Carregamento do mapa

O sistema carrega o mapa do Distrito Federal e o ajusta ao tamanho da janela da aplicação.
map_surface = load_and_scale_map()

---

## 2. Identificação de áreas válidas

O algoritmo percorre todos os pixels do mapa para identificar posições válidas onde um ponto pode ser criado.

Pixels considerados inválidos:

- áreas pretas (fora do mapa)
- regiões de água (lagos e rios)

---

## 3. Geração de pontos de atendimento

Os pontos são gerados aleatoriamente dentro das áreas válidas do mapa.

Cada ponto recebe os atributos relevantes:

- tipo de atendimento
- prioridade
- demanda de suprimentos
- janela de horário

Exemplo de ponto gerado:
Ponto 3
Tipo: Emergência obstétrica
Prioridade: 4
Janela de atendimento: 0h - 23h

---

## 4. Definição da rota inicial

A primeira rota é gerada utilizando ordenação baseada em prioridade:

1. maior prioridade primeiro
2. menor horário de atendimento
3. identificador do ponto

---

## 5. Visualização gráfica

O sistema apresenta:

- mapa do Distrito Federal
- pontos de atendimento coloridos por prioridade
- linhas conectando os pontos da rota
- painel lateral com a sequência de atendimento

---

# Detalhes do Algoritmo Genético

A otimização das rotas é realizada por um algoritmo genético customizado para o problema de roteirização de veículos com restrições. Abaixo estão os detalhes técnicos da sua implementação.

### Representação (Cromossomo)
Cada indivíduo da população, ou **cromossomo**, é representado como uma lista (permutação) de `ServicePoint`. A ordem dos pontos na lista define a sequência da rota de atendimento.

### Função de Fitness (Avaliação)
O objetivo do algoritmo é **minimizar** o valor de fitness. Uma rota de baixo custo é considerada de alta qualidade (mais "apta"). A função `calculate_fitness` não se baseia apenas na distância, mas em um custo total que inclui um sistema de penalidades para violação das restrições do negócio:

- **Distância Euclidiana**: A distância total percorrida na rota.
- **Penalidade de Janela de Tempo**: Aplica uma penalidade se o atendimento ocorrer **após** o fim da janela de tempo definida para o ponto. Atrasos em pontos de maior prioridade resultam em penalidades mais severas.
- **Penalidade de Capacidade**: Penaliza a rota se a soma das demandas dos pontos exceder a capacidade máxima do veículo (`CAPACIDADE = 25`).
- **Penalidade de Prioridade**: Adiciona um custo significativo por atraso no atendimento de pontos, ponderado pela prioridade do chamado.
- **Penalidade de Refrigeração**: Aplica uma penalidade se o tempo de viagem entre dois pontos for muito longo para um item que exige temperatura controlada.

### Seleção: Torneio
O método de seleção implementado é o **torneio** (`selection_by_tournament`). A cada seleção, um pequeno grupo de indivíduos (`tournament_size = 4`) é escolhido aleatoriamente da população, e o indivíduo com o melhor fitness (menor custo) dentro desse grupo é selecionado como um dos pais para a próxima geração.

### Crossover: Order Crossover (OX1)
O operador de cruzamento é o **Order Crossover** (`order_crossover`). Este método é ideal para cromossomos baseados em permutação, pois garante que o filho gerado seja uma rota válida (sem pontos duplicados ou ausentes). Ele funciona da seguinte maneira:
1. Um segmento aleatório da rota é copiado do **Pai 1** para o filho.
2. Os pontos restantes são preenchidos na ordem em que aparecem no **Pai 2**, ignorando aqueles que já foram copiados do Pai 1.

### Mutação
Para introduzir variabilidade genética e evitar a convergência prematura para ótimos locais, são utilizados dois operadores de mutação (`mutate`):
1. **Swap (Troca)**: Dois pontos aleatórios na rota são trocados de posição.
2. **Inversion (Inversão)**: Uma subsequência aleatória de pontos na rota tem sua ordem invertida.

A probabilidade de mutação é definida por `MUTATION_PROBABILITY = 0.20`.

### Elitismo
O algoritmo implementa o **elitismo** (`elite_size = 1`), garantindo que o melhor indivíduo da geração atual seja transferido diretamente para a próxima geração sem sofrer crossover ou mutação. Isso assegura que a qualidade da melhor solução encontrada nunca se degrade ao longo das gerações.

---

# Legenda de Prioridades

| Prioridade | Tipo de Atendimento | Cor |
|------|------|------|
| 4 | Emergência obstétrica | Vermelho |
| 3 | Violência doméstica | Laranja |
| 2 | Medicamento hormonal | Azul |
| 1 | Pós-parto | Verde |

---

# Interface do Sistema

A interface é dividida em duas áreas:

### Área esquerda

Mapa do Distrito Federal com:

- pontos de atendimento
- rota visual

### Área direita

Painel com:

- legenda de prioridades
- lista da rota de atendimento
- informações do tipo de atendimento

---

# Como Executar o Projeto

## 1. Clonar ou baixar o projeto
git clone <repositorio>
cd pos_tech_ia2

---

## 2. Instalar dependências
pip install -r requirements.txt

---

## 3. Executar o sistema
python main.py

---

# Exemplo de Execução

Ao executar o sistema, será aberta uma janela contendo:

- mapa do DF
- pontos de atendimento
- rota visual
- lista de atendimento no painel lateral

---

Este projeto foi desenvolvido como parte do **Tech Challenge Fase 2**, com foco na aplicação de **otimização de rotas para atendimento especializado à mulher**, especificamente voltados ao atendimento e à segurança da mulher.

---

# Licença

Projeto desenvolvido para fins educacionais.