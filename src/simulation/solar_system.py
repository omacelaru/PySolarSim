from .celestial_bodies import CelestialBody, Star
import numpy as np

class SolarSystem:
    def __init__(self):
        self.bodies = []
        self.time_scale = 1.0
        self.paused = False
    
    def add_body(self, body):
        self.bodies.append(body)
    
    def create_solar_system(self):
        # Create Sun
        sun = Star("Sun", 1.989e30, 696340000, [0, 0, 0])
        self.add_body(sun)
        
        # Create some example planets
        # Mercury
        mercury = CelestialBody(
            "Mercury",
            3.285e23,
            2439700,
            [57909050000, 0, 0],
            [0, 47400, 0],
            (0.7, 0.7, 0.7)
        )
        self.add_body(mercury)
        
        # Venus
        venus = CelestialBody(
            "Venus",
            4.867e24,
            6051800,
            [108208000000, 0, 0],
            [0, 35000, 0],
            (0.9, 0.7, 0.5)
        )
        self.add_body(venus)
        
        # Earth
        earth = CelestialBody(
            "Earth",
            5.972e24,
            6371000,
            [149600000000, 0, 0],
            [0, 29800, 0],
            (0.2, 0.5, 0.8)
        )
        self.add_body(earth)
    
    def update(self, dt):
        if not self.paused:
            # Update all bodies
            for body in self.bodies:
                body.update_position(dt * self.time_scale, self.bodies)
    
    def toggle_pause(self):
        self.paused = not self.paused
    
    def reset(self):
        self.bodies.clear()
        self.create_solar_system()
    
    def get_body_by_name(self, name):
        for body in self.bodies:
            if body.name == name:
                return body
        return None 