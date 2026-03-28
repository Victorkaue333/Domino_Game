"""
Menu principal do jogo de Dominó.
"""

import pygame
import sys
from typing import Optional

# Importa configurações
from config import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_TITLE,
    BG_GREEN,
    WHITE,
    YELLOW,
    BLACK,
    BLUE,
    FPS
)


class Button:
    """Representa um botão clicável no menu."""
    
    def __init__(self, x: int, y: int, width: int, height: int, text: str,
                 font: pygame.font.Font, color: tuple, hover_color: tuple):
        """
        Inicializa um botão.
        
        Args:
            x, y: Posição do botão.
            width, height: Dimensões do botão.
            text: Texto exibido no botão.
            font: Fonte do texto.
            color: Cor normal do botão.
            hover_color: Cor quando o mouse está sobre o botão.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
    
    def draw(self, surface: pygame.Surface) -> None:
        """Desenha o botão na superfície."""
        current_color = self.hover_color if self.is_hovered else self.color
        
        # Desenha o retângulo do botão
        pygame.draw.rect(surface, current_color, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 3)
        
        # Desenha o texto centralizado
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    def check_hover(self, mouse_pos: tuple[int, int]) -> None:
        """Atualiza estado de hover baseado na posição do mouse."""
        self.is_hovered = self.rect.collidepoint(mouse_pos)
    
    def is_clicked(self, mouse_pos: tuple[int, int]) -> bool:
        """Verifica se o botão foi clicado."""
        return self.rect.collidepoint(mouse_pos)


class Menu:
    """Menu principal do jogo."""
    
    def __init__(self):
        """Inicializa o menu."""
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        
        # Fontes
        self.title_font = pygame.font.SysFont(None, 72)
        self.button_font = pygame.font.SysFont(None, 36)
        self.text_font = pygame.font.SysFont(None, 24)
        
        # Cria botões
        button_width = 300
        button_height = 60
        button_x = (WINDOW_WIDTH - button_width) // 2
        start_y = 280
        spacing = 80
        
        self.buttons = [
            Button(button_x, start_y, button_width, button_height,
                   "Jogar", self.button_font, BLUE, (120, 180, 255)),
            Button(button_x, start_y + spacing, button_width, button_height,
                   "Configurações", self.button_font, BLUE, (120, 180, 255)),
            Button(button_x, start_y + spacing * 2, button_width, button_height,
                   "Regras", self.button_font, BLUE, (120, 180, 255)),
            Button(button_x, start_y + spacing * 3, button_width, button_height,
                   "Sair", self.button_font, BLUE, (120, 180, 255))
        ]
        
        self.selected_option: Optional[str] = None
    
    def handle_events(self) -> bool:
        """
        Processa eventos do menu.
        
        Returns:
            False se deve sair do menu, True caso contrário.
        """
        mouse_pos = pygame.mouse.get_pos()
        
        for button in self.buttons:
            button.check_hover(mouse_pos)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clique esquerdo
                    for i, button in enumerate(self.buttons):
                        if button.is_clicked(mouse_pos):
                            if i == 0:  # Jogar
                                self.selected_option = "jogar"
                                return False
                            elif i == 1:  # Configurações
                                self.show_settings()
                            elif i == 2:  # Regras
                                self.show_rules()
                            elif i == 3:  # Sair
                                self.selected_option = "sair"
                                return False
        
        return True
    
    def draw(self) -> None:
        """Desenha o menu."""
        self.screen.fill(BG_GREEN)
        
        # Desenha título
        title = self.title_font.render("DOMINÓ REAL", True, YELLOW)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 120))
        self.screen.blit(title, title_rect)
        
        # Desenha subtítulo
        subtitle = self.text_font.render("Versão 1.0", True, WHITE)
        subtitle_rect = subtitle.get_rect(center=(WINDOW_WIDTH // 2, 180))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Desenha botões
        for button in self.buttons:
            button.draw(self.screen)
        
        # Desenha rodapé
        footer = self.text_font.render(
            "Use o mouse para navegar | ESC para sair",
            True, WHITE
        )
        footer_rect = footer.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40))
        self.screen.blit(footer, footer_rect)
    
    def show_settings(self) -> None:
        """Exibe tela de configurações."""
        running = True
        back_button = Button(
            (WINDOW_WIDTH - 200) // 2,
            WINDOW_HEIGHT - 150,
            200, 50,
            "Voltar",
            self.button_font,
            BLUE,
            (120, 180, 255)
        )
        
        while running:
            mouse_pos = pygame.mouse.get_pos()
            back_button.check_hover(mouse_pos)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if back_button.is_clicked(mouse_pos):
                            running = False
            
            self.screen.fill(BG_GREEN)
            
            # Título
            title = self.title_font.render("Configurações", True, YELLOW)
            title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 80))
            self.screen.blit(title, title_rect)
            
            # Opções (placeholder)
            y_offset = 200
            options = [
                "Número de Jogadores: 4",
                "Pontuação Alvo: 10",
                "Dificuldade dos Bots: Médio",
                "Som: Ligado",
                "Música: Desligada"
            ]
            
            for option in options:
                text = self.text_font.render(option, True, WHITE)
                text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, y_offset))
                self.screen.blit(text, text_rect)
                y_offset += 50
            
            info = self.text_font.render(
                "As configurações podem ser alteradas no arquivo config.py",
                True, YELLOW
            )
            info_rect = info.get_rect(center=(WINDOW_WIDTH // 2, y_offset + 30))
            self.screen.blit(info, info_rect)
            
            back_button.draw(self.screen)
            
            pygame.display.flip()
            self.clock.tick(FPS)
    
    def show_rules(self) -> None:
        """Exibe tela de regras."""
        running = True
        back_button = Button(
            (WINDOW_WIDTH - 200) // 2,
            WINDOW_HEIGHT - 100,
            200, 50,
            "Voltar",
            self.button_font,
            BLUE,
            (120, 180, 255)
        )
        
        while running:
            mouse_pos = pygame.mouse.get_pos()
            back_button.check_hover(mouse_pos)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if back_button.is_clicked(mouse_pos):
                            running = False
            
            self.screen.fill(BG_GREEN)
            
            # Título
            title = self.title_font.render("Regras do Jogo", True, YELLOW)
            title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 60))
            self.screen.blit(title, title_rect)
            
            # Regras
            rules = [
                "Objetivo: Ser o primeiro a alcançar 10 pontos",
                "",
                "Controles:",
                "• Clique Esquerdo: jogar peça na ponta ESQUERDA",
                "• Clique Direito: jogar peça na ponta DIREITA",
                "• ESPAÇO: auto-jogada",
                "• B: batida em duas pontas (última peça)",
                "• V: alternar modo (compra/passa)",
                "• N: nova rodada/partida",
                "",
                "Pontuação:",
                "• Batida normal: 1 ponto",
                "• Batida com dupla: 2 pontos",
                "• Batida em duas pontas: 3 ou 4 pontos",
                "• Jogo fechado: 1 ponto"
            ]
            
            y_offset = 130
            for rule in rules:
                text = self.text_font.render(rule, True, WHITE)
                text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, y_offset))
                self.screen.blit(text, text_rect)
                y_offset += 35
            
            back_button.draw(self.screen)
            
            pygame.display.flip()
            self.clock.tick(FPS)
    
    def run(self) -> Optional[str]:
        """
        Executa o loop do menu.
        
        Returns:
            Opção selecionada ("jogar" ou "sair") ou None.
        """
        running = True
        
        while running:
            running = self.handle_events()
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)
        
        return self.selected_option


def show_menu() -> Optional[str]:
    """
    Exibe o menu principal.
    
    Returns:
        Opção selecionada pelo usuário.
    """
    menu = Menu()
    return menu.run()


if __name__ == "__main__":
    choice = show_menu()
    print(f"Opção selecionada: {choice}")
    pygame.quit()
