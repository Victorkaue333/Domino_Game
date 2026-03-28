"""
Testes unitários para o módulo board.py
"""

import unittest
from src.board import Player, MoveSide
from src.domino import DominoTile


class TestPlayer(unittest.TestCase):
    """Testes para a classe Player."""

    def test_player_creation_human(self):
        """Testa a criação de um jogador humano."""
        player = Player(name="João", is_human=True)
        self.assertEqual(player.name, "João")
        self.assertTrue(player.is_human)
        self.assertEqual(player.score, 0)
        self.assertEqual(len(player.hand), 0)

    def test_player_creation_bot(self):
        """Testa a criação de um bot."""
        player = Player(name="Bot 1", is_human=False)
        self.assertEqual(player.name, "Bot 1")
        self.assertFalse(player.is_human)

    def test_hand_points_empty(self):
        """Testa pontos com mão vazia."""
        player = Player(name="Test", is_human=True)
        self.assertEqual(player.hand_points(), 0)

    def test_hand_points_single_tile(self):
        """Testa pontos com uma peça."""
        player = Player(name="Test", is_human=True)
        player.hand.append(DominoTile(3, 5))
        self.assertEqual(player.hand_points(), 8)

    def test_hand_points_multiple_tiles(self):
        """Testa pontos com múltiplas peças."""
        player = Player(name="Test", is_human=True)
        player.hand.extend([
            DominoTile(2, 3),  # 5
            DominoTile(4, 4),  # 8
            DominoTile(1, 6),  # 7
        ])
        self.assertEqual(player.hand_points(), 20)

    def test_hand_modification(self):
        """Testa adição e remoção de peças da mão."""
        player = Player(name="Test", is_human=True)
        tile = DominoTile(3, 5)
        
        player.hand.append(tile)
        self.assertEqual(len(player.hand), 1)
        
        player.hand.remove(tile)
        self.assertEqual(len(player.hand), 0)


class TestMoveSide(unittest.TestCase):
    """Testes para o enum MoveSide."""

    def test_move_side_values(self):
        """Testa os valores do enum."""
        self.assertEqual(MoveSide.LEFT.value, "left")
        self.assertEqual(MoveSide.RIGHT.value, "right")
        self.assertEqual(MoveSide.BOTH.value, "both")

    def test_move_side_comparison(self):
        """Testa comparação entre valores do enum."""
        self.assertEqual(MoveSide.LEFT, MoveSide.LEFT)
        self.assertNotEqual(MoveSide.LEFT, MoveSide.RIGHT)


class TestDominoTileMatching(unittest.TestCase):
    """Testes de lógica de encaixe de peças."""

    def test_tile_matches_scenario_1(self):
        """Testa cenário básico de encaixe."""
        tile = DominoTile(3, 5)
        
        # Deve encaixar se a ponta da mesa for 3 ou 5
        self.assertTrue(tile.matches(3))
        self.assertTrue(tile.matches(5))
        
        # Não deve encaixar com outros valores
        self.assertFalse(tile.matches(1))
        self.assertFalse(tile.matches(6))

    def test_double_tile_matching(self):
        """Testa encaixe de peça dupla."""
        double = DominoTile(6, 6)
        
        # Dupla só encaixa com seu próprio valor
        self.assertTrue(double.matches(6))
        self.assertFalse(double.matches(5))

    def test_tile_flipping_for_placement(self):
        """Testa orientação de peça para encaixe."""
        tile = DominoTile(2, 5)
        
        # Se a ponta da mesa é 2, usamos a peça como está
        # Se a ponta é 5, devemos virar
        flipped = tile.flipped()
        
        self.assertEqual(tile.left, 2)
        self.assertEqual(tile.right, 5)
        self.assertEqual(flipped.left, 5)
        self.assertEqual(flipped.right, 2)


class TestGameLogic(unittest.TestCase):
    """Testes de lógica de jogo."""

    def test_winning_conditions(self):
        """Testa diferentes condições de vitória."""
        # Vitória normal (última peça jogada)
        # Vitória com dupla (carroça)
        # Vitória em duas pontas
        # Jogo fechado
        
        # Estes serão implementados conforme a lógica do jogo evolui
        pass

    def test_score_calculation(self):
        """Testa cálculo de pontuação."""
        # Batida normal = 1 ponto
        # Batida com dupla = 2 pontos
        # Batida em duas pontas = 3 ou 4 pontos
        # Jogo fechado = 1 ponto
        
        # Estes serão implementados conforme a lógica de pontuação
        pass


if __name__ == "__main__":
    unittest.main()
