''' 
Pathfinding Adventure Game
Authors: Philip Hallwirth, Jasmin Kropshofer, Manfred Trauner

This program implements a simple pathfinding adventure game using Pygame. 
The player's task is to find the shortest path between a red and a green block. 
The game allows the player to place blocks, remove obstacles, and calculate the 
shortest path using Dijkstra's algorithm.

Dependencies:
- Pygame
- Pygame Menu

'''

# import needed libraries
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
FONT = pygame.font.SysFont('Segoe UI Emoji', 24)
BIG_FONT = pygame.font.SysFont('Segoe UI Emoji', 36)

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

# Function calculating the shortest path (returns true, if a shortest path was found)
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
            return True # we found a path from start to end
        
        for neighbor in current_node.neighbors:
            if neighbor in visited: 
                continue # ignore all nodes, I´ve already visited
            
            new_distance = current_node.distance + 1
            if new_distance < neighbor.distance:
                neighbor.distance = new_distance
                neighbor.previous = current_node
                heapq.heappush(pq, (new_distance, neighbor))
                
    return False

# Draw the shortest path on grid
def reconstruct_path(end):
    current = end
    while current.previous:
        current = current.previous
        if current.color != "#00ff99" and current.color != "#ff0000": # dont overwrite the start- and end-block
            current.color = "#edffba" # draw the path

# Draw a grid with specified dimensions
def draw_grid():
    for i in range(ROWS):
        pygame.draw.line(screen, "#8c8c8c", (0, i * CELL_HEIGHT), (WIDTH, i * CELL_HEIGHT))
        for j in range(COLS):
            pygame.draw.line(screen, "#8c8c8c", (j * CELL_WIDTH, 0), (j * CELL_WIDTH, HEIGHT))

def game_end(player_wins):
    if player_wins:
        display_message("Congratulations!", "You found the shortest path! 😊", (0, 255, 0), (0, 255, 0))
    else:
        display_message("You Lose! 😔", "The computer found a shorter path.", (255, 0, 0), (255, 0, 0))

# Function to display a message in a separate window
def display_message(message1, message2, color1, color2):
    # Create a new window for the message
    message_screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game Result")

    # Render the messages
    message_text1 = BIG_FONT.render(message1, True, color1)
    message_text2 = BIG_FONT.render(message2, True, color2)

    # Fill the background with black
    message_screen.fill((0, 0, 0))

    # Blit the messages onto the screen
    message_screen.blit(message_text1, (WIDTH // 2 - 300, HEIGHT // 2 - 50))
    message_screen.blit(message_text2, (WIDTH // 2 - 300, HEIGHT // 2))

    # Update the display
    pygame.display.update()

    # Wait for a few seconds before closing
    pygame.time.wait(2000)

    start_the_game()

# Function to start the game
def start_the_game():
    grid = [[Node(i, j) for j in range(COLS)] for i in range(ROWS)]

    for row in grid:
        for node in row:
            node.add_neighbors(grid)

    # Set the start- and end-block randomly
    start = random.choice(random.choice(grid))
    end = random.choice(random.choice(grid))
    
    while end == start:
        end = random.choice(random.choice(grid))

    start.color = "#00ff99"
    end.color = "#ff0000"

    # Counter 
    block_counter = 0  # Counter for user-placed blocks
    path_length_dijkstra = 0 # Counter for shortes path

    # Flags that trigger events 
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
                win_text = BIG_FONT.render("Congratulations!", True, (0, 255, 0))
                win_text2 = BIG_FONT.render("You found the shortest path!😊", True, (0, 255, 0))

                screen.blit(win_text, (WIDTH // 2 - 300, HEIGHT // 2 - 50))
                screen.blit(win_text2, (WIDTH // 2 - 300, HEIGHT // 2))

                pygame.display.update()

                pygame.time.wait(2000)  
            else:
                pygame_menu.events.PAUSE = True
                lose_text = BIG_FONT.render("You Lose! 😔", True, (255, 0, 0))
                lose_text2 = BIG_FONT.render("The computer found a shorter path", True, (255, 0, 0))
                screen.blit(lose_text, (WIDTH // 2 - 80, HEIGHT // 2 - 50))
                screen.blit(lose_text2, (WIDTH // 2 - 150, HEIGHT // 2))

                pygame.display.update()
                
                pygame.time.wait(2000) 

        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Terminate program
                running = False
                pygame.quit()
                sys.exit()
            if pygame.mouse.get_pressed()[0]:  # Left-click (set block)
                pos = pygame.mouse.get_pos()
                row, col = pos[1] // CELL_HEIGHT, pos[0] // CELL_WIDTH
                node = grid[row][col]
                if node != start and node != end and not node.wall:
                    node.wall = True
                    node.color = "#000000"
                    block_counter += 1
            elif pygame.mouse.get_pressed()[2]:  # Right-click (remove block)
                pos = pygame.mouse.get_pos()
                row, col = pos[1] // CELL_HEIGHT, pos[0] // CELL_WIDTH
                node = grid[row][col]
                if node != start and node != end and node.wall:
                    node.wall = False
                    node.color = "#ffffff"
                    block_counter -= 1  # Decrement block counter
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: # Display shortest path
                    for row in grid:
                        for node in row:
                            node.add_neighbors(grid)
                    if dijkstra(grid, start, end): # A shortest path was found
                        reconstruct_path(end) # Draw the path on grid 

                        # Calculate the length of the shortest path
                        current = end
                        while current.previous:
                            path_length_dijkstra += 1
                            current = current.previous

                        dijkstra_was_calculated = True
                        game_ended = True 
                        player_wins= True if block_counter == path_length_dijkstra - 1 else False # Assumes that the shortest path will always be found by the computer
                        game_end(player_wins)

                if event.key == pygame.K_r: # Reset game
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
