# Domino Game (Python + Pygame)

Implementacao de domino com regras de partida e pontuacao baseadas no manual da Table Games.

Fonte das regras:
- https://tablegames.com.br/wp-content/uploads/2017/10/domino_manual_table_games.pdf

## O que foi implementado

- Jogo com ate 4 jogadores (1 humano + bots).
- Distribuicao de 6 pecas por jogador.
- Inicio da rodada por:
  - duplo-6;
  - maior dupla, caso nao exista duplo-6;
  - maior peca por valor, caso nao exista nenhuma dupla.
- Jogadas por turno em sentido horario.
- Validador de encaixe nas duas pontas.
- Modo normal: sem peca valida, passa a vez.
- Modo resgate do cemiterio: compra ate conseguir encaixar (ou acabar o cemiterio).
- Fechamento de jogo e vencedor por menor soma de pontos na mao.
- Pontuacao da partida ate 10 pontos:
  - batida normal: 1 ponto;
  - batida com dupla (carroca): 2 pontos;
  - batida em duas pontas com peca simples: 3 pontos;
  - batida em duas pontas com dupla: 4 pontos;
  - jogo fechado: 1 ponto.

## Controles

- Mouse esquerdo em uma peca: jogar na ponta esquerda.
- Mouse direito em uma peca: jogar na ponta direita.
- `Espaco`: auto-jogada.
- `B`: tentar batida em duas pontas (quando sobrar 1 peca).
- `V`: alternar modo de rodada (normal/resgate).
- `N`: iniciar nova rodada/partida.
- `Esc`: sair.

## Requisitos

- Python 3.10+
- pygame 2.6.1

## Como executar

```bash
pip install -r requirements.txt
python main.py
```

## Estrutura

```text
Domino_Game/
|-- main.py      # ponto de entrada
|-- board.py     # fluxo do jogo, regras e interface
|-- domino.py    # modelo e utilitarios de peca
|-- requirements.txt
`-- README.md
```
