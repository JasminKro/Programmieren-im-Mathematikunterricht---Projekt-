import pygame
import pygame_menu
import heapq
import sys
import random
from collections import deque

# Initialize Pygame
pygame.init()

# Screen dimensions and grid settings
GRID_WIDTH, GRID_HEIGHT = 800, 800
INFO_HEIGHT = 100
TOTAL_WIDTH, TOTAL_HEIGHT = GRID_WIDTH, GRID_HEIGHT + INFO_HEIGHT
ROWS, COLS = 20, 20
CELL_WIDTH = GRID_WIDTH // COLS
CELL_HEIGHT = GRID_HEIGHT // ROWS

# Fonts
FONT = pygame.font.SysFont('Segoe UI Emoji', 20)  # Smaller font size for status bar
BIG_FONT = pygame.font.SysFont('Segoe UI Emoji', 36)
END_FONT = pygame.font.SysFont('Segoe UI Emoji', 20)

# Colors
WHITE = "#ffffff"
BLACK = "#000000"
GREEN = "#00ff99"
RED = "#ff0000"
YELLOW = "#edffba"
OBSTACLE_COLOR = "#a9a9a9"  # Gray color for obstacles
INFO_BACKGROUND = "#dcdcdc"  # Light gray for info area background

# Initialize the screen
screen = pygame.display.set_mode((TOTAL_WIDTH, TOTAL_HEIGHT))
pygame.display.set_caption("Pathfinding Adventure")

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
        self.player_wall = False  # New attribute to mark player-placed walls

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, CELL_WIDTH, CELL_HEIGHT))

    def add_neighbors(self, grid):
        self.neighbors = []
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

# Function calculating the shortest path (returns true, if a shortest path was found)
def dijkstra(grid, start, end):
    for row in grid:
        for node in row:
            node.distance = float('inf')
            node.previous = None

    start.distance = 0
    pq = [(0, start)]
    visited = set()

    while pq:
        current_distance, current_node = heapq.heappop(pq)

        if current_node == end:
            return True

        visited.add(current_node)

        for neighbor in current_node.neighbors:
            if neighbor in visited or neighbor.wall:
                continue

            new_distance = current_distance + 1

            if new_distance < neighbor.distance:
                neighbor.distance = new_distance
                neighbor.previous = current_node
                heapq.heappush(pq, (new_distance, neighbor))

    return False

# Draw the shortest path on grid
def reconstruct_path(end):
    current = end
    length = 0
    while current.previous:
        current = current.previous
        length += 1
        if current.color not in [GREEN, RED]:
            current.color = YELLOW
    return length

# Draw a grid with specified dimensions
def draw_grid():
    for i in range(ROWS):
        pygame.draw.line(screen, "#8c8c8c", (0, i * CELL_HEIGHT), (GRID_WIDTH, i * CELL_HEIGHT))
        for j in range(COLS):
            pygame.draw.line(screen, "#8c8c8c", (j * CELL_WIDTH, 0), (j * CELL_WIDTH, GRID_HEIGHT))

def game_end(player_wins):
    if player_wins:
        display_message("Congratulations!", "You found the shortest path! 🏆😊", (0, 255, 0), (0, 255, 0), 5)
    else:
        display_message("You Lose! 😔🏳️", "The computer found a better path.", (255, 0, 0), (255, 0, 0), 5)

