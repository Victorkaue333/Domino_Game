"""
Configurações do jogo de Dominó.
Centralize todas as constantes e configurações modificáveis aqui.
"""

# === Configurações de Jogo ===
MAX_PIP_VALUE = 6  # Valor máximo das pintas nas peças (0 a 6)
HAND_TILES = 6  # Número de peças iniciais por jogador
PLAYER_COUNT = 4  # Número total de jogadores (1 humano + bots)
TARGET_SCORE = 10  # Pontuação necessária para vencer a partida
DRAW_MODE_DEFAULT = True  # Se True, compra do cemitério; se False, passa a vez

# === Configurações de Tempo (milissegundos) ===
ROUND_END_DELAY_MS = 2500  # Tempo para mostrar resultado antes da próxima rodada
BOT_TURN_DELAY_MS = 700  # Tempo de espera antes do bot jogar

# === Configurações de Janela ===
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
WINDOW_TITLE = "Domino Real"
FPS = 60  # Frames por segundo

# === Posições Y dos Elementos ===
TABLE_Y = 265  # Posição Y da mesa (onde as peças jogadas aparecem)
HAND_Y = 470  # Posição Y da mão do jogador humano (ajustado para melhor visualização)

# === Cores (RGB) ===
BG_GREEN = (34, 110, 42)  # Verde do fundo
TABLE_GREEN = (25, 82, 32)  # Verde da mesa
WHITE = (245, 245, 245)
TILE_COLOR = (240, 235, 220)  # Cor creme para as peças (mais realista)
BLACK = (15, 15, 15)
DARK_GRAY = (60, 60, 60)  # Cinza escuro para bordas
YELLOW = (255, 220, 90)  # Cor de destaque
RED = (215, 75, 70)  # Cor de erro
BLUE = (85, 145, 230)  # Cor de informação

# === Configurações de Peças ===
TILE_WIDTH = 62  # Largura das peças na mão
TILE_HEIGHT = 98  # Altura das peças na mão
TABLE_TILE_WIDTH = 50  # Largura das peças na mesa (aumentado para melhor visualização)
TABLE_TILE_HEIGHT = 28  # Altura das peças na mesa (aumentado para melhor visualização)
TILE_MIN_SPACING = 18  # Espaçamento mínimo entre peças
TILE_MAX_SPACING = 70  # Espaçamento máximo entre peças

# === Configurações de Fonte ===
TITLE_FONT_SIZE = 38
TEXT_FONT_SIZE = 27
SMALL_FONT_SIZE = 22
TABLE_FONT_SIZE = 24

# === Configurações de Som ===
ENABLE_SOUND = True  # Ativar/desativar sons
ENABLE_MUSIC = False  # Ativar/desativar música de fundo
SOUND_VOLUME = 0.7  # Volume dos sons (0.0 a 1.0)
MUSIC_VOLUME = 0.3  # Volume da música (0.0 a 1.0)

# === Configurações de IA ===
BOT_DIFFICULTY = "medium"  # "easy", "medium", "hard"
BOT_NAMES = ["Bot 1", "Bot 2", "Bot 3"]  # Nomes dos bots

# === Configurações de Debug ===
DEBUG_MODE = False  # Mostrar informações de debug
SHOW_FPS = False  # Mostrar FPS na tela
