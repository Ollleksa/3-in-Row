import sys
import pygame

import header

class Button(pygame.sprite.Sprite):
    """
    Class for buttons, but it dont do anything important for now.
    """
    def __init__(self, name, type, location):
        """
        Init button, load image and set location
        :param name: name of image for button
        :param type: type of button
        :param location: location of left top corner of image
        """
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        self.image, self.rect = header.load_image(name, -1)
        self.rect.left, self.rect.top = location

    def action(self, screen_type, pos):
        """
        Action of button but not really helpful
        :param screen_type: what screen (main menu, gameplay, highscore)
        :param pos: possition of the mouse
        :return: always return 1, if not exit game
        """
        if self.rect.collidepoint(pos):
            if self.type == 'exit':
                if screen_type == 0 or screen_type == 2:
                    pygame.quit()
                    sys.exit(1)
                if screen_type == 1:
                    return 1
            elif self.type == 'start':
                return 1
            elif self.type == 'cont':
                return 1
            elif self.type == 'HS':
                return 1

    def show(self, screen):
        """
        Show everything on screen.
        """
        screen.blit(self.image, self.rect)