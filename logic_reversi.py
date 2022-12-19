from typing import Union, Any

from board import matrix
from input import *
pointsA = 0
pointsB = 0
matrix1 = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 2, 0, 0, 0],
    [0, 0, 0, 2, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    ]


class ReversiBoard(Board):

    def __init__(self, matrix1=None, x=0, y=0, board_size=664):
        super().__init__(matrix1=matrix1, x=x, y=y, board_size=board_size)
        self.checkers_flip = []
        self.hints = []
        self.end0 = 0

    def possible_move(self, turn, xstart, ystart):
        for j in range(8):
            for i in range(8):
                if isinstance(self.matrix[i][j], Hints):
                    self.matrix[i][j] = Nones()

        if not isinstance(self.matrix[xstart][ystart], Nones) or not self.InMatrix(xstart, ystart):
            return self.checkers_flip

        self.matrix[xstart][ystart] = Chips()
        self.matrix[xstart][ystart].color = turn

        if turn == 'white':
            other_color = 'black'
        else:
            other_color = 'white'

        for dir in [[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]]:
            x, y = xstart, ystart
            x += dir[0]
            y += dir[1]
            if self.InMatrix(x, y) and not isinstance(self.matrix[x][y], Nones) and \
                    self.matrix[x][y].color == other_color:
                x += dir[0]
                y += dir[1]
                if not self.InMatrix(x, y):
                    continue
                while self.matrix[x][y].color == other_color and not isinstance(self.matrix[x][y], Nones):
                    x += dir[0]
                    y += dir[1]
                    if not self.InMatrix(x, y):
                        break
                if not self.InMatrix(x, y):
                    continue
                if self.matrix[x][y].color == self.matrix[xstart][ystart].color \
                        and not isinstance(self.matrix[x][y], Nones):
                    while True:
                        x -= dir[0]
                        y -= dir[1]
                        if x == xstart:
                            break
                        self.checkers_flip.append([x, y])

        self.matrix[xstart][ystart] = Nones()
        return self.checkers_flip

    def action(self, turn, xevent, yevent):
        """
        Проверяет что можно сделать с выбранной клеткой и совершает ход:
        ставит новую фишку, меняет цвет "побежденных" фишек, обнуляет хинты

        """

        self.hints = self.get_hints(turn)
        self.check_hints()
        if self.InMatrix(xevent, yevent):
            if isinstance(self.matrix[xevent][yevent], Hints):
                self.checkers_flip = self.possible_move(turn, xevent, yevent)
                self.flip(turn)
                self.matrix[xevent][yevent].color = turn
                for y in range(8):
                    for x in range(8):
                        if isinstance(self.matrix[x][y], Hints):
                            self.matrix[x][y] = Nones()

    def flip(self, turn):
        for [x, y] in self.checkers_flip:
            self.matrix[x][y].color = turn

    def GetPixelCoords(self, x, y):
        return self.x + self.board_size * (2 * x + 1) // 16, self.y + self.board_size * (2 * y + 1) // 16

    def InMatrix(self, x, y):
        if x is not None and y is not None:
            return (x >= 0) and (x < 8) and (y >= 0) and (y < 8)
        else:
            return False

    def get_hints(self, turn):
        self.hints = []
        for y in range(8):
            for x in range(8):
                if len(self.possible_move(turn, x, y)) != 0:
                    self.hints.append((x, y))
        return self.hints

    def check_hints(self):
        """
        Считает положение новых хинтов (соответственно возможных ходов)
        """
        end = 1
        for (x, y) in self.hints:
            xpixel, ypixel = self.GetPixelCoords(x, y)
            self.matrix[x][y] = Hints(xpixel, ypixel)
        for y in range(8):
            for x in range(8):
                continue
            if isinstance(self.matrix[x][y], Hints):
                end = 0
                break
        if end != 0:
            self.end0 += 1

    def check_end(self):
        """
        Проверяет закончилась ли игра, выводит победителя и тп
        """
        if self.end0 == 2:
            if pointsA > pointsB:
                print('победил игрок A с отрывом ', pointsA-pointsB)
            elif pointsA < pointsB:
                print('победил игрок B с отрывом ', pointsB-pointsA)
            else:
                print('ничья')
