import pygame as pg
from pygame.draw import *


def draw_board(screen):
    """
    Функция рисует игровое поле.
    board_size - ширина и высота картинки игрового поля
    """
    board_size = 664
    board = pg.image.load('board.jpg')
    screen.blit(board, (screen.get_width() - board_size, (screen.get_height() - board_size)/2))


def draw_background(screen):
    """
    Функция заливает фон белым цветом
    """
    screen.fill('white')


def draw_rules(screen):
    """
    Функция рисует прямоугольник с правилами. ПРАВИЛА НУЖНО ДОБАВИТЬ
    """
    rect_obj = rect(screen, 'white', (20, 250, 150, 400))
    text_object = pg.font.SysFont('arial', 36).render('Правила', True, 'black')
    text_rect = text_object.get_rect(center=rect_obj.center)
    screen.blit(text_object, text_rect)


def draw_all(screen):
    """
    Рисует доску, фон, фишки, хинты, окно правил
    """
    draw_background(screen)
    draw_board(screen)
    draw_rules(screen)


def text_all():
    """
    Выводит все что написано
    """
    pass


if __name__ == "__main__":
    print("This module is not for direct call!")