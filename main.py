import pygame as pg
import sys
from logic_reversi import *
from input import *
from board import *
from interface import *
from objects import *
from Locals import *
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


def main():
    """Главная функция главного модуля"""
    pg.init()
    screen = pg.display.set_mode((width, height))

    turn = Turn()
    print('Game started!')

    draw_all(screen, matrix)
    pg.display.update()
    clock = pg.time.Clock()

    finished = False
    while not finished:
        draw_all(screen, matrix)
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                finished = True
            elif event.type == pg.MOUSEBUTTONDOWN:
                x, y = check_on_board(event)
                turn = 1
                action(matrix, turn, x, y)
    print('Game finished!')
    pg.quit()


if __name__ == "__main__":
    main()
