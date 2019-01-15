import pygame

import header

class my_text():
    """
    Class for shoing text on screen.
    """
    def __init__(self, name = 'Comic Sans MS', size = 30):
        """
        Create text surfaces and font options.
        :param name: Name of font.
        :param size: Size of font.
        """
        self.myfont = pygame.font.SysFont(name, size)
        self.text_surface = None
        self.text_surface_2 = None

    def text_content(self):
        """
        create text content on surfaces.
        """
        value = str(header.score)
        self.text_surface = self.myfont.render(value, False, (0, 0, 255))
        value_2 = str(header.turn_left)
        self.text_surface_2 = self.myfont.render(value_2, False, (0, 0, 255))

    def show(self, screen):
        """
        Just bliting of screen.
        :param screen: On what screen we are doing it.
        """
        self.text_content()
        screen.blit(self.text_surface, (0, 0))
        screen.blit(self.text_surface_2, (0, 50))

class input_box():
    """
    Class for input box of the game.
    """
    def __init__(self):
        """
        Init font, and create surface.
        """
        self.myfont = pygame.font.SysFont('Comic Sans MS', 32)
        self.text = ''
        self.static_text = ''
        self.text_surface = self.myfont.render(self.text, False, (0, 0, 255))

    def writing(self, event):
        """
        Text generation on input box
        :param event: Key what had been pressed.
        :return: 1 if Enter was pressed, and 0 if anything else.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN and len(self.text) != 0:
                self.static_text = self.text
                self.text = ''
                return 1
            else:
                self.text += event.unicode
            self.text_surface = self.myfont.render(self.text, False, (0, 0, 255))
            return 0

    def return_HS(self):
        """
        Just creation of good looking hightscore result.
        :return: list [Score, Name]
        """
        main_data = [header.score, self.static_text]
        return main_data

    def show(self, screen):
        """
        Show input box on screen
        :param screen: Screen in witch we are showing
        """
        screen.blit(self.text_surface, (200, 40))

class Pop_out(pygame.sprite.Sprite):
    """
    Class for pop out window. Must show some text on screen and can be closed.
    For now it must show only HS on 600x600 png picture
    """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.dimension = 600
        self.image, self.rect = header.load_image("HS_frame.png", -1)
        self.rect.left, self.rect.top = 212, 84

    def show(self, screen):
        screen.blit(self.image, self.rect)


class HS_table():
    """
    Class for HighScore table
    """
    def __init__(self):
        """
        Init zero table with zero values and some font
        """
        self.HS_table = [['None', 0] for i in range(10)]
        self.myfont = pygame.font.SysFont('Comic Sans MS', 32)
        self.text = ''
        self.text_surface = None
        self.window = Pop_out()

    def new_data(self, new_HS):
        """
        Adding new data to the high score
        :param new_HS: New highscore in list format. [Score, Name]
        """
        temp = new_HS[:]
        for i in self.HS_table:
            print(i)
            if i[1] < temp[0]:
                i[0], temp[1] = temp[1], i[0]
                i[1], temp[0] = temp[0], i[1]
            else:
                pass

    def HS_write(self):
        """
        Write High socres in file.
        """
        with open('HS.dat', 'w') as f:
            for i in self.HS_table:
                for j in i:
                    f.write(str(j)+',')
                f.write('\n')

    def HS_read(self):
        """
        Read highscores from file to class.
        """
        field = []
        for line in open('HS.dat', 'r'):
            field.append([str(x) for x in line[:-2].split(',')])
        print(field)

        k = 0
        while k < 10:
            self.HS_table[k][0] = str(field[k][0])
            self.HS_table[k][1] = int(field[k][1])
            k += 1
        print(self.HS_table)

    def show(self, screen):
        """
        Show highscore on screen.
        """
        k = 0
        self.window.show(screen)
        for i in self.HS_table:
            self.text = i[0] + '------' + str(i[1])
            self.text_surface = self.myfont.render(self.text, False, (0, 0, 0))
            screen.blit(self.text_surface, (242, 114 + k*30))
            k += 1