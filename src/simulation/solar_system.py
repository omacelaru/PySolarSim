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
        
        self.bodies.extend([mercury, venus, earth, mars])
        
    def update(self, delta_time):
        # Slow down simulation for more realistic planet movement
        slow_factor = 0.1  # Lower = slower
        for body in self.bodies:
            body.update(delta_time * slow_factor)
            
    def get_bodies(self):
        return self.bodies 