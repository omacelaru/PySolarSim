# PySolarSim - Solar System Simulation

A basic 3D solar system simulation built with Python, PyOpenGL, and PyQt6.

## Features

- 3D visualization of a basic solar system
- Real-time orbital motion simulation
- Interactive camera controls (mouse, keyboard, UI)
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
python -m src.main
```

## Controls

### Camera Controls (Mouse & Keyboard)

- **Mouse Drag (stânga apăsat):** rotește camera (X/Y) în modul Free Camera
- **Scroll Mouse:** zoom in/out (în Free Camera/Top View: distanță, în Follow Planet: offset față de planetă)
- **Tastele W/S/A/D sau Săgeți:** rotește camera (sus/jos/stânga/dreapta)
- **Q/E:** rotește camera pe axa Z
- **+/- sau PageUp/PageDown:** zoom in/out (sau modifică distanța de follow)
- **Toate aceste controale sunt sincronizate cu slider-ele din UI**

### View Mode

- **Free Camera:** control total cu mouse/tastatură/slider-e
- **Follow Planet:** camera urmărește planeta selectată, distanța se ajustează cu slider sau scroll/+/–
- **Top View:** vedere de sus, zoom cu slider sau scroll/+/–

### Alte controale

- Play/Pause pentru simulare
- Viteză simulare
- Control iluminare
- Selectare și informații corp ceresc

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