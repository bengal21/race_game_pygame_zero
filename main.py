import pgzrun
from pgzero.actor import Actor
from pgzero.keyboard import keyboard
from random import randint
import pygame
import sys
from buttons import Button

WIDTH = 800
HEIGHT = 600
y_car = Actor('y_car')
r_car = Actor('r_car')
finish = Actor('finish')
y_car.pos = 250, 300
r_car.pos = 450, 300

SPEED = 4
track_count = 0
track_position = 450
track_width = 270
track_direction = False
track_left = []
track_right = []
game_status = 0


def draw():
    global game_status
    screen.fill('blue')
    if game_status == 0:
        y_car.draw()
        r_car.draw()
        b = 0
        while b < len(track_left):
            track_left[b].draw()
            track_right[b].draw()
            b += 1
    if track_count > 100:
        finish.pos = 400, 150
        finish.draw()
    if game_status == 1:
        screen.draw.text("Желтая машина победила!", center=(WIDTH / 2, HEIGHT / 2), fontsize=80, color="yellow")
    elif game_status == 2:
        screen.draw.text("Красная машина победила!", center=(WIDTH / 2, HEIGHT / 2), fontsize=80, color="red")


def update():
    global game_status, track_count
    if game_status == 0:
        if keyboard.left:
            r_car.x -= 2
        elif keyboard.a:
            y_car.x -= 2
        elif keyboard.right:
            r_car.x += 2
        elif keyboard.d:
            y_car.x += 2
        elif keyboard.up:
            r_car.y -= 2
        elif keyboard.w:
            y_car.y -= 2
        elif keyboard.down:
            r_car.y += 2
        elif keyboard.s:
            y_car.y += 2

        update_track()


def build_track():
    global track_count, track_left, track_right, track_position, track_width
    track_left.append(Actor("barrier", pos=(track_position - track_width, 0)))
    track_right.append(Actor("barrier", pos=(track_position + track_width, 0)))
    track_count += 1


def update_track():
    global track_count, track_position, track_direction, track_width, game_status
    b = 0
    while b < len(track_left):
        if r_car.colliderect(track_left[b]) or r_car.colliderect(track_right[b]) or y_car.colliderect(finish):
            game_status = 1
        elif y_car.colliderect(track_left[b]) or y_car.colliderect(track_right[b]) or r_car.colliderect(finish):
            game_status = 2
        elif y_car.colliderect(r_car):
            r_car.x += randint(-3, 3)
            r_car.y += randint(-3, 3)
            y_car.y += randint(-3, 3)
            y_car.x += randint(-3, 3)
        track_left[b].y += SPEED
        track_right[b].y += SPEED
        b += 1
    if track_left[len(track_left) - 1].y > 32:
        if track_direction == False:
            track_position += 16
        if track_direction == True:
            track_position -= 16
        if randint(0, 4) == 1:
            track_direction = not track_direction
        if track_position > 700 - track_width:
            track_direction = True
        if track_position < track_width:
            track_direction = False
        build_track()


def start():
    build_track()
    pgzrun.go()


pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.png")


def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)


def play():
    start()
    # pygame.quit()
    # sys.exit()


def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("МЕНЮ", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/start_but.png"), pos=(640, 250),
                             text_input="Играть", font=get_font(60), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/exit_but.png"), pos=(640, 450),
                             text_input="Выход", font=get_font(60), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()


main_menu()
