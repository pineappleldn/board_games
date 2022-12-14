import pygame as pg
import sys
from logic_reversi import *
from input import *
from board import *
from interface import *
from objects import *
from Locals import *
from logic_checkers import *


pg.init()
screen = pg.display.set_mode((width, height))
board = CornersBoard(matrix2, x=100, y=100, board_size=664)

clock = pg.time.Clock()
finished = False
while not finished:
    clock.tick(FPS)
    if board.winner() != 0:
        print(board.winner())
        finished = True
    for event in pg.event.get():
        if event.type == pg.QUIT:
            finished = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            col, row = board.check_on_board(event)
            board.select(row, col)

    board.draw(screen)
    board.draw_valid_moves(board.valid_moves, screen)
    pg.display.update()
pg.quit()