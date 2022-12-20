from screen import *

FPS = 30
width = 1200
height = 750
matrix = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 3, 0, 0, 0],
    [0, 0, 0, 1, 2, 3, 0, 0],
    [0, 0, 3, 2, 1, 0, 0, 0],
    [0, 0, 0, 3, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    ]

matrix2 = [
    [0, 2, 0, 2, 0, 2, 0, 2],
    [2, 0, 2, 0, 2, 0, 2, 0],
    [0, 2, 0, 2, 0, 2, 0, 2],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0],
    ]

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


def main():
    """Главная функция главного модуля"""
    pg.init()
    screen = pg.display.set_mode((width, height))
    background = Background(imageback, imagerules, boardimage, imagewhite, imageblack, crownimage, matrix, matrix2)
    background.set_mode(4)
    background.draw(screen)
    pg.display.update()
    clock = pg.time.Clock()
    finished = False
    print('Game started!')

    while not finished:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                finished = True
            elif event.type == pg.MOUSEBUTTONDOWN:
                background.position(event, screen)
        background.change_mode()
        background.draw(screen)
        pg.display.update()

    print('Game finished!')
    pg.quit()


if __name__ == "__main__":
    main()
