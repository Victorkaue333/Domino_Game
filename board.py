from typing import Optional

import pygame

from domino import DominoTile, generate_domino_set


WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
WINDOW_TITLE = "Domino Game"

TABLE_HEIGHT = 450
HAND_START_X = 200
HAND_Y = 550
HAND_SPACING = 90
HAND_SIZE = 7
FPS = 60

GREEN = (40, 120, 40)
DARK_GREEN = (30, 90, 30)


class DominoBoard:
    def __init__(self) -> None:
        self.draw_pile = generate_domino_set()
        self.hand = self._create_initial_hand()
        self.table: list[DominoTile] = []
        self.selected: Optional[DominoTile] = None
        self.drag_offset_x = 0
        self.drag_offset_y = 0

    def _create_initial_hand(self) -> list[DominoTile]:
        hand: list[DominoTile] = []

        for i in range(HAND_SIZE):
            left, right = self.draw_pile.pop()
            x = HAND_START_X + i * HAND_SPACING
            hand.append(DominoTile(left, right, x, HAND_Y))

        return hand

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r and self.selected:
            self.selected.rotate()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_mouse_down(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            self._handle_mouse_up()
        elif event.type == pygame.MOUSEMOTION:
            self._handle_mouse_motion(event)

    def _handle_mouse_down(self, event: pygame.event.Event) -> None:
        self.selected = None

        for tile in reversed(self.hand):
            if tile.rect.collidepoint(event.pos):
                self.selected = tile
                tile.dragging = True
                self.drag_offset_x = event.pos[0] - tile.rect.x
                self.drag_offset_y = event.pos[1] - tile.rect.y
                return

    def _handle_mouse_up(self) -> None:
        if not self.selected:
            return

        self.selected.dragging = False

        if self.selected.rect.y < TABLE_HEIGHT and self.selected in self.hand:
            self.hand.remove(self.selected)
            self.table.append(self.selected)

        self.selected = None

    def _handle_mouse_motion(self, event: pygame.event.Event) -> None:
        if self.selected and self.selected.dragging:
            self.selected.rect.x = event.pos[0] - self.drag_offset_x
            self.selected.rect.y = event.pos[1] - self.drag_offset_y

    def draw(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        surface.fill(GREEN)
        pygame.draw.rect(surface, DARK_GREEN, (0, 0, WINDOW_WIDTH, TABLE_HEIGHT))

        for tile in self.table:
            tile.draw(surface, font)

        for tile in self.hand:
            tile.draw(surface, font)


def run_game() -> None:
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()
    dot_font = pygame.font.SysFont(None, 32)

    board = DominoBoard()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                board.handle_event(event)

        board.draw(screen, dot_font)
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
