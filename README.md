# PySolarSim - Solar System Simulation

A 3D solar system simulation that allows users to explore and interact with planets, stars, and other celestial bodies in a realistic environment.

## Features

- Realistic 3D visualization of the solar system
- Physics-based simulation of celestial bodies
- Interactive camera controls
- Time scale adjustment
- Pause/Resume and Reset functionality
- Orbit trails visualization

## Requirements

- Python 3.8 or higher
- PyQt6
- PyOpenGL
- NumPy
- SciPy

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/PySolarSim.git
cd PySolarSim
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

Run the simulation:
```bash
python src/main.py
```

### Controls

- **Left Mouse Button + Drag**: Rotate camera
- **Mouse Wheel**: Zoom in/out
- **Pause/Resume Button**: Pause or resume the simulation
- **Reset Button**: Reset the simulation to initial state
- **Time Scale Slider**: Adjust the simulation speed

## Project Structure

```
PySolarSim/
├── src/
│   ├── main.py                 # Application entry point
│   ├── simulation/             # Simulation logic
│   │   ├── physics.py         # Physics calculations
│   │   ├── celestial_bodies.py # Celestial body classes
│   │   └── solar_system.py    # Solar system management
│   ├── graphics/              # Graphics and rendering
│   │   ├── renderer.py        # OpenGL rendering
│   │   └── effects.py         # Visual effects
│   └── ui/                    # User interface
│       └── main_window.py     # Main window and controls
├── assets/                    # Resources
│   ├── textures/             # Texture files
│   └── models/               # 3D models
├── tests/                    # Test files
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 