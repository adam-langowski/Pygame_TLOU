import sys
import pygame
import random
from pygame import mixer

pygame.init()

# SCREENS
width, height = 1920, 1024
screen = pygame.display.set_mode((width, height))
myFont = pygame.font.SysFont("Verdana", 36)
pygame.display.set_caption("Save Ellie - TLOU GAME")

programIcon = pygame.image.load('icon .png')
pygame.display.set_icon(programIcon)

bg = pygame.image.load("background_image.jpg")
menu_screen = pygame.image.load("menu_screen.jpg")
loss_screen = pygame.image.load("loss_screen.jpg")

# COLORS
player_yellow = (251, 222, 68)
opponents_red = (199, 49, 49)
background_blue = (40, 51, 79)

# VISUAL SETTINGS
Ellie_image = pygame.image.load('Ellie-TLOU-II.jpg').convert()
zombie_image = pygame.image.load('zombie.png').convert()
player_size = 100
player_position = [width / 2, height - 2 * player_size]

enemy_size = 100
enemy_position = [random.randint(0, width - enemy_size), height]
enemy_list = [enemy_position]

# MUSIC
mixer.init()
mixer.music.load('Tlou_music.mp3')
mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.2)

# CLOCK DEFINITION
clock = pygame.time.Clock()

# START VALUES
speed = 5
score = 0
level = 1
high_score = 0
previous_score = 0
game_over = False


def drop_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < 15 and delay < 0.039:
        x_pos = random.randint(0, width - enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])


def draw_enemies(enemy_list):
    for enemy_position in enemy_list:
        pygame.draw.rect(screen, opponents_red, (enemy_position[0], enemy_position[1], enemy_size, enemy_size))

        zombie_image = pygame.image.load('zombie.png').convert()
        zombie_image = pygame.transform.scale(zombie_image, (120, 120))
        rect = zombie_image.get_rect()
        rect.center = (enemy_position[0] + 40, enemy_position[1] + 40)
        screen.blit(zombie_image, rect)


def update_enemy_positions(enemy_list, score):
    for id, enemy_position in enumerate(enemy_list):
        if 0 <= enemy_position[1] < height:
            enemy_position[1] += speed
        else:
            enemy_list.pop(id)
            score += 1
    return score


def collision_check(enemy_list, player_position):
    for enemy_position in enemy_list:
        if detect_collision(enemy_position, player_position):
            return True
    return False


def set_level(score):
    if score < 50:
        speed = 5
        level = 1
    elif score < 80:
        speed = 7
        level = 2
    elif score < 120:
        speed = 9
        level = 3
    elif score < 150:
        speed = 11
        level = 4
    elif score < 200:
        speed = 13
        level = 5
    else:
        speed = 15
        level = 6
    return [speed, level]


