import pygame
from game import Game
from renderer import Renderer

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 640

# Create screen
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Lian Lian Kan")

# Create game and renderer instances
game = Game()
renderer = Renderer(screen)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                # Get mouse position
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Get shape at mouse position
                shape_info = game.get_shape_at(mouse_x, mouse_y)
                if shape_info:
                    grid_x, grid_y, shape = shape_info
                    # Select the cell
                    game.select_cell(grid_x, grid_y)
                    # Start timer if not already started
                    game.start_timer(pygame.time.get_ticks())
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                # Reset game
                game.reset()
    
    # Update game state
    game.update_time(pygame.time.get_ticks())
    
    # Render
    renderer.render(game)
    
    # Cap FPS
    clock.tick(60)

# Quit Pygame
pygame.quit()
