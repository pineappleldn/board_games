from interface import *
from Locals import *


def check_on_board(event):
    """
    Проверяет попал ли пользователь на доску, возвращает координаты квадрата в доске
    """
    if event.button == 1:
        if width - 664 <= event.pos[0] <= width - 1 and (height - 664)/2 <= event.pos[1] <= (height + 664)/2 - 1:
            return (event.pos[0] - (width - 664)) // 83, (event.pos[1] - (height - 664)/2) // 83


if __name__ == "__main__":
    print("This module is not for direct call!")
