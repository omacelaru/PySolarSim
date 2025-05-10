from .celestial_bodies import CelestialBody

class SolarSystem:
    def __init__(self):
        self.bodies = []
        self.initialize_basic_system()
        
    def initialize_basic_system(self):
        # Create the sun
        sun = CelestialBody("Sun", 1.0, 0.0, (1.0, 1.0, 0.0))
        self.bodies.append(sun)
        
        # Create some basic planets
        mercury = CelestialBody("Mercury", 0.4, 2.0, (0.7, 0.7, 0.7), 0.24)
        venus = CelestialBody("Venus", 0.6, 3.0, (0.9, 0.7, 0.5), 0.62)
        earth = CelestialBody("Earth", 0.7, 4.0, (0.0, 0.0, 1.0), 1.0)
        
        self.bodies.extend([mercury, venus, earth])
        
    def update(self, delta_time):
        for body in self.bodies:
            body.update(delta_time)
            
    def get_bodies(self):
        return self.bodies 