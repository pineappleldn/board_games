from objects import *
from Locals import *


class CornersBoard(Board):
    def __init__(self, matrix1=None, x=0, y=0, board_size=664):
        super().__init__(matrix1=matrix1, x=x, y=y, board_size=board_size)
        self.black_left = self.white_left = 12
        self.black_queens = self.white_queens = 0
        self.selected = None
        self.turn = 'white'
        self.valid_moves = {}

    def move(self, chip, row, col):
        self.matrix[chip.row][chip.col], self.matrix[row][col] = self.matrix[row][col], self.matrix[chip.row][chip.col]
        chip.row = row
        chip.col = col
        chip.x = self.x + self.board_size * (2 * chip.col + 1) / 16
        chip.y = self.y + self.board_size * (2 * chip.row + 1) / 16

        if row == 7 or row == 0:
            chip.make_queen()
            if chip.color == 'white':
                self.white_queens += 1
            else:
                self.black_queens += 1

    def get_chip(self, row, col):
        return self.matrix[row][col]

    def remove(self, chips):
        for chip in chips:
            self.matrix[chip.row][chip.col] = 0
            if chip != 0:
                if chip.color == 'white':
                    self.white_left -= 1
                else:
                    self.black_left -= 1

    def winner(self):
        if self.white_left <= 0:
            return 'Чёрные победили'
        elif self.black_left <= 0:
            return 'Белые победили'
        return 0

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
        chip = self.get_chip(row, col)
        if chip != 0 and chip.color == self.turn:
            self.selected = chip
            self.valid_moves = self.get_valid_moves(chip)
            return True
        return False

    def _move(self, row, col):
        chip = self.get_chip(row, col)
        if self.selected and chip == 0 and (row, col) in self.valid_moves:
            self.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.remove(skipped)
            self.change_turn()
        else:
            return False
        return True

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == 'black':
            self.turn = 'white'
        else:
            self.turn = 'black'

    def get_valid_moves(self, chip):
        moves = {}
        left = chip.col - 1
        right = chip.col + 1
        row = chip.row
        if chip.color == 'black' or chip.queen:
            moves.update(self._traverse_left(row + 1, min(row + 3, 8), 1, chip.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, 8), 1, chip.color, right))

        if chip.color == 'white' or chip.queen:
            moves.update(self._traverse_left(row - 1, max(row-3, -1), -1, chip.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, chip.color, right))
        return moves

    def draw_valid_moves(self, moves, screen):
        for move in moves:
            row, col = move
            pg.draw.circle(screen, 'red', (self.x + self.board_size * (2 * col + 1) / 16, self.y + self.board_size * (2 * row + 1) / 16), 15)

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for i in range(start, stop, step):
            if left < 0:
                break
            current = self.matrix[i][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(i, left)] = last + skipped
                else:
                    moves[(i, left)] = last
                if last:
                    if step == -1:
                        row = max(i - 3, 0)
                    else:
                        row = min(i + 3, 8)
                    moves.update(self._traverse_left(i+step, row, step, color, left-1, skipped=last))
                    moves.update(self._traverse_right(i + step, row, step, color, left+1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]
            left -= 1
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for i in range(start, stop, step):
            if right >= 8:
                break
            current = self.matrix[i][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(i, right)] = last + skipped
                else:
                    moves[(i, right)] = last
                if last:
                    if step == -1:
                        row = max(i - 3, 0)
                    else:
                        row = min(i + 3, 8)
                    moves.update(self._traverse_left(i + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(i + step, row, step, color, right + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]
            right += 1
        return moves
