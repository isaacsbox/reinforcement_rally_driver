from utils import *
from PIL import Image
import numpy as np

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drawing Program")


def init_grid(rows, cols, color):
    grid = []

    for i in range(rows):
        grid.append([])
        for _ in range(cols):
            grid[i].append(color)

    return grid


def draw_grid(win, grid):
    for i, row in enumerate(grid):
        for j, pixel in enumerate(row):
            pygame.draw.rect(win, pixel, (j * PIXEL_SIZE, i *
                                          PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))

    if DRAW_GRID_LINES:
        for i in range(ROWS + 1):
            pygame.draw.line(win, BLACK, (0, i * PIXEL_SIZE),
                             (WIDTH, i * PIXEL_SIZE))

        for i in range(COLS + 1):
            pygame.draw.line(win, BLACK, (i * PIXEL_SIZE, 0),
                             (i * PIXEL_SIZE, HEIGHT - TOOLBAR_HEIGHT))


def draw(win, grid, buttons):
    win.fill(BG_COLOR)
    draw_grid(win, grid)

    for button in buttons:
        button.draw(win)

    pygame.display.update()


def get_row_col_from_pos(pos):
    x, y = pos
    row = y // PIXEL_SIZE
    col = x // PIXEL_SIZE

    if row >= ROWS:
        raise IndexError

    return row, col


run = True
clock = pygame.time.Clock()
grid = init_grid(ROWS, COLS, BG_COLOR)
drawing_color = BLACK

button_y = HEIGHT - TOOLBAR_HEIGHT/2 - 25
buttons = [
    Button(10, button_y, 50, 50, BLACK),
    Button(250, button_y, 50, 50, WHITE, "Erase", BLACK),
    Button(310, button_y, 50, 50, WHITE, "Clear", BLACK)
]

while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()

            try:
                row, col = get_row_col_from_pos(pos)
                grid[row + 1][col] = drawing_color
                grid[row][col + 1] = drawing_color
                grid[row][col - 1] = drawing_color
                grid[row - 1][col] = drawing_color
                grid[row][col] = drawing_color

            except IndexError:
                for button in buttons:
                    if not button.clicked(pos):
                        continue

                    drawing_color = button.color
                    if button.text == "Clear":
                        grid = init_grid(ROWS, COLS, BG_COLOR)
                        drawing_color = BLACK

draw(WIN, grid, buttons)

# Creates a random image 100*100 
for j in range(COLS):
    for i in range(ROWS):
        print(grid[j][i] == (255, 255, 255))
        if grid[i][j] == (255, 255, 255):
            grid[i][j] = 255
        else:
            grid[i][j] = 0
            

mat = np.array(grid)
print(mat)

# Creates PIL image
img = Image.fromarray(mat)
img.show()


pygame.quit()
