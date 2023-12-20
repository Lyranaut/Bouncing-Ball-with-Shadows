import pygame
import pygame_gui
from pygame.locals import *
import sys
import random
import os
from sound_manager import *
from Graphics import *

#Add music to the game | Добавляем музыку в игру
sound_folder = os.path.join(os.path.dirname(__file__), 'sound')

pygame.init()

#Geting Screen Size | Получение размеров экрана
info = pygame.display.Info()
pygame.display.set_caption("2D Football Game")

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Main Menu | Главное меню

def main_menu():
    global selected_option
    global show_menu

    while True:
        screen.fill(Colores[0])

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
            color = Colores[4] if i == selected_option else (Colores[9])
            text = menu_font.render(option, True, color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - len(menu_options) * 25 + i * 50))

        pygame.display.flip()

#Restarting game for New Game button | Перезагрузка при New Game
def reset_game():
    global ball
    global ball_speed
    global initial_ball_speed
    global player1_pos
    global player2_pos
    global player1_speed
    global player2_speed
    global score_left
    global score_right
    global obstacles
    global start_time

    # Reset the ball | Возврат мяча в начальное положение
    ball.x = WIDTH // 2 - ball_size // 2
    ball.y = HEIGHT // 2 - ball_size // 2
    ballx = random.randint(-5, 5)
    bally = random.randint(-5, 5)
    initial_ball_speed = pygame.Vector2(ballx, bally)
    ball_speed = initial_ball_speed.copy()

    # Reset player positions and speeds | Возврат игроков в начальное положение
    player1_pos = pygame.Vector2(WIDTH - 260, HEIGHT // 2)
    player2_pos = pygame.Vector2(260, HEIGHT // 2)
    player1_speed = pygame.Vector2(0, 0)
    player2_speed = pygame.Vector2(0, 0)

    # Reset scores | Сброс счета
    score_left = 0
    score_right = 0

    # Regenerate obstacles | Регенерация преград
    obstacles = [pygame.Rect(random.randint(WIDTH // 3, 2 * WIDTH // 3 - 30), random.randint(0, HEIGHT - 30), 30, 30)
                 for _ in range(random.randint(0, 5))]

    # Reset the game timer | Перезапуск таймера
    start_time = pygame.time.get_ticks()


#Main menu function | Функция главного меню
def return_to_main_menu():
    global show_game_menu
    global selected_option

    # Reset game variables if needed | Рестарт если нужно
    reset_game()

    # Exit the game menu loop | Конец цикла меню
    show_game_menu = False

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Menu during the game(ESC) | Меню во время игры(ESC)
def game_menu():
    global show_game_menu
    global selected_option
    global show_menu

    while show_game_menu:
        screen.fill(Colores[0])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(game_menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(game_menu_options)
                elif event.key == pygame.K_ESCAPE:
                    show_game_menu = False
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
            color = Colores[4] if i == selected_option else (Colores[9])
            text = menu_font.render(option, True, color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - len(game_menu_options) * 25 + i * 50))

        pygame.display.flip()

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Option menu | меню опций


def options_menu():
    global selected_option
    global show_menu
    global screen
    global WIDTH, HEIGHT
    global volume

    fullscreen_toggle = False
    volume_toggle = False

    # Pygame GUI initialization | Инииализация Pygame GUI
    ui_manager = pygame_gui.UIManager((WIDTH, HEIGHT))

                                    # Create volume slider
                                                    #volume_slider_rect = pygame.Rect((WIDTH // 2 - 100, HEIGHT // 2 + 50), (200, 20))
                                                    #volume_slider = pygame_gui.elements.UIHorizontalSlider(volume_slider_rect, volume, (0.0, 1.0), manager=ui_manager)

    while True:
        screen.fill(Colores[0])

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
                            if fullscreen_toggle:
                                # Switch to full screen mode | Переключение в полноэкранный режим
                                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
                            else:
                                # Switch to screen mode with new window size | Переключение в оконный режим с новыми размерами окна
                                windowed_width, windowed_height = 1000, 800  # New window size | Новые размеры окна
                                screen = pygame.display.set_mode((windowed_width, windowed_height))
                            pygame.display.set_caption("2D Football Game")
                        elif selected_option == 2:  # Set Volume
                            # Set volume based on the slider value
                            volume_toggle = not volume_toggle
                            if volume_toggle:
                                volume = 0
                            else:
                                volume = 0.7
                            return
                    elif event.key == pygame.K_m:
                        volume_toggle = not volume_toggle
                        if volume_toggle:
                            volume = 0
                        else:
                            volume = 0.7
                    elif event.key == pygame.K_f:
                        fullscreen_toggle = not fullscreen_toggle
                        if fullscreen_toggle:
                            # Switch to full screen mode | Переключение в полноэкранный режим
                            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
                        else:
                             # Switch to screen mode with new window size | Переключение в оконный режим с новыми размерами окна
                            windowed_width, windowed_height = 900, 700  # New window size | Новые размеры окна
                            screen = pygame.display.set_mode((windowed_width, windowed_height))
                            
                             # Scaling of game objects and obstacles | Масштабирование игровых объектов и преград
                            ball.x = windowed_width // 2 - ball_size // 2
                            ball.y = windowed_height // 2 - ball_size // 2

                            player1_pos.x = windowed_width - 30
                            player2_pos.x = 30
                            
                            for obstacle in obstacles:
                                obstacle.x = random.randint(windowed_width // 3, 2 * windowed_width // 3 - 30)
                                obstacle.y = random.randint(0, windowed_height - 30)

                        pygame.display.set_caption("2D Football Game")

            elif event.type == pygame.VIDEORESIZE:
                #Geting new screen size | Получение новых размеров окна
                WIDTH, HEIGHT = event.size
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                
                #Scaling of game objects and obstacles | Масштабирование игровых объектов и преград
                ball.x = WIDTH // 2 - ball_size // 2
                ball.y = HEIGHT // 2 - ball_size // 2

                player1_pos.x = WIDTH - 30
                player2_pos.x = 30
                
                for obstacle in obstacles:
                    obstacle.x = random.randint(WIDTH // 3, 2 * WIDTH // 3 - 30)
                    obstacle.y = random.randint(0, HEIGHT - 30)

                #Update the position of the gates inside the screen | Обновляем положение ворот внутри экрана
                goal_left = max(10, WIDTH // 3)
                goal_right = min(2 * WIDTH // 3 - 30, WIDTH - 20)

                pygame.draw.line(screen, Colores[2], (goal_right, 0), (goal_right, HEIGHT), 2)

                # Update the UI manager with the current event | Обновленик UI менеджера для текущего события
                ui_manager.process_events(event)

        # Update the UI manager | Обновленик UI менеджера
        ui_manager.update(pygame.time.get_ticks() / 1000.0)

        # Draw GUI elements | Рисовка элементов
        ui_manager.draw_ui(screen)

        pygame.mixer.music.set_volume(volume)

        font = pygame.font.Font(None, 36)

        # Render and display the fullscreen toggle switch | Рендер и дисплей фулскрин свитчера
        toggle_text = font.render("Fullscreen", True, (Colores[1]))
        toggle_text1 = font.render("Music Mute", True, (Colores[1]))
        toggle_rect = toggle_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 35))
        toggle_rect1 = toggle_text1.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 35))
        pygame.draw.rect(screen, (Colores[1]), toggle_rect, 2)
        pygame.draw.rect(screen, (Colores[1]), toggle_rect1, 2)

        if fullscreen_toggle:
            pygame.draw.rect(screen, (Colores[5]), (toggle_rect.centerx, toggle_rect.top, toggle_rect.width // 2, toggle_rect.height), 0)
        else:
            pygame.draw.rect(screen, (Colores[2]), (toggle_rect.left, toggle_rect.top, toggle_rect.width // 2, toggle_rect.height), 0)

        screen.blit(toggle_text, toggle_rect.topleft)

        if volume_toggle:
            pygame.draw.rect(screen, (Colores[5]), (toggle_rect1.centerx, toggle_rect1.top, toggle_rect1.width // 2, toggle_rect1.height), 0)
        else:
            pygame.draw.rect(screen, (Colores[2]), (toggle_rect1.left, toggle_rect1.top, toggle_rect1.width // 2, toggle_rect1.height), 0)

        screen.blit(toggle_text1, toggle_rect1.topleft)
                                        # Render and display the volume label
                                        #volume_label = font.render("-  Music Volume  +", True, (255, 255, 255))
                                        #volume_label_rect = volume_label.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
                                        #screen.blit(volume_label, volume_label_rect.topleft)

        pygame.display.flip()


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Main game loop | Оснновной игровой цикл


while True:
    pygame.mixer.music.play(loops=-1)
    main_menu()
    
    pygame.mixer.music.stop()
    #game loop | цикл игры
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:      #control | управление
                if event.key == pygame.K_ESCAPE:
                  show_game_menu = True

        keys = pygame.key.get_pressed()

        if keys[K_UP]:
            player1_speed.y = -8
        elif keys[K_DOWN]:
            player1_speed.y = 8
        else:
            player1_speed.y = 0

        if keys[K_LEFT]:
            player1_speed.x = -8
        elif keys[K_RIGHT]:
            player1_speed.x = 8
        else:
            player1_speed.x = 0

        if keys[K_w]:
            player2_speed.y = -8
        elif keys[K_s]:
            player2_speed.y = 8
        else:
            player2_speed.y = 0

        if keys[K_a]:
            player2_speed.x = -8
        elif keys[K_d]:
            player2_speed.x = 8
        else:
            player2_speed.x = 0

        if show_game_menu:
            pygame.mixer.music.play(loops=-1)
            game_menu()
        else:
            pygame.mixer.music.stop()


        player1_pos += player1_speed
        player2_pos += player2_speed

        #Added code for timer |  Добавленный код для таймера
        elapsed_time = pygame.time.get_ticks() - start_time
        if elapsed_time >= game_duration:
            running = False

        #Goal system | система голов
        if ball.left < 0:
            ball.x = WIDTH // 2 - ball_size // 2
            ball.y = HEIGHT // 2 - ball_size // 2
            score_right += 1
            ball_speed = initial_ball_speed.copy()
            #Playing sound when scoring a goal | Воспроизведение звука при забитии гола
            play_goal_sound()
            initial_ball_speed = pygame.Vector2(random.randint(1, 5), random.randint(1, 5))
        elif ball.right > WIDTH:
            ball.x = WIDTH // 2 - ball_size // 2
            ball.y = HEIGHT // 2 - ball_size // 2
            score_left += 1
            ball_speed = initial_ball_speed.copy()
            #Playing sound when scoring a goal | Воспроизведение звука при забитии гола
            play_goal_sound()
            initial_ball_speed = pygame.Vector2(random.randint(1, 5), random.randint(1, 5))
        if ball.left < goal_left:
            ball.x = WIDTH // 2 - ball_size // 2
            ball.y = HEIGHT // 2 - ball_size // 2
            score_right += 1
            ball_speed = initial_ball_speed.copy()
            #Playing sound when scoring a goal | Воспроизведение звука при забитии гола
            play_goal_sound()
            initial_ball_speed = pygame.Vector2(random.randint(1, 5), random.randint(1, 5))
        elif ball.right > goal_right:
            ball.x = WIDTH // 2 - ball_size // 2
            ball.y = HEIGHT // 2 - ball_size // 2
            score_left += 1
            ball_speed = initial_ball_speed.copy()
            #Playing sound when scoring a goal | Воспроизведение звука при забитии гола
            play_goal_sound()
            initial_ball_speed = pygame.Vector2(random.randint(1, 5), random.randint(1, 5))

        #Blind screen wales | Глухие стены экрана
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

        #Handing ball collisions with players | Обработка столкновения мяча с игроками
        if pygame.Rect(player1_pos.x - player_radius, player1_pos.y - player_radius, player_radius * 2,
                    player_radius * 2).colliderect(ball):
            #Changes the ditection and speed of the ball depending on the collision the player  
            #Изменение направления и скорости мяча в зависимости от столкновения с игроком
            relative_speed = ball_speed - player1_speed
            relative_direction = pygame.Vector2(player1_pos - ball.center).normalize()
            ball_speed -= 1.75 * relative_speed.dot(relative_direction) * relative_direction

            # playing sound when the player hits the ball
            # Воспроизведение звука при отбитии мяча игроком
            play_hit_sound()

        if pygame.Rect(player2_pos.x - player_radius, player2_pos.y - player_radius, player_radius * 2,
                    player_radius * 2).colliderect(ball):
            #Changes the ditection and speed of the ball depending on the collision the player
            # Изменение направления и скорости мяча в зависимости от столкновения с игроком
            relative_speed = ball_speed - player2_speed
            relative_direction = pygame.Vector2(player2_pos - ball.center).normalize()
            ball_speed -= 1.75 * relative_speed.dot(relative_direction) * relative_direction

            # playing sound when the player hits the ball
            # Воспроизведение звука при отбитии мяча игроком
            play_hit_sound()

        # Handing player collisions with obstacles
        # Обработка столкновения игроков с преградами
        for obstacle in obstacles:
            # Pplayer 1 | Игрок 1
            if pygame.Rect(player1_pos.x - player_radius, player1_pos.y - player_radius, player_radius * 2,
                        player_radius * 2).colliderect(obstacle):
                overlap = player_radius + obstacle.width / 2 - player1_pos.distance_to(obstacle.center)
                direction = (obstacle.center - player1_pos).normalize()
                player1_pos -= overlap * direction

            #Pplayer 1 |  Игрок 2
            if pygame.Rect(player2_pos.x - player_radius, player2_pos.y - player_radius, player_radius * 2,
                        player_radius * 2).colliderect(obstacle):
                overlap = player_radius + obstacle.width / 2 - player2_pos.distance_to(obstacle.center)
                direction = (obstacle.center - player2_pos).normalize()
                player2_pos -= overlap * direction
        
        #Handing players collisions
        # Обработка столкновения игроков с игроками
        if player1_pos.distance_to(player2_pos) < 2 * player_radius:
            overlap = 2 * player_radius - player1_pos.distance_to(player2_pos)
            direction = (player2_pos - player1_pos).normalize()
            player1_pos -= overlap / 2 * direction
            player2_pos += overlap / 2 * direction

        ball.x += ball_speed.x
        ball.y += ball_speed.y

        # Bouncing ball with wall
        # Отскок мяча от стен
        if ball.left <= 0 or ball.right >= WIDTH:
            ball_speed.x = -ball_speed.x
            play_bounce_sound()

        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed.y = -ball_speed.y
            play_bounce_sound()

        # Handing ball collisions with obstacles | Обработка столкновения мяча с преградами
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

        #Graphic draw | отрисовка графики
        screen.fill(Colores[0])

        pygame.draw.ellipse(screen, Colores[4], ball)
        pygame.draw.circle(screen, Colores[7], (int(player1_pos.x), int(player1_pos.y)), player_radius)
        pygame.draw.circle(screen, Colores[3], (int(player2_pos.x), int(player2_pos.y)), player_radius)
        pygame.draw.line(screen, Colores[3], (goal_left, 0), (goal_left, HEIGHT), 2)
        pygame.draw.line(screen, Colores[2], (goal_right, 0), (goal_right, HEIGHT), 2)

        # Drawing obstacle | Отрисовка преград
        for obstacle in obstacles:
            pygame.draw.rect(screen, Colores[6], obstacle)

        font = pygame.font.Font(None, 36)
        # Добавленный код для отображения таймера
        # Show time

        if show_menu:
        # If the menu display flag is set, call the main menu | Если флаг отображения меню установлен, вызываем главное меню
            main_menu()
            #After returning from the menu, set the flag to False again |  После возврата из меню, снова устанавливаем флаг в False
            show_menu = False

        remaining_minutes = (game_duration - elapsed_time) // 1000 // 60
        remaining_seconds = (game_duration - elapsed_time) // 1000 % 60
        timer_display = font.render(f"{remaining_minutes}:{remaining_seconds:02}", True, Colores[8])
        #Draw a timer to the left of the score | Рисуем таймер слева от счета
        screen.blit(timer_display, (WIDTH // 2.2 - timer_display.get_width() // 2, 20))
        #Drowing ther score | Рисуем счет
        score_display = font.render(f"           | {score_left}  -  {score_right} | ", True, Colores[8])
        screen.blit(score_display, (WIDTH // 2 - score_display.get_width() // 2, 20))

        pygame.display.flip()

        clock.tick(FPS)

    #At the end of the timer, we display a messege about the winner | По окончании таймера выводим сообщение о победителе
    if score_left < score_right:
        winner_message = "Red Won!"
    elif score_left > score_right:
        winner_message = "Blue Won!"
    else:
        winner_message = "It's a Tie!"

    #Display the winner message of a black background | Отображаем сообщение о победителе на чёрном фоне
    screen.fill(Colores[0])
    winner_display = font.render(winner_message, True, Colores[1])
    screen.blit(winner_display, (WIDTH // 2 - winner_display.get_width() // 2, HEIGHT // 2 - winner_display.get_height() // 2))
    pygame.display.flip()

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #Wait some timebefor ending the program | Ждем некоторое время перед завершением программы
    pygame.time.wait(1000)

    pygame.quit()
    sys.exit()