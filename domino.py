import random
from typing import Optional

import pygame


pygame.init()

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700

TABLE_HEIGHT = 450
HAND_START_X = 200
HAND_Y = 550
HAND_SPACING = 90
HAND_SIZE = 7

TILE_WIDTH = 60
TILE_HEIGHT = 120

WINDOW_TITLE = "Domino"

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (40, 120, 40)
DARK_GREEN = (30, 90, 30)

DOT_FONT = pygame.font.SysFont(None, 32)


class Domino:
    def __init__(self, left: int, right: int, x: int, y: int) -> None:
        self.left = left
        self.right = right
        self.rect = pygame.Rect(x, y, TILE_WIDTH, TILE_HEIGHT)
        self.dragging = False

    def rotate(self) -> None:
        self.left, self.right = self.right, self.left

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, WHITE, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)

        top_text = DOT_FONT.render(str(self.left), True, BLACK)
        bottom_text = DOT_FONT.render(str(self.right), True, BLACK)

        surface.blit(top_text, (self.rect.x + 22, self.rect.y + 20))
        surface.blit(bottom_text, (self.rect.x + 22, self.rect.y + 70))

        pygame.draw.line(
            surface,
            BLACK,
            (self.rect.x, self.rect.y + TILE_HEIGHT // 2),
            (self.rect.x + TILE_WIDTH, self.rect.y + TILE_HEIGHT // 2),
            2,
        )


def generate_domino_set() -> list[tuple[int, int]]:
    tiles = []

    for left in range(7):
        for right in range(left, 7):
            tiles.append((left, right))

    random.shuffle(tiles)
    return tiles


def create_hand(tiles: list[tuple[int, int]]) -> list[Domino]:
    hand: list[Domino] = []

    for i in range(HAND_SIZE):
        left, right = tiles.pop()
        x = HAND_START_X + i * HAND_SPACING
        hand.append(Domino(left, right, x, HAND_Y))

    return hand


def handle_mouse_down(
    event: pygame.event.Event, hand: list[Domino]
) -> Optional[Domino]:
    for tile in hand:
        if tile.rect.collidepoint(event.pos):
            tile.dragging = True
            return tile
    return None


def handle_mouse_up(
    selected: Optional[Domino], hand: list[Domino], table: list[Domino]
) -> Optional[Domino]:
    if not selected:
        return None

    selected.dragging = False

    if selected.rect.y < TABLE_HEIGHT:
        table.append(selected)
        hand.remove(selected)

    return None


def handle_mouse_motion(event: pygame.event.Event, selected: Optional[Domino]) -> None:
    if selected and selected.dragging:
        selected.rect.x = event.pos[0] - TILE_WIDTH // 2
        selected.rect.y = event.pos[1] - TILE_HEIGHT // 2


def draw_scene(surface: pygame.Surface, hand: list[Domino], table: list[Domino]) -> None:
    surface.fill(GREEN)
    pygame.draw.rect(surface, DARK_GREEN, (0, 0, WINDOW_WIDTH, TABLE_HEIGHT))

    for tile in table:
        tile.draw(surface)

    for tile in hand:
        tile.draw(surface)


def run_game() -> None:
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)

    tiles = generate_domino_set()
    hand = create_hand(tiles)
    table: list[Domino] = []

    selected: Optional[Domino] = None
    running = True

    while running:
        draw_scene(screen, hand, table)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r and selected:
                selected.rotate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                selected = handle_mouse_down(event, hand) or selected
            elif event.type == pygame.MOUSEBUTTONUP:
                selected = handle_mouse_up(selected, hand, table)
            elif event.type == pygame.MOUSEMOTION:
                handle_mouse_motion(event, selected)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    run_game()
