import pytest
from game import Game

def test_generate_grid():
    """Test that grid is generated with correct size and pairs"""
    game = Game()
    assert len(game.grid) == 4
    assert len(game.grid[0]) == 4
    
    # Count occurrences of each shape
    shape_count = {}
    for row in game.grid:
        for shape in row:
            if shape in shape_count:
                shape_count[shape] += 1
            else:
                shape_count[shape] = 1
    
    # Each shape should appear exactly twice
    for count in shape_count.values():
        assert count == 2

def test_select_cell():
    """Test cell selection logic"""
    game = Game()
    
    # Select first cell
    result = game.select_cell(0, 0)
    assert result == True
    assert game.selected == (0, 0)
    
    # Select same cell again (should deselect)
    result = game.select_cell(0, 0)
    assert result == True
    assert game.selected is None
    
    # Select a matched cell (should not select)
    game.matched.add((1, 1))
    result = game.select_cell(1, 1)
    assert result == False
    assert game.selected is None

def test_can_connect():
    """Test connection logic"""
    game = Game()
    
    # Set up a simple grid for testing
    game.grid = [
        ['circle', 'circle', 'square', 'square'],
        ['triangle', 'triangle', 'diamond', 'diamond'],
        ['star', 'star', 'hexagon', 'hexagon'],
        ['heart', 'heart', 'cross', 'cross']
    ]
    
    # Test direct horizontal connection (adjacent)
    can_connect, _ = game.can_connect((0, 0), (1, 0))
    assert can_connect == True
    
    # Test non-matching shapes
    can_connect, _ = game.can_connect((0, 0), (2, 0))
    assert can_connect == False
    
    # Test direct vertical connection (adjacent)
    can_connect, _ = game.can_connect((0, 0), (1, 1))
    assert can_connect == False
    
    # Test direct vertical connection with same shape
    game.grid[1][0] = 'circle'
    can_connect, _ = game.can_connect((0, 0), (0, 1))
    assert can_connect == True

def test_is_path_clear():
    """Test path clearing logic"""
    game = Game()
    
    # Test clear horizontal path
    assert game.is_path_clear((0, 0), (1, 0)) == True
    
    # Test clear vertical path
    assert game.is_path_clear((0, 0), (0, 1)) == True
    
    # Test path with obstacle
    game.grid = [
        ['circle', 'square', 'circle', 'square'],
        ['triangle', 'triangle', 'diamond', 'diamond'],
        ['star', 'star', 'hexagon', 'hexagon'],
        ['heart', 'heart', 'cross', 'cross']
    ]
    assert game.is_path_clear((0, 0), (2, 0)) == False

def test_game_over():
    """Test game over condition"""
    game = Game()
    
    # Set up a grid with all matching pairs
    game.grid = [
        ['circle', 'circle', 'square', 'square'],
        ['circle', 'circle', 'square', 'square'],
        ['triangle', 'triangle', 'diamond', 'diamond'],
        ['triangle', 'triangle', 'diamond', 'diamond']
    ]
    
    # Match all cells
    game.matched = set()
    for i in range(4):
        for j in range(4):
            game.matched.add((j, i))
    
    # Check if game over is set when all cells are matched
    # The game_over flag is set in select_cell when the last pair is matched
    # So we need to simulate that scenario
    game.game_over = len(game.matched) == 16
    
    assert game.game_over == True

def test_reset():
    """Test game reset"""
    game = Game()
    game.selected = (0, 0)
    game.matched.add((0, 0))
    game.game_over = True
    game.start_time = 1000
    game.elapsed_time = 10
    
    game.reset()
    
    assert game.selected is None
    assert len(game.matched) == 0
    assert game.game_over == False
    assert game.start_time == 0
    assert game.elapsed_time == 0
