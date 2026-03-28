"""Módulo de peças de dominó e geração do conjunto de peças."""

from dataclasses import dataclass
import random


MAX_PIP_VALUE = 6
HAND_TILES = 6


@dataclass(frozen=True, slots=True)
class DominoTile:
    """Representa uma peça de dominó com dois lados (pintas).
    
    Attributes:
        left: Valor das pintas do lado esquerdo (0-6)
        right: Valor das pintas do lado direito (0-6)
    """
    left: int
    right: int

    def is_double(self) -> bool:
        """Verifica se a peça é uma dupla (carroça).
        
        Returns:
            True se ambos os lados têm o mesmo valor, False caso contrário.
        """
        return self.left == self.right

    def pip_sum(self) -> int:
        """Calcula a soma dos valores de ambos os lados.
        
        Returns:
            Soma total das pintas da peça.
        """
        return self.left + self.right

    def matches(self, pip: int) -> bool:
        """Verifica se a peça pode ser encaixada em uma ponta com o valor especificado.
        
        Args:
            pip: Valor da ponta da mesa onde se deseja encaixar.
            
        Returns:
            True se a peça pode ser encaixada, False caso contrário.
        """
        return self.left == pip or self.right == pip

    def flipped(self) -> "DominoTile":
        """Retorna uma nova peça com os lados invertidos.
        
        Returns:
            Nova peça com valores left e right trocados.
        """
        return DominoTile(self.right, self.left)


def generate_domino_set(max_value: int = MAX_PIP_VALUE) -> list[DominoTile]:
    """Gera um conjunto completo de peças de dominó embaralhadas.
    
    Args:
        max_value: Valor máximo das pintas (padrão: 6).
        
    Returns:
        Lista embaralhada contendo todas as peças do jogo (28 peças para max_value=6).
    """
    tiles: list[DominoTile] = []

    for left in range(max_value + 1):
        for right in range(left, max_value + 1):
            tiles.append(DominoTile(left, right))

    random.shuffle(tiles)
    return tiles


def tile_rank(tile: DominoTile) -> tuple[int, int, int]:
    """Calcula a classificação de uma peça para ordenação e decisões estratégicas.
    
    Args:
        tile: Peça a ser classificada.
        
    Returns:
        Tupla com (soma_total, maior_lado, menor_lado) para comparação.
    """
    highest_side = max(tile.left, tile.right)
    lowest_side = min(tile.left, tile.right)
    return (tile.pip_sum(), highest_side, lowest_side)