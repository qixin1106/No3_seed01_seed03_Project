import pygame
import random
from config import Config
from shape_renderer import ShapeRenderer

# Ignore pygame static analysis errors
# pyright: reportAttributeAccessIssue=false

class Game:
    def __init__(self, config):
        self.config = config
        self.shape_renderer = ShapeRenderer(config)
        self.reset()
    
    def reset(self):
        self.grid = self.generate_grid()
        self.selected_cell = None
        self.matched_cells = set()
        self.start_time = pygame.time.get_ticks()
        self.game_won = False
        self.connection_path = []  # Store the path for drawing connection line
    
    def generate_grid(self):
        # Create pairs of shapes
        shapes = self.config.SHAPES * 2
        random.shuffle(shapes)
        
        # Create 4x4 grid
        grid = []
        for i in range(self.config.GRID_SIZE):
            row = []
            for j in range(self.config.GRID_SIZE):
                shape = shapes[i * self.config.GRID_SIZE + j]
                row.append(shape)
            grid.append(row)
        
        return grid
    
    def handle_click(self, pos):
        if self.game_won:
            return
        
        # Convert mouse position to grid coordinates
        x, y = pos
        grid_x = (x - self.config.GRID_PADDING) // (self.config.CELL_SIZE + self.config.CELL_SPACING)
        grid_y = (y - self.config.GRID_PADDING) // (self.config.CELL_SIZE + self.config.CELL_SPACING)
        
        # Check if click is within grid bounds
        if 0 <= grid_x < self.config.GRID_SIZE and 0 <= grid_y < self.config.GRID_SIZE:
            cell = (grid_x, grid_y)
            
            # Check if cell is already matched
            if cell in self.matched_cells:
                return
            
            # If no cell selected, select this one
            if not self.selected_cell:
                self.selected_cell = cell
                self.connection_path = []  # Clear any existing path
            else:
                # If same cell clicked, deselect
                if self.selected_cell == cell:
                    self.selected_cell = None
                    self.connection_path = []
                else:
                    # Check if shapes match and can be connected
                    if self.grid[grid_y][grid_x] == self.grid[self.selected_cell[1]][self.selected_cell[0]]:
                        path = self.find_connection_path(self.selected_cell, cell)
                        if path:
                            # Match found
                            self.matched_cells.add(self.selected_cell)
                            self.matched_cells.add(cell)
                            self.selected_cell = None
                            self.connection_path = []
                            
                            # Check if game is won
                            if len(self.matched_cells) == self.config.GRID_SIZE * self.config.GRID_SIZE:
                                self.game_won = True
                        else:
                            # No valid path, just update selection
                            self.selected_cell = cell
                            self.connection_path = []
                    else:
                        # Different shapes, deselect first and select new one
                        self.selected_cell = cell
                        self.connection_path = []
    
    def find_connection_path(self, cell1, cell2):
        """Find a connection path between two cells with max 2 corners"""
        x1, y1 = cell1
        x2, y2 = cell2
        
        # Check if cells are the same (shouldn't happen)
        if cell1 == cell2:
            return []
        
        # Check if cells are already matched
        if cell1 in self.matched_cells or cell2 in self.matched_cells:
            return []
        
        # Check direct horizontal connection
        if y1 == y2:
            if self.is_horizontal_path_clear(x1, x2, y1):
                return [cell1, cell2]
        
        # Check direct vertical connection
        if x1 == x2:
            if self.is_vertical_path_clear(y1, y2, x1):
                return [cell1, cell2]
        
        # Check single corner connections (L-shape)
        # First horizontal then vertical
        if self.is_horizontal_path_clear(x1, x2, y1) and self.is_vertical_path_clear(y1, y2, x2):
            return [cell1, (x2, y1), cell2]
        
        # First vertical then horizontal
        if self.is_vertical_path_clear(y1, y2, x1) and self.is_horizontal_path_clear(x1, x2, y2):
            return [cell1, (x1, y2), cell2]
        
        # Check two corner connections (around the grid) with obstacle checking
        # Path goes around the top - only allowed if cells are in the same column or path is clear
        if self.is_top_path_clear(cell1, cell2):
            # Check if the horizontal path across the top is clear of obstacles
            if self.is_top_horizontal_path_clear(y1, y2):
                return [cell1, (-1, y1), (-1, y2), cell2]
        
        # Path goes around the bottom
        if self.is_bottom_path_clear(cell1, cell2):
            if self.is_bottom_horizontal_path_clear(y1, y2):
                return [cell1, (self.config.GRID_SIZE, y1), (self.config.GRID_SIZE, y2), cell2]
        
        # Path goes around the left
        if self.is_left_path_clear(cell1, cell2):
            if self.is_left_vertical_path_clear(x1, x2):
                return [cell1, (x1, -1), (x2, -1), cell2]
        
        # Path goes around the right
        if self.is_right_path_clear(cell1, cell2):
            if self.is_right_vertical_path_clear(x1, x2):
                return [cell1, (x1, self.config.GRID_SIZE), (x2, self.config.GRID_SIZE), cell2]
        
        return []
    
    def is_horizontal_path_clear(self, x1, x2, y):
        """Check if horizontal path between x1 and x2 in row y is clear"""
        min_x = min(x1, x2)
        max_x = max(x1, x2)
        for x in range(min_x + 1, max_x):
            if (x, y) not in self.matched_cells:
                return False
        return True
    
    def is_vertical_path_clear(self, y1, y2, x):
        """Check if vertical path between y1 and y2 in column x is clear"""
        min_y = min(y1, y2)
        max_y = max(y1, y2)
        for y in range(min_y + 1, max_y):
            if (x, y) not in self.matched_cells:
                return False
        return True
    
    def is_top_horizontal_path_clear(self, y1, y2):
        """Check if horizontal path across the top is clear of obstacles"""
        min_y = min(y1, y2)
        max_y = max(y1, y2)
        # Check if any cell in the columns between y1 and y2 has an obstacle in the top row
        for y in range(min_y, max_y + 1):
            # Check if there's any unmatched cell in the column y that is blocking the path
            # Since we're going around the top, we need to make sure that the vertical path from each cell to the top is clear
            # This is already done in is_top_path_clear, so we just need to check if the horizontal path across the top is clear
            # Since the top is outside the grid, there are no obstacles
            pass
        return True
    
    def is_bottom_horizontal_path_clear(self, y1, y2):
        """Check if horizontal path across the bottom is clear of obstacles"""
        min_y = min(y1, y2)
        max_y = max(y1, y2)
        # Check if any cell in the columns between y1 and y2 has an obstacle in the bottom row
        for y in range(min_y, max_y + 1):
            # Check if there's any unmatched cell in the column y that is blocking the path
            # Since we're going around the bottom, we need to make sure that the vertical path from each cell to the bottom is clear
            # This is already done in is_bottom_path_clear, so we just need to check if the horizontal path across the bottom is clear
            # Since the bottom is outside the grid, there are no obstacles
            pass
        return True
    
    def is_left_vertical_path_clear(self, x1, x2):
        """Check if vertical path across the left is clear of obstacles"""
        min_x = min(x1, x2)
        max_x = max(x1, x2)
        # Check if any cell in the rows between x1 and x2 has an obstacle in the left column
        for x in range(min_x, max_x + 1):
            # Check if there's any unmatched cell in the row x that is blocking the path
            # Since we're going around the left, we need to make sure that the horizontal path from each cell to the left is clear
            # This is already done in is_left_path_clear, so we just need to check if the vertical path across the left is clear
            # Since the left is outside the grid, there are no obstacles
            pass
        return True
    
    def is_right_vertical_path_clear(self, x1, x2):
        """Check if vertical path across the right is clear of obstacles"""
        min_x = min(x1, x2)
        max_x = max(x1, x2)
        # Check if any cell in the rows between x1 and x2 has an obstacle in the right column
        for x in range(min_x, max_x + 1):
            # Check if there's any unmatched cell in the row x that is blocking the path
            # Since we're going around the right, we need to make sure that the horizontal path from each cell to the right is clear
            # This is already done in is_right_path_clear, so we just need to check if the vertical path across the right is clear
            # Since the right is outside the grid, there are no obstacles
            pass
        return True
    
    def is_top_horizontal_path_clear(self, y1, y2):
        """Check if horizontal path across the top is clear of obstacles"""
        min_y = min(y1, y2)
        max_y = max(y1, y2)
        # Check if any cell in the top row (x=-1) has obstacles
        # Since x=-1 is outside the grid, there are no obstacles
        return True
    
    def is_bottom_horizontal_path_clear(self, y1, y2):
        """Check if horizontal path across the bottom is clear of obstacles"""
        min_y = min(y1, y2)
        max_y = max(y1, y2)
        # Check if any cell in the bottom row (x=GRID_SIZE) has obstacles
        # Since x=GRID_SIZE is outside the grid, there are no obstacles
        return True
    
    def is_left_vertical_path_clear(self, x1, x2):
        """Check if vertical path across the left is clear of obstacles"""
        min_x = min(x1, x2)
        max_x = max(x1, x2)
        # Check if any cell in the left column (y=-1) has obstacles
        # Since y=-1 is outside the grid, there are no obstacles
        return True
    
    def is_right_vertical_path_clear(self, x1, x2):
        """Check if vertical path across the right is clear of obstacles"""
        min_x = min(x1, x2)
        max_x = max(x1, x2)
        # Check if any cell in the right column (y=GRID_SIZE) has obstacles
        # Since y=GRID_SIZE is outside the grid, there are no obstacles
        return True
    
    def is_top_path_clear(self, cell1, cell2):
        """Check if path around the top of the grid is clear"""
        x1, y1 = cell1
        x2, y2 = cell2
        
        # Check vertical path from cell1 to top
        if not self.is_vertical_path_clear(0, y1, x1):
            return False
        
        # Check vertical path from cell2 to top
        if not self.is_vertical_path_clear(0, y2, x2):
            return False
        
        # Check if there's any obstacle between the two vertical paths at the top
        min_y = min(y1, y2)
        max_y = max(y1, y2)
        for y in range(min_y, max_y + 1):
            # Check if there's any unmatched cell in the column y that is blocking the path
            for x in range(self.config.GRID_SIZE):
                if (x, y) not in self.matched_cells and self.grid[x][y] is not None:
                    return False
        
        return True
    
    def is_bottom_path_clear(self, cell1, cell2):
        """Check if path around the bottom of the grid is clear"""
        x1, y1 = cell1
        x2, y2 = cell2
        grid_size = self.config.GRID_SIZE - 1
        
        # Check vertical path from cell1 to bottom
        if not self.is_vertical_path_clear(y1, grid_size, x1):
            return False
        
        # Check vertical path from cell2 to bottom
        if not self.is_vertical_path_clear(y2, grid_size, x2):
            return False
        
        # Check if there's any obstacle between the two vertical paths at the bottom
        min_y = min(y1, y2)
        max_y = max(y1, y2)
        for y in range(min_y, max_y + 1):
            # Check if there's any unmatched cell in the column y that is blocking the path
            for x in range(self.config.GRID_SIZE):
                if (x, y) not in self.matched_cells and self.grid[x][y] is not None:
                    return False
        
        return True
    
    def is_left_path_clear(self, cell1, cell2):
        """Check if path around the left of the grid is clear"""
        x1, y1 = cell1
        x2, y2 = cell2
        
        # Check horizontal path from cell1 to left
        if not self.is_horizontal_path_clear(0, x1, y1):
            return False
        
        # Check horizontal path from cell2 to left
        if not self.is_horizontal_path_clear(0, x2, y2):
            return False
        
        # Check if there's any obstacle between the two horizontal paths at the left
        min_x = min(x1, x2)
        max_x = max(x1, x2)
        for x in range(min_x, max_x + 1):
            # Check if there's any unmatched cell in the row x that is blocking the path
            for y in range(self.config.GRID_SIZE):
                if (x, y) not in self.matched_cells and self.grid[x][y] is not None:
                    return False
        
        return True
    
    def is_right_path_clear(self, cell1, cell2):
        """Check if path around the right of the grid is clear"""
        x1, y1 = cell1
        x2, y2 = cell2
        grid_size = self.config.GRID_SIZE - 1
        
        # Check horizontal path from cell1 to right
        if not self.is_horizontal_path_clear(x1, grid_size, y1):
            return False
        
        # Check horizontal path from cell2 to right
        if not self.is_horizontal_path_clear(x2, grid_size, y2):
            return False
        
        # Check if there's any obstacle between the two horizontal paths at the right
        min_x = min(x1, x2)
        max_x = max(x1, x2)
        for x in range(min_x, max_x + 1):
            # Check if there's any unmatched cell in the row x that is blocking the path
            for y in range(self.config.GRID_SIZE):
                if (x, y) not in self.matched_cells and self.grid[x][y] is not None:
                    return False
        
        return True
    
    def is_top_horizontal_path_clear(self, y1, y2):
        """Check if horizontal path across the top is clear of obstacles"""
        min_y = min(y1, y2)
        max_y = max(y1, y2)
        # Check if any cell in the top row (x=-1) has obstacles
        # Since x=-1 is outside the grid, there are no obstacles
        return True
    
    def is_bottom_horizontal_path_clear(self, y1, y2):
        """Check if horizontal path across the bottom is clear of obstacles"""
        min_y = min(y1, y2)
        max_y = max(y1, y2)
        # Check if any cell in the bottom row (x=GRID_SIZE) has obstacles
        # Since x=GRID_SIZE is outside the grid, there are no obstacles
        return True
    
    def is_left_vertical_path_clear(self, x1, x2):
        """Check if vertical path across the left is clear of obstacles"""
        min_x = min(x1, x2)
        max_x = max(x1, x2)
        # Check if any cell in the left column (y=-1) has obstacles
        # Since y=-1 is outside the grid, there are no obstacles
        return True
    
    def is_right_vertical_path_clear(self, x1, x2):
        """Check if vertical path across the right is clear of obstacles"""
        min_x = min(x1, x2)
        max_x = max(x1, x2)
        # Check if any cell in the right column (y=GRID_SIZE) has obstacles
        # Since y=GRID_SIZE is outside the grid, there are no obstacles
        return True
    
    def update(self):
        pass
    
    def render(self, screen):
        # Clear screen
        screen.fill(self.config.BACKGROUND_COLOR)
        
        # Render grid
        for y in range(self.config.GRID_SIZE):
            for x in range(self.config.GRID_SIZE):
                cell = (x, y)
                
                # Calculate cell position
                px = self.config.GRID_PADDING + x * (self.config.CELL_SIZE + self.config.CELL_SPACING)
                py = self.config.GRID_PADDING + y * (self.config.CELL_SIZE + self.config.CELL_SPACING)
                
                # Draw cell background
                pygame.draw.rect(screen, self.config.CELL_COLOR, (px, py, self.config.CELL_SIZE, self.config.CELL_SIZE))
                
                # Draw shape if not matched
                if cell not in self.matched_cells:
                    shape = self.grid[y][x]
                    self.shape_renderer.draw_shape(screen, shape, px + self.config.CELL_SIZE // 2, py + self.config.CELL_SIZE // 2)
                
                # Draw selected border
                if cell == self.selected_cell:
                    pygame.draw.rect(screen, self.config.SELECTED_BORDER_COLOR, 
                                    (px - self.config.SELECTED_BORDER_WIDTH, 
                                     py - self.config.SELECTED_BORDER_WIDTH, 
                                     self.config.CELL_SIZE + 2 * self.config.SELECTED_BORDER_WIDTH, 
                                     self.config.CELL_SIZE + 2 * self.config.SELECTED_BORDER_WIDTH), 
                                    self.config.SELECTED_BORDER_WIDTH)
        
        # Render connection path if two cells are selected and path exists
        if self.selected_cell:
            # Check if we're hovering over another valid cell
            mouse_pos = pygame.mouse.get_pos()
            x, y = mouse_pos
            grid_x = (x - self.config.GRID_PADDING) // (self.config.CELL_SIZE + self.config.CELL_SPACING)
            grid_y = (y - self.config.GRID_PADDING) // (self.config.CELL_SIZE + self.config.CELL_SPACING)
            
            if 0 <= grid_x < self.config.GRID_SIZE and 0 <= grid_y < self.config.GRID_SIZE:
                hover_cell = (grid_x, grid_y)
                if hover_cell != self.selected_cell and hover_cell not in self.matched_cells:
                    if self.grid[grid_y][grid_x] == self.grid[self.selected_cell[1]][self.selected_cell[0]]:
                        path = self.find_connection_path(self.selected_cell, hover_cell)
                        if path:
                            self.draw_connection_path(screen, path)
        
        # Render timer
        font = pygame.font.Font(None, self.config.FONT_SIZE)
        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
        timer_text = font.render(f"Time: {elapsed_time}s", True, self.config.FONT_COLOR)
        screen.blit(timer_text, (10, 10))
        
        # Render win message
        if self.game_won:
            win_text = font.render("CLEAR! Press R to restart", True, self.config.FONT_COLOR)
            text_rect = win_text.get_rect(center=(self.config.WINDOW_WIDTH // 2, self.config.WINDOW_HEIGHT // 2))
            screen.blit(win_text, text_rect)
    
    def draw_connection_path(self, screen, path):
        """Draw the connection path between two cells"""
        if not path or len(path) < 2:
            return
        
        # Convert grid coordinates to pixel coordinates
        pixel_path = []
        for (x, y) in path:
            # Handle off-grid coordinates (for around-the-grid paths)
            if x == -1:
                px = self.config.GRID_PADDING - self.config.CELL_SIZE // 2
            elif x == self.config.GRID_SIZE:
                px = self.config.GRID_PADDING + (self.config.GRID_SIZE - 1) * (self.config.CELL_SIZE + self.config.CELL_SPACING) + self.config.CELL_SIZE + self.config.CELL_SIZE // 2
            else:
                px = self.config.GRID_PADDING + x * (self.config.CELL_SIZE + self.config.CELL_SPACING) + self.config.CELL_SIZE // 2
            
            if y == -1:
                py = self.config.GRID_PADDING - self.config.CELL_SIZE // 2
            elif y == self.config.GRID_SIZE:
                py = self.config.GRID_PADDING + (self.config.GRID_SIZE - 1) * (self.config.CELL_SIZE + self.config.CELL_SPACING) + self.config.CELL_SIZE + self.config.CELL_SIZE // 2
            else:
                py = self.config.GRID_PADDING + y * (self.config.CELL_SIZE + self.config.CELL_SPACING) + self.config.CELL_SIZE // 2
            
            pixel_path.append((px, py))
        
        # Draw the path
        pygame.draw.lines(screen, (255, 255, 0), False, pixel_path, 3)
        
        # Draw circles at the corners
        for point in pixel_path:
            pygame.draw.circle(screen, (255, 255, 0), point, 5)
