import pygame
import copy
from sudoku_generator import *
from cell import *

EASY = 0
EASY_REMOVE = 30
MEDIUM = 1
MEDIUM_REMOVE = 40
HARD = 2
HARD_REMOVE = 50
BLACK = (0, 0, 0)
RED = (255, 0, 0)


class Board:
    def __init__(self, length, screen, difficulty):
        self.width = screen.get_width()
        self.length = length
        # self.box_length = int(math.sqrt(length))
        self.screen = screen
        self.difficulty = difficulty
        self.selected = None
        removed = 0
        if difficulty == EASY:
            removed = EASY_REMOVE
        elif difficulty == MEDIUM:
            removed = MEDIUM_REMOVE
        elif difficulty == HARD:
            removed = HARD_REMOVE
        sudoku = SudokuGenerator(length, removed)
        sudoku.fill_values()
        self.full_board = copy.deepcopy(sudoku.get_board())
        sudoku.remove_cells()
        self.board = sudoku.get_board()
        self.cells = [[Cell(self.board[i][j], j, i, self.screen)
                       for j in range(self.length)] for i in range(self.length)]

    def draw(self):
        margin = 5
        cell_width = (self.width - 2 * margin) / self.length
        box_length = int(math.sqrt(self.length))

        for i in range(self.length + 1):
            if i % box_length == 0:
                pygame.draw.line(self.screen, BLACK, (cell_width * i + margin, margin),
                                 (cell_width * i + margin, self.width - margin), 4)
            else:
                pygame.draw.line(self.screen, BLACK, (cell_width * i + margin, margin),
                                 (cell_width * i + margin, self.width - margin), 1)
        # pygame.draw.line(self.screen, BLACK, (self.width - 3, 0), (self.width - 3, self.width), 4)

        for i in range(self.length + 1):
            if i % box_length == 0:
                pygame.draw.line(self.screen, BLACK, (margin, cell_width * i + margin),
                                 (self.width - margin, cell_width * i + margin), 4)
            else:
                pygame.draw.line(self.screen, BLACK, (margin, cell_width * i + margin),
                                 (self.width - margin, cell_width * i + margin), 1)

        for i in range(self.length):
            for j in range(self.length):
                self.cells[i][j].draw(margin, cell_width)

        if self.selected is not None:
            upper_left = (margin + cell_width * self.selected[1],
                          cell_width * self.selected[0] + margin)
            lower_right = (margin + cell_width + cell_width * self.selected[1],
                           cell_width * self.selected[0] + margin + cell_width)
            pygame.draw.line(self.screen, RED, upper_left, (upper_left[0], upper_left[1] + cell_width), 8)
            pygame.draw.line(self.screen, RED, upper_left, (upper_left[0] + cell_width, upper_left[1]), 8)
            pygame.draw.line(self.screen, RED, (lower_right[0] - cell_width, lower_right[1]), lower_right, 8)
            pygame.draw.line(self.screen, RED, (lower_right[0], lower_right[1] - cell_width), lower_right, 8)

    def select(self, row, col):
        if row >= self.length or col >= self.length:
            return
        if self.cells[row][col].can_modify:
            self.selected = (row, col)
        else:
            self.selected = None

    def click(self, x, y):
        return y // (self.width // self.length), x // (self.width // self.length)

    def clear(self):
        self.selected = None
        for i in range(self.length):
            for j in range(self.length):
                if self.cells[i][j].can_modify:
                    self.cells[i][j].value = 0
                    self.cells[i][j].sketched_value = 0
        self.update_board()

    def sketch(self, value):
        if self.selected is not None and 1 <= value <= self.length:
            self.cells[self.selected[0]][self.selected[1]].sketched_value = value

    def place_number(self):
        if self.selected is not None:
            self.cells[self.selected[0]][self.selected[1]].value = \
                self.cells[self.selected[0]][self.selected[1]].sketched_value
            self.update_board()
            return self.check_board()

    def reset_to_original(self):
        self.clear()

    def is_full(self):
        for i in range(self.length):
            for j in range(self.length):
                if self.cells[i][j].value == 0:
                    return False
        return True

    def update_board(self):
        for i in range(self.length):
            for j in range(self.length):
                self.board[i][j] = self.cells[i][j].value

    def find_empty(self):
        for i in range(self.length):
            for j in range(self.length):
                if self.cells[i][j].value == 0:
                    return i, j

    def check_board(self):
        return self.board == self.full_board