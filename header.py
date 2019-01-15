# import needed modules
import os
import pickle
import pygame
from pygame.locals import *


def init():
    """
    Function initiate next variables:
    1) iterator_for_animation - used for smooth animation of token moving, changes during stages of animation
    2) animation_in_progress - just flag for informing that animation is going now
    3) anim_type - flag for showing what animation type currently in progress
    4) two_token_moving - variable for saving coordinates of two tokens witch needed to change, speed of moving and direction
    5) falling ones - list for coordinates of tokens that should to fall
    6) three_in_row - flag for is there tree tokens in row
    :return:
    """
    # Flag for is calculation in progress
    global iterator_for_animation
    iterator_for_animation = 0
    # Flag for animation
    global animation_in_progress
    animation_in_progress = False
    # Flag for anime type
    global anim_type
    anim_type = ''
    # Flag for visual moving of two tokens in progress, had coordinates of both, speed of moving and vector of moving
    global two_token_moving
    two_token_moving = (-1, -1, -1, -1, 0, 1)
    # The falling tokens
    global falling_ones
    falling_ones = []
    # Flag if cheging for three in row is needed
    global three_in_row
    three_in_row = True


def text_init():
    """
    Function initiate flags for score and turns left.
    :return:
    """
    # Number of tokens which were collapsed
    global score
    score = 0
    # Turns left
    global turn_left
    turn_left = 3


def is_continue():
    """
    Checking if continue is possible, if file with continue exist, but dont check if corrupted.
    :return:
    """
    if os.path.isfile('continue_data.dat'):
        return True
    else:
        return False


def data_from_cont():
    """
    Function create continue_data.dat file and write inside token types grid, score and turns left
    :param field: it must be list 10x10 with integers range(6)
    """
    f = open('continue_data.dat', 'br')
    temp_list = pickle.load(f)
    f.close()
    global score
    score = temp_list[1]
    global turn_left
    turn_left = temp_list[2]

    return temp_list[0]

# Without module pickle
#######################################
# def data_from_cont():
#     """
#     Loading data from continue_data.dat file to create game field.
#     :return: list 10x10 with token types. Score and turns left is loaded globally
#     """
#     field = []
#     with open('continue_data.dat', 'r') as f:
#         i = 0
#         for line in f:
#             i += 1
#             if i < 11:
#                 field.append([int(x) for x in line[:-2].split(',')])
#             elif i == 11:
#                 print(line)
#                 global score
#                 score = int(line)
#             else:
#                 global turn_left
#                 turn_left = int(line)
#     return field
#
#
# def data_in_cont(field):
#     """
#     Function create continue_data.dat file and write inside token types grid, score and turns left
#     :param field: it must be list 10x10 with integers range(6)
#     """
#     with open('continue_data.dat', 'w') as f:
#         for i in field:
#             for j in i:
#                 f.write(str(j) + ',')
#             f.write('\n')
#         f.write(str(score) + '\n')
#################################


def data_in_cont(field):
    """
    Function create continue_data.dat file and write inside token types grid, score and turns left
    :param field: it must be list 10x10 with integers range(6)
    """
    temp_list = [field, score, turn_left]
    f = open('continue_data.dat', 'bw')
    pickle.dump(temp_list, f)
    f.close()


def load_image(name, colorkey=None):
    """
    Function load pictures by using pygame.image.load().
    :param name: name of the picture. Start directory - directory of calling file
    :param colorkey: if None - no alpha chanel is used, if -1 - alpha color taken from first pixel
    :return: picture and rect for image.
    """
    fullname = os.path.join('pictures', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print('Cannot load image:', name)
        return None
    # if image.get_alpha() is None:
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    # else:
    #    image = image.convert_alpha()
    return image, image.get_rect()


class Background(pygame.sprite.Sprite):
    """
    Class only initiate Background by loading image.
    """

    def __init__(self, image_file, location):
        """
        Load background and set it in the location.
        :param image_file: file name. Home directory - game directory
        :param location: location of left top corner of picture
        """
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image, self.rect = load_image(image_file)
        self.rect.left, self.rect.top = location
