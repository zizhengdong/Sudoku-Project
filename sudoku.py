import math
from board import *
import pygame

WIDTH = 600
HEIGHT = 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 127, 0)
YELLOW = (255, 255, 255)
LENGTH = 9


class BoardManager:
    def __init__(self, win):
        self.state = 0
        self.width = win.get_width()
        self.height = win.get_height()
        self.screen = win
        self.board = None
        btn_width = self.width * 2 / 3 / 5
        margin = (self.width - btn_width * 5) / 2
        self.btn_01 = pygame.Rect(margin, self.height * 2 / 3, btn_width, btn_width / 2)
        self.btn_02 = pygame.Rect(margin + 2 * btn_width, self.height * 2 / 3, btn_width, btn_width / 2)
        self.btn_03 = pygame.Rect(margin + 4 * btn_width, self.height * 2 / 3, btn_width, btn_width / 2)
        self.btn_11 = pygame.Rect(margin, self.width + 20, btn_width, btn_width / 2)
        self.btn_12 = pygame.Rect(margin + 2 * btn_width, self.width + 20, btn_width, btn_width / 2)
        self.btn_13 = pygame.Rect(margin + 4 * btn_width, self.width + 20, btn_width, btn_width / 2)
        self.win_btn = pygame.Rect((self.width - btn_width) / 2, self.height / 2, btn_width, btn_width / 2)
        self.lose_btn = pygame.Rect((self.width - btn_width) / 2, self.height / 2, btn_width, btn_width / 2)

    def draw_welcome(self):
        self.add_text("Welcome to Sudoku", 56, (self.width / 2, self.height / 4))
        self.add_text("Select Game Mode", 40, (self.width / 2, self.height / 2))
        pygame.draw.rect(self.screen, ORANGE, self.btn_01)
        pygame.draw.rect(self.screen, ORANGE, self.btn_02)
        pygame.draw.rect(self.screen, ORANGE, self.btn_03)
        self.add_text("EASY", 16, self.btn_01.center)
        self.add_text("MEDIUM", 16, self.btn_02.center)
        self.add_text("HARD", 16, self.btn_03.center)

    def draw_lose(self):
        self.add_text("Game Over :(", 56, (self.width / 2, self.height / 4))
        pygame.draw.rect(self.screen, ORANGE, self.lose_btn)
        self.add_text("EXIT", 16, self.lose_btn.center)

    def draw_win(self):
        self.add_text("Game Won!", 56, (self.width / 2, self.height / 4))
        pygame.draw.rect(self.screen, ORANGE, self.win_btn)
        self.add_text("RESTART", 16, self.win_btn.center)

    def draw(self):
        self.screen.fill(WHITE)
        if self.state == 0:
            self.draw_welcome()
        elif self.state == 1:
            self.board.draw()
            self.draw_menu()
        elif self.state == 2:
            self.draw_win()
        elif self.state == 3:
            self.draw_lose()

    def welcome_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            pos = pygame.mouse.get_pos()
            if self.btn_01.collidepoint(pos):
                self.board = Board(LENGTH, self.screen, EASY)
                self.state = 1
            elif self.btn_02.collidepoint(pos):
                self.board = Board(LENGTH, self.screen, MEDIUM)
                self.state = 1
            elif self.btn_03.collidepoint(pos):
                self.board = Board(LENGTH, self.screen, HARD)
                self.state = 1

    def play_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            pos = pygame.mouse.get_pos()
            if self.btn_11.collidepoint(pos):
                self.board.reset_to_original()
            elif self.btn_12.collidepoint(pos):
                self.board = None
                self.state = 0
                return True
            elif self.btn_13.collidepoint(pos):
                pygame.quit()
                return False
            else:
                cell = self.board.click(pos[0], pos[1])
                self.board.select(cell[0], cell[1])
        if event.type == pygame.KEYDOWN:
            if 49 <= event.key <= 57:
                self.board.sketch(event.key - 48)
            elif 97 <= event.key <= 103:
                self.board.sketch(event.key - 87)
            elif event.key == pygame.K_RETURN:
                if self.board.place_number():
                    self.state = 2
                elif self.board.is_full():
                    self.state = 3
        return True

    def win_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            pos = pygame.mouse.get_pos()
            if self.win_btn.collidepoint(pos):
                self.board = None
                self.state = 0

    def lose_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            pos = pygame.mouse.get_pos()
            if self.lose_btn.collidepoint(pos):
                pygame.quit()
                return False
        return True

    def event_process(self, event):
        if self.state == 0:
            self.welcome_event(event)
        elif self.state == 1:
            if not self.play_event(event):
                return False
        elif self.state == 2:
            self.win_event(event)
        elif self.state == 3:
            if not self.lose_event(event):
                return False
        return True

    def add_text(self, text, size, center):
        my_font = pygame.font.SysFont('Comic Sans MS', size)
        val = my_font.render(text, True, BLACK)
        txt_rect = val.get_rect(center=center)
        self.screen.blit(val, txt_rect)

    def draw_menu(self):
        pygame.draw.rect(self.screen, ORANGE, self.btn_11)
        pygame.draw.rect(self.screen, ORANGE, self.btn_12)
        pygame.draw.rect(self.screen, ORANGE, self.btn_13)
        self.add_text("RESET", 16, self.btn_11.center)
        self.add_text("RESTART", 16, self.btn_12.center)
        self.add_text("EXIT", 16, self.btn_13.center)


