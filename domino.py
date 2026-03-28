import random

import pygame


TILE_WIDTH = 60
TILE_HEIGHT = 120

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class DominoTile:
    def __init__(self, left: int, right: int, x: int, y: int) -> None:
        self.left = left
        self.right = right
        self.rect = pygame.Rect(x, y, TILE_WIDTH, TILE_HEIGHT)
        self.dragging = False

    def rotate(self) -> None:
        self.left, self.right = self.right, self.left

    def draw(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        pygame.draw.rect(surface, WHITE, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)

        top_text = font.render(str(self.left), True, BLACK)
        bottom_text = font.render(str(self.right), True, BLACK)

        surface.blit(top_text, (self.rect.x + 22, self.rect.y + 20))
        surface.blit(bottom_text, (self.rect.x + 22, self.rect.y + 70))

        pygame.draw.line(
            surface,
            BLACK,
            (self.rect.x, self.rect.y + TILE_HEIGHT // 2),
            (self.rect.x + TILE_WIDTH, self.rect.y + TILE_HEIGHT // 2),
            2,
        )


def generate_domino_set(max_value: int = 6) -> list[tuple[int, int]]:
    tiles: list[tuple[int, int]] = []

    for left in range(max_value + 1):
        for right in range(left, max_value + 1):
            tiles.append((left, right))

    random.shuffle(tiles)
    return tiles
