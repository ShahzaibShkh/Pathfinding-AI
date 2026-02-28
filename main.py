import pygame
import sys
from collections import deque
from queue import PriorityQueue
import math

# Initialize pygame
pygame.init()

# Constants
GRID_WIDTH = 800
PANEL_WIDTH = 250
WIDTH = GRID_WIDTH + PANEL_WIDTH
HEIGHT = 800
ROWS = 50

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (128, 128, 128)
LIGHT_GREY = (220, 220, 220)
DARK_GREY = (50, 50, 50)
TURQUOISE = (64, 224, 208)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
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

def draw_panel(win, current_algo_idx, algorithms):
    pygame.draw.rect(win, LIGHT_GREY, (GRID_WIDTH, 0, PANEL_WIDTH, HEIGHT))
    
    font = pygame.font.SysFont('Arial', 24)
    font_bold = pygame.font.SysFont('Arial', 28, bold=True)
    inst_font = pygame.font.SysFont('Arial', 24)
    
    # Title
    title = font_bold.render("Algorithms:", True, BLACK)
    win.blit(title, (GRID_WIDTH + 20, 20))
    
    # Algorithms
    for i, algo in enumerate(algorithms):
        y_pos = 70 + i * 40
        if i == current_algo_idx:
            # Highlight with a visually distinct line and arrow
            pygame.draw.rect(win, (180, 200, 255), (GRID_WIDTH + 10, y_pos - 2, PANEL_WIDTH - 20, 32))
            text = font.render(f"> {algo}", True, RED)
        else:
            text = font.render(f"  {algo}", True, BLACK)
            
        win.blit(text, (GRID_WIDTH + 20, y_pos))
        
    start_y = 70 + len(algorithms) * 40 + 40
    
    # Instructions Title
    inst_title = font_bold.render("Instructions:", True, BLACK)
    win.blit(inst_title, (GRID_WIDTH + 20, start_y))
    
    instructions = [
        "Left Click:",
        " - Place Start (Green)",
        " - Place End (Red)",
        " - Draw Walls",
        "",
        "Right Click:",
        " - Erase Nodes",
        "",
        "Click on an algorithm",
        "above to select it."
    ]
    
    for i, line in enumerate(instructions):
        text = inst_font.render(line, True, DARK_GREY)
        win.blit(text, (GRID_WIDTH + 20, start_y + 40 + i * 30))
        
    # Standard Buttons
    pygame.draw.rect(win, (150, 200, 150), (GRID_WIDTH + 20, HEIGHT - 140, PANEL_WIDTH - 40, 50))
    start_text = font.render("Start Search", True, BLACK)
    win.blit(start_text, start_text.get_rect(center=(GRID_WIDTH + PANEL_WIDTH // 2, HEIGHT - 115)))

    pygame.draw.rect(win, (200, 150, 150), (GRID_WIDTH + 20, HEIGHT - 70, PANEL_WIDTH - 40, 50))
    reset_text = font.render("Reset", True, BLACK)
    win.blit(reset_text, reset_text.get_rect(center=(GRID_WIDTH + PANEL_WIDTH // 2, HEIGHT - 45)))

def draw(win, grid, rows, grid_width, current_algo_idx, algorithms):
    win.fill(WHITE)
    
    for row in grid:
        for node in row:
            node.draw(win)
            
    draw_grid_lines(win, rows, grid_width)
    draw_panel(win, current_algo_idx, algorithms)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    x, y = pos
    row = y // gap
    col = x // gap
    return row, col

def main():
    grid = make_grid(ROWS, GRID_WIDTH)
    start = None
    end = None
    run = True
    
    algorithms = ["BFS", "DFS", "Dijkstra", "A*", "Greedy"]
    current_algo_idx = 0

    while run:
        draw(WIN, grid, ROWS, GRID_WIDTH, current_algo_idx, algorithms)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Left Click (Held down for drawing walls continuously)
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                x, y = pos
                
                # Only check grid space clicks while holding left click
                # Side Panel clicks are handled specifically below for exact clicks
                if x < GRID_WIDTH:
                    # Grid click
                    row, col = get_clicked_pos(pos, ROWS, GRID_WIDTH)
                    if row < ROWS and col < ROWS:
                        node = grid[row][col]
                        
                        if not start and node != end and not node.is_wall():
                            start = node
                            start.make_start()
                        elif not end and node != start and not node.is_wall():
                            end = node
                            end.make_end()
                        elif node != end and node != start:
                            node.make_wall()

            # Right Click (Erase)
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                x, y = pos
                
                if x < GRID_WIDTH:
                    row, col = get_clicked_pos(pos, ROWS, GRID_WIDTH)
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
                    x, y = pos
                    if x >= GRID_WIDTH:
                        # Check Algorithm clicks
                        for i, algo in enumerate(algorithms):
                            y_pos = 70 + i * 40
                            if y_pos - 2 <= y <= y_pos + 30:
                                current_algo_idx = i
                                
                        # Check Start Button
                        if HEIGHT - 140 <= y <= HEIGHT - 90:
                            if start and end:
                                clear_paths(grid)
                                for row in grid:
                                    for node in row:
                                        node.update_neighbors(grid)
                                        
                                algo_name = algorithms[current_algo_idx]
                                if algo_name == "BFS":
                                    bfs(lambda: draw(WIN, grid, ROWS, GRID_WIDTH, current_algo_idx, algorithms), grid, start, end)
                                elif algo_name == "DFS":
                                    dfs(lambda: draw(WIN, grid, ROWS, GRID_WIDTH, current_algo_idx, algorithms), grid, start, end)
                                elif algo_name == "Dijkstra":
                                    dijkstra(lambda: draw(WIN, grid, ROWS, GRID_WIDTH, current_algo_idx, algorithms), grid, start, end)
                                elif algo_name == "A*":
                                    astar(lambda: draw(WIN, grid, ROWS, GRID_WIDTH, current_algo_idx, algorithms), grid, start, end)
                                elif algo_name == "Greedy":
                                    greedy_best_first(lambda: draw(WIN, grid, ROWS, GRID_WIDTH, current_algo_idx, algorithms), grid, start, end)
                        
                        # Check Reset Button
                        elif HEIGHT - 70 <= y <= HEIGHT - 20:
                            start = None
                            end = None
                            grid = make_grid(ROWS, GRID_WIDTH)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
