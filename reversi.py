from reversi_logic import *

pg.init()
screen = pg.display.set_mode((width, height))
reversi = ReversiBoard(matrix1, x=100, y=100, board_size=664)

clock = pg.time.Clock()
finished = False
while not finished:
    clock.tick(FPS)
    if reversi.end:
        finished = True
    for event in pg.event.get():
        if event.type == pg.QUIT:
            finished = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            reversi.move(event)
    reversi.draw(screen)
    pg.display.update()
pg.quit()
