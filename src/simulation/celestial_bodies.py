import numpy as np

class CelestialBody:
    def __init__(self, name, radius, distance, color, orbital_period=1.0):
        self.name = name
        self.radius = radius
        self.distance = distance
        self.color = color
        self.orbital_period = orbital_period
        self.angle = 0.0
        
    def update(self, delta_time):
        # Update the orbital position
        self.angle += (2 * np.pi / self.orbital_period) * delta_time
        if self.angle > 2 * np.pi:
            self.angle -= 2 * np.pi
            
    def get_position(self):
        # Calculate current position based on orbital parameters
        x = self.distance * np.cos(self.angle)
        y = self.distance * np.sin(self.angle)
        return np.array([x, y, 0.0])
        
    def get_color(self):
        return self.color 