import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 800
BUTTON_HEIGHT = 60
ROWS = 50

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (128, 128, 128)
LIGHT_GREY = (200, 200, 200)

WIN = pygame.display.set_mode((WIDTH, HEIGHT + BUTTON_HEIGHT))
pygame.display.set_caption("Pathfinding Visualizer")

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = col * width
        self.y = row * width
        self.color = WHITE
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def make_start(self):
        self.color = GREEN

    def make_end(self):
        self.color = RED

    def make_wall(self):
        self.color = BLACK

    def reset(self):
        self.color = WHITE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid

def draw_grid_lines(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw_button(win):
    pygame.draw.rect(win, LIGHT_GREY, (0, HEIGHT, WIDTH, BUTTON_HEIGHT))
    font = pygame.font.SysFont('Arial', 32)
    text = font.render('Reset', True, BLACK)
    # Center the text
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT + BUTTON_HEIGHT // 2))
    win.blit(text, text_rect)

def draw(win, grid, rows, width):
    win.fill(WHITE)
    
    for row in grid:
        for node in row:
            node.draw(win)
            
    draw_grid_lines(win, rows, width)
    draw_button(win)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    x, y = pos
    row = y // gap
    col = x // gap
    return row, col

def main():
    grid = make_grid(ROWS, WIDTH)
    start = None
    end = None
    run = True

    while run:
        draw(WIN, grid, ROWS, WIDTH)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Left Click (Draw Start, End, Walls)
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                
                # Check for Reset button click
                if pos[1] >= HEIGHT:
                    start = None
                    end = None
                    grid = make_grid(ROWS, WIDTH)
                    continue
                
                # Grid click
                row, col = get_clicked_pos(pos, ROWS, WIDTH)
                if row < ROWS and col < ROWS:
                    node = grid[row][col]
                    
                    if not start and node != end:
                        start = node
                        start.make_start()
                    elif not end and node != start:
                        end = node
                        end.make_end()
                    elif node != end and node != start:
                        node.make_wall()

            # Right Click (Erase)
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                
                if pos[1] < HEIGHT:
                    row, col = get_clicked_pos(pos, ROWS, WIDTH)
                    if row < ROWS and col < ROWS:
                        node = grid[row][col]
                        node.reset()
                        if node == start:
                            start = None
                        elif node == end:
                            end = None

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
