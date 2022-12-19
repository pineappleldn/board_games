import pygame as pg


class Nones:
    def __init__(self):
        self.color = None
        self.queen = None
        self.x = None
        self.y = None

    def draw(self, screen):
        pass


class Hints:
    def __init__(self, x=0, y=0, r=9):
        self.x = x
        self.y = y
        self.r = r
        self.color = (202, 21, 26)

    def draw(self, screen):
        """
        Рисует хинт
        """
        pg.draw.circle(screen, self.color, (self.x, self.y), self.r)


class Chips:
    def __init__(self, image_white, image_black, crown, x=0, y=0, color='white'):
        """
        initiates instance of a chip on the board
        :param x: x-coordinate of the chip
        :param y: y-coordinate of the chip
        """
        self.color = color
        self.x = x
        self.y = y
        self.queen = False
        self.image_black = image_black
        self.image_white = image_white
        self.crown = crown

    def turn_over(self):
        """
        Переворачивает фишку (меняет цвет)
        """
        if self.color == 'white':
            self.color = 'black'
        else:
            self.color = 'white'

    def draw(self, screen):
        """
        Рисует фишку
        """
        if self.color == 'white':
            screen.blit(self.image_white, (self.x - self.image_white.get_width() // 2,
                                           self.y - self.image_white.get_height() // 2))
        else:
            screen.blit(self.image_black, (self.x - self.image_black.get_width() // 2,
                                           self.y - self.image_black.get_height() // 2))
        if self.queen:
            screen.blit(self.crown, (self.x - self.crown.get_width() // 2, self.y - self.crown.get_height() // 2))

    def get_color(self):
        if self.color == 'white':
            return 1
        elif self.color == 'black':
            return 2

    def make_queen(self):
        self.queen = True


class Board:
    def __init__(self, board_image, image_white, image_black, crown, matrix1=None, x=0, y=0, board_size=573):
        self.matrix = [[0 for i in range(8)] for j in range(8)]
        self.x = x
        self.y = y
        self.board_size = board_size
        self.board_image = board_image
        self.image_black = image_black
        self.image_white = image_white
        self.crown = crown
        for i in range(8):
            for j in range(8):
                x = int(self.x + self.board_size * (2 * j + 1) / 16)
                y = int(self.y + self.board_size * (2 * i + 1) / 16)
                if matrix1[i][j] == 1:
                    self.matrix[i][j] = Chips(image_white, image_black, crown, x, y, color='white')
                elif matrix1[i][j] == 2:
                    self.matrix[i][j] = Chips(image_white, image_black, crown, x, y, color='black')
                elif matrix1[i][j] == 3:
                    self.matrix[i][j] = Hints(x, y)
                elif matrix1[i][j] == 0:
                    self.matrix[i][j] = Nones()

    def draw(self, screen):
        """
        Функция рисует игровое поле.
        board_size - ширина и высота картинки игрового поля
        """
        screen.blit(self.board_image, (self.x - 38, self.y - 38))
        for i in range(8):
            for j in range(8):
                if self.matrix[i][j] != 0:
                    self.matrix[i][j].draw(screen)

    def check_on_board(self, event):
        if event.button == 1:
            if self.x <= event.pos[0] <= self.x + self.board_size:
                if self.y <= event.pos[1] <= self.y + self.board_size:
                    return 8 * (event.pos[0] - self.x - 1) // self.board_size,\
                           8 * (event.pos[1] - self.y - 1) // self.board_size
        return None, None


if __name__ == "__main__":
    '''
    тест файла 
    '''
    boardimage = pg.image.load('board.png')
    boardimage.set_colorkey((255, 255, 255))
    imagewhite = pg.image.load('whitechip.png')
    imagewhite.set_colorkey((255, 255, 255))
    imageblack = pg.image.load('blackchip.png')
    imageblack.set_colorkey((255, 255, 255))
    crownimage = pg.image.load('crown.png')
    crownimage.set_colorkey((255, 255, 255))
    mat = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 2, 0, 0, 0, 0, 0],
        [0, 0, 2, 0, 3, 0, 0, 0],
        [0, 0, 1, 1, 2, 3, 0, 0],
        [0, 0, 3, 2, 1, 0, 0, 0],
        [0, 0, 0, 3, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        ]
    board = Board(boardimage, imagewhite, imageblack, crownimage, mat, 53, 53)
    scr = pg.display.set_mode((700, 700))
    board.draw(scr)
    pg.display.update()
    clock = pg.time.Clock()
    finished = False

    while not finished:
        clock.tick(1)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                finished = True
    pg.quit()
