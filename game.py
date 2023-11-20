import pygame
from pygame.locals import *
import sys

pygame.init()

# Получение размеров экрана
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

FPS = 60

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Инициализация Pygame с окном без границ
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
pygame.display.set_caption("2D Football Game")

ball_size = 20
ball = pygame.Rect(WIDTH // 2 - ball_size // 2, HEIGHT // 2 - ball_size // 2, ball_size, ball_size)
ball_speed = pygame.Vector2(3, 2)

player_radius = 20
player1_pos = pygame.Vector2(WIDTH - 30, HEIGHT // 2)
player2_pos = pygame.Vector2(30, HEIGHT // 2)
player1_speed = pygame.Vector2(0, 0)
player2_speed = pygame.Vector2(0, 0)

# Ворота
goal_left = 10
goal_right = WIDTH - 20

# Счетчики для каждого ворота
score_left = 0
score_right = 0

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    keys = pygame.key.get_pressed()

    if keys[K_UP]:
        player1_speed.y = -5
    elif keys[K_DOWN]:
        player1_speed.y = 5
    else:
        player1_speed.y = 0

    if keys[K_LEFT]:
        player1_speed.x = -5
    elif keys[K_RIGHT]:
        player1_speed.x = 5
    else:
        player1_speed.x = 0

    if keys[K_w]:
        player2_speed.y = -5
    elif keys[K_s]:
        player2_speed.y = 5
    else:
        player2_speed.y = 0

    if keys[K_a]:
        player2_speed.x = -5
    elif keys[K_d]:
        player2_speed.x = 5
    else:
        player2_speed.x = 0

    player1_pos += player1_speed
    player2_pos += player2_speed

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

    # Глухие стены экрана
    if player1_pos.x > WIDTH:
        player1_pos.x = WIDTH
    elif player1_pos.x < 0:
        player1_pos.x = 0

    if player2_pos.x > WIDTH:
        player2_pos.x = WIDTH
    elif player2_pos.x < 0:
        player2_pos.x = 0

    if player1_pos.y > HEIGHT:
        player1_pos.y = HEIGHT
    elif player1_pos.y < 0:
        player1_pos.y = 0

    if player2_pos.y > HEIGHT:
        player2_pos.y = HEIGHT
    elif player2_pos.y < 0:
        player2_pos.y = 0

    # Обработка столкновения игроков
    distance = player1_pos.distance_to(player2_pos)
    if distance < 2 * player_radius:
        overlap = 2 * player_radius - distance
        direction = (player2_pos - player1_pos).normalize()
        player1_pos -= 0.5 * overlap * direction
        player2_pos += 0.5 * overlap * direction

    ball.x += ball_speed.x
    ball.y += ball_speed.y

    # Отскок мяча от стен
    if ball.left <= 0 or ball.right >= WIDTH:
        ball_speed.x = -ball_speed.x

    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed.y = -ball_speed.y

    # Обработка столкновения мяча с игроками
    if pygame.Rect(player1_pos.x - player_radius, player1_pos.y - player_radius, player_radius * 2,
                   player_radius * 2).colliderect(ball) or \
            pygame.Rect(player2_pos.x - player_radius, player2_pos.y - player_radius, player_radius * 2,
                        player_radius * 2).colliderect(ball):
        ball_speed = -ball_speed

    screen.fill((0, 0, 0))

    pygame.draw.ellipse(screen, YELLOW, ball)
    pygame.draw.circle(screen, RED, (int(player1_pos.x), int(player1_pos.y)), player_radius)
    pygame.draw.circle(screen, BLUE, (int(player2_pos.x), int(player2_pos.y)), player_radius)
    pygame.draw.line(screen, BLUE, (goal_left, 0), (goal_left, HEIGHT), 2)
    pygame.draw.line(screen, RED, (goal_right, 0), (goal_right, HEIGHT), 2)
    font = pygame.font.Font(None, 36)
    score_display = font.render(f"{score_left} - {score_right}", True, WHITE)
    screen.blit(score_display, (WIDTH // 2 - score_display.get_width() // 2, 20))

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
sys.exit()
