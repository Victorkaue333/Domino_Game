"""
Testes unitários para o módulo domino.py
"""

import unittest
from src.domino import DominoTile, generate_domino_set, tile_rank, MAX_PIP_VALUE


class TestDominoTile(unittest.TestCase):
    """Testes para a classe DominoTile."""

    def test_tile_creation(self):
        """Testa a criação de uma peça de dominó."""
        tile = DominoTile(3, 5)
        self.assertEqual(tile.left, 3)
        self.assertEqual(tile.right, 5)

    def test_is_double_true(self):
        """Testa se uma dupla é corretamente identificada."""
        tile = DominoTile(4, 4)
        self.assertTrue(tile.is_double())

    def test_is_double_false(self):
        """Testa se uma peça não-dupla não é identificada como dupla."""
        tile = DominoTile(2, 5)
        self.assertFalse(tile.is_double())

    def test_pip_sum(self):
        """Testa o cálculo da soma das pintas."""
        tile = DominoTile(3, 5)
        self.assertEqual(tile.pip_sum(), 8)
        
        double = DominoTile(6, 6)
        self.assertEqual(double.pip_sum(), 12)

    def test_matches_left(self):
        """Testa se a peça encaixa pelo lado esquerdo."""
        tile = DominoTile(3, 5)
        self.assertTrue(tile.matches(3))

    def test_matches_right(self):
        """Testa se a peça encaixa pelo lado direito."""
        tile = DominoTile(3, 5)
        self.assertTrue(tile.matches(5))

    def test_matches_false(self):
        """Testa quando a peça não encaixa."""
        tile = DominoTile(3, 5)
        self.assertFalse(tile.matches(2))
        self.assertFalse(tile.matches(6))

    def test_flipped(self):
        """Testa se a peça é invertida corretamente."""
        tile = DominoTile(2, 6)
        flipped = tile.flipped()
        self.assertEqual(flipped.left, 6)
        self.assertEqual(flipped.right, 2)
        
        # Verifica que a peça original não foi alterada (frozen)
        self.assertEqual(tile.left, 2)
        self.assertEqual(tile.right, 6)

    def test_tile_immutability(self):
        """Testa se a peça é imutável (frozen)."""
        tile = DominoTile(3, 5)
        with self.assertRaises(AttributeError):
            tile.left = 4


class TestGenerateDominoSet(unittest.TestCase):
    """Testes para a função generate_domino_set."""

    def test_set_size(self):
        """Testa se o conjunto tem o número correto de peças."""
        domino_set = generate_domino_set()
        # Para max_value=6: (6+1)*(6+2)/2 = 28 peças
        expected_size = (MAX_PIP_VALUE + 1) * (MAX_PIP_VALUE + 2) // 2
        self.assertEqual(len(domino_set), expected_size)

    def test_set_uniqueness(self):
        """Testa se todas as peças são únicas."""
        domino_set = generate_domino_set()
        # Converte para tuplas para verificar unicidade
        tile_tuples = set()
        for tile in domino_set:
            # Normaliza (menor, maior) para evitar duplicatas como (3,5) e (5,3)
            normalized = tuple(sorted([tile.left, tile.right]))
            tile_tuples.add(normalized)
        
        self.assertEqual(len(tile_tuples), len(domino_set))

    def test_custom_max_value(self):
        """Testa a geração com valor máximo customizado."""
        domino_set = generate_domino_set(max_value=3)
        # Para max_value=3: (3+1)*(3+2)/2 = 10 peças
        expected_size = 10
        self.assertEqual(len(domino_set), expected_size)
        
        # Verifica se nenhuma peça tem valor maior que 3
        for tile in domino_set:
            self.assertLessEqual(tile.left, 3)
            self.assertLessEqual(tile.right, 3)

    def test_set_contains_doubles(self):
        """Testa se o conjunto contém todas as duplas esperadas."""
        domino_set = generate_domino_set()
        doubles = [tile for tile in domino_set if tile.is_double()]
        
        # Deve ter 7 duplas (0-0 até 6-6)
        self.assertEqual(len(doubles), MAX_PIP_VALUE + 1)

    def test_randomization(self):
        """Testa se as peças são embaralhadas."""
        set1 = generate_domino_set()
        set2 = generate_domino_set()
        
        # É extremamente improvável que duas gerações sejam idênticas
        # se estiverem sendo embaralhadas corretamente
        tiles_different = False
        for i in range(len(set1)):
            if set1[i] != set2[i]:
                tiles_different = True
                break
        
        self.assertTrue(tiles_different, "Os conjuntos devem ser embaralhados")


class TestTileRank(unittest.TestCase):
    """Testes para a função tile_rank."""

    def test_rank_order(self):
        """Testa se a classificação ordena corretamente."""
        tile1 = DominoTile(1, 2)  # soma=3
        tile2 = DominoTile(2, 3)  # soma=5
        tile3 = DominoTile(3, 4)  # soma=7
        
        rank1 = tile_rank(tile1)
        rank2 = tile_rank(tile2)
        rank3 = tile_rank(tile3)
        
        self.assertLess(rank1, rank2)
        self.assertLess(rank2, rank3)

    def test_rank_structure(self):
        """Testa a estrutura da tupla retornada."""
        tile = DominoTile(2, 5)
        rank = tile_rank(tile)
        
        self.assertEqual(len(rank), 3)
        self.assertEqual(rank[0], 7)  # soma
        self.assertEqual(rank[1], 5)  # maior lado
        self.assertEqual(rank[2], 2)  # menor lado

    def test_rank_double_vs_regular(self):
        """Testa classificação entre dupla e peça regular com mesma soma."""
        double = DominoTile(3, 3)  # soma=6
        regular = DominoTile(2, 4)  # soma=6
        
        rank_double = tile_rank(double)
        rank_regular = tile_rank(regular)
        
        # Com mesma soma, maior lado decide (3 vs 4)
        self.assertLess(rank_double, rank_regular)


if __name__ == "__main__":
    unittest.main()
