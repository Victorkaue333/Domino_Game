"""Módulo principal do jogo de dominó com lógica de jogo e renderização gráfica."""

from dataclasses import dataclass, field
from enum import Enum
import random
from typing import Optional

import pygame

from domino import HAND_TILES, MAX_PIP_VALUE, DominoTile, generate_domino_set, tile_rank
import sounds


WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
WINDOW_TITLE = "Domino Real"
FPS = 60

PLAYER_COUNT = 4
TARGET_SCORE = 10
ROUND_END_DELAY_MS = 2500
BOT_TURN_DELAY_MS = 700

TABLE_Y = 265
HAND_Y = 535

BG_GREEN = (34, 110, 42)
TABLE_GREEN = (25, 82, 32)
WHITE = (245, 245, 245)
BLACK = (15, 15, 15)
YELLOW = (255, 220, 90)
RED = (215, 75, 70)
BLUE = (85, 145, 230)


class MoveSide(Enum):
    """Representa o lado da mesa onde uma peça pode ser jogada."""
    LEFT = "left"
    RIGHT = "right"
    BOTH = "both"


@dataclass
class Player:
    """Representa um jogador no jogo de dominó.
    
    Attributes:
        name: Nome do jogador.
        is_human: True se for jogador humano, False se for bot.
        hand: Lista de peças na mão do jogador.
        score: Pontuação acumulada na partida.
    """
    name: str
    is_human: bool
    hand: list[DominoTile] = field(default_factory=list)
    score: int = 0

    def hand_points(self) -> int:
        """Calcula a soma dos pontos de todas as peças na mão.
        
        Returns:
            Soma total dos valores das peças.
        """
        return sum(tile.pip_sum() for tile in self.hand)


