# PySolarSim - Solar System Simulation

PySolarSim este o aplicație modernă pentru simularea și explorarea unui sistem solar 3D, cu accent pe interactivitate, realism și un UI minimalist, modern.

## Caracteristici principale

- **Vizualizare 3D a sistemului solar** cu Soarele, toate cele 8 planete și Pluto
- **Luna** orbitează corect Pământul
- **Inele pentru Saturn**
- **Traiectorii orbitale vizibile** (cu opțiune de on/off)
- **Poziții inițiale realiste și randomizate pentru planete**
- **Umbre 3D realiste** pe planete, în funcție de Soare
- **Moduri de cameră multiple**:
  - Free Camera (control total cu mouse/tastatură/slider)
  - Follow Planet (urmărește orice planetă sau Luna)
  - Top View (vedere de sus)
  - Lateral View (vedere laterală)
  - Oblic View (vedere diagonală)
- **UI modern, minimalist, cu accente moderne**
- **Selectare și afișare informații pentru orice corp ceresc**
- **Control viteză simulare, iluminare, zoom, rotație, etc.**

## Instalare

1. Clonează repository-ul:
```bash
git clone https://github.com/yourusername/PySolarSim.git
cd PySolarSim
```
2. Creează un mediu virtual (recomandat):
```bash
python -m venv .venv
source .venv/bin/activate  # Pe Windows: .venv\Scripts\activate
```
3. Instalează dependențele:
```bash
pip install -r requirements.txt
```

## Rulare

Pornește aplicația cu:
```bash
python -m src.main
```

## Controale și interacțiune

### Moduri de cameră
- **Free Camera:**
  - Rotește cu mouse-ul (drag stânga)
  - Zoom cu scroll sau slider
  - Rotește și cu tastele W/S/A/D sau săgeți, Q/E pentru axa Z
- **Follow Planet:**
  - Camera urmărește planeta selectată (sau Luna)
  - Distanța de follow se ajustează cu slider sau scroll
- **Top View / Lateral View / Oblic View:**
  - Vederi presetate pentru explorare rapidă
  - Zoom cu slider sau scroll

### UI și funcționalități
- **Dropdown pentru selectarea oricărui corp ceresc** (planete, Pluto, Luna)
- **Afișare informații detaliate** pentru corpul selectat
- **Buton Play/Pause** pentru simulare
- **Slider viteză simulare**
- **Control iluminare ambientală și difuză**
- **Checkbox "Show Orbits"** pentru a afișa/ascunde traiectoriile orbitale
- **Toate controalele sunt sincronizate între mouse, tastatură și UI**

### Alte detalii
- **Poziții inițiale randomizate** pentru realism
- **Umbre 3D pe planete** (partea de noapte)
- **Inele pentru Saturn**
- **UI minimalist, modern, cu accente albastre**

## Structura proiectului

```
PySolarSim/
├── src/
│   ├── main.py              # Punct de pornire aplicație
│   ├── simulation/          # Logica simulării
│   │   ├── celestial_bodies.py
│   │   └── solar_system.py
│   └── ui/                  # Interfața grafică
│       └── main_window.py
├── requirements.txt
├── style.qss                # Tema modernă a interfeței
└── README.md
```

# Python Docker Project

This project uses a multi-stage Docker build to create an efficient and secure Python 3.11 container.

## Features

- Python 3.11 runtime
- Multi-stage build for smaller image size
- Security best practices (non-root user)
- Optimized layer caching
- Virtual environment isolation

## Prerequisites

- Docker installed on your system
- Python 3.11 (for local development)

## Project Structure

```
.
├── Dockerfile
├── requirements.txt
├── main.py
└── README.md
```

## Building the Docker Image

To build the Docker image, run:

```bash
docker build -t pysolarsim .
```

## Running the Container

To run the container:

```bash
docker run pysolarsim
```

## Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
# or
.\venv\Scripts\activate  # On Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Dockerfile Features

- Uses `python:3.11-slim` as base image
- Multi-stage build to minimize final image size
- Environment optimizations:
  - `PYTHONDONTWRITEBYTECODE=1`: Prevents .pyc files
  - `PYTHONUNBUFFERED=1`: Unbuffered Python output
  - `PIP_NO_CACHE_DIR=1`: No pip cache
- Security features:
  - Non-root user
  - Proper file permissions
  - Isolated virtual environment

## Environment Variables

The following environment variables are set in the container:

- `PYTHONDONTWRITEBYTECODE=1`
- `PYTHONUNBUFFERED=1`
- `PIP_NO_CACHE_DIR=1`
- `PIP_DISABLE_PIP_VERSION_CHECK=1`

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 