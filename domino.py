from dataclasses import dataclass
import random


MAX_PIP_VALUE = 6
HAND_TILES = 6


@dataclass(frozen=True, slots=True)
class DominoTile:
    left: int
    right: int

    def is_double(self) -> bool:
        return self.left == self.right

    def pip_sum(self) -> int:
        return self.left + self.right

    def matches(self, pip: int) -> bool:
        return self.left == pip or self.right == pip

    def flipped(self) -> "DominoTile":
        return DominoTile(self.right, self.left)


def generate_domino_set(max_value: int = MAX_PIP_VALUE) -> list[DominoTile]:
    tiles: list[DominoTile] = []

    for left in range(max_value + 1):
        for right in range(left, max_value + 1):
            tiles.append(DominoTile(left, right))

    random.shuffle(tiles)
    return tiles


def tile_rank(tile: DominoTile) -> tuple[int, int, int]:
    highest_side = max(tile.left, tile.right)
    lowest_side = min(tile.left, tile.right)
    return (tile.pip_sum(), highest_side, lowest_side)