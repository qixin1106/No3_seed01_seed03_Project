# Pixel Link - Simple连连看 Game

A simple pixel-style连连看 game built with Pygame.

## Features

- 4x4 grid layout with 80x80px cells
- 8 different pixel art shapes:
  - Red Circle
  - Blue Square
  - Yellow Triangle
  - Green Diamond
  - Purple Star
  - Orange Hexagon
  - Pink Heart
  - Cyan Cross
- Basic connection rules:
  - Horizontal/vertical straight lines
  - Single corner折线 connections
- Timer showing elapsed time
- Win condition: Clear all shapes
- Reset functionality with R key

## Installation

```bash
uv sync
```

## Running the Game

```bash
uv run python main.py
```

## Testing

```bash
uv run pytest
```

## Controls

- **Mouse Click**: Select/deselect a cell
- **R Key**: Reset the game

## Game Rules

1. Click on an unmatched cell to select it
2. Click on another unmatched cell with the same shape
3. If the two cells can be connected with ≤2 corners and no obstacles, they will be eliminated
4. Clear all cells to win!
5. Press R to restart the game at any time

## Project Structure

```
.
├── main.py              # Main game loop
├── game.py              # Core game logic
├── config.py            # Game configuration
├── shape_renderer.py    # Shape drawing functions
├── test_game.py         # Unit tests
├── pyproject.toml       # Project dependencies
└── README.md           # This file
```
