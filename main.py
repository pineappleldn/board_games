import pygame as pg
import sys
from logic_reversi import *
from input import *
from board import *
from interface import *
from objects import *
from Locals import *
matrix1 = [
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

    print('Game started!')

    pg.display.update()
    clock = pg.time.Clock()
    reversi = Reversi_Board(matrix1)

    turn = 1

    finished = False
    while not finished:
        screen.fill('green')
        reversi.draw(screen)
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                finished = True
            elif event.type == pg.MOUSEBUTTONDOWN:
                x, y = reversi.check_on_board(event)
                reversi.action(turn, x, y)
                if turn == 1:
                    turn = 2
                else:
                    turn = 1

        pg.display.update()
    print('Game finished!')
    pg.quit()


if __name__ == "__main__":
    main()
