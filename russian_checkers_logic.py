from objects import *
from Locals import *


class CheckerBoard(Board):
    def __init__(self, matrix1=None, x=0, y=0, board_size=664):
        super().__init__(matrix1=matrix1, x=x, y=y, board_size=board_size)
        """
        конструктор класса CheckerBoard, который наследует класс Board
        turn - проверяет: ход принадлежит белым или нет
        pos1_x - номер колонки первого клика за ход
        pos1_y - номер строки первого клика за ход
        pos2_x - номер колонки клетки, выбранной для хода шашкой 
        pos2_y - номер строки клетки, выбранной для хода шашкой
        end - переменная, отвечающая за завершение игры
        """
        self.turn = True
        self.pos1_x = -1
        self.pos1_y = -1
        self.pos2_x = -1
        self.pos2_y = -1
        self.end = False

    def move(self):
        """
        перемещение шашки из начального положения в выбранное
        """
        x = int(self.x + self.board_size * (2 * self.pos2_x + 1) / 16)
        y = int(self.y + self.board_size * (2 * self.pos2_y + 1) / 16)
        if self.matrix[self.pos1_y][self.pos1_x].color is not None:
            self.matrix[self.pos2_y][self.pos2_x] = Chips(x, y, color=self.matrix[self.pos1_y][self.pos1_x].color)
            self.matrix[self.pos2_y][self.pos2_x].queen = self.matrix[self.pos1_y][self.pos1_x].queen
            self.matrix[self.pos1_y][self.pos1_x] = Nones()

    def position(self, event, screen):
        """
        в зависимости от очерёдности хода и положения выбранной клетки вызываются функции, которые непосредственно
        совершают ход.
        :param event: функция запускается только при нажатии левой кнопки мыши в области доски
        :param screen: выбор экрана для отрисовки
        """
        x, y = self.check_on_board(event)  # вычисляем координаты клетки
        if x is not None:
            if self.turn:
                if self.matrix[y][x].color == 'white':  # проверяем пешку игрока в выбранной клетке
                    self.pos1_x, self.pos1_y = x, y
                else:
                    if self.pos1_x != -1:  # клетка выбрана
                        self.pos2_x, self.pos2_y = x, y
                        self.turn_w(screen)
                    self.pos1_x = -1  # клетка не выбрана
            else:
                if self.matrix[y][x].color == 'black':  # проверяем пешку игрока в выбранной клетке
                    self.pos1_x, self.pos1_y = x, y
                else:
                    if self.pos1_x != -1:  # клетка выбрана
                        self.pos2_x, self.pos2_y = x, y
                        self.turn_b(screen)
                    self.pos1_x = -1  # клетка не выбрана

    def list_hw(self):
        """
        составляется список возможных ходов для 'белых'
        :return: список, в котором хранятся координаты клеток, куда возможен ход
        """
        spisok = self.check_turn_w([])  # здесь проверяем обязательные ходы
        if not spisok:
            spisok = self.check_nf_turn_w([])  # здесь проверяем оставшиеся ходы
        return spisok

    def list_hb(self):
        """
        составляется список возможных ходов для 'чёрных'
        :return: список, в котором хранятся координаты клеток, куда возможен ход
        """
        spisok = self.check_turn_b([])  # здесь проверяем обязательные ходы
        if not spisok:
            spisok = self.check_nf_turn_b([])  # здесь проверяем оставшиеся ходы
        return spisok

    def skan(self):
        """
        подсчёт очков, каждого игрока: за пешку на поле добаляется 1 очко, за дамку на поле - 3 очка
        :return:
        s_w - очки белых
        s_b - очки чёрных
        """
        s_w = 0
        s_b = 0
        for i in range(8):
            for j in range(8):
                if self.matrix[i][j].color == 'white':
                    if self.matrix[i][j].queen:
                        s_w += 3
                    else:
                        s_w += 1
                else:
                    if self.matrix[i][j].queen:
                        s_b += 3
                    else:
                        s_b += 1
        return s_b, s_w

    def turn_w(self, screen):
        """
        Делается проверка на наличие выбранной клетки в списке возможных ходов 'белых', если после этого есть ещё ходы,
        то ход остаётся у 'белых'.
        После хода переменная turn меняет значение.
        Также выполняется проверка на завершение игры.
        :param screen: выбор экрана для отрисовки
        """
        self.turn = False  # считаем ход 'белых' выполненным
        spisok = self.list_hw()
        if spisok:
            if ((self.pos1_x, self.pos1_y), (self.pos2_x, self.pos2_y)) \
                    in spisok:  # проверяем ход на соответствие правилам игры
                t_spisok = self.turn_checkers(screen)  # если всё хорошо, делаем ход
                if t_spisok:  # если есть ещё ход той же пешкой
                    self.turn = True  # считаем ход игрока невыполненным
            else:
                self.turn = True  # считаем ход игрока невыполненным

        s_b, s_w = self.skan()  # проверка на завершение игры
        if not s_w:
            print('Победили чёрные')
            self.end = True
        elif not s_b:
            print('Победили белые')
            self.end = True
        elif self.turn and not self.list_hw():
            print('Победили чёрные')
            self.end = True
        elif not self.turn and not self.list_hb():
            print('Победили белые')
            self.end = True
        pg.display.update()  # !!!обновление

    def turn_b(self, screen):
        """
        Делается проверка на наличие выбранной клетки в списке возможных ходов 'чёрных', если после этого есть ещё ходы,
        то ход остаётся у 'чёрных'.
        После хода переменная turn меняет значение.
        Также выполняется проверка на завершение игры.
        :param screen: выбор экрана для отрисовки
        """
        self.turn = True  # считаем ход игрока выполненным
        spisok = self.list_hb()
        if spisok:
            if ((self.pos1_x, self.pos1_y), (self.pos2_x, self.pos2_y)) \
                    in spisok:  # проверяем ход на соответствие правилам игры
                t_spisok = self.turn_checkers(screen)  # если всё хорошо, делаем ход
                if t_spisok:  # если есть ещё ход той же пешкой
                    self.turn = False  # считаем ход игрока невыполненным
            else:
                self.turn = False  # считаем ход игрока невыполненным

        s_b, s_w = self.skan()  # проверка на завершение игры
        if not s_w:
            print('Победили чёрные')
            self.end = True
        elif not s_b:
            print('Победили белые')
            self.end = True
        elif self.turn and not self.list_hw():
            print('Победили чёрные')
            self.end = True
        elif not self.turn and not self.list_hb():
            print('Победили белые')
            self.end = True
        pg.display.update()  # !!!обновление

    def turn_checkers(self, screen):
        """
        Совершается отрисовка положения после перемещения шашки, а также регулируется создание дамок и проверка на
        удары шашек другого цвета.
        :param screen: выбор экрана для отрисовки
        """
        self.move()
        self.draw(screen)  # рисуем игровое поле
        # превращение
        if self.pos2_y == 0 and self.matrix[self.pos2_y][self.pos2_x].color == 'white':
            self.matrix[self.pos2_y][self.pos2_x].queen = True
        # превращение
        if self.pos2_y == 7 and self.matrix[self.pos2_y][self.pos2_x].color == 'black':
            self.matrix[self.pos2_y][self.pos2_x].queen = True
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
                self.move()
                self.draw(screen)  # рисуем игровое поле
                # проверяем ход той же пешкой...
                if self.matrix[self.pos2_y][self.pos2_x].color == 'black':  # ...игрока 2
                    return self.check_f_turn_b([], self.pos2_x, self.pos2_y)  # возвращаем список доступных ходов
                elif self.matrix[self.pos2_y][self.pos2_x].color == 'white':  # ...игрока 1
                    return self.check_f_turn_w([], self.pos2_x, self.pos2_y)  # возвращаем список доступных ходов

    def check_turn_b(self, spisok):
        """
        проверка обязательных ходов для 'чёрных'
        :return: список, в которых хранятся клетки, в одну из которых ход должен быть обязательно совершён
        """
        for y in range(8):  # сканируем всё поле
            for x in range(8):
                spisok = self.check_f_turn_b(spisok, x, y)
        return spisok

    def check_f_turn_b(self, spisok, x, y):
        """
        алгоритм, который определяет возможность сделать удар за 'чёрных'
        :param x: столбец фишки, для которой делается проверка
        :param y: строка фишки, для которой делается проверка
        :param spisok: список с ходами
        :return: список, в котором записаны клетки, куда может быть сделан удар
        """
        if self.matrix[y][x].color == 'black' and not self.matrix[y][x].queen:  # пешка
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

    def check_nf_turn_b(self, spisok):
        """
        алгоритм, который определяет возможность сделать ход за 'чёрных'
        :param spisok: список с ходами
        :return: список, в котором записаны клетки, куда может быть сделан ход
        """
        for y in range(8):  # сканируем всё поле
            for x in range(8):
                if self.matrix[y][x].color == 'black' and not self.matrix[y][x].queen:  # пешка
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

    def check_turn_w(self, spisok):
        """
        проверка обязательных ходов для 'белых'
        :return: список, в которых хранятся клетки, в одну из которых ход должен быть обязательно совершён
        """
        for y in range(8):  # сканируем всё поле
            for x in range(8):
                spisok = self.check_f_turn_w(spisok, x, y)
        return spisok

    def check_f_turn_w(self, spisok, x, y):
        """
        алгоритм, который определяет возможность сделать удар за 'белых'
        :param x: столбец фишки, для которой делается проверка
        :param y: строка фишки, для которой делается проверка
        :param spisok: список с ходами
        :return: список, в котором записаны клетки, куда может быть сделан удар
        """
        if self.matrix[y][x].color == 'white' and not self.matrix[y][x].queen:  # пешка
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

    def check_nf_turn_w(self, spisok):
        """
        алгоритм, который определяет возможность сделать ход за 'чёрных'
        :param spisok: список с ходами
        :return: список, в котором записаны клетки, куда может быть сделан ход
        """
        for y in range(8):  # сканируем всё поле
            for x in range(8):
                if self.matrix[y][x].color == 'white' and not self.matrix[y][x].queen:  # пешка
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
