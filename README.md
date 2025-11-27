# PGGame - Rocket Car

A vertical scrolling racing game built with Pygame.

## Features

- **Vertical Layout**: 640x1280 pixel window
- **Dynamic Track**: 3/4/5 lanes that switch randomly every ≥3 seconds with smooth transitions
- **Player Control**: Yellow car that moves horizontally with A/D keys
- **Track Elements**:
  - Normal gray cars (fixed position)
  - Red cars (chase player when close)
  - Blue cars (avoid player when close)
  - Black trucks (1.5 lanes wide, minimal movement)
  - Gray obstacles (randomly distributed)
- **Collision Detection**: Collide with cars, obstacles, or boundaries to lose
- **Distance Tracking**: Track your driving distance in meters
- **Replay**: Press R to restart after game over

## Installation

1. Install dependencies:
```bash
uv sync
```

## Running the Game

```bash
uv run python main.py
```

## Controls

- **A/Left Arrow**: Move left
- **D/Right Arrow**: Move right
- **R**: Restart game (when game over)
- **ESC**: Exit game

## Game Rules

1. Avoid colliding with other cars, obstacles, or red boundaries
2. The track dynamically changes between 3, 4, or 5 lanes
3. Your car moves faster than all other elements
4. Try to achieve the longest distance possible

## Project Structure

```
race_car01/
├── main.py              # Entry point
├── game.py              # Main game logic
├── player.py            # Player car class
├── track.py             # Track system
├── elements.py          # Game elements (cars, obstacles)
├── config.py            # Game configuration
├── pyproject.toml       # Project dependencies
└── README.md           # This file
```

## Technologies Used

- Python 3.10+
- Pygame 2.6.1
- uv (package manager)

## License

MIT