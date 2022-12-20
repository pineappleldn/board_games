from objects import *


class ReversiBoard(Board):

    def __init__(self, matrix1=None, x=0, y=0, board_size=664):
        super().__init__(matrix1=matrix1, x=x, y=y, board_size=board_size)
        self.checkers_flip = []
        self.hints = []
        self.end = False
        self.end0 = 0
        self.turn = True
        self.pointsA = 0
        self.pointsB = 0

    def move(self, event):
        x, y = self.check_on_board(event)
        if x is not None and y is not None:
            self.action(x, y)

    def swap(self):
        if self.turn:
            self.turn = False
        else:
            self.turn = True

    def possible_move(self, xstart, ystart):
        for j in range(8):
            for i in range(8):
                if isinstance(self.matrix[i][j], Hints):
                    self.matrix[i][j] = Nones()
        self.checkers_flip = []
        if not isinstance(self.matrix[xstart][ystart], Nones):
            return self.checkers_flip

        xpixel, ypixel = self.GetPixelCoords(xstart, ystart)
        self.matrix[xstart][ystart] = Chips(xpixel, ypixel)
        if self.turn:
            self.matrix[xstart][ystart].color = 'white'
        else:
            self.matrix[xstart][ystart].color = 'black'

        if self.turn:
            other_color = 'black'
        else:
            other_color = 'white'

        for dir in [[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]]:
            x, y = xstart, ystart
            x += dir[0]
            y += dir[1]
            if self.InMatrix(x, y) and not isinstance(self.matrix[y][x], Nones) and \
                    self.matrix[y][x].color == other_color:
                x += dir[0]
                y += dir[1]
                if not self.InMatrix(x, y) or isinstance(self.matrix[y][x], Nones):
                    continue
                while self.matrix[y][x].color == other_color and not isinstance(self.matrix[y][x], Nones):
                    x += dir[0]
                    y += dir[1]
                    if not self.InMatrix(x, y):
                        break
                if not self.InMatrix(x, y):
                    continue
                if self.matrix[y][x].color == self.matrix[ystart][xstart].color \
                        and not isinstance(self.matrix[y][x], Nones):
                    while True:
                        x -= dir[0]
                        y -= dir[1]
                        if x == xstart:
                            break
                        self.checkers_flip.append([x, y])

        self.matrix[ystart][xstart] = Nones()
        return self.checkers_flip

    def action(self, xevent, yevent):
        """
        Проверяет что можно сделать с выбранной клеткой и совершает ход:
        ставит новую фишку, меняет цвет "побежденных" фишек, обнуляет хинты

        """
        self.check_hints()
        if self.InMatrix(xevent, yevent):
            if isinstance(self.matrix[yevent][xevent], Hints):
                xpixel, ypixel = self.GetPixelCoords(yevent, xevent)
                self.checkers_flip = self.possible_move(yevent, xevent)
                self.flip()
                self.matrix[yevent][xevent] = Chips(xpixel, ypixel)
                if self.turn:
                    self.matrix[yevent][xevent].color = 'white'
                else:
                    self.matrix[yevent][xevent].color = 'black'
                self.swap()
                for y in range(8):
                    for x in range(8):
                        if isinstance(self.matrix[y][x], Hints):
                            self.matrix[y][x] = Nones()

    def flip(self):
        for [x, y] in self.checkers_flip:
            if self.turn:
                self.matrix[y][x].color = 'white'
            else:
                self.matrix[y][x].color = 'black'

    def GetPixelCoords(self, x, y):
        return self.x + self.board_size * (2 * y + 1) // 16, self.y + self.board_size * (2 * x + 1) // 16

    def InMatrix(self, x, y):
        return (x >= 0) and (x < 8) and (y >= 0) and (y < 8)

    def get_hints(self):
        self.hints = []
        for y in range(8):
            for x in range(8):
                if len(self.possible_move(x, y)) != 0:
                    self.hints.append((x, y))

    def check_hints(self):
        """
        Считает положение новых хинтов (соответственно возможных ходов)
        """
        end = 1
        for (x, y) in self.hints:
            xpixel, ypixel = self.GetPixelCoords(x, y)
            self.matrix[y][x] = Hints(xpixel, ypixel)
        for y in range(8):
            for x in range(8):
                continue
            if isinstance(self.matrix[y][x], Hints):
                end = 0
                break
        if end != 0:
            self.end0 += 1

    def check_end(self):
        """
        Проверяет закончилась ли игра, выводит победителя и тп
        """
        if self.end0 == 2:
            if self.pointsA > self.pointsB:
                print('победил игрок A с отрывом ', self.pointsA-self.pointsB)
            elif self.pointsA < self.pointsB:
                print('победил игрок B с отрывом ', self.pointsB-self.pointsA)
            else:
                print('ничья')
            self.end = True
        else:
            self.end = False
