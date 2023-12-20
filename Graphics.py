import pygame
import pygame_gui
from pygame.locals import *
import sys
import random
import os
from sound_manager import *

pygame.init()

#Colores | Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
VIOLET = (238, 130, 238)
DARK_RED = (201, 10, 3)
DARK_GREEN = (3, 168, 47)
COLOR = (200, 200, 200)
Colores = [BLACK, WHITE, RED, BLUE, YELLOW, GREEN, VIOLET, DARK_RED, DARK_GREEN, COLOR]

#Geting Screen Size | Получение размеров экрана
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

FPS = 60

#Initializing Pygame with a borderless window | Инициализация Pygame с окном без границ
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)

#Customize the shape and size of the ball | Настройка формы и размеров мяча
ball_size = 20
ball = pygame.Rect(WIDTH // 2 - ball_size // 2, HEIGHT // 2 - ball_size // 2, ball_size, ball_size)
ballx = random.randint(-5, 5)
bally = random.randint(-5, 5)
initial_ball_speed = pygame.Vector2(ballx, bally)
ball_speed = initial_ball_speed.copy()

#Customize player shapes and sizes | Настройка формы и размеров игроков
player_radius = 20
player1_pos = pygame.Vector2(WIDTH - 260, HEIGHT // 2)
player2_pos = pygame.Vector2(260, HEIGHT // 2)
player1_speed = pygame.Vector2(0, 0)
player2_speed = pygame.Vector2(0, 0)

#Gates | Ворота
goal_left = 10
goal_right = WIDTH - 20

#Counters for each gate  |  Счетчики для каждого ворота
score_left = 0
score_right = 0

#Generation of rundom obstacles | Генерация случайных преград
obstacles = [pygame.Rect(random.randint(WIDTH // 3, 2 * WIDTH // 3 - 30), random.randint(0, HEIGHT - 30), random.randint(20, 50), random.randint(20, 50))
             for _ in range(random.randint(1, 5))]

#Added variables for the timer |  Добавленные переменные для таймера
start_time = pygame.time.get_ticks()
game_duration = 3 * 60 * 1000  # 3 minutes

#Variables for menu |  Переменные для меню
show_menu = False
show_game_menu = False
menu_font = pygame.font.Font(None, 50)
menu_options = ["Start", "Options", "Exit"]
game_menu_options = ["Resume", "New Game", "Options", "Main Menu", "Exit"]
resolution_options = ["800x600", "720x480", "640x480", "1280x800", "1280x720", "1024x768", "1920x1080"] 
selected_resolution = 0  # Индекс выбранного разрешения
selected_option = 0  # Индекс выбранной опции в меню
ui_manager = pygame_gui.UIManager((WIDTH, HEIGHT))
volume = 0.7

#Volume slder(inactive) | звуковой слайдер(отключено)
def create_volume_slider():
    volume_slider_rect = pygame.Rect((WIDTH // 2 - 100, HEIGHT // 2 + 50), (200, 20))
    volume_slider = pygame_gui.elements.UIHorizontalSlider(volume_slider_rect, 0.5, (0.0, 1.0), manager=ui_manager)
    return volume_slider

volume_slider = create_volume_slider()