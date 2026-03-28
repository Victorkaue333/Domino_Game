"""
Sistema de sons do jogo de Dominó.
Gera sons proceduralmente usando pygame.mixer.
"""

import pygame
import numpy as np
from typing import Optional

from src.config import ENABLE_SOUND, SOUND_VOLUME


class SoundManager:
    """Gerencia todos os sons do jogo."""
    
    def __init__(self):
        """Inicializa o gerenciador de sons."""
        self.enabled = ENABLE_SOUND
        self.volume = SOUND_VOLUME
        
        if not self.enabled:
            return
        
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self._create_sounds()
        except pygame.error as e:
            print(f"Erro ao inicializar mixer de áudio: {e}")
            self.enabled = False
    
    def _create_sounds(self) -> None:
        """Cria todos os sons proceduralmente."""
        if not self.enabled:
            return
        
        try:
            # Som de peça sendo colocada na mesa
            self.place_tile_sound = self._generate_click_sound(frequency=440, duration=0.1)
            
            # Som de compra do cemitério
            self.draw_tile_sound = self._generate_click_sound(frequency=330, duration=0.15)
            
            # Som de vitória
            self.win_sound = self._generate_victory_sound()
            
            # Som de erro/jogada inválida
            self.error_sound = self._generate_error_sound()
            
            # Som de passar a vez
            self.pass_sound = self._generate_pass_sound()
            
        except Exception as e:
            print(f"Erro ao criar sons: {e}")
            self.enabled = False
    
    def _generate_click_sound(self, frequency: int = 440, duration: float = 0.1) -> Optional[pygame.mixer.Sound]:
        """
        Gera um som de clique simples.
        
        Args:
            frequency: Frequência do som em Hz.
            duration: Duração do som em segundos.
            
        Returns:
            Som gerado ou None se falhar.
        """
        try:
            sample_rate = 22050
            samples = int(sample_rate * duration)
            
            # Gera onda senoidal
            wave = np.sin(2 * np.pi * frequency * np.linspace(0, duration, samples))
            
            # Aplica envelope de atenuação (fade out)
            envelope = np.linspace(1, 0, samples)
            wave = wave * envelope
            
            # Normaliza e converte para int16
            wave = (wave * 32767).astype(np.int16)
            
            # Cria som estéreo
            stereo_wave = np.column_stack((wave, wave))
            
            sound = pygame.mixer.Sound(stereo_wave)
            sound.set_volume(self.volume)
            return sound
        except Exception as e:
            print(f"Erro ao gerar som de clique: {e}")
            return None
    
    def _generate_victory_sound(self) -> Optional[pygame.mixer.Sound]:
        """Gera um som de vitória (escala ascendente)."""
        try:
            sample_rate = 22050
            duration = 0.5
            frequencies = [523, 659, 784]  # Dó, Mi, Sol (acorde de Dó maior)
            
            full_wave = None
            
            for freq in frequencies:
                samples = int(sample_rate * (duration / len(frequencies)))
                wave = np.sin(2 * np.pi * freq * np.linspace(0, duration / len(frequencies), samples))
                
                # Envelope
                envelope = np.concatenate([
                    np.linspace(0, 1, samples // 4),
                    np.ones(samples // 2),
                    np.linspace(1, 0, samples // 4)
                ])
                wave = wave * envelope
                
                if full_wave is None:
                    full_wave = wave
                else:
                    full_wave = np.concatenate([full_wave, wave])
            
            # Normaliza
            full_wave = (full_wave * 32767 * 0.5).astype(np.int16)
            stereo_wave = np.column_stack((full_wave, full_wave))
            
            sound = pygame.mixer.Sound(stereo_wave)
            sound.set_volume(self.volume)
            return sound
        except Exception as e:
            print(f"Erro ao gerar som de vitória: {e}")
            return None
    
    def _generate_error_sound(self) -> Optional[pygame.mixer.Sound]:
        """Gera um som de erro (tom descendente)."""
        try:
            sample_rate = 22050
            duration = 0.3
            
            # Tom descendente de 400Hz para 200Hz
            samples = int(sample_rate * duration)
            frequencies = np.linspace(400, 200, samples)
            
            wave = np.zeros(samples)
            for i in range(samples):
                wave[i] = np.sin(2 * np.pi * frequencies[i] * i / sample_rate)
            
            # Envelope
            envelope = np.linspace(1, 0, samples)
            wave = wave * envelope
            
            # Normaliza
            wave = (wave * 32767 * 0.3).astype(np.int16)
            stereo_wave = np.column_stack((wave, wave))
            
            sound = pygame.mixer.Sound(stereo_wave)
            sound.set_volume(self.volume)
            return sound
        except Exception as e:
            print(f"Erro ao gerar som de erro: {e}")
            return None
    
    def _generate_pass_sound(self) -> Optional[pygame.mixer.Sound]:
        """Gera um som suave para passar a vez."""
        try:
            sample_rate = 22050
            duration = 0.2
            frequency = 300
            
            samples = int(sample_rate * duration)
            wave = np.sin(2 * np.pi * frequency * np.linspace(0, duration, samples))
            
            # Envelope suave
            envelope = np.concatenate([
                np.linspace(0, 1, samples // 3),
                np.linspace(1, 0, 2 * samples // 3)
            ])
            wave = wave * envelope
            
            # Normaliza
            wave = (wave * 32767 * 0.2).astype(np.int16)
            stereo_wave = np.column_stack((wave, wave))
            
            sound = pygame.mixer.Sound(stereo_wave)
            sound.set_volume(self.volume)
            return sound
        except Exception as e:
            print(f"Erro ao gerar som de passar: {e}")
            return None
    
    def play_place_tile(self) -> None:
        """Toca o som de colocar peça."""
        if self.enabled and hasattr(self, 'place_tile_sound') and self.place_tile_sound:
            self.place_tile_sound.play()
    
    def play_draw_tile(self) -> None:
        """Toca o som de comprar peça."""
        if self.enabled and hasattr(self, 'draw_tile_sound') and self.draw_tile_sound:
            self.draw_tile_sound.play()
    
    def play_win(self) -> None:
        """Toca o som de vitória."""
        if self.enabled and hasattr(self, 'win_sound') and self.win_sound:
            self.win_sound.play()
    
    def play_error(self) -> None:
        """Toca o som de erro."""
        if self.enabled and hasattr(self, 'error_sound') and self.error_sound:
            self.error_sound.play()
    
    def play_pass(self) -> None:
        """Toca o som de passar a vez."""
        if self.enabled and hasattr(self, 'pass_sound') and self.pass_sound:
            self.pass_sound.play()
    
    def set_volume(self, volume: float) -> None:
        """
        Define o volume dos sons.
        
        Args:
            volume: Volume entre 0.0 e 1.0.
        """
        self.volume = max(0.0, min(1.0, volume))
        
        if self.enabled:
            for attr_name in ['place_tile_sound', 'draw_tile_sound', 'win_sound', 
                             'error_sound', 'pass_sound']:
                if hasattr(self, attr_name):
                    sound = getattr(self, attr_name)
                    if sound:
                        sound.set_volume(self.volume)
    
    def toggle_sound(self) -> None:
        """Liga/desliga os sons."""
        self.enabled = not self.enabled
    
    def is_enabled(self) -> bool:
        """Retorna se o som está habilitado."""
        return self.enabled


# Instância global do gerenciador de sons
_sound_manager: Optional[SoundManager] = None


def get_sound_manager() -> SoundManager:
    """
    Retorna a instância global do gerenciador de sons.
    
    Returns:
        Instância do SoundManager.
    """
    global _sound_manager
    if _sound_manager is None:
        _sound_manager = SoundManager()
    return _sound_manager


# Funções de conveniência
def play_place_tile() -> None:
    """Toca o som de colocar peça."""
    get_sound_manager().play_place_tile()


def play_draw_tile() -> None:
    """Toca o som de comprar peça."""
    get_sound_manager().play_draw_tile()


def play_win() -> None:
    """Toca o som de vitória."""
    get_sound_manager().play_win()


def play_error() -> None:
    """Toca o som de erro."""
    get_sound_manager().play_error()


def play_pass() -> None:
    """Toca o som de passar a vez."""
    get_sound_manager().play_pass()
