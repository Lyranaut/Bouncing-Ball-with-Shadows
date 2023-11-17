import pygame
from pygame.locals import *
import math

pygame.init()

# Определение параметров окна
WIDTH, HEIGHT = 800, 600
FPS = 60

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
SHADOW = (192, 192, 192)

# Инициализация Pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball with Shadows")

# Игровые объекты - мяч и игроки
ball_size = 20
ball = pygame.Rect(WIDTH // 2 - ball_size // 2, HEIGHT // 2 - ball_size // 2, ball_size, ball_size)
ball_speed = pygame.Vector2(3, 2)

player_size = 50
player1 = pygame.Rect(WIDTH - 30, HEIGHT // 2 - player_size // 2, 10, player_size)
player2 = pygame.Rect(20, HEIGHT // 2 - player_size // 2, 10, player_size)

# Вертикальная линия по центру
center_line = pygame.Rect(WIDTH // 2 - 2, 0, 4, HEIGHT)

# Изначальные позиции игроков
initial_player1_x = player1.x
initial_player2_x = player2.x

# Скорость игроков
player_speed = 5

# Ворота
goal_left = 10
goal_right = WIDTH - 20

# Счетчики для каждого ворота
score_left = 0
score_right = 0

# Основной цикл игры
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Управление движением игрока 1
    if keys[K_UP] and player1.top > 0:
        player1.y -= player_speed
    if keys[K_DOWN] and player1.bottom < HEIGHT and not player1.colliderect(center_line):
        player1.y += player_speed
    if keys[K_LEFT] and player1.left > WIDTH // 2 + 2:
        player1.x -= player_speed
    if keys[K_RIGHT] and player1.right < WIDTH:
        player1.x += player_speed

    # Движение мяча
    ball.x += ball_speed.x
    ball.y += ball_speed.y

    # Отскок мяча от стен
    if ball.left <= 0 or ball.right >= WIDTH:
        ball_speed.x = -ball_speed.x  # Отскок от левой и правой границ окна

    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed.y = -ball_speed.y  # Отскок от верхней и нижней границ окна

    # Возвращение мяча в центр поля при попадании в ворота
    if ball.left < 0:
        ball.x = WIDTH // 2 - ball_size // 2
        ball.y = HEIGHT // 2 - ball_size // 2
        score_right += 1
    elif ball.right > WIDTH:
        ball.x = WIDTH // 2 - ball_size // 2
        ball.y = HEIGHT // 2 - ball_size // 2
        score_left += 1

    if ball.left < goal_left:
        ball.x = WIDTH // 2 - ball_size // 2
        ball.y = HEIGHT // 2 - ball_size // 2
        score_right += 1
    elif ball.right > goal_right:
        ball.x = WIDTH // 2 - ball_size // 2
        ball.y = HEIGHT // 2 - ball_size // 2
        score_left += 1

    # Управление движением второго игрока (ИИ)
    if ball.y < player2.y + player_size // 2:
        player2.y -= player_speed
    elif ball.y > player2.y + player_size // 2:
        player2.y += player_speed

    # Обработка столкновения мяча с игроками
    if player1.colliderect(ball) or player2.colliderect(ball):
        normal = pygame.Vector2(ball.x - (player1.x + player2.x) / 2, ball.y - (player1.y + player2.y) / 2).normalize()
        ball_speed = ball_speed.reflect(normal)

    # Очистка экрана
    screen.fill((0, 0, 0))

    # Рисование мяча и теней
    pygame.draw.ellipse(screen, SHADOW, (ball.x - 5, ball.y - 5, ball_size + 10, ball_size + 10))
    pygame.draw.ellipse(screen, RED, ball)

    # Рисование теней игроков
    pygame.draw.ellipse(screen, SHADOW, player1)
    pygame.draw.ellipse(screen, SHADOW, player2)

    # Рисование игроков
    pygame.draw.ellipse(screen, WHITE, player1)
    pygame.draw.ellipse(screen, WHITE, player2)

    # Рисование ворот
    pygame.draw.line(screen, WHITE, (goal_left, 0), (goal_left, HEIGHT), 2)
    pygame.draw.line(screen, WHITE, (goal_right, 0), (goal_right, HEIGHT), 2)

    # Рисование линии центра поля
    pygame.draw.rect(screen, WHITE, center_line)

    # Отображение счета
    font = pygame.font.Font(None, 36)
    score_display = font.render(f"{score_left} - {score_right}", True, WHITE)
    screen.blit(score_display, (WIDTH // 2 - score_display.get_width() // 2, 20))

    # Обновление экрана
    pygame.display.flip()

    # Установка FPS
    clock.tick(FPS)

pygame.quit()
