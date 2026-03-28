# 🎲 Domino Game (Python)

Jogo de dominó completo com interface gráfica desenvolvido em Python com Pygame. O jogo implementa as regras oficiais do dominó e inclui modo multiplayer local com bots inteligentes.

![Status](https://img.shields.io/badge/status-active-success.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Características:

- 🎮 **Menu principal interativo** com navegação intuitiva
- 🤖 **Inteligência artificial** para oponentes bots
- 🎵 **Sistema de sons** proceduralmente gerados
- 🎨 **Interface gráfica** limpa e responsiva
- 📊 **Sistema de pontuação** baseado nas regras oficiais
- ⚙️ **Configurações personalizáveis** via arquivo de configuração
- 🧪 **Testes unitários** incluídos
- 📖 **Código bem documentado** com docstrings completas

## 📌 Status do Projeto:

✅ **Totalmente funcional e jogável!**

- ✅ Menu principal com navegação
- ✅ Tela de regras integrada
- ✅ Tela de configurações
- ✅ Sistema de sons completo
- ✅ Jogo completo com 4 jogadores (1 humano + 3 bots)
- ✅ Todas as regras oficiais implementadas
- ✅ Sistema de pontuação funcional

## 🎯 Características do Jogo

### Modos de Jogo
- **Modo Resgate**: Compra peças do cemitério até conseguir jogar
- **Modo Passa**: Passa a vez quando não pode jogar

### Regras Implementadas
- Partida com até 4 jogadores (1 humano + bots)
- Distribuição de 6 peças por jogador
- Início por duplo-6 ou maior peça
- Validação completa de encaixes
- Sistema de pontuação oficial:
  - Batida normal: 1 ponto
  - Batida com dupla (carroça): 2 pontos
  - Batida em duas pontas (simples): 3 pontos
  - Batida em duas pontas (dupla): 4 pontos
  - Jogo fechado: 1 ponto
- Meta de 10 pontos para vencer a partida

## 🎮 Controles

### Menu
- **Mouse**: Navegar e clicar nos botões
- **ESC**: Voltar/Sair

### Jogo
- **Clique Esquerdo**: Jogar peça na ponta ESQUERDA
- **Clique Direito**: Jogar peça na ponta DIREITA
- **ESPAÇO**: Auto-jogada (joga automaticamente)
- **B**: Batida em duas pontas (quando tiver apenas 1 peça)
- **V**: Alternar modo (resgate/passa)
- **N**: Nova rodada/partida
- **ESC**: Voltar ao menu

## ⚙️ Requisitos

- 🐍 **Python 3.10+**
- 📦 Dependências listadas em `requirements.txt`:
  - pygame 2.6.1
  - numpy 1.26.4
  - pytest 8.0.0 (para testes)

## 🚀 Como Executar

### Instalação

```bash
# Clone o repositório
git clone https://github.com/Victorkaue333/Domino_Game.git
cd Domino_Game

# Instale as dependências
pip install -r requirements.txt

# Execute o jogo
python main.py
```

### Executar Testes

```bash
# Rodar todos os testes
pytest

# Rodar com cobertura
pytest --cov=. --cov-report=html

# Rodar testes específicos
python -m unittest test_domino.py
python -m unittest test_board.py
```

## 🗂️ Estrutura do Projeto

```text
Domino_Game/
├── main.py              # Ponto de entrada do jogo
├── menu.py              # Menu principal e telas auxiliares
├── board.py             # Lógica principal do jogo e renderização
├── domino.py            # Classe de peças e geração do conjunto
├── sounds.py            # Sistema de geração de sons
├── config.py            # Configurações do jogo
├── test_domino.py       # Testes unitários para domino.py
├── test_board.py        # Testes unitários para board.py
├── requirements.txt     # Dependências do projeto
├── README.md            # Este arquivo
├── LICENSE              # Licença MIT
└── Doc/
    └── Implementado.md  # Documentação de implementação
```

## ⚙️ Configurações

Você pode personalizar diversos aspectos do jogo editando o arquivo `config.py`:

- Número de jogadores
- Pontuação alvo
- Cores da interface
- Velocidade dos bots
- Configurações de som
- Tamanhos de janela e fontes
- E muito mais!

## 🎨 Capturas de Tela

*(Em desenvolvimento: adicionar screenshots do menu e jogo)*

## 🧪 Testes

O projeto inclui testes unitários abrangentes:

- **test_domino.py**: Testa a lógica das peças (criação, encaixe, classificação)
- **test_board.py**: Testa jogadores, movimentos e lógica de jogo

Execute `pytest` para rodar todos os testes.

## 🛠️ Desenvolvimento

### Estrutura do Código

O código está organizado em módulos bem definidos:

- **domino.py**: Classes e funções para peças de dominó
- **board.py**: Lógica do jogo, turnos e renderização
- **menu.py**: Interface de menus
- **sounds.py**: Geração procedural de sons
- **config.py**: Configurações centralizadas

Todos os módulos possuem docstrings completas e seguem as melhores práticas de Python.

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/NovaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona NovaFeature'`)
4. Push para a branch (`git push origin feature/NovaFeature`)
5. Abrir um Pull Request

## 📝 Melhorias Futuras

- [ ] Animações suaves ao jogar peças
- [ ] Diferentes níveis de dificuldade para bots
- [ ] Sistema de estatísticas de partidas
- [ ] Save/Load de partidas
- [ ] Multiplayer online
- [ ] Suporte a diferentes conjuntos de peças (dominó 9, 12)
- [ ] Modo torneio
- [ ] Temas visuais customizáveis

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👨‍💻 Autor

**Victor Kaue**

- GitHub: [@Victorkaue333](https://github.com/Victorkaue333)

## 🙏 Agradecimentos

- Regras baseadas no manual da Table Games
- Desenvolvido como projeto educacional e de entretenimento

---

⭐ Se você gostou deste projeto, considere dar uma estrela no repositório!
