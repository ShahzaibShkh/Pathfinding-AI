import pygame
import sys
from collections import deque

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
TURQUOISE = (64, 224, 208)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)

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
        self.neighbors = []

    def get_pos(self):
        return self.row, self.col

    def is_wall(self):
        return self.color == BLACK

    def make_start(self):
        self.color = GREEN

    def make_closed(self):
        self.color = TURQUOISE

    def make_open(self):
        self.color = PURPLE

    def make_wall(self):
        self.color = BLACK

    def make_end(self):
        self.color = RED

    def make_path(self):
        self.color = YELLOW

    def reset(self):
        self.color = WHITE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
        
    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_wall(): # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_wall(): # UP
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_wall(): # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_wall(): # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        if current.color != GREEN:
            current.make_path()
        draw()

def bfs(draw, grid, start, end):
    queue = deque([start])
    came_from = {}
    visited = {start}
    
    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        current = queue.popleft()
        
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True
            
        for neighbor in current.neighbors:
            if neighbor not in visited:
                came_from[neighbor] = current
                visited.add(neighbor)
                queue.append(neighbor)
                if neighbor != end:
                    neighbor.make_open()
                
        draw()
        
        if current != start and current != end:
            current.make_closed()
            
    return False

def dfs(draw, grid, start, end):
    stack = [start]
    came_from = {}
    visited = {start}
    
    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        current = stack.pop()
        
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True
            
        for neighbor in current.neighbors:
            if neighbor not in visited:
                came_from[neighbor] = current
                visited.add(neighbor)
                stack.append(neighbor)
                if neighbor != end:
                    neighbor.make_open()
                
        draw()
        
        if current != start and current != end:
            current.make_closed()
            
    return False

def clear_paths(grid):
    for row in grid:
        for node in row:
            if node.color in [TURQUOISE, PURPLE, YELLOW]:
                node.reset()

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

def draw_buttons(win):
    pygame.draw.rect(win, LIGHT_GREY, (0, HEIGHT, WIDTH, BUTTON_HEIGHT))
    font = pygame.font.SysFont('Arial', 32)
    
    # Button 1: BFS
    pygame.draw.rect(win, (150, 150, 200), (0, HEIGHT, WIDTH//3, BUTTON_HEIGHT))
    text_bfs = font.render('Run BFS', True, BLACK)
    win.blit(text_bfs, text_bfs.get_rect(center=(WIDTH//6, HEIGHT + BUTTON_HEIGHT // 2)))

    # Button 2: DFS
    pygame.draw.rect(win, (150, 200, 150), (WIDTH//3, HEIGHT, WIDTH//3, BUTTON_HEIGHT))
    text_dfs = font.render('Run DFS', True, BLACK)
    win.blit(text_dfs, text_dfs.get_rect(center=(WIDTH//2, HEIGHT + BUTTON_HEIGHT // 2)))

    # Button 3: Reset
    pygame.draw.rect(win, (200, 150, 150), (2*WIDTH//3, HEIGHT, WIDTH//3, BUTTON_HEIGHT))
    text_reset = font.render('Reset', True, BLACK)
    win.blit(text_reset, text_reset.get_rect(center=(5*WIDTH//6, HEIGHT + BUTTON_HEIGHT // 2)))

def draw(win, grid, rows, width):
    win.fill(WHITE)
    
    for row in grid:
        for node in row:
            node.draw(win)
            
    draw_grid_lines(win, rows, width)
    draw_buttons(win)
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

            # Left Click
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                
                # Check for buttons click
                if pos[1] >= HEIGHT:
                    if pos[0] < WIDTH // 3:
                        # BFS
                        if start and end:
                            clear_paths(grid)
                            for row in grid:
                                for node in row:
                                    node.update_neighbors(grid)
                            bfs(lambda: draw(WIN, grid, ROWS, WIDTH), grid, start, end)
                    elif pos[0] < 2 * WIDTH // 3:
                        # DFS
                        if start and end:
                            clear_paths(grid)
                            for row in grid:
                                for node in row:
                                    node.update_neighbors(grid)
                            dfs(lambda: draw(WIN, grid, ROWS, WIDTH), grid, start, end)
                    else:
                        # Reset
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
