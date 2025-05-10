# PySolarSim - Solar System Simulation

A basic 3D solar system simulation built with Python, PyOpenGL, and PyQt6.

## Features

- 3D visualization of a basic solar system
- Real-time orbital motion simulation
- Interactive camera controls
- Basic planet information display

## Requirements

- Python 3.x
- PyOpenGL
- PyQt6
- NumPy

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/PySolarSim.git
cd PySolarSim
```

2. Create a virtual environment (recommended):
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

To start the simulation, run:
```bash
python src/main.py
```

## Controls

- The view automatically rotates to show the solar system from different angles
- Use the "Reset View" button to reset the camera position
- The simulation runs in real-time with planets orbiting the sun at different speeds

## Project Structure

```
PySolarSim/
├── src/
│   ├── main.py              # Application entry point
│   ├── simulation/          # Simulation logic
│   │   ├── celestial_bodies.py
│   │   └── solar_system.py
│   └── ui/                  # User interface
│       └── main_window.py
├── requirements.txt
└── README.md
```

## Contributing

Feel free to submit issues and enhancement requests! 