# Function to display a message in a separate window with countdown
def display_message(message1, message2, color1, color2, countdown):
    # Create a new window for the message
    message_screen = pygame.display.set_mode((TOTAL_WIDTH, TOTAL_HEIGHT))
    pygame.display.set_caption("Game Result")

    # Timer for countdown
    start_ticks = pygame.time.get_ticks()

    running = True
    while running:
        seconds = (pygame.time.get_ticks() - start_ticks) // 1000  # Calculate how many seconds passed
        remaining_time = countdown - seconds

        # Render the messages
        message_text1 = BIG_FONT.render(message1, True, color1)
        message_text2 = BIG_FONT.render(message2, True, color2)
        countdown_text = BIG_FONT.render(f"Results shown in {remaining_time}...", True, (255, 255, 255))

        # Fill the background with black
        message_screen.fill("#a6d7ff")

        # Blit the messages onto the screen
        message_screen.blit(message_text1, (GRID_WIDTH // 2 - 300, GRID_HEIGHT // 2 - 50))
        message_screen.blit(message_text2, (GRID_WIDTH // 2 - 300, GRID_HEIGHT // 2))
        message_screen.blit(countdown_text, (GRID_WIDTH // 2 - 300, GRID_HEIGHT // 2 + 50))

        # Update the display
        pygame.display.update()

        # Check if countdown has reached zero
        if remaining_time <= 0:
            running = False

def are_neighbors(node1, node2):
    return (node1.row == node2.row and abs(node1.col - node2.col) == 1) or (node1.col == node2.col and abs(node1.row - node2.row) == 1)

# Function to place random obstacles
def place_random_obstacles(grid, num_obstacles, points):
    obstacles = 0
    while obstacles < num_obstacles:
        row = random.randint(0, ROWS - 2)  # Ensure there's space for a 2x2 obstacle
        col = random.randint(0, COLS - 2)
        nodes = [grid[row][col], grid[row+1][col], grid[row][col+1], grid[row+1][col+1]]
        if all(node not in points and not node.wall for node in nodes):
            for node in nodes:
                node.wall = True
                node.color = OBSTACLE_COLOR
            obstacles += 1

# Function to start the game
def start_the_game():
    global grid
    grid = [[Node(i, j) for j in range(COLS)] for i in range(ROWS)]

    for row in grid:
        for node in row:
            node.add_neighbors(grid)

    # Set the start and end blocks randomly
    start = random.choice(random.choice(grid))
    end = random.choice(random.choice(grid))

    while end == start or are_neighbors(end, start):
        end = random.choice(random.choice(grid))

    start.color = GREEN
    end.color = RED

    points = [start, end]

    # Place random obstacles
    num_obstacles = random.randint(5, 15)  # Adjust the range as needed
    place_random_obstacles(grid, num_obstacles, points)

    # Counter
    block_counter = 0  # Counter for user-placed blocks
    path_length_dijkstra = 0 # Counter for shortest path

    # Flags that trigger events
    dijkstra_was_calculated = False
    game_ended = False
    player_wins = False

    running = True

    while running:
        screen.fill(WHITE)
        screen.fill(INFO_BACKGROUND, (0, GRID_HEIGHT, TOTAL_WIDTH, INFO_HEIGHT))  # Info background
        for row in grid:
            for node in row:
                node.draw()
        draw_grid()

        # Display block counter and evaluation prompt
        if not dijkstra_was_calculated:
            block_text = FONT.render("Blocks placed: " + str(block_counter), True, (0, 0, 0))
            screen.blit(block_text, (10, GRID_HEIGHT + 10))
            evaluation_text = FONT.render("<space> for evaluating my solution", True, (0, 0, 0))
            screen.blit(evaluation_text, (10, GRID_HEIGHT + 40))
        else:
            comparison_text = FONT.render("Your solution compared to the solution of Dijkstra's Algorithm:", True, (0, 0, 0))
            block_vs_length_text = FONT.render(f"Blocks placed: {block_counter} vs. Shortest path length: {path_length_dijkstra}", True, (0, 0, 0))
            reset_text = FONT.render("Press R to reset the game and start a new one", True, (0, 0, 0))
            screen.blit(comparison_text, (10, GRID_HEIGHT + 10))
            screen.blit(block_vs_length_text, (10, GRID_HEIGHT + 40))
            screen.blit(reset_text, (10, GRID_HEIGHT + 70))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Terminate program
                running = False
                pygame.quit()
                sys.exit()
            if pygame.mouse.get_pressed()[0]:  # Left-click (set block)
                pos = pygame.mouse.get_pos()
                if pos[1] < GRID_HEIGHT:
                    row, col = pos[1] // CELL_HEIGHT, pos[0] // CELL_WIDTH
                    node = grid[row][col]
                    if node != start and node != end and not node.wall:
                        if not node.player_wall:
                            node.player_wall = True  # Mark as player-placed wall
                            node.color = BLACK
                            block_counter += 1
            elif pygame.mouse.get_pressed()[2]:  # Right-click (remove block)
                pos = pygame.mouse.get_pos()
                if pos[1] < GRID_HEIGHT:
                    row, col = pos[1] // CELL_HEIGHT, pos[0] // CELL_WIDTH
                    node = grid[row][col]
                    if node != start and node != end and node.player_wall:
                        node.wall = False
                        node.player_wall = False  # Unmark as player-placed wall
                        node.color = WHITE
                        block_counter -= 1  # Decrement block counter
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: # Display shortest path
                    path_length_dijkstra = 0
                    if player_path_valid(grid, start, end):
                        if dijkstra(grid, start, end):
                            path_length_dijkstra = reconstruct_path(end) - 1  # Subtract 1 to exclude start or end node
                            dijkstra_was_calculated = True
                            game_ended = True
                            player_wins = block_counter <= path_length_dijkstra  # Player wins if they use fewer or equal blocks
                            game_end(player_wins)
                    else:
                        display_message("Invalid Path!", "Please ensure your path connects the green and red blocks.", (255, 0, 0), (255, 0, 0), 3)

                if event.key == pygame.K_r: # Reset game
                    start_the_game()

def player_path_valid(grid, start, end):
    visited = set()
    queue = deque([start])

    while queue:
        current = queue.popleft()
        if current == end:
            return True
        visited.add(current)

        neighbors = []
        if current.row < ROWS - 1 and (grid[current.row + 1][current.col].player_wall or grid[current.row + 1][current.col] == end):
            neighbors.append(grid[current.row + 1][current.col])
        if current.row > 0 and (grid[current.row - 1][current.col].player_wall or grid[current.row - 1][current.col] == end):
            neighbors.append(grid[current.row - 1][current.col])
        if current.col < COLS - 1 and (grid[current.row][current.col + 1].player_wall or grid[current.row][current.col + 1] == end):
            neighbors.append(grid[current.row][current.col + 1])
        if current.col > 0 and (grid[current.row][current.col - 1].player_wall or grid[current.row][current.col - 1] == end):
            neighbors.append(grid[current.row][current.col - 1])

        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return False

def main():
    # General menu settings
    theme = pygame_menu.themes.THEME_SOLARIZED.copy()
    theme.title_font = pygame_menu.font.FONT_COMIC_NEUE
    theme.title_font_size = 50
    theme.widget_font = pygame_menu.font.FONT_COMIC_NEUE
    theme.widget_font_size = 30
    theme.background_color = "#a6d7ff"
    theme.title_background_color = "#3a78ab"
    theme.title_font_color = "#000000"
    theme.widget_font_color = "#000000"
    theme.selection_color = "#ff0000"

    # Create the menu with instructions
    menu = pygame_menu.Menu('Pathfinding Adventure', TOTAL_WIDTH, TOTAL_HEIGHT, theme=theme)
    menu.add.label("Your task is to find the shortest path between")
    menu.add.label("the green and red blocks! Try to find the shortest")
    menu.add.label("path and beat the computer.")

    menu.add.label(" ")
    menu.add.label("Instructions:")
    menu.add.label("Left-click on cells to create walls (black).")
    menu.add.label("Right-click on cells to remove walls.")
    menu.add.label("Press SPACE to find the shortest path (yellow).")
    menu.add.label("Press 'R' to reset the grid.")
    menu.add.button('Start Game', start_the_game)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    # Main loop
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if menu.is_enabled():
            menu.update(events)
            menu.draw(screen)

        pygame.display.update()

if __name__ == "__main__":
    main()
