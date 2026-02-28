import pygame
import sys
from collections import deque
from queue import PriorityQueue
import math

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

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def h_euclidean(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def greedy_best_first(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    visited = {start}
    
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        current = open_set.get()[2]
        
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True
            
        for neighbor in current.neighbors:
            if neighbor not in visited:
                came_from[neighbor] = current
                visited.add(neighbor)
                count += 1
                open_set.put((h_euclidean(neighbor.get_pos(), end.get_pos()), count, neighbor))
                if neighbor != end:
                    neighbor.make_open()
                        
        draw()
        
        if current != start and current != end:
            current.make_closed()
            
    return False

def astar(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())
    
    open_set_hash = {start}
    
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        current = open_set.get()[2]
        open_set_hash.remove(current)
        
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True
            
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1
            
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    if neighbor != end:
                        neighbor.make_open()
                        
        draw()
        
        if current != start and current != end:
            current.make_closed()
            
    return False

def dijkstra(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    
    open_set_hash = {start}
    
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        current = open_set.get()[2]
        open_set_hash.remove(current)
        
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True
            
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1
            
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((g_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    if neighbor != end:
                        neighbor.make_open()
                        
        draw()
        
        if current != start and current != end:
            current.make_closed()
            
    return False

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

def draw_buttons(win, current_algo):
    pygame.draw.rect(win, LIGHT_GREY, (0, HEIGHT, WIDTH, BUTTON_HEIGHT))
    font = pygame.font.SysFont('Arial', 32)
    
    # Button 1: Toggle Algorithm
    pygame.draw.rect(win, (150, 150, 200), (0, HEIGHT, WIDTH//3, BUTTON_HEIGHT))
    text_algo = font.render(f'Algo: {current_algo}', True, BLACK)
    win.blit(text_algo, text_algo.get_rect(center=(WIDTH//6, HEIGHT + BUTTON_HEIGHT // 2)))

    # Button 2: Start
    pygame.draw.rect(win, (150, 200, 150), (WIDTH//3, HEIGHT, WIDTH//3, BUTTON_HEIGHT))
    text_start = font.render('Start Search', True, BLACK)
    win.blit(text_start, text_start.get_rect(center=(WIDTH//2, HEIGHT + BUTTON_HEIGHT // 2)))

    # Button 3: Reset
    pygame.draw.rect(win, (200, 150, 150), (2*WIDTH//3, HEIGHT, WIDTH//3, BUTTON_HEIGHT))
    text_reset = font.render('Reset', True, BLACK)
    win.blit(text_reset, text_reset.get_rect(center=(5*WIDTH//6, HEIGHT + BUTTON_HEIGHT // 2)))

def draw(win, grid, rows, width, current_algo):
    win.fill(WHITE)
    
    for row in grid:
        for node in row:
            node.draw(win)
            
    draw_grid_lines(win, rows, width)
    draw_buttons(win, current_algo)
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
    
    algorithms = ["BFS", "DFS", "Dijkstra", "A*", "Greedy"]
    current_algo_idx = 0

    while run:
        draw(WIN, grid, ROWS, WIDTH, algorithms[current_algo_idx])
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Left Click
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                
                # Check for buttons click
                if pos[1] >= HEIGHT:
                    if pos[0] < WIDTH // 3:
                        # Toggle Mode
                        # To debounce the click, we can wait until mouse button goes up or just process one toggle per click event
                        # But since it's checking in the loop it might flicker if held.
                        # We should process button clicks only on MOUSEBUTTONDOWN to avoid rapid toggling
                        pass
                    elif pos[0] < 2 * WIDTH // 3:
                        # Start Search
                        pass
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
                            
            # Process MOUSEBUTTONDOWN for buttons to avoid rapid triggering if held
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if pos[1] >= HEIGHT:
                        if pos[0] < WIDTH // 3:
                            # Toggle Mode
                            current_algo_idx = (current_algo_idx + 1) % len(algorithms)
                        elif pos[0] < 2 * WIDTH // 3:
                            # Start Search
                            if start and end:
                                clear_paths(grid)
                                for row in grid:
                                    for node in row:
                                        node.update_neighbors(grid)
                                        
                                algo_name = algorithms[current_algo_idx]
                                if algo_name == "BFS":
                                    bfs(lambda: draw(WIN, grid, ROWS, WIDTH, algo_name), grid, start, end)
                                elif algo_name == "DFS":
                                    dfs(lambda: draw(WIN, grid, ROWS, WIDTH, algo_name), grid, start, end)
                                elif algo_name == "Dijkstra":
                                    dijkstra(lambda: draw(WIN, grid, ROWS, WIDTH, algo_name), grid, start, end)
                                elif algo_name == "A*":
                                    astar(lambda: draw(WIN, grid, ROWS, WIDTH, algo_name), grid, start, end)
                                elif algo_name == "Greedy":
                                    greedy_best_first(lambda: draw(WIN, grid, ROWS, WIDTH, algo_name), grid, start, end)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
