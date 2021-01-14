import pygame
from random import choice
import os
import sys
import sqlite3

con = sqlite3.connect('records.db')
cur = con.cursor()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)

    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [load_image("star.png")]
    for scale in (20, 25, 50):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx // 4, dy // 4]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = 0.01

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles(position):
    # количество создаваемых частиц
    particle_count = 25
    # возможные скорости
    numbers = range(-100, 100)
    for _ in range(particle_count):
        Particle(position, choice(numbers) / 10, choice(numbers) / 10)


all_sprites = pygame.sprite.Group()


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[[0, 0]] * width for _ in range(height)]
        self.n = 0
        self.score = 0
        self.second = 6 #choice([1, 2, 3, 4, 5, 6, 7])
        self.interval = 2
        self.game = False
        self.pause = False
        self.left = 10
        self.top = 10
        self.cell_size = 26
        self.lines = 0
        self.conservation = False

    def new_game(self):
        self.board = [[[0, 0]] * width for _ in range(height)]

        if not (self.game):
            self.score = 0
            self.lines = 0
            self.game = True
        else:

            self.conservation = False
            self.game = False

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.second = None

    def fall(self):
        arr = [[[0, 0]] * self.width for _ in range(self.height)]
        stopp = False

        for i in range(self.width):
            for j in range(self.height):

                if self.board[j][i][0]:
                    if self.board[j][i][1]:

                        if j < self.height - 2:
                            if self.board[j + 2][i][0] and not (self.board[j + 2][i][1]):
                                stopp = True
                        if j < self.height - 1:
                            arr[j + 1][i] = self.board[j][i]
                            if j + 1 == self.height - 1:
                                stopp = True
                    else:
                        arr[j][i] = self.board[j][i]

        if stopp:
            self.stop()
        self.board = arr[::]
        if self.game:
            self.new_deration()

    def leftt(self):

        new_arr = [[[0, 0]] * self.width for _ in range(self.height)]
        end = False
        for i in range(self.width):
            for j in range(self.height):
                if self.board[j][i][1]:
                    if i == 0:
                        end = True

                    if i + 1 < board.width and self.board[j][i - 1][0] and not (self.board[j][i - 1][1]):
                        end = True

        if not (end):
            for i in range(board.width):
                for j in range(board.height):

                    if self.board[j][i][1]:
                        new_arr[j][i - 1] = self.board[j][i]
                    if self.board[j][i][0] and not (self.board[j][i][1]):
                        new_arr[j][i] = self.board[j][i]
            stopp = False
            for i in range(board.width):
                for j in range(board.height):
                    if new_arr[j][i][0]:
                        if new_arr[j][i][1]:
                            if j < board.height - 2:
                                if new_arr[j + 1][i][0] and not (new_arr[j + 1][i][1]):
                                    stopp = True
            if stopp:
                self.stop()
            self.board = new_arr[::]

    def right(self):
        new_arr = [[[0, 0]] * self.width for _ in range(self.height)]
        end = False
        for i in range(self.width):
            for j in range(self.height):

                if self.board[j][i][1]:

                    if i == board.width - 1:
                        end = True

                    if i + 1 < self.width and self.board[j][i + 1][0] and not (self.board[j][i + 1][1]):
                        end = True
        if not (end):
            for i in range(self.width):
                for j in range(self.height):

                    if self.board[j][i][1] and i < self.width - 1:
                        new_arr[j][i + 1] = self.board[j][i]
                    if self.board[j][i][0] and not (self.board[j][i][1]):
                        new_arr[j][i] = self.board[j][i]
            stopp = False
            for i in range(self.width):
                for j in range(self.height):
                    if new_arr[j][i][0]:
                        if new_arr[j][i][1]:
                            if j < self.height - 2:
                                if new_arr[j + 1][i][0] and not (new_arr[j + 1][i][1]):
                                    stopp = True
            if stopp:
                self.stop()
            self.board = new_arr[::]
        if self.game:
            self.new_deration()

    def left_down(self):
        total = []
        for i in range(self.width):
            for j in range(self.height):
                if self.board[j][i][1]:
                    total.append([i, j])
        if total:
            arr = sorted(total, key=lambda x: (x[0], -x[1]))[0]
            return sorted(total, key=lambda x: (x[0], -x[1]))[0]

    def turn(self):
        if self.left_down() is None:
            return
        x, y = self.left_down()

        if self.board[y][x][0] == 1:
            if self.board[y - 1][x][1] and x - 1 != -1:

                if self.board[y + 1][x] == self.board[y + 1][x - 1] == [0, 0]:
                    self.board[y - 1][x] = [0, 0]
                    self.board[y + 1][x + 1] = [0, 0]
                    self.board[y + 1][x] = [1, 1]
                    self.board[y + 1][x - 1] = [1, 1]
                    if (self.board[y + 2][x][0] and not (self.board[y + 2][x][1])) or (
                            self.board[y + 2][x - 1][0] and not (self.board[y + 2][x - 1][1])):
                        self.stop()

            elif not (self.board[y - 1][x][1]):

                if self.board[y - 2][x + 1] == self.board[y][x + 2] == [0, 0]:
                    self.board[y][x] = [0, 0]
                    self.board[y][x + 1] = [0, 0]
                    self.board[y - 2][x + 1] = [1, 1]
                    self.board[y][x + 2] = [1, 1]
                    if self.board[y + 1][x + 2][0] and not (self.board[y + 1][x + 2][1]):
                        self.stop()
        if self.board[y][x][0] == 2:

            if self.board[y - 1][x][0] and self.n == 0 and x != 0 and x + 2 in range(self.width):
                if self.board[y - 2][x + 2] == self.board[y - 2][x + 1] == self.board[y - 2][x - 1] == [0, 0]:

                    self.board[y][x] = [0, 0]
                    self.board[y - 1][x] = [0, 0]
                    self.board[y - 3][x] = [0, 0]
                    self.board[y - 2][x - 1] = [2, 1]
                    self.board[y - 2][x + 1] = [2, 1]
                    self.board[y - 2][x + 2] = [2, 1]
                    self.n = 1
                    if self.board[y - 1][x + 2][0] and not (self.board[y - 1][x + 2][1]):
                        self.stop()
                    if self.board[y - 1][x - 1][0] and not (self.board[y - 1][x - 1][1]):
                        self.stop()
            elif self.board[y - 1][x][0] and self.n == 1 and x > 1 and x + 1 in range(self.width):
                if self.board[y - 2][x - 1] == self.board[y - 2][x - 2] == self.board[y - 2][x + 1] == [0, 0]:
                    self.n = 0

                    self.board[y][x] = [0, 0]
                    self.board[y - 1][x] = [0, 0]
                    self.board[y - 3][x] = [0, 0]
                    self.board[y - 2][x - 1] = [2, 1]
                    self.board[y - 2][x - 2] = [2, 1]
                    self.board[y - 2][x + 1] = [2, 1]
            elif x + 1 in range(self.width) and self.board[y][x + 1][0] and self.n == 1 and y + 2 in range(self.height):
                if self.board[y - 1][x + 2] == self.board[y + 1][x + 2] == self.board[y + 2][x + 2] == [0, 0]:

                    self.board[y][x] = [0, 0]
                    self.board[y][x + 1] = [0, 0]
                    self.board[y][x + 3] = [0, 0]
                    self.board[y - 1][x + 2] = [2, 1]
                    self.board[y + 1][x + 2] = [2, 1]
                    self.board[y + 2][x + 2] = [2, 1]

                    if y + 2 == self.height - 1:
                        self.stop()
                    if y + 3 < self.height:
                        if self.board[y + 3][x + 2][0] and not (self.board[y + 3][x + 2][1]):
                            self.stop()



            elif x + 1 in range(self.width) and self.board[y][x + 1][0] and self.n == 0 and y + 2 in range(self.height):
                if self.board[y - 1][x + 1] == self.board[y + 1][x + 1] == self.board[y + 2][x + 1] == [0, 0]:

                    self.board[y][x] = [0, 0]
                    self.board[y][x + 2] = [0, 0]
                    self.board[y][x + 3] = [0, 0]
                    self.board[y - 1][x + 1] = [2, 1]
                    self.board[y + 1][x + 1] = [2, 1]
                    self.board[y + 2][x + 1] = [2, 1]
                    if y + 2 == self.height - 1:
                        self.stop()
                    if y + 3 == self.height or (self.board[y + 3][x + 2][0] and not (self.board[y + 3][x + 2][1])):
                        self.stop()
        if self.board[y][x][0] == 3:
            if self.board[y - 1][x + 1][0] == 3:

                if x < self.width - 2 and self.board[y][x + 1] == self.board[y][x + 2] == [0, 0]:
                    self.board[y][x] = [0, 0]
                    self.board[y - 2][x + 1] = [0, 0]
                    self.board[y][x + 1] = [3, 1]
                    self.board[y][x + 2] = [3, 1]
                    if self.board[y + 1][x + 2][0] and not (self.board[y + 1][x + 2][1]):
                        self.stop()

            elif self.board[y][x + 1][0] == 3:

                if y < self.height - 3 and self.board[y + 1][x] == self.board[y + 2][x] == [0, 0]:

                    self.board[y][x] = [0, 0]
                    self.board[y + 1][x + 2] = [0, 0]
                    self.board[y + 1][x] = [3, 1]
                    self.board[y + 2][x] = [3, 1]
                    if self.board[y + 3][x][0] and not (self.board[y + 3][x][1]):
                        self.stop()
        if self.board[y][x][0] == 5:
            if x + 1 < self.width and self.board[y - 1][x] == [5, 1] == self.board[y - 2][x + 1]:

                if x + 2 < self.width and self.board[y - 2][x + 2] == self.board[y - 1][x + 2] == [0, 0]:
                    self.board[y][x] = [0, 0]
                    self.board[y - 1][x] = [0, 0]
                    self.board[y - 2][x + 2] = [5, 1]
                    self.board[y - 1][x + 2] = [5, 1]
                    if self.board[y][x + 2][0] and not (self.board[y][x + 2][1]):
                        self.stop()
            elif x + 2 < self.width and self.board[y][x + 1] == [5, 1] == self.board[y + 1][x + 2]:

                if self.board[y + 2][x + 2] == self.board[y + 2][x + 1] == [0, 0]:
                    self.board[y][x] = [0, 0]
                    self.board[y][x + 1] = [0, 0]
                    self.board[y + 2][x + 2] = [5, 1]
                    self.board[y + 2][x + 1] = [5, 1]
                    if self.board[y + 3][x + 2][0] and not (self.board[y + 3][x + 2][1]):
                        self.stop()
                    if self.board[y + 3][x + 1][0] and not (self.board[y + 3][x + 1][1]):
                        self.stop()
            elif x > 0 and self.board[y - 2][x + 1] == [5, 1]:
                if self.board[y][x - 1] == self.board[y - 1][x - 1] == [0, 0]:
                    self.board[y - 1][x + 1] = [0, 0]
                    self.board[y - 2][x + 1] = [0, 0]
                    self.board[y][x - 1] = [5, 1]
                    self.board[y - 1][x - 1] = [5, 1]
                    if self.board[y + 1][x - 1][0] and not (self.board[y + 1][x - 1][1]):
                        self.stop()
            elif self.board[y - 1][x] == [5, 1] == self.board[y][x + 2]:

                if self.board[y - 2][x] == self.board[y - 2][x + 1] == [0, 0]:
                    self.board[y - 2][x] = [5, 1]
                    self.board[y - 2][x + 1] = [5, 1]
                    self.board[y][x + 1] = [0, 0]
                    self.board[y][x + 2] = [0, 0]

        if self.board[y][x][0] == 6:
            if x > 0 and x + 1 < self.width and self.board[y][x + 1] == self.board[y + 1][x + 1] \
                    == self.board[y][x + 1] == [6, 1]:

                if self.board[y + 2][x] == self.board[y + 2][x - 1] == [0, 0]:
                    self.board[y][x] = [0, 0]
                    self.board[y][x + 1] = [0, 0]
                    self.board[y + 2][x] = [6, 1]
                    self.board[y + 2][x - 1] = [6, 1]

                    if self.board[y + 3][x - 1][0] and not (self.board[y + 3][x - 1][1]):
                        self.stop()
            elif x < 8 and self.board[y][x] == self.board[y][x + 1] == self.board[y][x + 2] == [6, 1]:

                if self.board[y - 1][x] == self.board[y - 2][x] == [0, 0]:
                    self.board[y][x + 2] = [0, 0]
                    self.board[y - 1][x + 2] = [0, 0]
                    self.board[y - 1][x] = [6, 1]
                    self.board[y - 2][x] = [6, 1]
            elif x < 8 and self.board[y][x] == self.board[y - 1][x] == self.board[y - 2][x] == [6, 1]:

                if self.board[y - 2][x + 1] == self.board[y - 2][x + 2] == [0, 0]:
                    self.board[y][x] = [0, 0]
                    self.board[y][x + 1] = [0, 0]
                    self.board[y - 2][x + 1] = [6, 1]
                    self.board[y - 2][x + 2] = [6, 1]
                    if self.board[y - 1][x + 2][0] and not (self.board[y - 1][x + 2][1]):
                        self.stop()
            elif self.board[y - 1][x] == self.board[y - 1][x + 1] == self.board[y - 1][x + 2] == [6, 1]:
                if self.board[y][x + 2] == self.board[y + 1][x + 2] == [0, 0]:
                    self.board[y][x] = [0, 0]
                    self.board[y - 1][x] = [0, 0]
                    self.board[y][x + 2] = [6, 1]
                    self.board[y + 1][x + 2] = [6, 1]

                    if y + 2 == self.height or (self.board[y + 2][x + 2][0] and not (self.board[y + 2][x + 2][1])):
                        self.stop()
        if self.board[y][x][0] == 7:
            if y > 1 and x + 2 in range(self.width) and self.board[y][x + 1] == self.board[y][x + 2] == \
                    self.board[y - 1][x + 1] == [7, 1]:

                if self.board[y - 1][x] == self.board[y - 2][x] == [0, 0]:
                    self.board[y][x + 1] = [0, 0]
                    self.board[y][x + 2] = [0, 0]
                    self.board[y - 1][x] = [7, 1]
                    self.board[y - 2][x] = [7, 1]


            elif x + 2 < self.width and self.board[y - 1][x] == self.board[y - 2][x] == [7, 1]:
                if self.board[y - 2][x + 1] == self.board[y - 2][x + 2] == [0, 0]:
                    self.board[y][x] = [0, 0]
                    self.board[y - 1][x] = [0, 0]
                    self.board[y - 2][x + 1] = [7, 1]
                    self.board[y - 2][x + 2] = [7, 1]
                    if self.board[y - 1][x + 2][0] and not (self.board[y - 1][x + 2][1]):
                        self.stop()

            elif x + 2 < self.width and self.board[y][x + 2] == self.board[y + 1][x + 1] == [7, 1]:

                if self.board[y + 1][x + 2] == self.board[y + 2][x + 2] == [0, 0]:
                    self.board[y][x] = [0, 0]
                    self.board[y][x + 1] = [0, 0]
                    self.board[y + 1][x + 2] = [7, 1]
                    self.board[y + 2][x + 2] = [7, 1]
                    if self.board[y + 3][x + 2][0] and not (self.board[y + 3][x + 2][1]):
                        self.stop()

            elif x > 0 and self.board[y][x + 1] == self.board[y - 1][x + 1] == self.board[y + 1][x + 1]:

                if self.board[y + 1][x - 1] == self.board[y + 1][x] == [0, 0]:
                    self.board[y - 1][x + 1] = [0, 0]
                    self.board[y][x + 1] = [0, 0]
                    self.board[y + 1][x - 1] = [7, 1]
                    self.board[y + 1][x] = [7, 1]
                    if (self.board[y + 2][x][0] and not (self.board[y + 2][x][1])) or (
                            self.board[y + 2][x - 1][0] and not (self.board[y + 2][x - 1][1])):
                        self.stop()

    def render(self, screen):
        screen.blit(image, (-500, 0))

        font = pygame.font.Font(None, 30)
        text = font.render('Счёт: ' + str(self.score), True, (255, 255, 255))
        screen.blit(text, (300, 170))
        font = pygame.font.Font(None, 30)
        text = font.render('Линии: ' + str(self.lines), True, (255, 255, 255))
        screen.blit(text, (300, 200))
        pygame.draw.rect(screen, 'white',
                         (self.left, self.top,
                          (self.cell_size + self.interval) * 10, (self.cell_size + self.interval) * 20), 1)
        for i in range(self.width):
            for j in range(self.height):

                if self.board[j][i][0] == 1:
                    pygame.draw.rect(screen, 'red',

                                     (i * (self.cell_size + self.interval) + self.left + 2,
                                      j * (self.cell_size + self.interval) + self.top + 2,
                                      self.cell_size - 4, self.cell_size - 4))
                if self.board[j][i][0] == 2:
                    pygame.draw.rect(screen, 'green',
                                     (i * (self.cell_size + self.interval) + self.left + 2,
                                      j * (self.cell_size + self.interval) + self.top + 2,
                                      self.cell_size - 4, self.cell_size - 4))
                if self.board[j][i][0] == 3:
                    pygame.draw.rect(screen, 'yellow',
                                     (i * (self.cell_size + self.interval) + self.left + 2,
                                      j * (self.cell_size + self.interval) + self.top + 2,
                                      self.cell_size - 4, self.cell_size - 4))
                if self.board[j][i][0] == 4:
                    pygame.draw.rect(screen, 'blue',
                                     (i * (self.cell_size + self.interval) + self.left + 2,
                                      j * (self.cell_size + self.interval) + self.top + 2,
                                      self.cell_size - 4, self.cell_size - 4))
                if self.board[j][i][0] == 5:
                    pygame.draw.rect(screen, 'pink',
                                     (i * (self.cell_size + self.interval) + self.left + 2,
                                      j * (self.cell_size + self.interval) + self.top + 2,
                                      self.cell_size - 4, self.cell_size - 4))
                if self.board[j][i][0] == 6:
                    pygame.draw.rect(screen, 'white',
                                     (i * (self.cell_size + self.interval) + self.left + 2,
                                      j * (self.cell_size + self.interval) + self.top + 2,
                                      self.cell_size - 4, self.cell_size - 4))
                if self.board[j][i][0] == 7:
                    pygame.draw.rect(screen, 'grey',
                                     (i * (self.cell_size + self.interval) + self.left + 2,
                                      j * (self.cell_size + self.interval) + self.top + 2,
                                      self.cell_size - 4, self.cell_size - 4))
        font = pygame.font.Font(None, 40)
        text = font.render('МЕНЮ', True, (255, 255, 255))
        screen.blit(text, (300, 500))

        if self.pause:
            font = pygame.font.Font(None, 40)
            text = font.render('ПАУЗА', True, (255, 0, 0))
            screen.blit(text, (300, 400))
        else:
            font = pygame.font.Font(None, 40)
            text = font.render('ПАУЗА', True, (0, 255, 0))
            screen.blit(text, (300, 400))
        if self.second == 2:
            arr = [[0, 1, 0, 0],
                   [0, 1, 0, 0],
                   [0, 1, 0, 0],
                   [0, 1, 0, 0],
                   ]
        if self.second == 1:
            arr = [[1, 0, 0, 0],
                   [1, 1, 0, 0],
                   [0, 1, 0, 0],
                   [0, 0, 0, 0],
                   ]
        if self.second == 3:
            arr = [[0, 1, 0, 0],
                   [1, 1, 0, 0],
                   [1, 0, 0, 0],
                   [0, 0, 0, 0],
                   ]
        if self.second == 4:
            arr = [[1, 1, 0, 0],
                   [1, 1, 0, 0],
                   [0, 0, 0, 0],
                   [0, 0, 0, 0],
                   ]
        if self.second == 5:
            arr = [[1, 1, 0, 0],
                   [1, 0, 0, 0],
                   [1, 0, 0, 0],
                   [0, 0, 0, 0],
                   ]
        if self.second == 6:
            arr = [[1, 1, 0, 0],
                   [0, 1, 0, 0],
                   [0, 1, 0, 0],
                   [0, 0, 0, 0],
                   ]
        if self.second == 7:
            arr = [[0, 1, 0, 0],
                   [1, 1, 1, 0],
                   [0, 0, 0, 0],
                   [0, 0, 0, 0],
                   ]
        for i in range(4):
            for j in range(4):
                if arr[j][i]:
                    pygame.draw.rect(screen, 'red',
                                     (i * (self.cell_size + self.interval) + 300 + 2,
                                      j * (self.cell_size + self.interval) + self.top + 2,
                                      self.cell_size - 4, self.cell_size - 4))

    def loss(self):
        if any([bool(e[0]) for e in self.board[0]]):
            self.game = False
            self.conservation = False

    def stop(self):

        for i in range(self.width):
            for j in range(self.height):
                self.board[j][i][1] = 0
        self.loss()

    def new_row(self):
        k = 0
        for i in range(self.height):
            row = True
            for j in range(self.width):
                if self.board[i][j] == [0, 0]:
                    row = False
            if row:
                arr = self.board[::]
                del arr[i]
                k += 1
                arr.insert(0, [[0, 0] for el in range(self.width)])
                self.board = arr[::]
        self.score += k * 100
        self.lines += k

    def menu(self):
        font = pygame.font.Font(None, 50)
        text = font.render('ИГРАТЬ', True, (255, 255, 255))
        screen.blit(text, (150, 230))

        font = pygame.font.Font(None, 50)
        text = font.render('УПРАВЛЕНИЕ', True, (255, 255, 255))
        screen.blit(text, (150, 280))

        font = pygame.font.Font(None, 50)
        text = font.render('РЕКОРДЫ', True, (255, 255, 255))
        screen.blit(text, (150, 330))

        font = pygame.font.Font(None, 50)
        text = font.render('О ПРОЕКТЕ', True, (255, 255, 255))
        screen.blit(text, (150, 380))

        font = pygame.font.Font(None, 50)
        text = font.render('ВЫХОД', True, (255, 255, 255))
        screen.blit(text, (150, 430))
        self.game = False

    def new_deration(self):
        new = True
        for i in range(self.width):
            for j in range(self.height):
                if self.board[j][i][1]:
                    new = False
        if new:

            first = self.second
            self.second = choice([1, 2, 3, 4, 5, 6, 7])

            if first == 1:
                if self.board[0][4] == self.board[1][4] == self.board[1][5] == self.board[2][5] == [0, 0]:
                    self.board[0][4] = [1, 1]
                    self.board[1][4] = [1, 1]
                    self.board[1][5] = [1, 1]
                    self.board[2][5] = [1, 1]
                else:
                    self.game = False
            if first == 2:
                if self.board[0][5] == self.board[1][5] == self.board[3][5] == self.board[2][5]:
                    self.board[0][5] = [2, 1]
                    self.board[1][5] = [2, 1]
                    self.board[3][5] = [2, 1]
                    self.board[2][5] = [2, 1]
                else:
                    self.game = False
            if first == 3:
                if self.board[0][6] == self.board[1][6] == self.board[1][5] == self.board[2][5]:
                    self.board[0][6] = [3, 1]
                    self.board[1][6] = [3, 1]
                    self.board[1][5] = [3, 1]
                    self.board[2][5] = [3, 1]
                else:
                    self.game = False
            if first == 4:
                if self.board[0][6] == [0, 0] == self.board[0][5] == self.board[1][5] == self.board[1][6]:
                    self.board[0][6] = [4, 1]
                    self.board[0][5] = [4, 1]
                    self.board[1][5] = [4, 1]
                    self.board[1][6] = [4, 1]
                else:
                    self.game = False
            if first == 5:
                if [0, 0] == self.board[0][5] == self.board[0][6] == self.board[1][5] == self.board[2][5]:
                    self.board[0][5] = [5, 1]
                    self.board[0][6] = [5, 1]
                    self.board[1][5] = [5, 1]
                    self.board[2][5] = [5, 1]
                else:
                    self.game = False
            if first == 6:
                if self.board[0][5] == self.board[0][6] == self.board[1][6] == self.board[2][6] == [0, 0]:
                    self.board[0][5] = [6, 1]
                    self.board[0][6] = [6, 1]
                    self.board[1][6] = [6, 1]
                    self.board[2][6] = [6, 1]
                else:

                    self.game = False
            if first == 7:
                if [0, 0] == self.board[0][5] == self.board[1][6] == self.board[1][5] == self.board[1][4]:
                    self.board[0][5] = [7, 1]
                    self.board[1][6] = [7, 1]
                    self.board[1][5] = [7, 1]
                    self.board[1][4] = [7, 1]
                else:
                    self.game = False
            self.new_row()

    def authorss(self):
        font = pygame.font.Font(None, 30)
        text = font.render('Программирование Чубаков Степан', True, (255, 255, 255))
        screen.blit(text, (60, 170))

        font = pygame.font.Font(None, 30)
        text = font.render('Графика и дизайн Чубаков Степан', True, (255, 255, 255))
        screen.blit(text, (60, 220))

        font = pygame.font.Font(None, 30)
        text = font.render('Звуки и музыка Чубаков Степан', True, (255, 255, 255))
        screen.blit(text, (60, 270))

        font = pygame.font.Font(None, 30)
        text = font.render('Тестирование Чубаков Степан', True, (255, 255, 255))
        screen.blit(text, (60, 320))
        font = pygame.font.Font(None, 40)
        text = font.render('МЕНЮ', True, (255, 255, 255))
        screen.blit(text, (300, 500))

    def managementt(self):
        font = pygame.font.Font(None, 25)
        text = font.render('ПРОБЕЛ - поворот фигуры', True, (255, 255, 255))
        screen.blit(text, (60, 170))

        font = pygame.font.Font(None, 25)
        text = font.render('СТРЕЛКА ВЛЕВО - сдвиг фигуры влево', True, (255, 255, 255))
        screen.blit(text, (60, 220))

        font = pygame.font.Font(None, 25)
        text = font.render('СТРЕЛКА ВПРАВО - сдвиг фигуры вправо', True, (255, 255, 255))
        screen.blit(text, (60, 270))

        font = pygame.font.Font(None, 25)
        text = font.render('СТРЕЛКА ВНИЗ - ускорение', True, (255, 255, 255))
        screen.blit(text, (60, 320))

        font = pygame.font.Font(None, 40)
        text = font.render('МЕНЮ', True, (255, 255, 255))
        screen.blit(text, (300, 500))

    def recordss(self):
        font = pygame.font.Font(None, 40)
        text = font.render('МЕНЮ', True, (255, 255, 255))
        screen.blit(text, (300, 500))

        result = cur.execute("""SELECT name,score FROM records""").fetchall()
        result = sorted(result, key=lambda x: -x[1])
        for i in range(min(len(result), 8)):
            font = pygame.font.Font(None, 40)
            text = font.render(result[i][0] + ' - ' + str(result[i][1]), True, (255, 255, 255))
            screen.blit(text, (100, 170 + 50 * i))

    def soxr(self, name):
        result = cur.execute("""INSERT INTO records(name,score) VALUES(?,?)""", (name, self.score,))  ###.fetchall()
        con.commit()


