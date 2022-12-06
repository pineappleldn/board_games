import pygame as pg


class Chips:
    def __init__(self, screen):
        self.color = 'white'
        self.screen = screen
        self.x = 0
        self.y = 0
        self.r = 30

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


class Board:
    def __init__(self, screen):
        self.matrix = []
        self.screen = screen
        self.x = 0
        self.y = 0
        self.board_size = 0
        self.square_size = 0

    def draw_board(self, screen):
        """
        Функция рисует игровое поле.
        board_size - ширина и высота картинки игрового поля
        """
        board = pg.image.load('board.jpg')
        screen.blit(board, (screen.get_width() - self.board_size, (screen.get_height() - self.board_size) / 2))

    def draw_cheaps(self, screen):
        for x in range(8):
            for y in range(8):
                chip = Chips(screen)
                hint = Hints(screen)
                chip.x = screen.get_width() - board_size + 83 * (2 * x + 1) / 2
                chip.y = (screen.get_height() - board_size) / 2 + 83 * (2 * y + 1) / 2
                hint.x = screen.get_width() - board_size + 83 * (2 * x + 1) / 2
                hint.y = (screen.get_height() - board_size) / 2 + 83 * (2 * y + 1) / 2
                if matrix[x][y] == 1:
                    chip.color = 'white'
                    chip.draw()
                elif matrix[x][y] == 2:
                    chip.color = 'black'
                    chip.draw()
                elif matrix[x][y] == 3:
                    hint.draw()

