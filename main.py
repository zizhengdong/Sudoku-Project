from sudoku import *


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Sudoku')
screen.fill(WHITE)

bm = BoardManager(screen)
is_running = True
while is_running:
    pygame.display.flip()
    bm.draw()
    for event in pygame.event.get():
        if not bm.event_process(event):
            is_running = False

        if event.type == pygame.QUIT:
            is_running = False
pygame.quit()
