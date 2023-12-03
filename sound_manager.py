import pygame
import os

sound_folder = os.path.join(os.path.dirname(__file__), 'sound')

pygame.init()

# Загрузка звуков
goal_sound = pygame.mixer.Sound(os.path.join(sound_folder, "mixkit-winning-a-coin-video-game-2069.wav"))
hit_sound = pygame.mixer.Sound(os.path.join(sound_folder, "lovi-myach.wav"))
bounce_sound = pygame.mixer.Sound(os.path.join(sound_folder, "otskok-myacha.wav"))
pygame.mixer.music.load(os.path.join(sound_folder, "main-menu-1.wav"))

# Установка громкости
pygame.mixer.music.set_volume(0.5)
bounce_sound.set_volume(0.5)
hit_sound.set_volume(0.5)
goal_sound.set_volume(0.5)

def play_goal_sound():
    goal_sound.play()

def play_hit_sound():
    hit_sound.play()

def play_bounce_sound():
    bounce_sound.play()

def play_background_music():
    pygame.mixer.music.play(loops=-1)
