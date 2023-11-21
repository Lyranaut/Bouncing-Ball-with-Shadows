import pygame
from pygame.locals import *
import sys
import random
import os

sound_folder = os.path.join(os.path.dirname(__file__), 'sound')

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

goal_sound = pygame.mixer.Sound(os.path.join(sound_folder, "mixkit-winning-a-coin-video-game-2069.wav"))
hit_sound = pygame.mixer.Sound(os.path.join(sound_folder, "lovi-myach.wav"))
bounce_sound = pygame.mixer.Sound(os.path.join(sound_folder, "otskok-myacha.wav"))
bounce_sound.set_volume(0.5)
hit_sound.set_volume(0.5)
goal_sound.set_volume(0.5)

ball_size = 20
ball = pygame.Rect(WIDTH // 2 - ball_size // 2, HEIGHT // 2 - ball_size // 2, ball_size, ball_size)
initial_ball_speed = pygame.Vector2(3, 2)
ball_speed = initial_ball_speed.copy()

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

# Генерация случайных преград (красных квадратов)
obstacles = [pygame.Rect(random.randint(WIDTH // 3, 2 * WIDTH // 3 - 30), random.randint(0, HEIGHT - 30), 30, 30)
             for _ in range(5)]

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
        ball_speed = initial_ball_speed.copy()
        # Воспроизведение звука при забитии гола
        goal_sound.play()
    elif ball.right > WIDTH:
        ball.x = WIDTH // 2 - ball_size // 2
        ball.y = HEIGHT // 2 - ball_size // 2
        score_left += 1
        ball_speed = initial_ball_speed.copy()
        # Воспроизведение звука при забитии гола
        goal_sound.play()

    if ball.left < goal_left:
        ball.x = WIDTH // 2 - ball_size // 2
        ball.y = HEIGHT // 2 - ball_size // 2
        score_right += 1
        ball_speed = initial_ball_speed.copy()
        # Воспроизведение звука при забитии гола
        goal_sound.play()
    elif ball.right > goal_right:
        ball.x = WIDTH // 2 - ball_size // 2
        ball.y = HEIGHT // 2 - ball_size // 2
        score_left += 1
        ball_speed = initial_ball_speed.copy()
        # Воспроизведение звука при забитии гола
        goal_sound.play()

    # Глухие стены экрана
    if player1_pos.x > WIDTH - player_radius:
        player1_pos.x = WIDTH - player_radius
    elif player1_pos.x < player_radius:
        player1_pos.x = player_radius

    if player2_pos.x > WIDTH - player_radius:
        player2_pos.x = WIDTH - player_radius
    elif player2_pos.x < player_radius:
        player2_pos.x = player_radius

    if player1_pos.y > HEIGHT - player_radius:
        player1_pos.y = HEIGHT - player_radius
    elif player1_pos.y < player_radius:
        player1_pos.y = player_radius

    if player2_pos.y > HEIGHT - player_radius:
        player2_pos.y = HEIGHT - player_radius
    elif player2_pos.y < player_radius:
        player2_pos.y = player_radius

    # Обработка столкновения мяча с игроками
    if pygame.Rect(player1_pos.x - player_radius, player1_pos.y - player_radius, player_radius * 2,
                player_radius * 2).colliderect(ball):
        # Изменение направления и скорости мяча в зависимости от столкновения с игроком
        relative_speed = ball_speed - player1_speed
        relative_direction = pygame.Vector2(player1_pos - ball.center).normalize()
        ball_speed -= 2 * relative_speed.dot(relative_direction) * relative_direction

        # Воспроизведение звука при отбитии мяча игроком
        hit_sound.play()

    if pygame.Rect(player2_pos.x - player_radius, player2_pos.y - player_radius, player_radius * 2,
                player_radius * 2).colliderect(ball):
        # Изменение направления и скорости мяча в зависимости от столкновения с игроком
        relative_speed = ball_speed - player2_speed
        relative_direction = pygame.Vector2(player2_pos - ball.center).normalize()
        ball_speed -= 2 * relative_speed.dot(relative_direction) * relative_direction

        # Воспроизведение звука при отбитии мяча игроком
        hit_sound.play()

    # Обработка столкновения игроков с преградами
    for obstacle in obstacles:
        # Игрок 1
        if pygame.Rect(player1_pos.x - player_radius, player1_pos.y - player_radius, player_radius * 2,
                       player_radius * 2).colliderect(obstacle):
            overlap = player_radius + obstacle.width / 2 - player1_pos.distance_to(obstacle.center)
            direction = (obstacle.center - player1_pos).normalize()
            player1_pos -= overlap * direction

        # Игрок 2
        if pygame.Rect(player2_pos.x - player_radius, player2_pos.y - player_radius, player_radius * 2,
                       player_radius * 2).colliderect(obstacle):
            overlap = player_radius + obstacle.width / 2 - player2_pos.distance_to(obstacle.center)
            direction = (obstacle.center - player2_pos).normalize()
            player2_pos -= overlap * direction

    ball.x += ball_speed.x
    ball.y += ball_speed.y

    # Отскок мяча от стен
    if ball.left <= 0 or ball.right >= WIDTH:
        ball_speed.x = -ball_speed.x
        bounce_sound.play()

    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed.y = -ball_speed.y
        bounce_sound.play()

    # Обработка столкновения мяча с преградами
    for obstacle in obstacles:
        if obstacle.colliderect(ball):
            intersection = ball.clip(obstacle)

            if intersection.width > intersection.height:
                ball_speed.y = -ball_speed.y
                ball.y += 2 * (intersection.height * (ball_speed.y > 0) - intersection.height * (ball_speed.y < 0))
            else:
                ball_speed.x = -ball_speed.x
                ball.x += 2 * (intersection.width * (ball_speed.x > 0) - intersection.width * (ball_speed.x < 0))
            bounce_sound.play()

    screen.fill((0, 0, 0))

    pygame.draw.ellipse(screen, YELLOW, ball)
    pygame.draw.circle(screen, RED, (int(player1_pos.x), int(player1_pos.y)), player_radius)
    pygame.draw.circle(screen, BLUE, (int(player2_pos.x), int(player2_pos.y)), player_radius)
    pygame.draw.line(screen, BLUE, (goal_left, 0), (goal_left, HEIGHT), 2)
    pygame.draw.line(screen, RED, (goal_right, 0), (goal_right, HEIGHT), 2)

    # Отрисовка преград
    for obstacle in obstacles:
        pygame.draw.rect(screen, WHITE, obstacle)

    font = pygame.font.Font(None, 36)
    score_display = font.render(f"{score_left} - {score_right}", True, WHITE)
    screen.blit(score_display, (WIDTH // 2 - score_display.get_width() // 2, 20))

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
sys.exit()
