import pygame


class Cell:
    def __init__(self, value, row, col, screen):
        self.row = row
        self.col = col
        self.screen = screen
        # self.width=screen.get_width()
        self.value = value
        self.sketched_value = value
        self.can_modify = (value == 0)

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value

    def draw(self, margin, cell_width):
        if self.sketched_value:
            my_font = pygame.font.SysFont('Comic Sans MS', int(cell_width / 2))
            center = (margin + self.row * cell_width + cell_width / 3,
                      margin + self.col * cell_width + cell_width / 5)
            color = (0, 0, 0)
            if not self.can_modify:
                color = (100, 100, 100)
            if self.value != self.sketched_value:
                color = (220, 220, 220)
            val = my_font.render(str(self.sketched_value), True, color)
            self.screen.blit(val, center)