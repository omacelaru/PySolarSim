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

## Rulare cu Docker

Poți rula aplicația și în container Docker (necesită X11 pentru interfață grafică):

1. Construiește imaginea:
```bash
docker build -t pysolarsim .
```
2. Rulează aplicația (pe Linux, cu X11 forwarding):
```bash
docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix pysolarsim
```
3. Pe Windows, folosește un X server (VcXsrv/Xming) și setează variabila DISPLAY corespunzător.

> Notă: Aplicațiile GUI în Docker necesită X11 forwarding sau un X server local.

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
├── Dockerfile               # Containerizare rapidă
└── README.md
``` 