import pygame as pg
from pygame.draw import *
from objects import *
board_size = 664


def draw_board(screen):
    """
    Функция рисует игровое поле.
    board_size - ширина и высота картинки игрового поля
    """
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


def draw_cheaps(matrix, screen):
    for x in range(8):
        for y in range(8):
            chip = Chips(screen)
            hint = Hints(screen)
            chip.x = screen.get_width() - board_size + 83*(2*x+1)/2
            chip.y = (screen.get_height() - board_size)/2 + 83*(2*y+1)/2
            hint.x = screen.get_width() - board_size + 83*(2*x+1)/2
            hint.y = (screen.get_height() - board_size)/2 + 83*(2*y+1)/2
            if matrix[x][y] == 1:
                chip.color = 'white'
                chip.draw(screen)
            elif matrix[x][y] == 2:
                chip.color = 'black'
                chip.draw(screen)
            elif matrix[x][y] == 3:
                hint.draw(screen)


def draw_all(screen, matrix):
    """
    Рисует доску, фон, фишки, хинты, окно правил
    """
    draw_background(screen)
    draw_board(screen)
    draw_rules(screen)
    draw_cheaps(matrix, screen)


def text_all():
    """
    Выводит все что написано
    """
    pass


if __name__ == "__main__":
    print("This module is not for direct call!")







