import pygame
import pygame_gui
from pygame.locals import *
import sys
import random
import os
from sound_manager import play_goal_sound, play_hit_sound, play_bounce_sound, play_background_music

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
GREEN = (0, 255, 0)

# Инициализация Pygame с окном без границ
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
pygame.display.set_caption("2D Football Game")

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
resolution_options = ["800x600", "720x480", "640x480", "1280x800", "1280x720", "1024x768", "1920x1080"] 
selected_resolution = 0  # Индекс выбранного разрешения
selected_option = 0  # Индекс выбранной опции в меню
ui_manager = pygame_gui.UIManager((WIDTH, HEIGHT))
volume = 0.5

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

def create_volume_slider():
    volume_slider_rect = pygame.Rect((WIDTH // 2 - 100, HEIGHT // 2 + 50), (200, 20))
    volume_slider = pygame_gui.elements.UIHorizontalSlider(volume_slider_rect, 0.5, (0.0, 1.0), manager=ui_manager)
    return volume_slider

volume_slider = create_volume_slider()

def options_menu():
    global selected_option
    global show_menu
    global screen
    global WIDTH, HEIGHT
    global volume

    fullscreen_toggle = False

    # Pygame GUI initialization
    ui_manager = pygame_gui.UIManager((WIDTH, HEIGHT))

    # Create volume slider
    volume_slider_rect = pygame.Rect((WIDTH // 2 - 100, HEIGHT // 2 + 50), (200, 20))
    volume_slider = pygame_gui.elements.UIHorizontalSlider(volume_slider_rect, volume, (0.0, 1.0), manager=ui_manager)

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
                elif event.key == pygame.K_ESCAPE:
                    show_menu = True
                    return
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:  # Back
                        show_menu = True
                        return
                    elif selected_option == 1:  # Toggle Fullscreen
                        fullscreen_toggle = not fullscreen_toggle
                        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN if fullscreen_toggle else 0)
                        pygame.display.set_caption("2D Football Game")
                    elif selected_option == 2:  # Set Volume
                        # Set volume based on the slider value
                        pygame.mixer.music.set_volume(volume_slider.get_current_value())
                        show_menu = True
                        return
            elif event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    if event.ui_element == volume_slider:
                        # Update the volume value
                        volume = volume_slider.get_current_value()

            # Update the UI manager with the current event
            ui_manager.process_events(event)

        # Update the UI manager
        ui_manager.update(pygame.time.get_ticks() / 1000.0)

        # Draw GUI elements
        ui_manager.draw_ui(screen)

        pygame.mixer.music.set_volume(volume)

        font = pygame.font.Font(None, 36)

        # Render and display the fullscreen toggle switch
        toggle_text = font.render("Fullscreen", True, (255, 255, 255))
        toggle_rect = toggle_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        pygame.draw.rect(screen, (255, 255, 255), toggle_rect, 2)

        if fullscreen_toggle:
            pygame.draw.rect(screen, (0, 255, 0), (toggle_rect.centerx, toggle_rect.top, toggle_rect.width // 2, toggle_rect.height), 0)
        else:
            pygame.draw.rect(screen, (255, 0, 0), (toggle_rect.left, toggle_rect.top, toggle_rect.width // 2, toggle_rect.height), 0)

        screen.blit(toggle_text, toggle_rect.topleft)

        # Render and display the volume label
        volume_label = font.render("-  Music Volume  +", True, (255, 255, 255))
        volume_label_rect = volume_label.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
        screen.blit(volume_label, volume_label_rect.topleft)

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
            play_goal_sound()
        elif ball.right > WIDTH:
            ball.x = WIDTH // 2 - ball_size // 2
            ball.y = HEIGHT // 2 - ball_size // 2
            score_left += 1
            ball_speed = initial_ball_speed.copy()
            # Воспроизведение звука при забитии гола
            play_goal_sound()
        if ball.left < goal_left:
            ball.x = WIDTH // 2 - ball_size // 2
            ball.y = HEIGHT // 2 - ball_size // 2
            score_right += 1
            ball_speed = initial_ball_speed.copy()
            # Воспроизведение звука при забитии гола
            play_goal_sound()
        elif ball.right > goal_right:
            ball.x = WIDTH // 2 - ball_size // 2
            ball.y = HEIGHT // 2 - ball_size // 2
            score_left += 1
            ball_speed = initial_ball_speed.copy()
            # Воспроизведение звука при забитии гола
            play_goal_sound()

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
            play_hit_sound()

        if pygame.Rect(player2_pos.x - player_radius, player2_pos.y - player_radius, player_radius * 2,
                    player_radius * 2).colliderect(ball):
            # Изменение направления и скорости мяча в зависимости от столкновения с игроком
            relative_speed = ball_speed - player2_speed
            relative_direction = pygame.Vector2(player2_pos - ball.center).normalize()
            ball_speed -= 2 * relative_speed.dot(relative_direction) * relative_direction

            # Воспроизведение звука при отбитии мяча игроком
            play_hit_sound()

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
            play_bounce_sound()

        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed.y = -ball_speed.y
            play_bounce_sound()

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
                play_bounce_sound()

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