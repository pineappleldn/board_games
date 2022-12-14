import pygame as pg
from Locals import *


class Chips:
    def __init__(self, x=0, y=0, row=0, col=0, r=30, color='white'):
        """
        initiates instance of a chip on the board
        :param x: x-coordinate of the chip
        :param y: y-coordinate of the chip
        :param r: radius of the chip
        """
        self.color = color
        self.x = x
        self.y = y
        self.row = row
        self.col = col
        self.r = r
        self.queen = False

    def turn_over(self):
        """
        Переворачивает фишку (меняет цвет) (подумать над анимацией градиента)
        """
        if self.color == 'white':
            self.color = 'black'
        else:
            self.color = 'white'

    def draw(self, screen):
        """
        Рисует фишку
        """
        pg.draw.circle(screen, self.color, (self.x, self.y), self.r)
        if self.queen:
            screen.blit(crown, (self.x - crown.get_width()//2, self.y - crown.get_height()//2))

    def get_color(self):
        if self.color == 'white':
            return 1
        elif self.color == 'black':
            return 2

    def make_queen(self):
        self.queen = True

    def __repr__(self):
        return str(self.color)


class Hints:
    def __init__(self, x=0, y=0, r=15):
        self.x = x
        self.y = y
        self.r = r
        self.color = (255, 0, 0, 200)

    def draw(self, screen):
        """
        Рисует хинт
        """
        pg.draw.circle(screen, self.color, (self.x, self.y), self.r)



class Board:
    board_size: int

    def __init__(self, matrix1=None, x=0, y=0, board_size=664):
        self.matrix = [[0 for i in range(8)] for j in range(8)]
        self.x = x
        self.y = y
        self.board_size = board_size
        self.image = pg.image.load('board.jpg')
        for i in range(8):
            for j in range(8):
                x = int(self.x + self.board_size * (2 * i + 1) / 16)
                y = int(self.y + self.board_size * (2 * j + 1) / 16)
                if matrix1[j][i] == 1:
                    self.matrix[j][i] = Chips(x, y, j, i, color='white')
                elif matrix1[j][i] == 2:
                    self.matrix[j][i] = Chips(x, y, j, i, color='black')
                elif matrix1[j][i] == 3:
                    self.matrix[j][i] = Hints(x, y)
        pass
    # noinspection PyUnresolvedReferences
    def draw(self, screen):
        """
        Функция рисует игровое поле.
        board_size - ширина и высота картинки игрового поля
        """
        screen.blit(self.image, (self.x, self.y))
        for i in range(8):
            for j in range(8):
                if self.matrix[i][j] != 0:
                    self.matrix[i][j].draw(screen)

    def check_on_board(self, event):
        if event.button == 1:
            if self.x <= event.pos[0] <= self.x + self.board_size:
                if self.y <= event.pos[1] <= self.y + self.board_size:
                    return 8*(event.pos[0] - self.x) // self.board_size, 8*(event.pos[1] - self.y) // self.board_size




