from anyboard import *


class ReversiHints(Hints):
    def __init__(self, x=0, y=0, r=9):
        super().__init__(x=x, y=y, r=r)

    def draw(self, screen):
        """
        Переводит координаты из положения на доске в пиксели, рисует хинт
        """
        x = int(538 + 573 * (2 * self.y + 1) / 16)
        y = int(88 + 573 * (2 * self.x + 1) / 16)
        pg.draw.circle(screen, self.color, (x, y), self.r)


class ReversiChips(Chips):
    def __init__(self, image_white, image_black, crown, x=0, y=0, color='white'):
        super().__init__(image_white=image_white, image_black=image_black, crown=crown, x=x, y=y, color=color)

    def draw(self, screen):
        """
        Переводит координаты из положения на доске в пиксели, рисует фишку
        """
        x = int(538 + 573 * (2 * self.y + 1) / 16)
        y = int(88 + 573 * (2 * self.x + 1) / 16)
        if self.color == 'white':
            screen.blit(self.image_white, (x - self.image_white.get_width() // 2,
                                           y - self.image_white.get_height() // 2))
        else:
            screen.blit(self.image_black, (x - self.image_black.get_width() // 2,
                                           y - self.image_black.get_height() // 2))
        if self.queen:
            screen.blit(self.crown, (self.x - self.crown.get_width() // 2, self.y - self.crown.get_height() // 2))


class ReversiBoard(Board):
    def __init__(self, board_image, image_white, image_black, crown, matrix1=None, x=0, y=0, board_size=573):
        super().__init__(board_image=board_image, image_white=image_white, image_black=image_black, crown=crown,
                         matrix1=matrix1, x=x, y=y, board_size=board_size)
        """Конструктор класса;x, y, board_size - параметры доски на экране;
        turn - индикатор того, чей ход
        end - индикатор конца игры
        pointsA, pointsB - счет первого и второго игрока соответственно
        hints - список возможных ходов
        checkers_flip - список фишек, которые надо перевернуть после хода"""

        self.checkers_flip = []
        self.hints = []
        self.end = False
        self.end0 = 0
        self.turn = True
        self.pointsA = 0
        self.pointsB = 0
        self.end_phrase = ''

    def position(self, event, screen):
        """Ход, посчет очков, проверка, закончилась ли игра"""
        x, y = self.check_on_board(event)
        if x is not None and y is not None:
            self.action(y, x)
            self.score()
            self.check_end()

    def swap(self):
        """ смена хода """
        if self.turn:
            self.turn = False
        else:
            self.turn = True

    def possible_move(self, xstart, ystart):
        """Проверка возможности хода в клетку с координатами xstart, ystart;
        Если ход возможен, то возвращает список фишек, которые надо перевернуть"""
        for j in range(8):
            for i in range(8):
                if isinstance(self.matrix[i][j], Hints):
                    self.matrix[i][j] = Nones()
        self.checkers_flip = []
        if not isinstance(self.matrix[xstart][ystart], Nones):
            return self.checkers_flip

        xpixel, ypixel = xstart, ystart
        self.matrix[xstart][ystart] = ReversiChips(self.image_white, self.image_black, self.crown, xpixel, ypixel)
        if self.turn:
            self.matrix[xstart][ystart].color = 'white'
        else:
            self.matrix[xstart][ystart].color = 'black'

        if self.turn:
            other_color = 'black'
        else:
            other_color = 'white'
        self.checkers_flip = []
        for dir in [(0, 1), (0, -1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            x, y = xstart, ystart
            x += dir[0]
            y += dir[1]
            if self.InMatrix(x, y) and not isinstance(self.matrix[x][y], Nones) and \
                    self.matrix[x][y].color == other_color:
                x += dir[0]
                y += dir[1]
                if not self.InMatrix(x, y) or isinstance(self.matrix[x][y], Nones):
                    continue
                while self.matrix[x][y].color == other_color:
                    x += dir[0]
                    y += dir[1]
                    if not self.InMatrix(x, y):
                        break
                if not self.InMatrix(x, y):
                    continue
                if self.matrix[x][y].color == self.matrix[xstart][ystart].color:
                    while True:
                        x -= dir[0]
                        y -= dir[1]
                        if (x == xstart) and (y == ystart):
                            break
                        self.checkers_flip.append([x, y])

        self.matrix[xstart][ystart] = Nones()
        return self.checkers_flip

    def action(self, xevent, yevent):
        """
        Проверяет что можно сделать с выбранной клеткой и совершает ход:
        ставит новую фишку, меняет цвет "побежденных" фишек, обнуляет хинты

        """
        self.get_hints()
        self.check_hints()
        if self.InMatrix(xevent, yevent):
            if isinstance(self.matrix[xevent][yevent], Hints):
                xpixel, ypixel = xevent, yevent
                if len(self.possible_move(xevent, yevent)) == 0:
                    return False
                else:
                    self.possible_move(xevent, yevent)
                    self.flip()
                    self.matrix[xevent][yevent] = ReversiChips(self.image_white, self.image_black, self.crown, xpixel, ypixel)
                    if self.turn:
                        self.matrix[xevent][yevent].color = 'white'
                    else:
                        self.matrix[xevent][yevent].color = 'black'
                if len(self.hints) == 0:
                    self.swap()
                for y in range(8):
                    for x in range(8):
                        if isinstance(self.matrix[x][y], Hints):
                            self.matrix[x][y] = Nones()
                self.swap()
                self.get_hints()
                self.check_hints()
        return True

    def flip(self):
        """Смена цвета замыкаемых фишек"""
        for [x, y] in self.checkers_flip:
            if self.turn:
                self.matrix[x][y].color = 'white'
            else:
                self.matrix[x][y].color = 'black'

    def InMatrix(self, x, y):
        """Проверка принадлежности доске"""
        return (x >= 0) and (x < 8) and (y >= 0) and (y < 8)

    def get_hints(self):
        """Получение списка хинтов"""
        self.hints = []
        for y in range(8):
            for x in range(8):
                if len(self.possible_move(x, y)) != 0:
                    self.hints.append((x, y))

    def score(self):
        """Подсчет очков"""
        self.pointsA = 0
        self.pointsB = 0
        for x in range(8):
            for y in range(8):
                if not isinstance(self.matrix[x][y], Nones):
                    if self.matrix[x][y].color == 'white':
                        self.pointsA += 1
                    if self.matrix[x][y].color == 'black':
                        self.pointsB += 1

    def check_hints(self):
        """
        Считает положение новых хинтов (соответственно возможных ходов)
        """
        end = 1
        for (x, y) in self.hints:
            xpixel, ypixel = x, y
            self.matrix[x][y] = ReversiHints(xpixel, ypixel)
        for y in range(8):
            for x in range(8):
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
            if self.pointsA > self.pointsB:
                self.end_phrase = 'Победили белые'
            elif self.pointsA < self.pointsB:
                self.end_phrase = 'Победили чёрные'
            else:
                self.end_phrase = 'Победила дружба!'
            self.end = True
        else:
            self.end = False
