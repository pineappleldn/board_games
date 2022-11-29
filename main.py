import pygame as pg
import sys
from logic_reversi import *
from input import *
from board import *
from interface import *
from objects import *

width = 900
height = 900
screen = pg.display.set_mode((width, height))


def main():
    """Главная функция главного модуля"""
    pg.init()
    turn = Turn()
    finished = False
    print('Game started!')

    while not finished:
        finished = True

    print('Game finished!')
    pg.quit()


if __name__ == "__main__":
    main()
