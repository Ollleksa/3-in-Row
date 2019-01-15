import random
import copy
import pygame

import header


class G_Token(pygame.sprite.Sprite):
    """
    Class for one token on field. So far only initiate tokens but maybe it will do something more
    """
    def __init__(self, location, t_type, active=False):
        """
        Load token of the concrete type in location.
        :param location: location of left top corner of token
        :param type: type of the token (color)
        :param active: if token is active should be True
        """
        if t_type != -1:
            pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
            if active:
                name = 'button_' + str(t_type) + 'A.png'
            else:
                name = 'button_' + str(t_type) + '.png'
            self.b_type = t_type
            self.image, self.rect = header.load_image(name, -1)
            self.rect.left, self.rect.top = location
        else:
            pygame.sprite.Sprite.__init__(self)
            name = 'cracked.png'
            self.b_type = t_type
            self.image, self.rect = header.load_image(name, -1)
            self.rect.left, self.rect.top = location
        self.rect.left += 192
        self.rect.top += 64



class G_Field():
    """
    It is main class for game - field 10x10 with many attributes. Can be divide into smaller classes in future
    """
    # i - column, j - row (but it is hard)
    def __init__(self, cont=False):
        """
        Initiate field for game.
        :param cont: If True - then load data for field from continue_data.dat. If False - create random field.
        """
        self.active_token = None
        if cont:
            self.token_types = header.data_from_cont()
        else:
            self.token_types = [[random.randrange(0, 6, 1) for i in range(10)] for j in range(10)]
        self.old_grid = copy.deepcopy(self.token_types)
        self.Gtoken = [[G_Token([i * 64, j * 64], self.token_types[j][i]) for i in range(10)] for j in range(10)]

    def save(self):
        """
        Save field in file
        """
        header.data_in_cont(self.token_types)

    def mouse_interactions(self, pos):
        """
        Calculation for mouse interaction with field. For now we can only click on token.
        :param pos: Should be position of the mouse. (x, y)
        :return: None. It changes global variable if moving is needed
        """
        # get what token is mouse above
        i = (pos[0] - 192) // 64
        j = (pos[1] - 64) // 64
        if i < 10 and j < 10:
            # if there was no active token before - activate it
            if self.active_token is None:
                self.active_token = tuple((i, j, self.token_types[j][i]))
                self.Gtoken[j][i] = G_Token([i * 64, j * 64], self.token_types[j][i], True)
            # if active token is present, then chek if it is on the one line
            elif i == self.active_token[0] or j == self.active_token[1]:
                self.Gtoken[self.active_token[1]][self.active_token[0]] = G_Token([self.active_token[0] * 64, self.active_token[1] * 64], self.active_token[2])
                #Here must be checking if change is even possible? Check if 3inRow is created...
                #print('Check point three: ', self.check_point_three(i,j,self.active_token[2]))
                if self.check_point_three(i, j, self.active_token[2]) or self.check_point_three(self.active_token[0], self.active_token[1], self.token_types[j][i]):
                    self.token_types[self.active_token[1]][self.active_token[0]], self.token_types[j][i] = self.token_types[j][i], self.active_token[2]
                    self.change_tokens()
                self.active_token = None
            else:
                self.active_token = None
        else:
            self.active_token = None

    def check_point_three(self, i, j, new_token_type):
        """
        Function checks if you new token create three in row condition.
        :param i: column of new token
        :param j: row of new token
        :param new_token_type: type of new token
        :return: return True or False if Three in row is created or not
        """
        try:
            if 0 < j < 9 and self.token_types[j-1][i] == self.token_types[j+1][i] == new_token_type:
                return True
            elif 0 < i < 9 and self.token_types[j][i-1] == self.token_types[j][i+1] == new_token_type:
                return True
            elif 1 < j and self.token_types[j-2][i] == self.token_types[j-1][i] == new_token_type:
                return True
            elif 8 > j and self.token_types[j+2][i] == self.token_types[j+1][i] == new_token_type:
                return True
            elif 1 < i and self.token_types[j][i-2] == self.token_types[j][i-1] == new_token_type:
                return True
            elif 8 > i and self.token_types[j][i+2] == self.token_types[j][i+1] == new_token_type:
                return True
            else:
                return False
        except:
            return False

    # calculation for changing tokens
    def change_tokens(self):
        """
        Function for changing two tokens. Calculation between to grids to check what changed.
        :return: Changing global variables to made a move.
        """
        tempi = []
        tempj = []
        for i in range(10):
            for j in range(10):
                if self.old_grid[j][i] != self.token_types[j][i]:
                    tempi.append(i)
                    tempj.append(j)

        if len(tempi) > 0:
            i1, i2 = tempi[0], tempi[1]
            j1, j2 = tempj[0], tempj[1]

            self.old_grid = copy.deepcopy(self.token_types)

            #moving speed
            if i1 - i2 != 0:
                m_time = 8 * (i1 - i2)
            elif j1 - j2 != 0:
                m_time = 8 * (j1 - j2)
            reverse = 1
            if m_time < 0:
                reverse = - 1
                m_time = -1 * m_time

            #print(m_time)
            header.two_token_moving = (i1, j1, i2, j2, m_time, reverse)
            header.anim_type = 'changing two'
            header.animation_in_progress = True
            header.turn_left -= 1

    # change two tokens (visual). One iteration
    def moving_two(self, i1, j1, i2, j2, reverse):
        """
        One iteration to moving two tokens.
        :param i1, j1, i2, j2: coordinates ow two tokens
        :param reverse: What direction tokens moves. Correction to create right moving
        """
        if i1 - i2 != 0:
            self.Gtoken[j1][i1].rect.left = self.Gtoken[j1][i1].rect.left - reverse * 8  # * (i1 - i2)
            self.Gtoken[j2][i2].rect.left = self.Gtoken[j2][i2].rect.left + reverse * 8  # * (i1 - i2)
        if j1 - j2 != 0:
            self.Gtoken[j1][i1].rect.top = self.Gtoken[j1][i1].rect.top - reverse * 8  # * (j1 - j2)
            self.Gtoken[j2][i2].rect.top = self.Gtoken[j2][i2].rect.top + reverse * 8  # * (j1 - j2)

    # change two tokens
    def moving_two_iter(self):
        """
        Moving iterations. With different conditions
        """
        if header.iterator_for_animation < header.two_token_moving[4]:
            self.moving_two(header.two_token_moving[0], header.two_token_moving[1], header.two_token_moving[2], header.two_token_moving[3], header.two_token_moving[5])
            header.iterator_for_animation += 1
        elif header.iterator_for_animation == header.two_token_moving[4]:
            header.iterator_for_animation = 0
            header.three_in_row = True
            header.two_token_moving = (-1, -1, -1, -1, 0, 1)
            header.animation_in_progress = False

    # show all in screen
    def show(self, screen):
        """
        Showing all grid on screen
        :param screen: Name of the screen
        """
        for i in range(10):
            for j in range(10):
                screen.blit(self.Gtoken[i][j].image, self.Gtoken[i][j].rect)

    def check_three(self):
        """
        Checking for three in row. Working cool. Make almost everything.
        If there was matching - start the diappearing/falling process.
        :return: True or False depending on is there three in row or not.
        """
        match = False
        matched_tokens = set()
        for i in range(10):
            j = 0
            temp = {(0, i)}
            n = 1
            while j < 9:
                if self.token_types[j][i] == self.token_types[j + 1][i]:
                    temp.add((j + 1, i))
                    n += 1
                elif n < 3:
                    temp = {(j+1, i)}
                    n = 1
                else:
                    matched_tokens = matched_tokens.union(temp)
                    match = True
                    temp = {(j + 1, i)}
                    n = 1
                j += 1

            if n >= 3:
                matched_tokens = matched_tokens.union(temp)
                match = True

        for j in range(10):
            i = 0
            temp = {(j, 0)}
            n = 1
            while i < 9:
                if self.token_types[j][i] == self.token_types[j][i+1]:
                    temp.add((j, i+1))
                    n += 1
                elif n < 3:
                    temp = {(j, i+1)}
                    n = 1
                else:
                    matched_tokens = matched_tokens.union(temp)
                    match = True
                    temp = {(j, i + 1)}
                    n = 1
                i += 1

            if n >= 3:
                matched_tokens = matched_tokens.union(temp)
                match = True
        # print('Matched: ', matched_tokens)

        # Falling process started
        if match:
            for k in matched_tokens:
                header.score += 1
                self.token_types[k[0]][k[1]] = -1
                header.anim_type = 'disappearing'
                header.animation_in_progress = True
            return True
        else:
            return False

    #This function make animation after disappearing of three in row tokens
    def disappearing(self):
        """
        One iteration of falling process. Depends hightly on iterator_for_animation global variable.
        """
        m_time = 8          # standart moving time (one grid in 8 iteration)
        # disappear for three iterations
        if header.iterator_for_animation == 0:
            self.Gtoken = [[G_Token([i * 64, j * 64], self.token_types[j][i]) for i in range(10)] for j in range(10)]
            header.iterator_for_animation += 1
        elif header.iterator_for_animation < 3: header.iterator_for_animation += 1
        # begin falling process by calculating time to fall and starting falling
        elif header.iterator_for_animation == 3:
            header.falling_ones = self.falling()
            header.iterator_for_animation += 1
            #print('Falling ones: ', loading.falling_ones)
            if len(header.falling_ones) == 0:
                header.iterator_for_animation = m_time + 3
            else:
                m_time = self.moving_speed()
                header.iterator_for_animation += 1
            self.falling_animation()
            print(m_time)
        elif header.iterator_for_animation < m_time + 3:
            self.falling_animation()
            header.iterator_for_animation += 1
        # fall is ended
        elif header.iterator_for_animation == m_time + 3:
            self.old_grid = copy.deepcopy(self.token_types)
            self.Gtoken = [[G_Token([i * 64, j * 64], self.token_types[j][i]) for i in range(10)] for j in range(10)]
            if len(header.falling_ones) == 0:
                header.falling_ones = []
                header.animation_in_progress = False
            header.iterator_for_animation = 0

    def falling(self):
        """
        Function to find what tockens is falling.
        We are going one column in time then go from bottom to up to find first missing token, then looking for next not missing. If it is - than it fall, if not then create random one and it mast fall.
        :return: list of coordinates of tokens that falls.
        """
        falling_ones = list()
        for i in range(10):
            j = 9
            is_falling = False
            while j >= 0:
                if self.token_types[j][i] == -1:
                    # if you go up to top and dont found any token
                    if j == 0:
                        self.token_types[j][i] = random.randrange(0, 6, 1)
                        self.Gtoken[j][i] = G_Token([i * 64, j * 64], self.token_types[j][i])
                    # if there is token up on free space
                    else:
                        is_falling = True
                        k = 1
                        while j-k >= 0:
                            if j-k == 0 and self.token_types[j-k][i] == -1:
                                self.token_types[j - k][i] = random.randrange(0, 6, 1)
                                self.Gtoken[j-k][i] = G_Token([i * 64, (j-k) * 64], self.token_types[j - k][i])

                            if self.token_types[j - k][i] != -1:
                                self.token_types[j][i] = self.token_types[j - k][i]
                                self.token_types[j - k][i] = -1
                                falling_ones.append(tuple((i, j - k, j)))
                                break
                            k += 1
                if is_falling: break
                j -= 1
        return falling_ones

    def falling_animation(self):
        """
        One iteration of falling animation
        """
        for col in header.falling_ones:
            if (header.iterator_for_animation - 3) < (col[2] - col[1]) * 8:
                self.Gtoken[col[1]][col[0]].rect.top = self.Gtoken[col[1]][col[0]].rect.top + 8 # * (col[1] - col[2])

    def moving_speed(self):
        """
        Function find moving time (not speed) for falling of tokens. It is the time of the longest fall.
        :return: Time of falling.
        """
        max = header.falling_ones[0][2] - header.falling_ones[0][1]
        for col in header.falling_ones:
            if col[2] - col[1] > max:
                max = col[2] - col[1]

        return 8 * max