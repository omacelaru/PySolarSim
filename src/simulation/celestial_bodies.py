import numpy as np
import random

class CelestialBody:
    def __init__(self, name, radius, distance, color, orbital_period=1.0, 
                 orbital_inclination=0.0, rotation_period=1.0, mass=1.0):
        self.name = name
        self.radius = radius
        self.distance = distance
        self.color = color
        self.orbital_period = orbital_period
        self.orbital_inclination = orbital_inclination
        self.rotation_period = rotation_period
        self.mass = mass
        self.angle = random.uniform(0, 2 * np.pi)  # Random initial position
        self.rotation_angle = 0.0
        
    def update(self, delta_time):
        # Update orbital position
        self.angle += (2 * np.pi / self.orbital_period) * delta_time
        if self.angle > 2 * np.pi:
            self.angle -= 2 * np.pi
            
        # Update rotation
        self.rotation_angle += (2 * np.pi / self.rotation_period) * delta_time
        if self.rotation_angle > 2 * np.pi:
            self.rotation_angle -= 2 * np.pi
            
    def get_position(self):
        # Calculate current position based on orbital parameters
        x = self.distance * np.cos(self.angle)
        y = self.distance * np.sin(self.angle) * np.cos(self.orbital_inclination)
        z = self.distance * np.sin(self.angle) * np.sin(self.orbital_inclination)
        z_offset = getattr(self, 'z_offset', 0.0)
        return np.array([x, y, z + z_offset])
        
    def get_color(self):
        return self.color
        
    def get_rotation_matrix(self):
        # Create 4x4 rotation matrix for the body's own rotation
        cos_angle = np.cos(self.rotation_angle)
        sin_angle = np.sin(self.rotation_angle)
        
        # Create a 4x4 matrix
        matrix = np.identity(4, dtype=np.float32)
        
        # Set the rotation components
        matrix[0, 0] = cos_angle
        matrix[0, 1] = -sin_angle
        matrix[1, 0] = sin_angle
        matrix[1, 1] = cos_angle
        
        return matrix 