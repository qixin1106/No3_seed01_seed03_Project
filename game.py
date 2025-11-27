import random

# Game constants
GRID_SIZE = 4
CELL_SIZE = 80
CELL_SPACING = 10
WINDOW_SIZE = 640

# Colors (RGB)
BACKGROUND_COLOR = (200, 200, 200)
CELL_COLOR = (150, 150, 150)
SELECTED_BORDER_COLOR = (255, 255, 255)
SELECTED_BORDER_WIDTH = 2

# Shape types
SHAPES = [
    'circle',
    'square',
    'triangle',
    'diamond',
    'star',
    'hexagon',
    'heart',
    'cross'
]

class Game:
    def __init__(self):
        self.grid = []
        self.selected = None
        self.matched = set()
        self.start_time = 0
        self.elapsed_time = 0
        self.game_over = False
        self.generate_grid()

    def generate_grid(self):
        """Generate a new random grid with pairs of shapes"""
        # Create pairs of shapes
        shape_pairs = SHAPES * 2
        random.shuffle(shape_pairs)
        
        # Create grid
        self.grid = []
        for i in range(GRID_SIZE):
            row = []
            for j in range(GRID_SIZE):
                shape = shape_pairs[i * GRID_SIZE + j]
                row.append(shape)
            self.grid.append(row)
        
        self.selected = None
        self.matched = set()
        self.game_over = False
        self.start_time = 0
        self.elapsed_time = 0

    def get_shape_at(self, x, y):
        """Get the shape at the given screen coordinates"""
        # Calculate grid position from screen coordinates
        grid_width = GRID_SIZE * (CELL_SIZE + CELL_SPACING) - CELL_SPACING
        grid_height = GRID_SIZE * (CELL_SIZE + CELL_SPACING) - CELL_SPACING
        start_x = (WINDOW_SIZE - grid_width) // 2
        start_y = (WINDOW_SIZE - grid_height) // 2
        
        # Calculate grid coordinates
        grid_x = (x - start_x) // (CELL_SIZE + CELL_SPACING)
        grid_y = (y - start_y) // (CELL_SIZE + CELL_SPACING)
        
        if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
            return grid_x, grid_y, self.grid[grid_y][grid_x]
        return None

    def select_cell(self, grid_x, grid_y):
        """Select a cell if it's not already matched"""
        if (grid_x, grid_y) in self.matched:
            return False
        
        if self.selected is None:
            self.selected = (grid_x, grid_y)
            return True
        else:
            # Check if same cell selected
            if self.selected == (grid_x, grid_y):
                self.selected = None
                return True
            
            # Check if same shape
            if self.grid[self.selected[1]][self.selected[0]] == self.grid[grid_y][grid_x]:
                # Check if they can be connected
                can_connect, _ = self.can_connect(self.selected, (grid_x, grid_y))
                if can_connect:
                    # Match them
                    self.matched.add(self.selected)
                    self.matched.add((grid_x, grid_y))
                    self.selected = None
                    
                    # Check if game over
                    if len(self.matched) == GRID_SIZE * GRID_SIZE:
                        self.game_over = True
                    return True
            
            # Not a match, select new cell
            self.selected = (grid_x, grid_y)
            return True
        return False

    def can_connect(self, pos1, pos2):
        """Check if two positions can be connected with <=2 corners and return the path"""
        x1, y1 = pos1
        x2, y2 = pos2
        
        # Same cell
        if pos1 == pos2:
            return False, []
        
        # Check if same shape (already checked before, but just in case)
        if self.grid[y1][x1] != self.grid[y2][x2]:
            return False, []
        
        # Check direct horizontal connection (0 corners)
        if y1 == y2:
            if self.is_path_clear(pos1, pos2):
                return True, [pos1, pos2]
        
        # Check direct vertical connection (0 corners)
        if x1 == x2:
            if self.is_path_clear(pos1, pos2):
                return True, [pos1, pos2]
        
        # Check single corner connection (two possibilities)
        # First corner at (x2, y1)
        if self.is_path_clear((x1, y1), (x2, y1)) and self.is_path_clear((x2, y1), (x2, y2)):
            return True, [pos1, (x2, y1), pos2]
        
        # Second corner at (x1, y2)
        if self.is_path_clear((x1, y1), (x1, y2)) and self.is_path_clear((x1, y2), (x2, y2)):
            return True, [pos1, (x1, y2), pos2]
        
        # Check outer corner connections (around the grid)
        # For ABA pattern: A(0,0), B(1,0), A(2,0) can be connected via top or bottom
        # Check left outer path
        if self.is_outer_path_clear(pos1, pos2, 'left'):
            return True, [pos1, (-1, y1), (-1, y2), pos2]
        
        # Check right outer path
        if self.is_outer_path_clear(pos1, pos2, 'right'):
            return True, [pos1, (GRID_SIZE, y1), (GRID_SIZE, y2), pos2]
        
        # Check top outer path
        if self.is_outer_path_clear(pos1, pos2, 'top'):
            return True, [pos1, (x1, -1), (x2, -1), pos2]
        
        # Check bottom outer path
        if self.is_outer_path_clear(pos1, pos2, 'bottom'):
            return True, [pos1, (x1, GRID_SIZE), (x2, GRID_SIZE), pos2]
        
        return False, []
    
    def is_outer_path_clear(self, pos1, pos2, direction):
        """Check if outer path is clear between two positions"""
        x1, y1 = pos1
        x2, y2 = pos2
        
        if direction == 'left':
            # Move left from both positions to column -1, then connect
            # Check path from pos1 to ( -1, y1 )
            if not self.is_path_clear_outer(pos1, (-1, y1)):
                return False
            # Check path from pos2 to ( -1, y2 )
            if not self.is_path_clear_outer(pos2, (-1, y2)):
                return False
            # Check path between ( -1, y1 ) and ( -1, y2 )
            if not self.is_path_clear_outer((-1, y1), (-1, y2)):
                return False
            return True
        
        elif direction == 'right':
            # Move right from both positions to column GRID_SIZE
            if not self.is_path_clear_outer(pos1, (GRID_SIZE, y1)):
                return False
            if not self.is_path_clear_outer(pos2, (GRID_SIZE, y2)):
                return False
            if not self.is_path_clear_outer((GRID_SIZE, y1), (GRID_SIZE, y2)):
                return False
            return True
        
        elif direction == 'top':
            # Move up from both positions to row -1
            if not self.is_path_clear_outer(pos1, (x1, -1)):
                return False
            if not self.is_path_clear_outer(pos2, (x2, -1)):
                return False
            if not self.is_path_clear_outer((x1, -1), (x2, -1)):
                return False
            return True
        
        elif direction == 'bottom':
            # Move down from both positions to row GRID_SIZE
            if not self.is_path_clear_outer(pos1, (x1, GRID_SIZE)):
                return False
            if not self.is_path_clear_outer(pos2, (x2, GRID_SIZE)):
                return False
            if not self.is_path_clear_outer((x1, GRID_SIZE), (x2, GRID_SIZE)):
                return False
            return True
        
        return False
    
    def is_path_clear_outer(self, pos1, pos2):
        """Check if path between two positions is clear, including outer positions (-1, y), (GRID_SIZE, y), (x, -1), (x, GRID_SIZE)"""
        x1, y1 = pos1
        x2, y2 = pos2
        
        # Must be same row or column
        if x1 != x2 and y1 != y2:
            return False
        
        if x1 == x2:
            # Same column
            min_y = min(y1, y2)
            max_y = max(y1, y2)
            # Check all cells between (excluding outer positions)
            for y in range(min_y + 1, max_y):
                # Skip outer positions
                if 0 <= y < GRID_SIZE:
                    if (x1, y) not in self.matched:
                        return False
        else:
            # Same row
            min_x = min(x1, x2)
            max_x = max(x1, x2)
            # Check all cells between (excluding outer positions)
            for x in range(min_x + 1, max_x):
                # Skip outer positions
                if 0 <= x < GRID_SIZE:
                    if (x, y1) not in self.matched:
                        return False
        
        return True

    def is_path_clear(self, pos1, pos2):
        """Check if path between two positions is clear (same row or column)"""
        x1, y1 = pos1
        x2, y2 = pos2
        
        # Must be same row or column
        if x1 != x2 and y1 != y2:
            return False
        
        if x1 == x2:
            # Same column
            min_y = min(y1, y2)
            max_y = max(y1, y2)
            for y in range(min_y + 1, max_y):
                # Check if cell is not empty (contains an unmatched element)
                if self.grid[y][x1] is not None and (x1, y) not in self.matched:
                    return False
        else:
            # Same row
            min_x = min(x1, x2)
            max_x = max(x1, x2)
            for x in range(min_x + 1, max_x):
                # Check if cell is not empty (contains an unmatched element)
                if self.grid[y1][x] is not None and (x, y1) not in self.matched:
                    return False
        
        return True

    def update_time(self, current_time):
        """Update elapsed time"""
        if not self.game_over and self.start_time > 0:
            self.elapsed_time = (current_time - self.start_time) // 1000

    def start_timer(self, current_time):
        """Start the game timer"""
        if self.start_time == 0:
            self.start_time = current_time

    def reset(self):
        """Reset the game"""
        self.generate_grid()
