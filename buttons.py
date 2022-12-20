import pygame as pg


class Buttons:
    """
    класс кнопок
    """
    def __init__(self, x, y, mode, name):
        """
        конструктор кнопки, принимает координату, действие и название
        """
        self.x = x
        self.y = y
        self.mode = mode
        self.name = name
        self.size_x, self.size_y = pg.font.SysFont('centuryschoolbookполужирныйкурсив', 50).size(self.name)

    def draw(self, screen):
        """
        отрисовывает кнопку
        """
        text = pg.font.SysFont('centuryschoolbookполужирныйкурсив', 50).render(self.name, False, 'black')
        screen.blit(text, (self.x, self.y))

    def position(self, event):
        """
        обработка кнопкой клика, проверка попадания
        """
        if event.button == 1:
            if self.x <= event.pos[0] <= self.x + self.size_x:
                if self.y <= event.pos[1] <= self.y + self.size_y:
                    return self.mode
        return None
