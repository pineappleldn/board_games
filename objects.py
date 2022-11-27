import pygame as pg


class Chips:
    def __init__(self, screen):
        self.color = 'white'
        self.screen = screen
        self.x = 0
        self.y = 0
        self.r = 35

    def turn_over(self):
        """
        Переворачивает фишку (меняет цвет) (подумать над анимацией градиента)
        """
        if self.color == 'white':
            self.color = 'black'
        else:
            self.color = 'white'

    def draw(self):
        """
        Рисует фишку
        """
        pg.draw.circle(self.screen, self.color, (self.x, self.y), self.r)
        pg.draw.circle(self.screen, 'black', (self.x, self.y), self.r, 1)


class Hints:
    def __init__(self, screen):
        self.screen = screen
        self.x = 0
        self.y = 0
        self.r = 15
        self.color = (255, 0, 0, 200)

    def draw(self):
        """
        Рисует хинт
        """
        pg.draw.circle(self.screen, self.color, (self.x, self.y), self.r)


class Turn:
    def __init__(self):
        self.state = 0
        self.count = 0

    def turn_turn(self):
        """
        передает ход от одного игрока к другому
        """
        if self.state == 0:
            self.state = 1
        else:
            self.state = 0