class DominoBoard:
    """Gerencia a lógica do jogo e renderização gráfica.
    
    Esta classe controla o estado do jogo, turnos, validação de movimentos,
    pontuação e renderização da interface gráfica.
    
    Attributes:
        players: Lista de jogadores participando do jogo.
        draw_mode: Se True, permite comprar do cemitério; se False, passa a vez.
        boneyard: Peças ainda disponíveis no cemitério.
        chain: Sequência de peças jogadas na mesa.
        left_end: Valor da ponta esquerda da mesa.
        right_end: Valor da ponta direita da mesa.
    """
    def __init__(self, player_count: int = PLAYER_COUNT, draw_mode: bool = True) -> None:
        if player_count < 2 or player_count > 4:
            raise ValueError("player_count must be between 2 and 4")

        self.players = self._build_players(player_count)
        self.draw_mode = draw_mode

        self.boneyard: list[DominoTile] = []
        self.chain: list[DominoTile] = []
        self.left_end: Optional[int] = None
        self.right_end: Optional[int] = None

        self.current_player_index = 0
        self.pass_streak = 0
        self.turn_setup_needed = True

        self.round_over = False
        self.match_over = False
        self.round_end_at = 0
        self.bot_action_at = 0

        self.status_message = ""

        self.title_font = pygame.font.SysFont(None, 38)
        self.text_font = pygame.font.SysFont(None, 27)
        self.small_font = pygame.font.SysFont(None, 22)
        self.table_font = pygame.font.SysFont(None, 24)

        self.human_hand_rects: list[pygame.Rect] = []
        self._start_round()

    @property
    def current_player(self) -> Player:
        return self.players[self.current_player_index]

    def _build_players(self, player_count: int) -> list[Player]:
        players = [Player(name="Voce", is_human=True)]
        for i in range(1, player_count):
            players.append(Player(name=f"Bot {i}", is_human=False))
        return players

    def _start_round(self) -> None:
        self.round_over = False
        self.turn_setup_needed = True
        self.pass_streak = 0
        self.chain = []
        self.left_end = None
        self.right_end = None
        self.human_hand_rects = []

        pile = generate_domino_set()
        for player in self.players:
            player.hand.clear()

        for _ in range(HAND_TILES):
            for player in self.players:
                player.hand.append(pile.pop())

        self.boneyard = pile

        starter_index, opening_tile = self._find_starter()
        self._place_opening_tile(starter_index, opening_tile)
        self.current_player_index = (starter_index + 1) % len(self.players)
        self.turn_setup_needed = True

        self.status_message = (
            f"Nova rodada: {self.players[starter_index].name} iniciou com "
            f"{opening_tile.left}/{opening_tile.right}."
        )

    def _find_starter(self) -> tuple[int, DominoTile]:
        for value in range(MAX_PIP_VALUE, -1, -1):
            target_double = DominoTile(value, value)
            for index, player in enumerate(self.players):
                if target_double in player.hand:
                    return index, target_double

        best_index = 0
        best_tile = self.players[0].hand[0]
        best_rank = tile_rank(best_tile)
        for index, player in enumerate(self.players):
            for tile in player.hand:
                rank = tile_rank(tile)
                if rank > best_rank:
                    best_rank = rank
                    best_index = index
                    best_tile = tile

        return best_index, best_tile

    def _place_opening_tile(self, player_index: int, tile: DominoTile) -> None:
        player = self.players[player_index]
        player.hand.remove(tile)

        self.chain = [tile]
        self.left_end = tile.left
        self.right_end = tile.right

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            self._handle_keydown(event.key)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_mouse_click(event)

    def _handle_keydown(self, key: int) -> None:
        if key == pygame.K_v:
            self.draw_mode = not self.draw_mode
            mode = "resgate no cemiterio" if self.draw_mode else "passa a vez sem resgate"
            self.status_message = f"Modo alterado: {mode}."
            return

        if key == pygame.K_n:
            if self.match_over:
                self._reset_match()
            elif self.round_over:
                self._start_round()
            return

        if key == pygame.K_SPACE and self._is_human_turn_ready():
            self._play_human_auto_move()
            return

        if key == pygame.K_b and self._is_human_turn_ready():
            self._try_human_both_finish()

    def _handle_mouse_click(self, event: pygame.event.Event) -> None:
        if not self._is_human_turn_ready():
            return

        side = None
        if event.button == 1:
            side = MoveSide.LEFT
        elif event.button == 3:
            side = MoveSide.RIGHT

        if side is None:
            return

        tile_index = self._clicked_human_tile_index(event.pos)
        if tile_index is None:
            return

        self._try_play_move(self.current_player_index, tile_index, side)

    def _is_human_turn_ready(self) -> bool:
        return (
            not self.round_over
            and not self.turn_setup_needed
            and self.current_player.is_human
        )

    def _clicked_human_tile_index(self, position: tuple[int, int]) -> Optional[int]:
        if not self.human_hand_rects:
            self.human_hand_rects = self._build_human_hand_rects()

        for index, rect in enumerate(self.human_hand_rects):
            if rect.collidepoint(position):
                return index
        return None

    def update(self) -> None:
        now = pygame.time.get_ticks()

        if self.round_over:
            if not self.match_over and now >= self.round_end_at:
                self._start_round()
            return

        if self.turn_setup_needed:
            self._setup_current_turn()
            if self.round_over:
                return

        if self.current_player.is_human:
            return

        if now >= self.bot_action_at:
            self._play_bot_turn()

    def _setup_current_turn(self) -> None:
        player = self.current_player

        drawn = 0
        if not self._has_playable_move(player):
            drawn = self._draw_until_playable(player)

        if drawn > 0:
            sounds.play_draw_tile()
            self.status_message = f"{player.name} comprou {drawn} peca(s) do cemiterio."

        if not self._has_playable_move(player):
            self.pass_streak += 1
            sounds.play_pass()
            self.status_message = f"{player.name} passou a vez."
            self._end_turn_after_pass()
            return

        self.turn_setup_needed = False
        if player.is_human:
            self.status_message = (
                "Sua vez: clique esquerdo joga na ponta ESQUERDA, "
                "clique direito joga na ponta DIREITA."
            )
        else:
            self.status_message = f"Vez de {player.name}..."
            self.bot_action_at = pygame.time.get_ticks() + BOT_TURN_DELAY_MS

    def _draw_until_playable(self, player: Player) -> int:
        if not self.draw_mode:
            return 0

        drawn = 0
        while self.boneyard and not self._has_playable_move(player):
            player.hand.append(self.boneyard.pop())
            drawn += 1
        return drawn

    def _end_turn_after_pass(self) -> None:
        if self.pass_streak >= len(self.players):
            self._finish_blocked_round()
            return

        self._advance_turn()

    def _play_bot_turn(self) -> None:
        player = self.current_player
        moves = self._list_playable_moves(player)
        if not moves:
            self.pass_streak += 1
            sounds.play_pass()
            self.status_message = f"{player.name} passou a vez."
            self._end_turn_after_pass()
            return

        chosen_index, chosen_side = self._choose_bot_move(player, moves)
        self._try_play_move(self.current_player_index, chosen_index, chosen_side)

    def _choose_bot_move(
        self, player: Player, moves: list[tuple[int, MoveSide]]
    ) -> tuple[int, MoveSide]:
        if len(player.hand) == 1:
            best = moves[0]
            best_points = self._win_points(player.hand[best[0]], best[1])
            for option in moves[1:]:
                points = self._win_points(player.hand[option[0]], option[1])
                if points > best_points:
                    best_points = points
                    best = option
            return best

        ranked_moves: list[tuple[int, tuple[int, int, int], int]] = []
        for tile_index, side in moves:
            tile = player.hand[tile_index]
            side_bonus = 1 if side == MoveSide.RIGHT else 0
            ranked_moves.append((tile_index, tile_rank(tile), side_bonus))

        ranked_moves.sort(key=lambda item: (item[1], item[2]), reverse=True)
        top_rank = ranked_moves[0][1]
        top_moves = [
            (index, side)
            for index, side in moves
            if tile_rank(player.hand[index]) == top_rank
        ]
        return random.choice(top_moves)

    def _try_human_both_finish(self) -> None:
        player = self.current_player
        if len(player.hand) != 1:
            self.status_message = "Batida em duas pontas so e valida com a ultima peca."
            return

        sides = self._playable_sides(player.hand[0], len(player.hand))
        if MoveSide.BOTH not in sides:
            self.status_message = "A ultima peca nao encaixa nas duas pontas."
            return

        self._try_play_move(self.current_player_index, 0, MoveSide.BOTH)

    def _play_human_auto_move(self) -> None:
        player = self.current_player
        moves = self._list_playable_moves(player)
        if not moves:
            self.status_message = "Nao ha jogada valida agora."
            return

        preferred = moves[0]
        if len(player.hand) == 1:
            best_points = self._win_points(player.hand[preferred[0]], preferred[1])
            for move in moves[1:]:
                points = self._win_points(player.hand[move[0]], move[1])
                if points > best_points:
                    best_points = points
                    preferred = move

        self._try_play_move(self.current_player_index, preferred[0], preferred[1])

    def _try_play_move(self, player_index: int, tile_index: int, side: MoveSide) -> None:
        if player_index != self.current_player_index:
            return

        player = self.current_player
        if tile_index < 0 or tile_index >= len(player.hand):
            return

        tile = player.hand[tile_index]
        valid_sides = self._playable_sides(tile, len(player.hand))
        if side not in valid_sides:
            sounds.play_error()
            side_name = "esquerda" if side == MoveSide.LEFT else "direita"
            self.status_message = (
                f"Jogada invalida: a peca {tile.left}/{tile.right} nao encaixa na {side_name}."
            )
            return

        player.hand.pop(tile_index)
        self.pass_streak = 0

        if side == MoveSide.BOTH:
            sounds.play_win()
            points = self._win_points(tile, MoveSide.BOTH)
            self._finish_round(
                winner_index=player_index,
                points=points,
                reason=f"batida em duas pontas com {tile.left}/{tile.right}",
            )
            return

        sounds.play_place_tile()
        self._place_chain_tile(tile, side)

        if not player.hand:
            sounds.play_win()
            points = self._win_points(tile, side)
            reason = f"batida com {tile.left}/{tile.right}"
            self._finish_round(winner_index=player_index, points=points, reason=reason)
            return

        self._advance_turn()

    def _place_chain_tile(self, tile: DominoTile, side: MoveSide) -> None:
        if self.left_end is None or self.right_end is None:
            self.chain = [tile]
            self.left_end = tile.left
            self.right_end = tile.right
            return

        if side == MoveSide.LEFT:
            oriented = tile if tile.right == self.left_end else tile.flipped()
            self.chain.insert(0, oriented)
            self.left_end = oriented.left
            self.status_message = (
                f"{self.current_player.name} jogou {tile.left}/{tile.right} na esquerda."
            )
            return

        oriented = tile if tile.left == self.right_end else tile.flipped()
        self.chain.append(oriented)
        self.right_end = oriented.right
        self.status_message = (
            f"{self.current_player.name} jogou {tile.left}/{tile.right} na direita."
        )

    def _finish_blocked_round(self) -> None:
        points_by_player = [player.hand_points() for player in self.players]
        lowest_points = min(points_by_player)
        winner_candidates = [
            index for index, value in enumerate(points_by_player) if value == lowest_points
        ]
        winner_index = winner_candidates[0]

        self._finish_round(
            winner_index=winner_index,
            points=1,
            reason=f"jogo fechado, menor mao ({lowest_points} pontos)",
        )

    def _finish_round(self, winner_index: int, points: int, reason: str) -> None:
        winner = self.players[winner_index]
        winner.score += points

        self.round_over = True
        self.turn_setup_needed = False
        self.round_end_at = pygame.time.get_ticks() + ROUND_END_DELAY_MS

        if winner.score >= TARGET_SCORE:
            self.match_over = True
            self.status_message = (
                f"{winner.name} venceu a partida com {winner.score} pontos ({reason}). "
                "Pressione N para nova partida."
            )
            return

        self.status_message = (
            f"{winner.name} venceu a rodada ({reason}) e marcou {points} ponto(s). "
            "Nova rodada em instantes."
        )

    def _reset_match(self) -> None:
        for player in self.players:
            player.score = 0
        self.match_over = False
        self._start_round()

    def _advance_turn(self) -> None:
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.turn_setup_needed = True

    def _has_playable_move(self, player: Player) -> bool:
        for tile in player.hand:
            if self._playable_sides(tile, len(player.hand)):
                return True
        return False

    def _list_playable_moves(self, player: Player) -> list[tuple[int, MoveSide]]:
        moves: list[tuple[int, MoveSide]] = []
        for index, tile in enumerate(player.hand):
            for side in self._playable_sides(tile, len(player.hand)):
                moves.append((index, side))
        return moves

    def _playable_sides(self, tile: DominoTile, hand_size: int) -> list[MoveSide]:
        if self.left_end is None or self.right_end is None:
            return [MoveSide.RIGHT]

        sides: list[MoveSide] = []
        if tile.matches(self.left_end):
            sides.append(MoveSide.LEFT)
        if tile.matches(self.right_end):
            sides.append(MoveSide.RIGHT)

        can_close_both_ends = False
        if hand_size == 1:
            if self.left_end == self.right_end:
                can_close_both_ends = (
                    tile.left == self.left_end and tile.right == self.right_end
                )
            else:
                can_close_both_ends = (
                    (tile.left == self.left_end and tile.right == self.right_end)
                    or (tile.left == self.right_end and tile.right == self.left_end)
                )

        if can_close_both_ends:
            sides.append(MoveSide.BOTH)

        return sides

    def _win_points(self, tile: DominoTile, side: MoveSide) -> int:
        if side == MoveSide.BOTH:
            return 4 if tile.is_double() else 3
        return 2 if tile.is_double() else 1

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(BG_GREEN)
        pygame.draw.rect(surface, TABLE_GREEN, (0, 70, WINDOW_WIDTH, 360))

        self._draw_header(surface)
        self._draw_table(surface)
        self._draw_human_hand(surface)
        self._draw_footer(surface)

    def _draw_header(self, surface: pygame.Surface) -> None:
        title = self.title_font.render(WINDOW_TITLE, True, WHITE)
        surface.blit(title, (20, 14))

        mode_text = "Modo: resgate no cemiterio" if self.draw_mode else "Modo: passa sem comprar"
        mode_render = self.small_font.render(mode_text, True, WHITE)
        surface.blit(mode_render, (20, 50))

        pile_render = self.small_font.render(
            f"Cemiterio: {len(self.boneyard)} pecas", True, WHITE
        )
        surface.blit(pile_render, (275, 50))

        score_x = 520
        for index, player in enumerate(self.players):
            color = YELLOW if index == self.current_player_index and not self.round_over else WHITE
            text = (
                f"{player.name}: {player.score} pts | "
                f"{len(player.hand)} pecas | mao {player.hand_points()}"
            )
            render = self.small_font.render(text, True, color)
            surface.blit(render, (score_x, 14 + index * 22))

    def _draw_table(self, surface: pygame.Surface) -> None:
        if not self.chain:
            empty_render = self.text_font.render("Mesa vazia", True, WHITE)
            surface.blit(empty_render, (WINDOW_WIDTH // 2 - 45, TABLE_Y))
            return

        tile_count = len(self.chain)
        tile_w = 40
        tile_h = 22
        gap = 2
        total_width = tile_count * tile_w + max(0, tile_count - 1) * gap
        start_x = (WINDOW_WIDTH - total_width) // 2

        for index, tile in enumerate(self.chain):
            x = start_x + index * (tile_w + gap)
            rect = pygame.Rect(x, TABLE_Y, tile_w, tile_h)
            pygame.draw.rect(surface, WHITE, rect)
            pygame.draw.rect(surface, BLACK, rect, 2)
            pygame.draw.line(
                surface,
                BLACK,
                (rect.x + rect.width // 2, rect.y),
                (rect.x + rect.width // 2, rect.y + rect.height),
                1,
            )

            left_value = self.table_font.render(str(tile.left), True, BLACK)
            right_value = self.table_font.render(str(tile.right), True, BLACK)
            surface.blit(left_value, (rect.x + 8, rect.y + 2))
            surface.blit(right_value, (rect.x + 24, rect.y + 2))

        ends_text = f"Pontas abertas: {self.left_end} | {self.right_end}"
        ends_render = self.text_font.render(ends_text, True, WHITE)
        surface.blit(ends_render, (WINDOW_WIDTH // 2 - 95, TABLE_Y - 36))

    def _draw_human_hand(self, surface: pygame.Surface) -> None:
        player = self.players[0]
        self.human_hand_rects = self._build_human_hand_rects()
        playable_map = self._human_playable_map() if self._is_human_turn_ready() else {}

        for index, tile in enumerate(player.hand):
            rect = self.human_hand_rects[index]

            border_color = WHITE
            border_width = 2
            if index in playable_map:
                border_color = YELLOW
                border_width = 4

            pygame.draw.rect(surface, WHITE, rect)
            pygame.draw.rect(surface, border_color, rect, border_width)
            pygame.draw.line(
                surface,
                BLACK,
                (rect.x, rect.y + rect.height // 2),
                (rect.x + rect.width, rect.y + rect.height // 2),
                2,
            )

            top_text = self.text_font.render(str(tile.left), True, BLACK)
            bottom_text = self.text_font.render(str(tile.right), True, BLACK)
            surface.blit(top_text, (rect.x + rect.width // 2 - 6, rect.y + 16))
            surface.blit(bottom_text, (rect.x + rect.width // 2 - 6, rect.y + 62))

    def _build_human_hand_rects(self) -> list[pygame.Rect]:
        hand_size = len(self.players[0].hand)
        if hand_size == 0:
            return []

        tile_w = 62
        tile_h = 98
        if hand_size == 1:
            spacing = 0
        else:
            spacing = min(70, max(18, (WINDOW_WIDTH - 120 - tile_w) // (hand_size - 1)))

        total_width = tile_w + (hand_size - 1) * spacing
        start_x = (WINDOW_WIDTH - total_width) // 2

        rects: list[pygame.Rect] = []
        for index in range(hand_size):
            x = start_x + index * spacing
            rects.append(pygame.Rect(x, HAND_Y, tile_w, tile_h))
        return rects

    def _human_playable_map(self) -> dict[int, list[MoveSide]]:
        playable: dict[int, list[MoveSide]] = {}
        player = self.players[0]
        for index, tile in enumerate(player.hand):
            sides = self._playable_sides(tile, len(player.hand))
            if sides:
                playable[index] = sides
        return playable

    def _draw_footer(self, surface: pygame.Surface) -> None:
        if self._is_human_turn_ready():
            guide_1 = "Clique esquerdo: joga na ESQUERDA | Clique direito: joga na DIREITA"
            guide_2 = "Espaco: auto-jogada | B: batida em duas pontas | V: alterna modo | N: nova partida"
        elif self.round_over:
            if self.match_over:
                guide_1 = "Partida encerrada."
                guide_2 = "Pressione N para reiniciar a partida."
            else:
                guide_1 = "Rodada encerrada."
                guide_2 = "A proxima rodada inicia automaticamente."
        else:
            guide_1 = "Aguarde sua vez."
            guide_2 = "V alterna modo de jogo entre rodadas."

        guide_1_render = self.small_font.render(guide_1, True, WHITE)
        guide_2_render = self.small_font.render(guide_2, True, WHITE)
        surface.blit(guide_1_render, (20, WINDOW_HEIGHT - 62))
        surface.blit(guide_2_render, (20, WINDOW_HEIGHT - 40))

        status_color = RED if "invalida" in self.status_message else BLUE
        status_bg = pygame.Rect(0, WINDOW_HEIGHT - 92, WINDOW_WIDTH, 26)
        pygame.draw.rect(surface, status_color, status_bg)
        status_render = self.small_font.render(self.status_message, True, WHITE)
        surface.blit(status_render, (14, WINDOW_HEIGHT - 88))


def run_game() -> None:
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()
    board = DominoBoard()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            else:
                board.handle_event(event)

        board.update()
        board.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