def detect_collision(player_pos, enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    e_x = enemy_pos[0]
    e_y = enemy_pos[1]

    if (p_x <= e_x < (p_x + player_size)) or (e_x <= p_x < (e_x + enemy_size)):
        if (p_y <= e_y < (p_y + player_size)) or (e_y <= p_y < (e_y + enemy_size)):
            return True
    return False


def show_result(text):
    global game_over, player_position, enemy_position, score, level, speed, high_score, previous_score

    screen.blit(loss_screen, (0, 0))
    show_signature()

    final_score = (pygame.font.SysFont("arialblack", 50)).render(text, True, (0, 0, 0))
    screen.blit(final_score, (width/2 - 180, height/2 - 400))
    replay_text = (pygame.font.SysFont("arialblack", 32)).render("Press space to restart", True, (0, 0, 0))
    screen.blit(replay_text, (width/2 - 187, height/2 - 320))
    quit_text = (pygame.font.SysFont("arialblack", 32)).render("Press 'Q' to go back to main menu", True, (0, 0, 0))
    screen.blit(quit_text, (width / 2 - 285, height / 2 - 285))
    pygame.display.update()
    pygame.event.clear()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    previous_score = score
                    if score > high_score:
                        high_score = score
                    score = 0
                    level = 1
                    speed = 5
                    player_position = [width / 2, height - 2 * player_size]
                    enemy_position = [random.randint(0, width - enemy_size), 0]
                    enemy_list.clear()
                    play()
                elif event.key == pygame.K_q:
                    menu()


def menu():
    global menu_screen

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    play()
                elif event.key == pygame.K_q:
                    sys.exit()
                elif event.key == pygame.K_i:
                    instructions()

        screen.blit(menu_screen, (0, 0))

        play_text = "PLAY > PRESS 'P'"
        play_text = (pygame.font.SysFont("impact", 52)).render(play_text, True, (0, 0, 0))
        screen.blit(play_text, (width - 1500, height - 580))

        quit_text = "QUIT > PRESS 'Q'"
        quit_text = (pygame.font.SysFont("impact", 52)).render(quit_text, True, (0, 0, 0))
        screen.blit(quit_text, (width - 1500, height - 460))

        instructions_text = "INSTRUCTIONS > PRESS 'I'"
        instructions_text = (pygame.font.SysFont("impact", 52)).render(instructions_text, True, (0, 0, 0))
        screen.blit(instructions_text, (width - 1500, height - 520))

        show_signature()
        pygame.display.update()


def show_signature():
    signature_text = "Game by Adam Langowski"
    signature_text = (pygame.font.SysFont("lucidahandwriting", 28)).render(signature_text, True, (0, 0, 0))
    screen.blit(signature_text, (width - 1820, height - 100))


def instructions():
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    menu()

        screen.blit(menu_screen, (0, 0))

        instructions_text = "Move with arrows LEFT & RIGHT to avoid zombies."
        instructions_text = (pygame.font.SysFont("arialblack", 28)).render(instructions_text, True, (0, 0, 0))
        screen.blit(instructions_text, (width - 1700, height - 600))

        instructions_text2 = "There are 6 difficulty levels."
        instructions_text2 = (pygame.font.SysFont("arialblack", 28)).render(instructions_text2, True, (0, 0, 0))
        screen.blit(instructions_text2, (width - 1700, height - 560))

        menu_text = "MAIN MENU > PRESS 'M'"
        menu_text = (pygame.font.SysFont("impact", 36)).render(menu_text, True, (0, 0, 0))
        screen.blit(menu_text, (width - 1600, height - 480))

        show_signature()
        pygame.display.update()


def play():
    global game_over, player_position, score, level, speed, Ellie_image, zombie_image

    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # PLAYER MOVEMENT
            if event.type == pygame.KEYDOWN:
                x = player_position[0]
                y = player_position[1]
                if event.key == pygame.K_LEFT and x > player_size:
                    x -= player_size
                elif event.key == pygame.K_RIGHT and x < width - 2 * player_size:
                    x += player_size
                player_position = [x, y]

        screen.blit(bg, (0, 0))
        show_signature()

        # PLAYER ICON
        pygame.draw.rect(screen, player_yellow, (player_position[0], player_position[1], player_size, player_size))
        Ellie_image = pygame.image.load('Ellie-TLOU-II.jpg').convert()
        Ellie_image = pygame.transform.scale(Ellie_image, (120, 120))
        rect = Ellie_image.get_rect()
        rect.center = (player_position[0]+40, player_position[1]+40)
        screen.blit(Ellie_image, rect)

        drop_enemies(enemy_list)
        score = update_enemy_positions(enemy_list, score)
        speed = set_level(score)[0]
        level = set_level(score)[1]

        score_text = ("Your score: " + str(score))
        score_text = myFont.render(score_text, True,  (0, 0, 0))
        screen.blit(score_text, (width - 300, height - 70))

        high_score_text = ("High score: " + str(high_score))
        high_score_text = myFont.render(high_score_text, True, (0, 0, 0))
        screen.blit(high_score_text, (10, 10))

        level_text = ("Level:" + str(level))
        level_text = myFont.render(level_text, True, (0, 0, 0))
        screen.blit(level_text, (width - 500, height - 70))

        draw_enemies(enemy_list)
        final_score = ("Final score: " + str(score))

        if collision_check(enemy_list, player_position):
            show_result(final_score)
            game_over = False

        clock.tick(64)
        pygame.display.update()


if __name__ == "__main__":
    menu()
