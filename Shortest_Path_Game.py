import pygame
import pygame_menu
import heapq
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions and grid settings
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 20, 20
CELL_WIDTH = WIDTH // COLS
CELL_HEIGHT = HEIGHT // ROWS

# Fonts
FONT = pygame.font.SysFont('comic_sans', 24)
BIG_FONT = pygame.font.SysFont('comic_sans', 36)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinding Adventure")


# Node class for Dijkstra's algorithm
class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = col * CELL_WIDTH
        self.y = row * CELL_HEIGHT
        self.color = "#ffffff"
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
        if current.color != "#00ff99" and current.color != "#ff0000":
            current.color = "#edffba"


def draw_grid():
    for i in range(ROWS):
        pygame.draw.line(screen, "#8c8c8c", (0, i * CELL_HEIGHT), (WIDTH, i * CELL_HEIGHT))
        for j in range(COLS):
            pygame.draw.line(screen, "#8c8c8c", (j * CELL_WIDTH, 0), (j * CELL_WIDTH, HEIGHT))


def start_the_game():
    grid = [[Node(i, j) for j in range(COLS)] for i in range(ROWS)]

    for row in grid:
        for node in row:
            node.add_neighbors(grid)

    start = random.choice(random.choice(grid))
    end = random.choice(random.choice(grid))


    while end == start:
        end = random.choice(random.choice(grid))

    start.color = "#00ff99"
    end.color = "#ff0000"

    block_counter = 0  # Counter for user-placed blocks
    path_length_dijkstra = 0  # Counter for shortes path

    # flags
    dijkstra_was_calculated = False
    game_ended = False
    player_wins = False

    running = True

    while running:
        screen.fill("#ffffff")
        for row in grid:
            for node in row:
                node.draw()
        draw_grid()

        # Display block counter
        block_text = FONT.render("Blocks placed: " + str(block_counter), True, (0, 0, 0))
        screen.blit(block_text, (10, 10))

        if dijkstra_was_calculated:
            # Display the length of the shortest path
            length_text = FONT.render("Shortest path length: " + str(path_length_dijkstra - 1), True, (0, 0, 0))
            screen.blit(length_text, (520, 10))

        pygame.display.update()

        if game_ended:
            if player_wins:
                pygame_menu.events.PAUSE = True
                win_text = BIG_FONT.render("Congratulations! :)", True, (0, 255, 0))
                win_text2 = BIG_FONT.render("You beat the computer", True, (0, 255, 0))

                screen.blit(win_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
                screen.blit(win_text2, (WIDTH // 2 - 200, HEIGHT // 2))

                pygame.time.wait(2000)

                pygame.display.update()
            else:
                pygame_menu.events.PAUSE = True
                lose_text = BIG_FONT.render("You Lose! :(", True, (255, 0, 0))
                lose_text2 = BIG_FONT.render("The computer won", True, (255, 0, 0))
                screen.blit(lose_text, (WIDTH // 2 - 80, HEIGHT // 2 - 50))
                screen.blit(lose_text2, (WIDTH // 2 - 150, HEIGHT // 2))

                pygame.display.update()

                pygame.time.wait(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if pygame.mouse.get_pressed()[0]:  # Left-click
                pos = pygame.mouse.get_pos()
                row, col = pos[1] // CELL_HEIGHT, pos[0] // CELL_WIDTH
                node = grid[row][col]
                if node != start and node != end and not node.wall:
                    node.wall = True
                    node.color = "#000000"
                    block_counter += 1
            elif pygame.mouse.get_pressed()[2]:  # Right-click
                pos = pygame.mouse.get_pos()
                row, col = pos[1] // CELL_HEIGHT, pos[0] // CELL_WIDTH
                node = grid[row][col]
                if node != start and node != end and node.wall:
                    node.wall = False
                    node.color = "#ffffff"
                    block_counter -= 1  # Decrement block counter
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for row in grid:
                        for node in row:
                            node.add_neighbors(grid)
                    if dijkstra(grid, start, end):
                        reconstruct_path(end)
                        # Calculate the length of the shortest path
                        current = end
                        while current.previous:
                            path_length_dijkstra += 1
                            current = current.previous

                        dijkstra_was_calculated = True
                        game_ended = True
                        player_wins = True if block_counter == path_length_dijkstra - 1 else False  # assumes that the shortest path will always be found by the computer
                if event.key == pygame.K_r:
                    start_the_game()


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
    menu = pygame_menu.Menu('Pathfinding Adventure', WIDTH, HEIGHT, theme=theme)
    menu.add.label("Your task is to find the shortest path between")
    menu.add.label("the red and the green block! Try to find the shortest")
    menu.add.label("path and beat the computer.")

    menu.add.label(" ")
    menu.add.label("Instructions:")
    menu.add.label("Left-click on cells to create walls (black).")
    menu.add.label("Right-click on cells to remove walls.")
    menu.add.label("Press SPACE to find the shortest path (blue).")
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
