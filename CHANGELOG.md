# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [1.2.1] - 2026-03-28

### Adicionado
- 📸 **Galeria de capturas de tela** no README
  - 4 screenshots mostrando menu, jogo e interface
  - Layout em tabela 2x2 para visualização organizada
  - Legendas descritivas para cada imagem
- 🖼️ Pasta `imgs/` com screenshots do projeto

### Melhorado
- README mais visual e atrativo
- Melhor demonstração das funcionalidades do jogo

## [1.2.0] - 2026-03-28

### Alterado
- 📁 **Reorganização completa do projeto em estrutura modular**
  - Código fonte movido para pasta `src/`
  - Testes movidos para pasta `tests/`
  - Documentação movida para pasta `docs/`
- 🚀 Criado script `run.py` na raiz para facilitar execução
- 📦 Estrutura profissional seguindo boas práticas Python
- 📖 README atualizado com nova estrutura
- 🔧 Imports atualizados para refletir nova organização

### Melhorado
- Melhor separação de responsabilidades
- Facilita manutenção e expansão futura
- Estrutura mais profissional e escalável

## [1.1.0] - 2026-03-28

### Adicionado
- 🎲 **Sistema visual de pintas nas peças** - As peças agora mostram pontos reais ao invés de números
- 🎨 Design realista de peças de dominó com cor creme/bege
- ✨ Bordas aprimoradas com cores que destacam peças jogáveis

### Melhorado
- Peças maiores e mais visíveis na mesa (50x28 ao invés de 40x22)
- Visual mais profissional e autêntico
- Melhor experiência visual geral do jogo

## [1.0.0] - 2026-03-28

### Adicionado
- 🎮 Menu principal completo com navegação intuitiva
- 🎯 Jogo de dominó totalmente funcional
- 🤖 Sistema de IA para bots adversários
- 🎵 Sistema de sons proceduralmente gerados
- ⚙️ Arquivo de configuração centralizado (config.py)
- 📖 Docstrings completas em todo o código
- 🧪 Testes unitários para domino.py e board.py
- 📝 Documentação completa no README.md
- 📄 Licença MIT
- 🙈 Arquivo .gitignore apropriado

### Implementado
- Sistema de pontuação segundo regras oficiais
- Validação completa de jogadas
- Dois modos de jogo (resgate/passa)
- Tela de regras integrada
- Tela de configurações
- Sistema de turnos
- Detecção de vitória e jogo fechado
- Interface gráfica com Pygame

### Regras do Jogo
- Partida com 4 jogadores (1 humano + 3 bots)
- Distribuição de 6 peças por jogador
- Início por duplo-6 ou maior peça
- Batida normal: 1 ponto
- Batida com dupla (carroça): 2 pontos
- Batida em duas pontas (simples): 3 pontos
- Batida em duas pontas (dupla): 4 pontos
- Jogo fechado: 1 ponto
- Meta de 10 pontos para vencer

### Controles
- Clique esquerdo/direito para jogar peças
- ESPAÇO para auto-jogada
- B para batida em duas pontas
- V para alternar modo
- N para nova rodada/partida
- ESC para voltar ao menu

## [Não Lançado]

### Planejado
- Animações suaves ao jogar peças
- Diferentes níveis de dificuldade para bots
- Sistema de estatísticas de partidas
- Save/Load de partidas
- Multiplayer online
- Temas visuais customizáveis
- Sistema de conquistas/achievements
- Replay de partidas
- Modo torneio

---

[1.0.0]: https://github.com/Victorkaue333/Domino_Game/releases/tag/v1.0.0
