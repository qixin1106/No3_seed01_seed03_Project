import pytest
import pygame
from game import Game
from config import Config

class TestGame:
    def setup_method(self):
        pygame.init()
        self.config = Config()
        self.game = Game(self.config)
    
    def teardown_method(self):
        pygame.quit()
    
    def test_generate_grid(self):
        grid = self.game.generate_grid()
        assert len(grid) == 4
        assert len(grid[0]) == 4
        
        # Check that all shapes appear exactly twice
        shape_count = {}
        for row in grid:
            for shape in row:
                if shape in shape_count:
                    shape_count[shape] += 1
                else:
                    shape_count[shape] = 1
        
        for count in shape_count.values():
            assert count == 2
    
    def test_can_connect_same_row(self):
        # Test horizontal connection in same row
        self.game.grid = [
            ["circle", "circle", "square", "triangle"],
            ["line", "square", "triangle", "circle"],
            ["square", "triangle", "circle", "line"],
            ["triangle", "line", "square", "circle"]
        ]
        self.game.matched_cells = {}
        
        # Test direct horizontal connection
        path = self.game.find_connection_path((0, 0), (1, 0))
        assert path is not None
        assert len(path) == 2
    
    def test_can_connect_same_column(self):
        # Test vertical connection in same column
        self.game.grid = [
            ["circle", "square", "triangle", "line"],
            ["square", "circle", "circle", "triangle"],
            ["triangle", "line", "square", "circle"],
            ["line", "triangle", "circle", "square"]
        ]
        self.game.matched_cells = {}
        
        # Test direct vertical connection
        path = self.game.find_connection_path((1, 0), (1, 1))
        assert path is not None
        assert len(path) == 2
    
    def test_can_connect_single_corner(self):
        # Test L-shape connection (single corner)
        self.game.grid = [
            ["circle", "matched", "matched", "circle"],
            ["matched", "matched", "matched", "matched"],
            ["matched", "matched", "matched", "matched"],
            ["matched", "matched", "matched", "circle"]
        ]
        # Mock matched cells to create a clear path
        self.game.matched_cells = { (1,0), (2,0), (0,1), (1,1), (2,1), (3,1),
                                   (0,2), (1,2), (2,2), (3,2), (0,3), (1,3), (2,3) }
        
        # Test L-shape connection
        path = self.game.find_connection_path((0, 0), (3, 3))
        assert path is not None
        assert len(path) > 0
    
    def test_cannot_connect_with_obstacle(self):
        # Test that cells with obstacles can't connect directly and can't find alternative path either
        self.game.grid = [
            ["circle", "square", "circle", "triangle"],
            ["line", "circle", "square", "triangle"],
            ["square", "triangle", "circle", "line"],
            ["triangle", "line", "square", "circle"]
        ]
        self.game.matched_cells = {}
    
        # Cells have obstacle between them and no alternative path available
        path = self.game.find_connection_path((0, 0), (2, 0))
        assert path == []
    
    def test_handle_click(self):
        # Test cell selection and matching
        self.game.grid = [
            ["circle", "circle", "square", "triangle"],
            ["line", "square", "triangle", "circle"],
            ["square", "triangle", "circle", "line"],
            ["triangle", "line", "square", "circle"]
        ]
        
        # Click first circle
        self.game.handle_click((self.config.GRID_PADDING + 20, self.config.GRID_PADDING + 20))
        assert self.game.selected_cell == (0, 0)
        
        # Click second circle (match)
        self.game.handle_click((self.config.GRID_PADDING + self.config.CELL_SIZE + self.config.CELL_SPACING + 20, 
                               self.config.GRID_PADDING + 20))
        
        # Check that both cells are matched
        assert (0, 0) in self.game.matched_cells
        assert (1, 0) in self.game.matched_cells
        assert self.game.selected_cell is None
    
    def test_game_won(self):
        # Test game win condition
        self.game.grid = [
            ["circle", "circle", "square", "square"],
            ["triangle", "triangle", "line", "line"],
            ["diamond", "diamond", "star", "star"],
            ["hexagon", "hexagon", "heart", "heart"]
        ]
        
        # Match all cells except the first two
        self.game.matched_cells = set()
        for y in range(4):
            for x in range(4):
                if (x, y) != (0, 0) and (x, y) != (1, 0):
                    self.game.matched_cells.add((x, y))
        
        # Click the last two cells to win
        self.game.handle_click((self.config.GRID_PADDING + 20, self.config.GRID_PADDING + 20))
        self.game.handle_click((self.config.GRID_PADDING + self.config.CELL_SIZE + self.config.CELL_SPACING + 20, 
                               self.config.GRID_PADDING + 20))
        
        assert self.game.game_won is True
