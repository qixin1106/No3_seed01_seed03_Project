class Config:
    def __init__(self):
        # Window settings
        self.WINDOW_WIDTH = 640
        self.WINDOW_HEIGHT = 640
        self.BACKGROUND_COLOR = (200, 200, 200)
        
        # Grid settings
        self.GRID_SIZE = 4
        self.CELL_SIZE = 80
        self.CELL_SPACING = 10
        self.GRID_PADDING = (self.WINDOW_WIDTH - (self.GRID_SIZE * self.CELL_SIZE + (self.GRID_SIZE - 1) * self.CELL_SPACING)) // 2
        
        # Colors
        self.CELL_COLOR = (150, 150, 150)
        self.SELECTED_BORDER_COLOR = (255, 255, 255)
        self.SELECTED_BORDER_WIDTH = 2
        
        # Shapes (8 types)
        self.SHAPES = [
            "circle",    # Red circle
            "square",    # Blue square
            "triangle",  # Yellow triangle
            "diamond",   # Green diamond
            "star",      # Purple star
            "hexagon",   # Orange hexagon
            "heart",     # Pink heart
            "cross"      # Cyan cross
        ]
        
        # Shape colors
        self.SHAPE_COLORS = {
            "circle": (255, 0, 0),
            "square": (0, 0, 255),
            "triangle": (255, 255, 0),
            "diamond": (0, 255, 0),
            "star": (128, 0, 128),
            "hexagon": (255, 165, 0),
            "heart": (255, 192, 203),
            "cross": (0, 255, 255)
        }
        
        # Font settings
        self.FONT_SIZE = 24
        self.FONT_COLOR = (0, 0, 0)
