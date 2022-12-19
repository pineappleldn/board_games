from objects import *
from Locals import *


class CornersBoard(Board):
    def __init__(self, matrix1=None, x=0, y=0, board_size=664):
        super().__init__(matrix1=matrix1, x=x, y=y, board_size=board_size)
        self.turn = True
        self.pos1_x = -1
        self.pos1_y = -1
        self.pos2_x = -1
        self.pos2_y = -1
        self.end = False

    def move(self):
        x = int(self.x + self.board_size * (2 * self.pos2_x + 1) / 16)
        y = int(self.y + self.board_size * (2 * self.pos2_y + 1) / 16)
        if self.matrix[self.pos1_y][self.pos1_x].color is not None:
            self.matrix[self.pos2_y][self.pos2_x] = Chips(x, y, color=self.matrix[self.pos1_y][self.pos1_x].color)
            self.matrix[self.pos2_y][self.pos2_x].queen = self.matrix[self.pos1_y][self.pos1_x].queen
            self.matrix[self.pos1_y][self.pos1_x] = Nones()

    def position(self, event, screen):  # выбор клетки для хода 2
        x, y = self.check_on_board(event)  # вычисляем координаты клетки
        if x is not None:
            if self.turn:
                if self.matrix[y][x].color == 'white':  # проверяем пешку игрока в выбранной клетке
                    self.pos1_x, self.pos1_y = x, y
                else:
                    if self.pos1_x != -1:  # клетка выбрана
                        self.pos2_x, self.pos2_y = x, y
                        self.hod_igroka1(screen)
                    self.pos1_x = -1  # клетка не выбрана
            else:
                if self.matrix[y][x].color == 'black':  # проверяем пешку игрока в выбранной клетке
                    self.pos1_x, self.pos1_y = x, y
                else:
                    if self.pos1_x != -1:  # клетка выбрана
                        self.pos2_x, self.pos2_y = x, y
                        self.hod_igroka2(screen)
                    self.pos1_x = -1  # клетка не выбрана

    def spisok_hi1(self):  # составляем список ходов игрока
        spisok = self.prosmotr_hodov_i1([])  # здесь проверяем обязательные ходы
        if not spisok:
            spisok = self.prosmotr_hodov_i2([])  # здесь проверяем оставшиеся ходы
        return spisok

    def spisok_hi2(self):  # составляем список ходов игрока
        spisok = self.prosmotr_hodov_k1([])  # здесь проверяем обязательные ходы
        if not spisok:
            spisok = self.prosmotr_hodov_k2([])  # здесь проверяем оставшиеся ходы
        return spisok

    def skan(self):  # подсчёт пешек на поле
        s_i = 0
        s_k = 0
        for i in range(8):
            for j in range(8):
                if self.matrix[i][j].color == 'white':
                    if self.matrix[i][j].queen:
                        s_i += 3
                    else:
                        s_i += 1
                else:
                    if self.matrix[i][j].queen:
                        s_k += 3
                    else:
                        s_k += 1
        return s_k, s_i

    def hod_igroka1(self, screen):
        self.turn = False  # считаем ход игрока выполненным
        spisok = self.spisok_hi1()
        if spisok:
            if ((self.pos1_x, self.pos1_y), (self.pos2_x, self.pos2_y)) \
                    in spisok:  # проверяем ход на соответствие правилам игры
                t_spisok = self.hod(1, screen)  # если всё хорошо, делаем ход
                if t_spisok:  # если есть ещё ход той же пешкой
                    self.turn = True  # считаем ход игрока невыполненным
            else:
                self.turn = True  # считаем ход игрока невыполненным
        s_k, s_i = self.skan()
        if not s_i:
            print('Победили чёрные')
            self.end = True
        elif not s_k:
            print('Победили белые')
            self.end = True
        elif self.turn and not self.spisok_hi1():
            print('Победили чёрные')
            self.end = True
        elif not self.turn and not self.spisok_hi2():
            print('Победили белые')
            self.end = True
        pg.display.update()  # !!!обновление

    def hod_igroka2(self, screen):
        self.turn = True  # считаем ход игрока выполненным
        spisok = self.spisok_hi2()
        if spisok:
            if ((self.pos1_x, self.pos1_y), (self.pos2_x, self.pos2_y)) \
                    in spisok:  # проверяем ход на соответствие правилам игры
                t_spisok = self.hod(1, screen)  # если всё хорошо, делаем ход
                if t_spisok:  # если есть ещё ход той же пешкой
                    self.turn = False  # считаем ход игрока невыполненным
            else:
                self.turn = False  # считаем ход игрока невыполненным

                # определяем победителя
        s_k, s_i = self.skan()
        if not s_i:
            print('Победили чёрные')
            self.end = True
        elif not s_k:
            print('Победили белые')
            self.end = True
        elif self.turn and not self.spisok_hi1():
            print('Победили чёрные')
            self.end = True
        elif not self.turn and not self.spisok_hi2():
            print('Победили белые')
            self.end = True
        pg.display.update()  # !!!обновление

    def hod(self, f, screen):
        if f:
            self.move()
            self.draw(screen)  # рисуем игровое поле
        # превращение
        if self.pos2_y == 0 and self.matrix[self.pos2_y][self.pos2_x].color == 'white':
            self.matrix[self.pos2_y][self.pos2_x].queen = True
        # превращение
        if self.pos2_y == 7 and self.matrix[self.pos2_y][self.pos2_x].color == 'black':
            self.matrix[self.pos2_y][self.pos2_x].queen = True
        # делаем ход
        self.move()

        # рубим пешку
        kx = ky = 1
        if self.pos1_x < self.pos2_x:
            kx = -1
        if self.pos1_y < self.pos2_y:
            ky = -1
        x_poz, y_poz = self.pos2_x, self.pos2_y
        while (self.pos1_x != x_poz) or (self.pos1_y != y_poz):
            x_poz += kx
            y_poz += ky
            if self.matrix[y_poz][x_poz].color is not None:
                self.matrix[y_poz][x_poz] = Nones()
                if f:
                    self.move()
                    self.draw(screen)  # рисуем игровое поле
                # проверяем ход той же пешкой...
                if self.matrix[self.pos2_y][self.pos2_x].color == 'black':  # ...компьютера
                    return self.prosmotr_hodov_k1p([], self.pos2_x, self.pos2_y)  # возвращаем список доступных ходов
                elif self.matrix[self.pos2_y][self.pos2_x].color == 'white':  # ...игрока
                    return self.prosmotr_hodov_i1p([], self.pos2_x, self.pos2_y)  # возвращаем список доступных ходов
        if f:
            self.move()
            self.draw(screen)  # рисуем игровое поле

    def prosmotr_hodov_k1(self, spisok):  # проверка наличия обязательных ходов
        for y in range(8):  # сканируем всё поле
            for x in range(8):
                spisok = self.prosmotr_hodov_k1p(spisok, x, y)
        return spisok

    def prosmotr_hodov_k1p(self, spisok, x, y):
        if self.matrix[y][x].color == 'black' and self.matrix[y][x].queen == False:  # пешка
            for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
                if 0 <= y + iy + iy <= 7 and 0 <= x + ix + ix <= 7:
                    if self.matrix[y + iy][x + ix].color == 'white':
                        if self.matrix[y + iy + iy][x + ix + ix].color is None:
                            spisok.append(((x, y), (x + ix + ix, y + iy + iy)))  # запись хода в конец списка
        if self.matrix[y][x].queen and self.matrix[y][x].color == 'black':  # дамка
            for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
                osh = 0  # определение правильности хода
                for i in range(1, 8):
                    if 0 <= y + iy * i <= 7 and 0 <= x + ix * i <= 7:
                        if osh == 1:
                            spisok.append(((x, y), (x + ix * i, y + iy * i)))  # запись хода в конец списка
                        if self.matrix[y + iy * i][x + ix * i].color == 'white':
                            osh += 1
                        if self.matrix[y + iy * i][x + ix * i].color == 'black' or osh == 2:
                            if osh > 0:
                                spisok.pop()  # удаление хода из списка
                            break
        return spisok

    def prosmotr_hodov_k2(self, spisok):  # проверка наличия остальных ходов
        for y in range(8):  # сканируем всё поле
            for x in range(8):
                if self.matrix[y][x].color == 'black' and self.matrix[y][x].queen == False:  # пешка
                    for ix, iy in (-1, 1), (1, 1):
                        if 0 <= y + iy <= 7 and 0 <= x + ix <= 7:
                            if self.matrix[y + iy][x + ix].color is None:
                                spisok.append(((x, y), (x + ix, y + iy)))  # запись хода в конец списка
                            if self.matrix[y + iy][x + ix].color == 'white':
                                if 0 <= y + iy * 2 <= 7 and 0 <= x + ix * 2 <= 7:
                                    if self.matrix[y + iy * 2][x + ix * 2].color is None:
                                        spisok.append(((x, y), (
                                            x + ix * 2, y + iy * 2)))  # запись хода в конец списка
                if self.matrix[y][x].color == 'black' and self.matrix[y][x].queen:  # дамка
                    for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
                        osh = 0  # определение правильности хода
                        for i in range(1, 8):
                            if 0 <= y + iy * i <= 7 and 0 <= x + ix * i <= 7:
                                if self.matrix[y + iy * i][x + ix * i].color is None:
                                    spisok.append(((x, y), (x + ix * i, y + iy * i)))  # запись хода в конец списка
                                if self.matrix[y + iy * i][x + ix * i].color == 'white':
                                    osh += 1
                                if self.matrix[y + iy * i][x + ix * i].color == 'black' or osh == 2:
                                    break
        return spisok

    def prosmotr_hodov_i1(self, spisok):  # проверка наличия обязательных ходов
        spisok = []  # список ходов
        for y in range(8):  # сканируем всё поле
            for x in range(8):
                spisok = self.prosmotr_hodov_i1p(spisok, x, y)
        return spisok

    def prosmotr_hodov_i1p(self, spisok, x, y):
        if self.matrix[y][x].color == 'white' and self.matrix[y][x].queen == False:  # пешка
            for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
                if 0 <= y + iy + iy <= 7 and 0 <= x + ix + ix <= 7:
                    if self.matrix[y + iy][x + ix].color == 'black':
                        if self.matrix[y + iy + iy][x + ix + ix].color is None:
                            spisok.append(((x, y), (x + ix + ix, y + iy + iy)))  # запись хода в конец списка
        if self.matrix[y][x].queen and self.matrix[y][x].color == 'white':  # дамка
            for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
                osh = 0  # определение правильности хода
                for i in range(1, 8):
                    if 0 <= y + iy * i <= 7 and 0 <= x + ix * i <= 7:
                        if osh == 1:
                            spisok.append(((x, y), (x + ix * i, y + iy * i)))  # запись хода в конец списка
                        if self.matrix[y + iy * i][x + ix * i].color == 'black':
                            osh += 1
                        if self.matrix[y + iy * i][x + ix * i].color == 'white' or osh == 2:
                            if osh > 0:
                                spisok.pop()  # удаление хода из списка
                            break
        return spisok

    def prosmotr_hodov_i2(self, spisok):  # проверка наличия остальных ходов
        for y in range(8):  # сканируем всё поле
            for x in range(8):
                if self.matrix[y][x].color == 'white' and self.matrix[y][x].queen == False:  # пешка
                    for ix, iy in (-1, -1), (1, -1):
                        if 0 <= y + iy <= 7 and 0 <= x + ix <= 7:
                            if self.matrix[y + iy][x + ix].color is None:
                                spisok.append(((x, y), (x + ix, y + iy)))  # запись хода в конец списка
                            if self.matrix[y + iy][x + ix].color == 'black':
                                if 0 <= y + iy * 2 <= 7 and 0 <= x + ix * 2 <= 7:
                                    if self.matrix[y + iy * 2][x + ix * 2].color is None:
                                        spisok.append(((x, y), (
                                            x + ix * 2, y + iy * 2)))  # запись хода в конец списка
                if self.matrix[y][x].queen and self.matrix[y][x].color == 'white':  # пешка с короной
                    for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
                        osh = 0  # определение правильности хода
                        for i in range(1, 8):
                            if 0 <= y + iy * i <= 7 and 0 <= x + ix * i <= 7:
                                if self.matrix[y + iy * i][x + ix * i].color is None:
                                    spisok.append(((x, y), (x + ix * i, y + iy * i)))  # запись хода в конец списка
                                if self.matrix[y + iy * i][x + ix * i].color == 'black':
                                    osh += 1
                                if self.matrix[y + iy * i][x + ix * i].color == 'white' or osh == 2:
                                    break
        return spisok
