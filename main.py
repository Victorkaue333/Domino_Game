"""
Arquivo principal do jogo de Dominó.
Gerencia o fluxo entre menu e jogo.
"""

import pygame
from menu import show_menu
from board import run_game


def main() -> None:
    """Função principal que controla o fluxo do jogo."""
    while True:
        choice = show_menu()
        
        if choice == "jogar":
            run_game()
            # Após o jogo, volta ao menu
        elif choice == "sair" or choice is None:
            break
    
    pygame.quit()


if __name__ == "__main__":
    main()
