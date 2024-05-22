import pygame
import heapq
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions and grid settings
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 20, 20
CELL_WIDTH = WIDTH // COLS
CELL_HEIGHT = HEIGHT // ROWS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dijkstra's Algorithm Visualization")

# Node class for Dijkstra's algorithm
class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = col * CELL_WIDTH
        self.y = row * CELL_HEIGHT
        self.color = WHITE
        self.neighbors = []
        self.distance = float('inf')
        self.previous = None
        self.wall = False

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, CELL_WIDTH, CELL_HEIGHT))

    def add_neighbors(self, grid):
        if self.row < ROWS - 1 and not grid[self.row + 1][self.col].wall:
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].wall:
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < COLS - 1 and not grid[self.row][self.col + 1].wall:
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].wall:
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return self.distance < other.distance

def dijkstra(grid, start, end):
    start.distance = 0
    pq = [(0, start)]
    visited = set()
    
    while pq:
        current_distance, current_node = heapq.heappop(pq)
        
        if current_node in visited:
            continue
        
        visited.add(current_node)
        
        if current_node == end:
            return True
        
        for neighbor in current_node.neighbors:
            if neighbor in visited or neighbor.wall:
                continue
            
            new_distance = current_node.distance + 1
            if new_distance < neighbor.distance:
                neighbor.distance = new_distance
                neighbor.previous = current_node
                heapq.heappush(pq, (new_distance, neighbor))
                
    return False

def reconstruct_path(end):
    current = end
    while current.previous:
        current = current.previous
        if current.color != GREEN:
            current.color = BLUE

def draw_grid():
    for i in range(ROWS):
        pygame.draw.line(screen, GREY, (0, i * CELL_HEIGHT), (WIDTH, i * CELL_HEIGHT))
        for j in range(COLS):
            pygame.draw.line(screen, GREY, (j * CELL_WIDTH, 0), (j * CELL_WIDTH, HEIGHT))

def main():
    grid = [[Node(i, j) for j in range(COLS)] for i in range(ROWS)]

    for row in grid:
        for node in row:
            node.add_neighbors(grid)

    start = None
    end = None
    running = True

    while running:
        screen.fill(WHITE)
        for row in grid:
            for node in row:
                node.draw()
        draw_grid()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if pygame.mouse.get_pressed()[0]:  # Left-click
                pos = pygame.mouse.get_pos()
                row, col = pos[1] // CELL_HEIGHT, pos[0] // CELL_WIDTH
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.color = GREEN
                elif not end and node != start:
                    end = node
                    end.color = RED
                elif node != end and node != start:
                    node.wall = True
                    node.color = BLACK
            elif pygame.mouse.get_pressed()[2]:  # Right-click
                pos = pygame.mouse.get_pos()
                row, col = pos[1] // CELL_HEIGHT, pos[0] // CELL_WIDTH
                node = grid[row][col]
                node.wall = False
                node.color = WHITE
                if node == start:
                    start = None
                elif node == end:
                    end = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.add_neighbors(grid)
                    dijkstra(grid, start, end)
                    reconstruct_path(end)
                if event.key == pygame.K_r:
                    start = None
                    end = None
                    grid = [[Node(i, j) for j in range(COLS)] for i in range(ROWS)]
                    for row in grid:
                        for node in row:
                            node.add_neighbors(grid)

if __name__ == "__main__":
    main()
