from main import *
import pygame as pg
from pygame.draw import *
board_size = 664

def draw_board():
    """
    Функция рисует игровое поле.
    board_size - ширина и высота картинки игрового поля
    """
    global board_size
    board = pg.image.load('board.jpg')
    screen.blit(board, (width - board_size, (height - board_size)/2))


def draw_background():
    """
    Функция заливает фон белым цветом
    """
    screen.fill('white')


def draw_rules():
    """
    Функция рисует прямоугольник с правилами. ПРАВИЛА НУЖНО ДОБАВИТЬ
    """
    rect_obj = rect(screen, 'white', (20, 250, 150, 400))
    text_object = pg.font.SysFont('arial', 36).render('Правила', True, 'white')
    text_rect = text_object.get_rect(center=rect_obj.center)
    screen.blit(text_object, text_rect)


def draw_all():
    """
    Рисует доску, фон, фишки, хинты, окно правил
    """
    draw_background()
    draw_board()
    draw_rules()


def text_all():
    """
    Выводит все что написано
    """
    pass


if __name__ == "__main__":
    print("This module is not for direct call!")