if __name__ == '__main__':
    pygame.init()
    size = width, height = 450, 600
    screen_rect = (0, 0, width, height)
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption('ЗВЁЗДНЫЙ ТЕТРИС')

    board = Board(10, 20)
    running = True
    clock = pygame.time.Clock()
    down = 0
    image = load_image("space.jpg")

    menu = True
    right = False
    leftt = False
    ll = 0
    rr = 0
    speed = 0.7
    authors = False
    management = False
    records = False
    pygame.mixer.music.load('music.mp3')
    pygame.mixer.music.play(loops=-1)

    font = pygame.font.Font(None, 32)
    input_box = pygame.Rect(100, 100, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    name = ''
    n = 0
    while running:
        if n != board.score and board.game:
            n = board.score

            create_particles((145, 285))
        if leftt and ll > 0.2:
            board.leftt()
            ll -= 0.2
        if right and rr > 0.2:
            board.right()
            rr -= 0.2

        tem = clock.tick() / 1000

        down += tem
        if right:
            rr += tem
        if leftt:
            ll += tem

        if down > speed:
            if not (board.pause):
                board.fall()
            down -= speed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if active and not (board.conservation):
                    if event.key == pygame.K_RETURN:

                        board.soxr(name)
                        active = False
                        board.conservation = True
                        name = ''
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        if len(name) < 20:
                            name += event.unicode
                if event.key == 32:
                    if not (board.pause):
                        board.turn()
                if event.key == 1073741903:
                    if not (board.pause):
                        right = True
                        board.right()

                if event.key == 1073741904:
                    if not (board.pause):
                        leftt = True
                        board.leftt()
                if event.key == 1073741905:
                    speed = 0.1

            if event.type == pygame.KEYUP:
                if event.key == 1073741905:
                    speed = 0.7
                if event.key == 1073741903:
                    rr = 0
                    right = False
                if event.key == 1073741904:
                    leftt = False
                    ll = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not (board.game):
                    if input_box.collidepoint(event.pos):

                        active = not active
                    else:
                        active = False
                    color = color_active if active else color_inactive
                x, y = event.pos

                if menu:
                    n = 0
                    if 290 > x > 150 and 262 > y > 230:
                        board.new_game()
                        menu = False
                    if 290 > x > 150 and 450 > y > 430:
                        running = False

                    if 350 > x > 150 and 410 > y > 380:
                        authors = True
                        menu = False

                    if 400 > x > 150 and 310 > y > 282:
                        management = True
                        menu = False
                    if 335 > x > 150 and 360 > y > 332:
                        records = True
                        menu = False
                else:

                    if 400 > x > 300 and 430 > y > 390:
                        if not (board.pause):
                            board.pause = True
                        else:
                            board.pause = False
                    if 400 > x > 300 and 530 > y > 490:
                        menu = True
                        authors = False
                        management = False
                        records = False

        board.render(screen)
        if not (board.game):
            screen.blit(image, (-500, 0))

            txt_surface = font.render(name, True, color)

            width = max(200, txt_surface.get_width() + 10)
            input_box.w = width

            screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))

            pygame.draw.rect(screen, color, input_box, 2)
            font = pygame.font.Font(None, 40)
            text = font.render('Вы набрали ' + str(board.score) + ' очков', True, (255, 255, 255))
            screen.blit(text, (100, 200))

            font = pygame.font.Font(None, 20)
            text = font.render('ВВЕДИТЕ СВОЁ ИМЯ И НАЖМИТЕ Enter', True, (255, 255, 255))
            screen.blit(text, (100, 80))

            font = pygame.font.Font(None, 40)
            text = font.render('МЕНЮ', True, (255, 255, 255))
            screen.blit(text, (300, 500))
        if menu:
            screen.blit(image, (-50, 0))
            board.menu()
        if authors:
            screen.blit(image, (-50, 0))
            board.authorss()
        if management:
            screen.blit(image, (-50, 0))
            board.managementt()
        if records:
            screen.blit(image, (-50, 0))
            board.recordss()

        all_sprites.update()

        all_sprites.draw(screen)

        pygame.display.flip()
    pygame.quit()
