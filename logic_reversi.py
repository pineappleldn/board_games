from board import matrix
from objects import *

pointsA = 0
pointsB = 0


def update_points(matrix):
    """
    Подчситывает очки игроков
    """
    global pointsA, pointsB
    pointsA = 0
    pointsB = 0
    for lst in matrix:
        pointsA += lst.count(1)
        pointsB += lst.count(2)

def action(matrix, event, turn):
    """
    Проверяет что можно сделать с выбранной клеткой и совершает ход:
    ставит новую фишку, меняет цвет "побежденных" фишек, обнуляет хинты

    """
    end0 = 0
    hints = get_hints(matrix)
    check_hints(matrix, hints)
    if InMatrix(xevent, yevent):
        if matrix[xevent][yevent] == 3:
            flip(matrix, xevent, yevent)
            matrix[xevent][yevent] = turn
            for x in range(8):
                for y in range(8):
                    if matrix[x][y] == 3:
                        matrix[x][y] == 0


def flip(matrix, xstart, ystart):
    global turn, checkers_flip
    for [x, y] in checkers_flip:
        matrix[x][y] = turn
def InMatrix(x,y):
    return x>=0 and x<8 and y>=0 and y<8

def possible_move(matrix,xstart,ystart):
    global turn
    if matrix[xstart, ystart] != 0 or not InMatrix(xstart, ystart):
        return False

    other_player = 0
    if turn.state == 1:
        matrix[xstart][ystart] = 1
        other_player = 2
    else:
        matrix[xstart][ystart] = 2
        other_player = 1

    checkers_flip = []
    for dir in [[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]]:
        x, y = xstart, ystart
        x += dir[0]
        y += dir[1]
        if InMatrix(x, y) and matrix[x][y] == other_player:
            x += dir[0]
            y += dir[1]
            if not InMatrix(x, y):
                continue
            while matrix[x][y] == other_player:
                x += dir[0]
                y += dir[1]
                if not InMatrix(x, y):
                    break
            if not InMatrix(x, y):
                continue
            if matrix[x][y] == matrix[xstart][ystart]:
                while True:
                    x -= dir[0]
                    y -= dir[1]
                    if x == xstart:
                        break
                    checkers_flip.append([x, y])

    matrix[xstart][ystart] = 0
    if len(checkers_flip) == 0:
        return False
    return checkers_flip

def get_hints(matrix):
    hints = []
    for x in range(8):
        for y in range(8):
            if possible_move(matrix,x,y) != False:
                hints.append((x,y))
    return hints

def check_hints(matrix, hints):
    """
    Считает положение новых хинтов (соответственно возможных ходов)
    """
    global end0
    end = 1
    for (x, y) in hints:
        matrix[x][y] = 3
    for x in range(8):
        for y in range (8):
            if matrix[x][y] == 3:
                end = 0
                break
    if end != 0:
        end0 += 1


def check_end(turn):
    """
    Проверяет закончилась ли игра, выводит победителя и тп
    """
    global end0
    if end0 == 2:
        if pointsA > pointsB:
            print('победил игрок A с отрывом ', pointsA-pointsB)
        elif pointsA < pointsB:
            print('победил игрок B с отрывом ', pointsB-pointsA)
        else:
            print('ничья')
