import pygame
import random

pygame.init()

WIDTH = 1200
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dominó")

WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (40,120,40)

TILE_W = 60
TILE_H = 120


class Domino:

    def __init__(self, a, b, x, y):
        self.a = a
        self.b = b
        self.rect = pygame.Rect(x, y, TILE_W, TILE_H)
        self.dragging = False
        self.rotation = 0

    def rotate(self):
        self.a, self.b = self.b, self.a

    def draw(self, screen):

        pygame.draw.rect(screen, WHITE, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)

        font = pygame.font.SysFont(None, 32)

        t1 = font.render(str(self.a), True, BLACK)
        t2 = font.render(str(self.b), True, BLACK)

        screen.blit(t1,(self.rect.x+22,self.rect.y+20))
        screen.blit(t2,(self.rect.x+22,self.rect.y+70))

        pygame.draw.line(
            screen,
            BLACK,
            (self.rect.x,self.rect.y+TILE_H/2),
            (self.rect.x+TILE_W,self.rect.y+TILE_H/2),
            2
        )


def gerar_domino():

    pecas = []

    for i in range(7):
        for j in range(i,7):
            pecas.append((i,j))

    random.shuffle(pecas)

    return pecas


def criar_mao(pecas):

    mao = []

    for i in range(7):

        a,b = pecas.pop()

        x = 200 + i*90
        y = 550

        mao.append(Domino(a,b,x,y))

    return mao


pecas = gerar_domino()

mao = criar_mao(pecas)

mesa = []

selected = None

running = True

while running:

    screen.fill(GREEN)

    pygame.draw.rect(screen,(30,90,30),(0,0,WIDTH,450))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r and selected:
                selected.rotate()

        if event.type == pygame.MOUSEBUTTONDOWN:

            for p in mao:

                if p.rect.collidepoint(event.pos):

                    selected = p
                    p.dragging = True

        if event.type == pygame.MOUSEBUTTONUP:

            if selected:

                selected.dragging = False

                if selected.rect.y < 450:

                    mesa.append(selected)
                    mao.remove(selected)

                selected = None

        if event.type == pygame.MOUSEMOTION:

            if selected and selected.dragging:

                selected.rect.x = event.pos[0] - TILE_W/2
                selected.rect.y = event.pos[1] - TILE_H/2

    for p in mesa:
        p.draw(screen)

    for p in mao:
        p.draw(screen)

    pygame.display.update()

pygame.quit()