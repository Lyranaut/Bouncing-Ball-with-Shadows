import pygame
from pygame.locals import *
import sys
import random
import os
import settings


#загрузка звуков
sound_folder = os.path.join(os.path.dirname(__file__), 'sound')

pygame.init()

# Получение размеров экрана
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

FPS = 60

#Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Инициализация Pygame с окном без границ
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
pygame.display.set_caption("2D Football Game")

#подключение звуков
goal_sound = pygame.mixer.Sound(os.path.join(sound_folder, "mixkit-winning-a-coin-video-game-2069.wav"))
hit_sound = pygame.mixer.Sound(os.path.join(sound_folder, "lovi-myach.wav"))
bounce_sound = pygame.mixer.Sound(os.path.join(sound_folder, "otskok-myacha.wav"))
pygame.mixer.music.load(os.path.join(sound_folder, "main-menu-1.wav"))
pygame.mixer.music.set_volume(0.5)
bounce_sound.set_volume(0.5)
hit_sound.set_volume(0.5)
goal_sound.set_volume(0.5)

#настройка формы и размеров мяча
ball_size = 20
ball = pygame.Rect(WIDTH // 2 - ball_size // 2, HEIGHT // 2 - ball_size // 2, ball_size, ball_size)
initial_ball_speed = pygame.Vector2(3, 2)
ball_speed = initial_ball_speed.copy()

#настройка формы и размеров игроков
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

# Добавленные переменные для таймера
start_time = pygame.time.get_ticks()
game_duration = 3 * 60 * 1000  # 3 minutes

# Переменные для главного меню
show_menu = False
show_game_menu = False
menu_font = pygame.font.Font(None, 50)
menu_options = ["Start", "Options", "Exit"]
game_menu_options = ["Resume", "New Game", "Options", "Main Menu", "Exit"]
resolution_options = ["800x600", "1024x768", "1280x720", "1920x1080"] 
selected_resolution = 0  # Индекс выбранного разрешения
selected_option = 0  # Индекс выбранной опции в меню

def main_menu():
    global selected_option  # Добавленная строка
    global show_menu

    while True:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:  # Start
                        return
                    elif selected_option == 1:  # Options
                        options_menu()
                    elif selected_option == 2:  # Exit
                        pygame.quit()
                        sys.exit()


        for i, option in enumerate(menu_options):
            color = YELLOW if i == selected_option else (200, 200, 200)
            text = menu_font.render(option, True, color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - len(menu_options) * 25 + i * 50))

        pygame.display.flip()

