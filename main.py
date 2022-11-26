import pygame as pg
from logic_reversi import *
from input import *
from board import *
from interface import *
from objects import *


def main():
    """Главная функция главного модуля"""
    pg.init()

    width = 900
    height = 900
    screen = pg.display.set_mode((width, height))

    turn = Turn()
    finished = False
    print('Game started!')

    while not finished:
        finished = True

    print('Game finished!')
    pg.quit()


if __name__ == "__main__":
    main()
