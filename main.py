# import needed modules
import sys
import os
import pygame
from pygame.locals import *
import random

# other files of game
import header
import game_token
import inscriptions
import buttons

# initiate PyGame and fonts
pygame.init()
pygame.font.init()

# initiate some other constants
size = 1024, 768
screen = pygame.display.set_mode(size)

# caption of window
pygame.display.set_caption('First One')

# Control time
clock = pygame.time.Clock()

# loading backgrounds
background = header.Background('background.jpg', [0, 0])
background_MM = header.Background('background_MM.jpg', [0, 0])
background_HS = header.Background('background_HS.jpg', [0, 0])

# field init
random.seed()
Field = game_token.G_Field()
# init text
first_text = inscriptions.my_text()
input_HS = inscriptions.input_box()
HS_table = inscriptions.HS_table()
if not os.path.isfile('HS.dat'):
    HS_table.HS_write()
HS_table.HS_read()
# load buttons
start_button = buttons.Button('start_butt.png', 'start', (0, 480))
exit_button = buttons.Button('Exit_butt.png', 'exit', (0, 668))
cont_button = buttons.Button('Continue_butt.png', 'cont', (0, 280))
HS_button = buttons.Button('HS_show.png', 'HS', (0, 120))
# init global variables
iterator_for_moving = 0
header.init()
header.text_init()
popup_window_status = False

# start screen (0 - main menu, 1 - game, 2 - final menu)
screen_type = 0

# game main loop
while 1:
    clock.tick(60)          # fix fps rate
    # main menu manipulations
    if screen_type == 0:
        # events checking ( we only can exit and press buttons)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(1)
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                exit_button.action(screen_type, pygame.mouse.get_pos())
                if start_button.action(screen_type, pygame.mouse.get_pos()):
                    screen_type = 1
                if cont_button.action(screen_type, pygame.mouse.get_pos()):
                    try:
                        Field = game_token.G_Field(True)
                        screen_type = 1
                    except:
                        pass
                if HS_button.action(screen_type, pygame.mouse.get_pos()):
                    popup_window_status = not popup_window_status

        # showing all on screen
        screen.fill([255, 255, 255])
        screen.blit(background_MM.image, background_MM.rect)
        exit_button.show(screen)
        HS_button.show(screen)
        if header.is_continue():
            cont_button.show(screen)
        start_button.show(screen)
        if popup_window_status:
            HS_table.show(screen)
    # main game screen
    if screen_type == 1:
        # Calculations for three in row, while not falling
        if header.three_in_row and (not header.animation_in_progress):
            header.three_in_row = Field.check_three()
            # print('Checking three in row')
            # if no turns left and no more three in row - then exit to HS menu
            if (not header.three_in_row) and header.turn_left == 0:
                if header.is_continue():
                    os.remove('continue_data.dat')
                screen_type = 2

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(1)
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                # we had only exit button on it, so here it goes
                if exit_button.action(screen_type, pygame.mouse.get_pos()):
                    Field.save()
                    screen_type = 2
                # interaction with mouse
                Field.mouse_interactions(pygame.mouse.get_pos())

        # Moving animation ( we can had some different ones)
        if header.animation_in_progress:
            if header.anim_type == 'changing two':
                Field.moving_two_iter()
            elif header.anim_type == 'disappearing':
                Field.disappearing()
            elif header.anim_type == 'falling':
                Field.falling()

        # Screen reloading
        screen.fill([255, 255, 255])
        screen.blit(background.image, background.rect)
        Field.show(screen)
        first_text.show(screen)
        exit_button.show(screen)
    # final score and exit menu
    if screen_type == 2:
        # we can press buttons and write our HS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(1)
            # what happens when we type
            elif event.type == pygame.KEYDOWN:
                if input_HS.writing(event):
                    HS_table.new_data(input_HS.return_HS())
                    HS_table.HS_write()
            # buttons interactions
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                exit_button.action(screen_type, pygame.mouse.get_pos())
                if start_button.action(screen_type, pygame.mouse.get_pos()):
                    Field = game_token.G_Field()
                    header.init()
                    header.text_init()
                    screen_type = 1
                if cont_button.action(screen_type, pygame.mouse.get_pos()) and header.turn_left != 0:
                    screen_type = 1
        # screen reloading
        screen.fill([255, 255, 255])
        screen.blit(background_HS.image, background_HS.rect)
        input_HS.show(screen)
        HS_table.show(screen)
        exit_button.show(screen)
        start_button.show(screen)
        # we can continue only if some turns left
        if header.turn_left != 0:
            cont_button.show(screen)
        first_text.show(screen)
    # whats it?
    pygame.display.flip()
