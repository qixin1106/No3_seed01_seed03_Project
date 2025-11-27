# Lian Lian Kan (连连看)

A simple pixel-style连连看 game built with Pygame.

## Features

- 4x4 grid layout with 8 different pixel art shapes
- Simple matching mechanics with ≤2 corner connection rules
- Real-time timer showing elapsed time
- Game over screen with restart option
- Pure Pygame drawing (no external assets)

## Installation

```bash
uv sync
```

## Running the Game

```bash
uv run python main.py
```

## Playing the Game

1. Click on any cell to select it
2. Click on another cell with the same shape
3. If they can be connected with ≤2 corners, they will be removed
4. Clear all cells to win
5. Press 'R' at any time to restart the game

## Testing

```bash
uv run pytest test_game.py
```
