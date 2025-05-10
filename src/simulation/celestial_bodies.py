import numpy as np

class CelestialBody:
    def __init__(self, name, mass, radius, position, velocity, color):
        self.name = name
        self.mass = mass
        self.radius = radius
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.color = color
        self.orbit_points = []
        self.max_orbit_points = 1000
    
    def update_position(self, dt, bodies):
        # Simple Euler integration for now
        # Will be replaced with more accurate methods later
        acceleration = np.zeros(3)
        
        # Calculate gravitational forces from other bodies
        for body in bodies:
            if body is not self:
                r = body.position - self.position
                distance = np.linalg.norm(r)
                if distance > 0:
                    force = 6.67430e-11 * self.mass * body.mass / (distance * distance)
                    direction = r / distance
                    acceleration += force * direction / self.mass
        
        # Update velocity and position
        self.velocity += acceleration * dt
        self.position += self.velocity * dt
        
        # Store orbit point
        self.orbit_points.append(self.position.copy())
        if len(self.orbit_points) > self.max_orbit_points:
            self.orbit_points.pop(0)
    
    def get_orbit_points(self):
        return np.array(self.orbit_points)

class Star(CelestialBody):
    def __init__(self, name, mass, radius, position, color=(1, 1, 0)):
        super().__init__(name, mass, radius, position, [0, 0, 0], color)
        self.luminosity = 1.0  # Relative to Sun
        self.temperature = 5778  # Kelvin 