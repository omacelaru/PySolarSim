import numpy as np
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class CelestialBody:
    name: str
    mass: float  # in kg
    radius: float  # in meters
    position: np.ndarray  # in meters
    velocity: np.ndarray  # in m/s
    color: Tuple[float, float, float]
    rotation_period: float  # in seconds
    orbital_period: float  # in seconds
    parent: 'CelestialBody' = None

class SolarSystem:
    def __init__(self):
        self.bodies: List[CelestialBody] = []
        self.G = 6.67430e-11  # Gravitational constant
        self.time = 0.0  # Simulation time in seconds
        
    def add_sun(self):
        """Add the sun to the solar system"""
        sun = CelestialBody(
            name="Sun",
            mass=1.989e30,  # kg
            radius=696340e3,  # meters
            position=np.array([0.0, 0.0, 0.0]),
            velocity=np.array([0.0, 0.0, 0.0]),
            color=(1.0, 0.8, 0.0),
            rotation_period=25.05 * 24 * 3600,  # 25.05 days in seconds
            orbital_period=0
        )
        self.bodies.append(sun)
        
    def add_planet(self, planet: CelestialBody):
        """Add a planet to the solar system"""
        self.bodies.append(planet)
        
    def calculate_gravitational_force(self, body1: CelestialBody, body2: CelestialBody) -> np.ndarray:
        """Calculate gravitational force between two bodies"""
        r = body2.position - body1.position
        distance = np.linalg.norm(r)
        if distance == 0:
            return np.zeros(3)
            
        force_magnitude = self.G * body1.mass * body2.mass / (distance ** 2)
        force_direction = r / distance
        return force_magnitude * force_direction
        
    def update(self, dt: float):
        """Update the positions and velocities of all bodies"""
        # Calculate forces
        forces = {body: np.zeros(3) for body in self.bodies}
        
        for i, body1 in enumerate(self.bodies):
            for body2 in self.bodies[i+1:]:
                force = self.calculate_gravitational_force(body1, body2)
                forces[body1] += force
                forces[body2] -= force
                
        # Update positions and velocities
        for body in self.bodies:
            # F = ma -> a = F/m
            acceleration = forces[body] / body.mass
            
            # Update velocity using acceleration
            body.velocity += acceleration * dt
            
            # Update position using velocity
            body.position += body.velocity * dt
            
        # Update simulation time
        self.time += dt
            
    def get_orbital_velocity(self, mass: float, distance: float) -> float:
        """Calculate the orbital velocity for a circular orbit"""
        return np.sqrt(self.G * mass / distance) 