def reset_game():
    global ball
    global ball_speed
    global player1_pos
    global player2_pos
    global player1_speed
    global player2_speed
    global score_left
    global score_right
    global obstacles
    global start_time

    # Reset the ball
    ball.x = WIDTH // 2 - ball_size // 2
    ball.y = HEIGHT // 2 - ball_size // 2
    ball_speed = initial_ball_speed.copy()

    # Reset player positions and speeds
    player1_pos = pygame.Vector2(WIDTH - 30, HEIGHT // 2)
    player2_pos = pygame.Vector2(30, HEIGHT // 2)
    player1_speed = pygame.Vector2(0, 0)
    player2_speed = pygame.Vector2(0, 0)

    # Reset scores
    score_left = 0
    score_right = 0

    # Regenerate obstacles
    obstacles = [pygame.Rect(random.randint(WIDTH // 3, 2 * WIDTH // 3 - 30), random.randint(0, HEIGHT - 30), 30, 30)
                 for _ in range(5)]

    # Reset the game timer
    start_time = pygame.time.get_ticks()



def return_to_main_menu():
    global show_game_menu
    global selected_option

    # Reset game variables if needed
    reset_game()

    # Exit the game menu loop
    show_game_menu = False



# Остальной код без изменений
def game_menu():
    global show_game_menu
    global selected_option
    global show_menu

    while show_game_menu:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(game_menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(game_menu_options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:  # Resume
                        show_game_menu = False
                    elif selected_option == 1:  # New Game
                        reset_game()
                        show_game_menu = False
                    elif selected_option == 2:  # Options
                        options_menu()
                    elif selected_option == 3:  # Main Menu
                        return_to_main_menu()
                        show_menu = True
                    elif selected_option == 4:  # Exit
                        pygame.quit()
                        sys.exit()

        for i, option in enumerate(game_menu_options):
            color = YELLOW if i == selected_option else (200, 200, 200)
            text = menu_font.render(option, True, color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - len(game_menu_options) * 25 + i * 50))

        pygame.display.flip()

def options_menu():
    global selected_option
    global show_menu
    global screen
    global WIDTH, HEIGHT
    global selected_resolution

    fullscreen_checkbox = False

    while True:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % 3
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % 3
                elif event.key == pygame.K_LEFT:  
                    selected_resolution = (selected_resolution - 1) % len(resolution_options)
                elif event.key == pygame.K_RIGHT:
                    selected_resolution = (selected_resolution + 1) % len(resolution_options)
                elif event.key == pygame.K_ESCAPE:
                    show_menu = True
                    return
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:  # Back
                        show_menu = True
                        return
                    elif selected_option == 1:  # Apply Changes
                        resolution = resolution_options[selected_resolution].split('x')
                        WIDTH, HEIGHT = int(resolution[0]), int(resolution[1])
                        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN if fullscreen_checkbox else 0)
                        pygame.display.set_caption("2D Football Game")
                        return
                    elif selected_option == 2:  # Fullscreen
                        fullscreen_checkbox = not fullscreen_checkbox
                        pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN if fullscreen_checkbox else 0)
                        pygame.display.set_caption("2D Football Game")

        for i, option in enumerate(resolution_options):
            color = WHITE if i == selected_resolution else (200, 200, 200)
            text = menu_font.render(option, True, color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - len(resolution_options) * 25 + i * 50))

        # Отображение чекбокса после выбора качества
        checkbox_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + len(resolution_options) * 50, 20, 20)
        pygame.draw.rect(screen, WHITE, checkbox_rect, 2)
        if fullscreen_checkbox:
            pygame.draw.line(screen, WHITE, (checkbox_rect.left + 5, checkbox_rect.centery),
                            (checkbox_rect.centerx, checkbox_rect.bottom - 5), 2)
            pygame.draw.line(screen, WHITE, (checkbox_rect.centerx, checkbox_rect.bottom - 5),
                            (checkbox_rect.right - 5, checkbox_rect.top + 5), 2)
        font = pygame.font.Font(None, 36)
        text = font.render("Fullscreen", True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2 + 30, HEIGHT // 2 + len(resolution_options) * 50 - 25))

        pygame.display.flip()

while True:
    pygame.mixer.music.play(loops=-1)
    main_menu()
    
    pygame.mixer.music.stop()
    #цикл игры
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:      #управление
                if event.key == pygame.K_ESCAPE:
                  show_game_menu = True

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

        if show_game_menu:
            pygame.mixer.music.play(loops=-1)
            game_menu()
        else:
            pygame.mixer.music.stop()


        player1_pos += player1_speed
        player2_pos += player2_speed

        # Добавленный код для таймера
        elapsed_time = pygame.time.get_ticks() - start_time
        if elapsed_time >= game_duration:
            running = False

        #система голов
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
        
        # Обработка столкновения игроков с игроками
        if player1_pos.distance_to(player2_pos) < 2 * player_radius:
            overlap = 2 * player_radius - player1_pos.distance_to(player2_pos)
            direction = (player2_pos - player1_pos).normalize()
            player1_pos -= overlap / 2 * direction
            player2_pos += overlap / 2 * direction

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

        #отрисовка графики
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
        # Добавленный код для отображения таймера

        if show_menu:
        # Если флаг отображения меню установлен, вызываем главное меню
            main_menu()
            # После возврата из меню, снова устанавливаем флаг в False
            show_menu = False

        remaining_minutes = (game_duration - elapsed_time) // 1000 // 60
        remaining_seconds = (game_duration - elapsed_time) // 1000 % 60
        timer_display = font.render(f"{remaining_minutes}:{remaining_seconds:02}", True, WHITE)
        # Рисуем таймер слева от счета
        screen.blit(timer_display, (WIDTH // 4 - timer_display.get_width() // 2, 20))
        # Рисуем счет
        score_display = font.render(f"{score_left} - {score_right}", True, WHITE)
        screen.blit(score_display, (WIDTH // 2 - score_display.get_width() // 2, 20))

        pygame.display.flip()

        clock.tick(FPS)

    # По окончании таймера выводим сообщение о победителе
    if score_left < score_right:
        winner_message = "Red Won!"
    elif score_left > score_right:
        winner_message = "Blue Won!"
    else:
        winner_message = "It's a Tie!"

    # Отображаем сообщение о победителе на чёрном фоне
    screen.fill((0, 0, 0))
    winner_display = font.render(winner_message, True, WHITE)
    screen.blit(winner_display, (WIDTH // 2 - winner_display.get_width() // 2, HEIGHT // 2 - winner_display.get_height() // 2))
    pygame.display.flip()

    # Ждем некоторое время перед завершением программы
    pygame.time.wait(5000)

    pygame.quit()
    sys.exit()