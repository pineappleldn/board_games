class Chips:
    color = 'white'
    x = 0
    y = 0

    def turn_over(self):
        """
        Переворачивает фишку (меняет цвет) (подумать над анимацией градиента)
        """
        pass

    def draw(self):
        """
        Рисует фишку
        """
        pass


class Hints:
    x = 0
    y = 0

    def draw(self):
        """
        Рисует хинт
        """
        pass


class Turn:
    state = 0
    count = 0

    def turn_turn(self):
        """
        передает ход от одного игрока к другому
        """
        pass
