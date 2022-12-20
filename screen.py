from reversi_logic import *
from russian_checkers_logic import *
from anyboard import *
pg.font.init()


class Background:
    def __init__(self, image_back, image_rules, board_image,
                 image_white, image_black, crown, matrix1=None, matrix2=None):
        self.image = image_back
        self.image_rules = image_rules
        self.reversi = ReversiBoard(board_image, image_white, image_black, crown, matrix1, 538, 88)
        self.checkers = CheckerBoard(board_image, image_white, image_black, crown, matrix2, 538, 88)
        self.active_board = Nones()
        self.mode = 4

    def set_mode(self, mode):
        """
        устанавливает режим экрана
        :param mode: 1 - игра реверси, 2 - игра шашки, 3 - игра поддавки, 4 - экран главного меню, 5 - конец игры
        """
        self.mode = mode
        if self.mode == 1:
            self.active_board = self.reversi
        elif self.mode == 2:
            self.active_board = self.checkers
        elif self.mode == 3:
            self.active_board = self.checkers
        elif self.mode == 4 or mode == 5:
            phase = self.active_board.end_phrase
            self.active_board = Nones()
            self.active_board.end_phrase = phase

    def draw(self, screen):
        screen.blit(self.image, (0, 0))
        self.active_board.draw(screen)
        if self.mode == 1 or self.mode == 2 or self.mode == 3:
            screen.blit(self.image_rules, (150, 260))
            if (self.active_board.turn and self.mode != 3) or\
                    (self.mode == 3 and not self.active_board.turn):
                text = pg.font.SysFont('centuryschoolbookполужирныйкурсив', 36).render('Ход белых', False, 'black')
                screen.blit(text, (200, 170))
            else:
                text = pg.font.SysFont('centuryschoolbookполужирныйкурсив', 36).render('Ход чёрных', False, 'black')
                screen.blit(text, (200, 170))
        if self.mode == 1:
            t1 = pg.font.SysFont('centuryschoolbookполужирныйкурсив', 17).render('Замыкайте своими', False, 'black')
            t2 = pg.font.SysFont('centuryschoolbookполужирныйкурсив', 17).render('фишками фишки соперника',
                                                                                 False, 'black')
            t3 = pg.font.SysFont('centuryschoolbookполужирныйкурсив', 17).render('и они станут вашими.', False, 'black')
            t4 = pg.font.SysFont('centuryschoolbookполужирныйкурсив', 17).render('Цель игры - заполучить',
                                                                                 False, 'black')
            t5 = pg.font.SysFont('centuryschoolbookполужирныйкурсив', 17).render('больше фишек, чем',
                                                                                 False, 'black')
            t6 = pg.font.SysFont('centuryschoolbookполужирныйкурсив', 17).render('соперник', False, 'black')
            screen.blit(t1, (190, 290))
            screen.blit(t2, (180, 320))
            screen.blit(t3, (190, 350))
            screen.blit(t4, (190, 380))
            screen.blit(t5, (190, 410))
            screen.blit(t6, (190, 440))
        elif self.mode == 2:
            t1 = pg.font.SysFont('centuryschoolbookполужирныйкурсив', 17).render('Простая шашка ходит', False, 'black')
            t2 = pg.font.SysFont('centuryschoolbookполужирныйкурсив', 17).render('только по диагонали вперед',
                                                                                 False, 'black')
            t3 = pg.font.SysFont('centuryschoolbookполужирныйкурсив', 17).render('дамка может ходить на',
                                                                                 False, 'black')
            t4 = pg.font.SysFont('centuryschoolbookполужирныйкурсив', 17).render('любое число полей.', False, 'black')
            t5 = pg.font.SysFont('centuryschoolbookполужирныйкурсив', 17).render('Цель игры - съесть или',
                                                                                 False, 'black')
            t6 = pg.font.SysFont('centuryschoolbookполужирныйкурсив', 17).render('запереть все шашки', False, 'black')
            t7 = pg.font.SysFont('centuryschoolbookполужирныйкурсив', 17).render('противника', False, 'black')
            screen.blit(t1, (190, 290))
            screen.blit(t2, (180, 320))
            screen.blit(t3, (190, 350))
            screen.blit(t4, (190, 380))
            screen.blit(t5, (190, 410))
            screen.blit(t6, (190, 440))
            screen.blit(t7, (190, 470))
        elif self.mode == 3:
            t1 = pg.font.SysFont('centuryschoolbookполужирныйкурсив', 17).render('Умеете выигрывать', False, 'black')
            t2 = pg.font.SysFont('centuryschoolbookполужирныйкурсив', 17).render('в шашки?', False, 'black')
            t3 = pg.font.SysFont('centuryschoolbookполужирныйкурсив', 17).render('Попробуйте проиграть!',
                                                                                 False, 'black')
            screen.blit(t1, (190, 290))
            screen.blit(t2, (190, 320))
            screen.blit(t3, (190, 350))
        elif self.mode == 4:
            text = pg.font.SysFont('centuryschoolbookполужирныйкурсив', 45).render('В какую игру вы хотите сыграть?',
                                                                                   False, 'black')
            screen.blit(text, (200, 150))
        elif self.mode == 5:
            text = pg.font.SysFont('centuryschoolbookполужирныйкурсив', 45).render(self.active_board.end_phrase,
                                                                                   False, 'black')
            screen.blit(text, (400, 150))

    def position(self, event, screen):
        self.active_board.position(event, screen)

    def change_mode(self):
        if self.active_board.end:
            self.set_mode(5)


if __name__ == "__main__":
    '''
    тест файла 
    '''
    imageback = pg.image.load('resources/background.jpg')
    imagerules = pg.image.load('resources/rulesheet.png')
    imagerules.set_colorkey((255, 255, 255))
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
    background = Background(imageback, imagerules, boardimage,
                            imagewhite, imageblack, crownimage, mat, mat)
    background.set_mode(5)
    scr = pg.display.set_mode((1200, 750))
    background.active_board.end_phrase = 'Победили белые'
    background.draw(scr)
    pg.display.update()
    clock = pg.time.Clock()
    finished = False

    while not finished:
        clock.tick(1)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                finished = True
    pg.quit()
