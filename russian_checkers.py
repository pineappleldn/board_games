from russian_checkers_logic import *

pg.init()
screen = pg.display.set_mode((width, height))
board = CheckerBoard(matrix2, x=100, y=100, board_size=664)

clock = pg.time.Clock()
finished = False
while not finished:
    clock.tick(FPS)
    if board.end:
        finished = True
    for event in pg.event.get():
        if event.type == pg.QUIT:
            finished = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            board.position(event, screen)
    board.draw(screen)
    pg.display.update()
pg.quit()
