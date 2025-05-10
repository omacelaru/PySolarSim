from .celestial_bodies import CelestialBody

class SolarSystem:
    def __init__(self):
        self.bodies = []
        self.initialize_basic_system()
        
    def initialize_basic_system(self):
        # Create the sun with realistic parameters
        sun = CelestialBody(
            name="Sun",
            radius=2.0,  # Scaled down for visualization
            distance=0.0,
            color=(1.0, 0.8, 0.0),  # More realistic sun color
            rotation_period=27.0  # Earth days
        )
        self.bodies.append(sun)
        
        # Create planets with more realistic parameters
        mercury = CelestialBody(
            name="Mercury",
            radius=0.4,
            distance=3.0,
            color=(0.7, 0.7, 0.7),
            orbital_period=0.24,  # Earth years
            orbital_inclination=0.034,  # radians
            rotation_period=58.6  # Earth days
        )
        
        venus = CelestialBody(
            name="Venus",
            radius=0.6,
            distance=4.0,
            color=(0.9, 0.7, 0.5),
            orbital_period=0.62,
            orbital_inclination=0.003,  # radians
            rotation_period=243.0  # Earth days (retrograde)
        )
        
        earth = CelestialBody(
            name="Earth",
            radius=0.7,
            distance=5.0,
            color=(0.2, 0.4, 0.8),
            orbital_period=1.0,
            orbital_inclination=0.0,
            rotation_period=1.0  # Earth days
        )
        
        mars = CelestialBody(
            name="Mars",
            radius=0.5,
            distance=6.0,
            color=(0.8, 0.3, 0.2),
            orbital_period=1.88,
            orbital_inclination=0.032,  # radians
            rotation_period=1.03  # Earth days
        )
        
        jupiter = CelestialBody(
            name="Jupiter",
            radius=1.2,
            distance=8.0,
            color=(0.9, 0.8, 0.6),
            orbital_period=11.86,
            orbital_inclination=0.022,  # radians
            rotation_period=0.41  # Earth days
        )
        
        saturn = CelestialBody(
            name="Saturn",
            radius=1.0,
            distance=10.0,
            color=(0.9, 0.8, 0.5),
            orbital_period=29.46,
            orbital_inclination=0.043,  # radians
            rotation_period=0.45  # Earth days
        )
        
        uranus = CelestialBody(
            name="Uranus",
            radius=0.8,
            distance=12.0,
            color=(0.6, 0.8, 0.9),
            orbital_period=84.01,
            orbital_inclination=0.013,  # radians
            rotation_period=0.72  # Earth days
        )
        
        neptune = CelestialBody(
            name="Neptune",
            radius=0.8,
            distance=14.0,
            color=(0.3, 0.5, 0.9),
            orbital_period=164.8,
            orbital_inclination=0.030,  # radians
            rotation_period=0.67  # Earth days
        )
        
        pluto = CelestialBody(
            name="Pluto",
            radius=0.2,
            distance=16.0,
            color=(0.8, 0.8, 0.7),
            orbital_period=248.0,
            orbital_inclination=0.157,  # radians
            rotation_period=6.39  # Earth days
        )
        
        self.bodies.extend([
            mercury, venus, earth, mars, jupiter, saturn, uranus, neptune, pluto
        ])
        # Add the Moon as a satellite of Earth
        self.satellites = {"Earth": []}
        moon = CelestialBody(
            name="Moon",
            radius=0.18,
            distance=0.9,  # Scaled distance from Earth
            color=(0.8, 0.8, 0.85),
            orbital_period=0.0748,  # Earth years (~27.3 days)
            orbital_inclination=0.089,  # radians (~5.1 deg)
            rotation_period=27.3  # Synchronous rotation
        )
        self.satellites["Earth"].append(moon)
        
    def update(self, delta_time):
        # Slow down simulation for more realistic planet movement
        slow_factor = 0.1  # Lower = slower
        for body in self.bodies:
            body.update(delta_time * slow_factor)
        # Update satellites
        for planet, moons in getattr(self, 'satellites', {}).items():
            for moon in moons:
                moon.update(delta_time * slow_factor)
            
    def get_bodies(self):
        return self.bodies

    def get_satellites(self, planet_name):
        return self.satellites.get(planet_name, []) 