from board import matrix
from objects import *
from input import *
pointsA = 0
pointsB = 0

class Reversi_Board(Board):

    def __init__(self):
        super().__init__()
        self.checkers_flip = checkers_flip = []
        self.hints = hints = []

    def possible_move(self, turn, xstart, ystart):

        checkers_flip = []
        if self.matrix[xstart][ystart] != 0 or not self.InMatrix(xstart, ystart):
            return checkers_flip

        player = Chips()
        player.color = 'white'
        other_player = Chips()
        other_player.color = 'black'

        if turn == 1:
            self.matrix[xstart][ystart] = player
        else:
            player.color = 'black'
            other_player.color = 'white'
            self.matrix[xstart][ystart] = player

        for dir in [[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]]:
            x, y = xstart, ystart
            x += dir[0]
            y += dir[1]
            if self.InMatrix(x, y) and self.matrix[x][y] == other_player:
                x += dir[0]
                y += dir[1]
                if not self.InMatrix(x, y):
                    continue
                while self.matrix[x][y] == other_player:
                    x += dir[0]
                    y += dir[1]
                    if not self.InMatrix(x, y):
                        break
                if not self.InMatrix(x, y):
                    continue
                if self.matrix[x][y] == self.matrix[xstart][ystart]:
                    while True:
                        x -= dir[0]
                        y -= dir[1]
                        if x == xstart:
                            break
                        self.checkers_flip.append([x, y])

        self.matrix[xstart][ystart] = 0
        return self.checkers_flip


    def action(self, turn, xevent, yevent):
        """
        Проверяет что можно сделать с выбранной клеткой и совершает ход:
        ставит новую фишку, меняет цвет "побежденных" фишек, обнуляет хинты

        """
        global end0
        end0 = 0

        player = Chips()
        player.color = 'white'
        other_player = Chips()
        other_player.color = 'black'
        if turn == 1:
            self.matrix[xevent][yevent] = player
        else:
            player.color = 'black'
            other_player.color = 'white'
            self.matrix[xevent][yevent] = player
        self.hints = self.get_hints(self, turn)
        self.check_hints(self)
        if self.InMatrix(xevent, yevent):
            if self.matrix[xevent][yevent] == Hints():
                self.checkers_flip = self.possible_move(self, turn, xevent, yevent)
                self.flip(self, turn)
                self.matrix[xevent][yevent] = turn
                for x in range(8):
                    for y in range(8):
                        if matrix[x][y] == Hints():
                            matrix[x][y] = 0

    def get_turn(self, turn):
        chip = Chips()
        if turn == 1:
            chip.color = 'white'
        else:
            chip.color = 'black'
    def flip(self, turn):
        for [x, y] in self.checkers_flip:
            self.matrix[x][y] = turn


    def InMatrix(self,x,y):
        return x>=0 and x<8 and y>=0 and y<8



    def get_hints(self, turn):
        self.hints = []
        for x in range(8):
            for y in range(8):
                if len(self.possible_move(matrix, turn, x, y)) != 0:
                    self.hints.append((x,y))
        return self.hints

    def check_hints(self):
        """
        Считает положение новых хинтов (соответственно возможных ходов)
        """
        global end0
        end = 1
        for (x, y) in self.hints:
            matrix[x][y] = 3
        for x in range(8):
            for y in range (8):
                if matrix[x][y] == 3:
                    end = 0
                    break
        if end != 0:
            end0 += 1


    def check_end(self):
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
