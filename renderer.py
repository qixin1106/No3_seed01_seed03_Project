import pygame
from game import Game, GRID_SIZE, CELL_SIZE, CELL_SPACING, WINDOW_SIZE, BACKGROUND_COLOR, CELL_COLOR, SELECTED_BORDER_COLOR, SELECTED_BORDER_WIDTH

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)

    def draw_background(self):
        """Draw the background"""
        self.screen.fill(BACKGROUND_COLOR)

    def draw_grid(self, game):
        """Draw the game grid"""
        # Calculate grid position to center it
        grid_width = GRID_SIZE * (CELL_SIZE + CELL_SPACING) - CELL_SPACING
        grid_height = GRID_SIZE * (CELL_SIZE + CELL_SPACING) - CELL_SPACING
        start_x = (WINDOW_SIZE - grid_width) // 2
        start_y = (WINDOW_SIZE - grid_height) // 2
        
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                # Calculate cell position
                x = start_x + col * (CELL_SIZE + CELL_SPACING)
                y = start_y + row * (CELL_SIZE + CELL_SPACING)
                
                # Draw cell background
                pygame.draw.rect(self.screen, CELL_COLOR, (x, y, CELL_SIZE, CELL_SIZE))
                
                # Draw selected border if cell is selected
                if game.selected == (col, row):
                    pygame.draw.rect(self.screen, SELECTED_BORDER_COLOR, (x, y, CELL_SIZE, CELL_SIZE), SELECTED_BORDER_WIDTH)
                
                # Draw shape if cell is not matched
                if (col, row) not in game.matched:
                    shape = game.grid[row][col]
                    self.draw_shape(x + CELL_SIZE // 2, y + CELL_SIZE // 2, shape)

    def draw_shape(self, center_x, center_y, shape):
        """Draw a pixel-style shape at the given center position"""
        size = 16  # 16x16 pixel shapes
        
        if shape == 'circle':
            pygame.draw.circle(self.screen, (255, 0, 0), (center_x, center_y), size // 2)
        elif shape == 'square':
            pygame.draw.rect(self.screen, (0, 0, 255), (center_x - size // 2, center_y - size // 2, size, size))
        elif shape == 'triangle':
            points = [
                (center_x, center_y - size // 2),
                (center_x - size // 2, center_y + size // 2),
                (center_x + size // 2, center_y + size // 2)
            ]
            pygame.draw.polygon(self.screen, (255, 255, 0), points)
        elif shape == 'diamond':
            points = [
                (center_x, center_y - size // 2),
                (center_x + size // 2, center_y),
                (center_x, center_y + size // 2),
                (center_x - size // 2, center_y)
            ]
            pygame.draw.polygon(self.screen, (0, 255, 0), points)
        elif shape == 'star':
            # Simplified 5-point star
            points = []
            for i in range(5):
                angle = i * 72
                x = center_x + (size // 2) * pygame.math.Vector2.from_polar((1, angle)).x
                y = center_y + (size // 2) * pygame.math.Vector2.from_polar((1, angle)).y
                points.append((x, y))
                
                angle = (i * 72) + 36
                x = center_x + (size // 4) * pygame.math.Vector2.from_polar((1, angle)).x
                y = center_y + (size // 4) * pygame.math.Vector2.from_polar((1, angle)).y
                points.append((x, y))
            pygame.draw.polygon(self.screen, (128, 0, 128), points)
        elif shape == 'hexagon':
            points = []
            for i in range(6):
                angle = i * 60
                x = center_x + (size // 2) * pygame.math.Vector2.from_polar((1, angle)).x
                y = center_y + (size // 2) * pygame.math.Vector2.from_polar((1, angle)).y
                points.append((x, y))
            pygame.draw.polygon(self.screen, (255, 165, 0), points)
        elif shape == 'heart':
            # Simplified heart shape
            points = [
                (center_x, center_y + size // 4),
                (center_x - size // 3, center_y - size // 4),
                (center_x - size // 6, center_y - size // 2),
                (center_x, center_y - size // 3),
                (center_x + size // 6, center_y - size // 2),
                (center_x + size // 3, center_y - size // 4)
            ]
            pygame.draw.polygon(self.screen, (255, 105, 180), points)
        elif shape == 'cross':
            # Cross shape
            pygame.draw.rect(self.screen, (0, 255, 255), (center_x - size // 6, center_y - size // 2, size // 3, size))
            pygame.draw.rect(self.screen, (0, 255, 255), (center_x - size // 2, center_y - size // 6, size, size // 3))

    def draw_timer(self, game):
        """Draw the elapsed time in the top-left corner"""
        time_text = self.font.render(f"Time: {game.elapsed_time}s", True, (0, 0, 0))
        self.screen.blit(time_text, (10, 10))

    def draw_game_over(self):
        """Draw game over text"""
        game_over_text = self.font.render("You Win! Press R to Restart", True, (0, 0, 0))
        text_rect = game_over_text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))
        self.screen.blit(game_over_text, text_rect)
    
    def draw_connection(self, game):
        """Draw connection line between two selected elements"""
        if game.selected is None:
            return
        
        # Calculate grid position to center it
        grid_width = GRID_SIZE * (CELL_SIZE + CELL_SPACING) - CELL_SPACING
        grid_height = GRID_SIZE * (CELL_SIZE + CELL_SPACING) - CELL_SPACING
        start_x = (WINDOW_SIZE - grid_width) // 2
        start_y = (WINDOW_SIZE - grid_height) // 2
        
        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # Get shape at mouse position
        shape_info = game.get_shape_at(mouse_x, mouse_y)
        
        if shape_info:
            grid_x, grid_y, shape = shape_info
            # Check if it's a different cell and not matched
            if (grid_x, grid_y) != game.selected and (grid_x, grid_y) not in game.matched:
                # Check if they can be connected and get the path
                can_connect, path = game.can_connect(game.selected, (grid_x, grid_y))
                
                if path:
                    # Convert grid positions to screen coordinates
                    screen_path = []
                    for (x, y) in path:
                        # Handle outer path positions (-1 or GRID_SIZE)
                        if x == -1:
                            # Left of grid
                            screen_x = start_x - CELL_SPACING // 2
                        elif x == GRID_SIZE:
                            # Right of grid
                            screen_x = start_x + grid_width + CELL_SPACING // 2
                        else:
                            # Inside grid
                            screen_x = start_x + x * (CELL_SIZE + CELL_SPACING) + CELL_SIZE // 2
                            
                        if y == -1:
                            # Top of grid
                            screen_y = start_y - CELL_SPACING // 2
                        elif y == GRID_SIZE:
                            # Bottom of grid
                            screen_y = start_y + grid_height + CELL_SPACING // 2
                        else:
                            # Inside grid
                            screen_y = start_y + y * (CELL_SIZE + CELL_SPACING) + CELL_SIZE // 2
                            
                        screen_path.append((screen_x, screen_y))
                    
                    # Draw the connection line
                    if can_connect:
                        # Draw green connection line
                        pygame.draw.lines(self.screen, (0, 255, 0), False, screen_path, 2)
                    else:
                        # Draw red connection line
                        pygame.draw.lines(self.screen, (255, 0, 0), False, screen_path, 2)

    def render(self, game):
        """Render the entire game screen"""
        self.draw_background()
        self.draw_grid(game)
        self.draw_timer(game)
        self.draw_connection(game)
        if game.game_over:
            self.draw_game_over()
        pygame.display.flip()
