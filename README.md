# Serpents Per Second

A SNES-styled Snake game built with Python and pygame-ce featuring pixel-perfect graphics, multiple game modes, and chiptune audio.

## Features

- **SNES-style graphics**: 256×224 internal resolution with integer scaling (3x-6x)
- **Four game modes**:
  - **Classic**: Wrap-around edges, no walls
  - **Boxed**: Border collision = death
  - **Maze**: Navigate through prebuilt wall layouts
  - **Time Attack**: Score as much as possible in 120 seconds
- **Progressive difficulty**: Snake speed increases with each food eaten
- **High scores**: Top 10 leaderboard per mode with 3-letter name entry
- **Chiptune audio**: Menu and gameplay music with sound effects

## Requirements

- Python 3.12+
- Windows (primary target)

## Installation

### From Source

```bash
# Clone the repository
git clone <repository-url>
cd SerpentsPerSecond

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -e .

# Run the game
python main.py
```

### Development Setup

```bash
# Install with development dependencies
pip install -e ".[dev]"

# Run linting
ruff check .

# Run type checking
mypy src

# Run tests
pytest

# Run tests with coverage
pytest --cov=src --cov-report=html
```

## Building Executable

```bash
# Install PyInstaller
pip install pyinstaller

# Build Windows executable
pyinstaller --noconfirm --onefile --windowed --name SerpentsPerSecond main.py --add-data "assets;assets"

# Executable will be in dist/SerpentsPerSecond.exe
```

## Controls

| Action | Keys |
|--------|------|
| Move Up | ↑ / W |
| Move Down | ↓ / S |
| Move Left | ← / A |
| Move Right | → / D |
| Confirm / Select | Enter |
| Back / Cancel | Escape |
| Pause | P |

## Game Rules

### Movement
- Snake moves on a 16×14 grid
- Only the most recent direction input is applied each tick
- 180° turns are not allowed
- Starting speed: 8 ticks/second
- Speed increases by 0.25 ticks/second per food (max: 14 ticks/second)

### Scoring
- Each food: +10 points
- Time Attack only: +1 point per second survived

## Save Files

Game data is stored in:
```
%APPDATA%\SerpentsPerSecond\
├── saves\
│   ├── settings.json
│   └── highscores.json
└── app.log
```

### Settings

```json
{
  "version": 1,
  "scale": 4,
  "fullscreen": false,
  "music_volume": 0.7,
  "sfx_volume": 0.8
}
```

### High Scores

```json
{
  "version": 1,
  "classic": [{"name": "AAA", "score": 100, "ts": "2025-12-30T18:00:00Z"}],
  "boxed": [],
  "maze": [],
  "time_attack": []
}
```

## Environment Variables (Optional)

| Variable | Description | Example |
|----------|-------------|---------|
| `SPS_FORCE_SCALE` | Override scale (3-6) | `SPS_FORCE_SCALE=4` |
| `SPS_FORCE_WINDOWED` | Force windowed mode | `SPS_FORCE_WINDOWED=1` |
| `SPS_LOG_LEVEL` | Log level | `SPS_LOG_LEVEL=DEBUG` |

## Project Structure

```
SerpentsPerSecond/
├── main.py                 # Entry point
├── pyproject.toml          # Project configuration
├── src/
│   ├── app.py              # Main application
│   ├── constants.py        # Game constants
│   ├── scenes/             # Scene state machine
│   ├── systems/            # Core systems (audio, input, scaling)
│   ├── content/            # Mode rules and maze maps
│   ├── render/             # Sprite and font rendering
│   └── game/               # Game logic (snake, food, collision)
├── assets/
│   ├── sprites/            # PNG sprite sheets
│   └── audio/              # OGG music and WAV sound effects
└── tests/                  # Unit and integration tests
```

## License

MIT License
