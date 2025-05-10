import numpy as np
from typing import List, Tuple
from dataclasses import dataclass
from physics.solar_system import CelestialBody
import random  # Add this import

class CelestialGenerator:
    def __init__(self):
        # Constants for realistic planet generation
        self.MIN_PLANET_MASS = 3.3e23  # Mercury's mass
        self.MAX_PLANET_MASS = 1.9e27  # Jupiter's mass
        self.MIN_PLANET_RADIUS = 2.4e6  # Mercury's radius
        self.MAX_PLANET_RADIUS = 7.0e7  # Jupiter's radius
        self.MIN_ORBITAL_DISTANCE = 5.8e10  # Mercury's distance
        self.MAX_ORBITAL_DISTANCE = 4.5e12  # Neptune's distance
        
        # Color palettes for different planet types
        self.ROCKY_PLANET_COLORS = [
            (0.8, 0.4, 0.2),  # Mars-like
            (0.6, 0.6, 0.6),  # Mercury-like
            (0.4, 0.4, 0.8),  # Earth-like
            (0.8, 0.8, 0.4),  # Venus-like
        ]
        
        self.GAS_GIANT_COLORS = [
            (0.8, 0.6, 0.4),  # Jupiter-like
            (0.6, 0.8, 0.8),  # Uranus-like
            (0.4, 0.6, 0.8),  # Neptune-like
            (0.8, 0.8, 0.6),  # Saturn-like
        ]
        
    def generate_planets(self, num_planets: int) -> List[CelestialBody]:
        """Generate a set of planets with realistic properties"""
        planets = []
        sun_mass = 1.989e30  # Sun's mass
        
        for i in range(num_planets):
            # Determine if it's a rocky planet or gas giant
            is_gas_giant = np.random.random() < 0.3  # 30% chance of gas giant
            
            # Generate mass and radius
            if is_gas_giant:
                mass = np.random.uniform(self.MAX_PLANET_MASS * 0.5, self.MAX_PLANET_MASS)
                radius = np.random.uniform(self.MAX_PLANET_RADIUS * 0.5, self.MAX_PLANET_RADIUS)
                color = random.choice(self.GAS_GIANT_COLORS)  # Use Python's random.choice
            else:
                mass = np.random.uniform(self.MIN_PLANET_MASS, self.MIN_PLANET_MASS * 10)
                radius = np.random.uniform(self.MIN_PLANET_RADIUS, self.MIN_PLANET_RADIUS * 3)
                color = random.choice(self.ROCKY_PLANET_COLORS)  # Use Python's random.choice
                
            # Generate orbital distance
            orbital_distance = self.MIN_ORBITAL_DISTANCE * (1.5 ** i)  # Bode's law-like spacing
            
            # Calculate orbital velocity
            orbital_velocity = np.sqrt(6.67430e-11 * sun_mass / orbital_distance)
            
            # Generate random orbital plane
            inclination = np.random.uniform(-0.1, 0.1)  # Small inclination
            angle = np.random.uniform(0, 2 * np.pi)
            
            # Calculate position and velocity
            position = np.array([
                orbital_distance * np.cos(angle),
                orbital_distance * np.sin(angle) * np.sin(inclination),
                orbital_distance * np.sin(angle) * np.cos(inclination)
            ])
            
            velocity = np.array([
                -orbital_velocity * np.sin(angle),
                orbital_velocity * np.cos(angle) * np.sin(inclination),
                orbital_velocity * np.cos(angle) * np.cos(inclination)
            ])
            
            # Calculate rotation and orbital periods
            rotation_period = np.random.uniform(0.5, 2.0) * 24 * 3600  # 0.5-2 Earth days
            orbital_period = 2 * np.pi * np.sqrt(orbital_distance ** 3 / (6.67430e-11 * sun_mass))
            
            # Create planet
            planet = CelestialBody(
                name=f"Planet {i+1}",
                mass=mass,
                radius=radius,
                position=position,
                velocity=velocity,
                color=color,
                rotation_period=rotation_period,
                orbital_period=orbital_period
            )
            
            planets.append(planet)
            
        return planets
        
    def generate_moons(self, planet: CelestialBody, num_moons: int) -> List[CelestialBody]:
        """Generate moons for a given planet"""
        moons = []
        
        for i in range(num_moons):
            # Generate moon properties
            mass = planet.mass * np.random.uniform(1e-4, 1e-2)
            radius = planet.radius * np.random.uniform(0.01, 0.1)
            
            # Generate orbital distance
            orbital_distance = planet.radius * np.random.uniform(2, 10)
            
            # Calculate orbital velocity
            orbital_velocity = np.sqrt(6.67430e-11 * planet.mass / orbital_distance)
            
            # Generate random orbital plane
            angle = np.random.uniform(0, 2 * np.pi)
            
            # Calculate position and velocity relative to planet
            position = planet.position + np.array([
                orbital_distance * np.cos(angle),
                0,
                orbital_distance * np.sin(angle)
            ])
            
            velocity = planet.velocity + np.array([
                -orbital_velocity * np.sin(angle),
                0,
                orbital_velocity * np.cos(angle)
            ])
            
            # Calculate rotation and orbital periods
            rotation_period = np.random.uniform(0.5, 2.0) * 24 * 3600
            orbital_period = 2 * np.pi * np.sqrt(orbital_distance ** 3 / (6.67430e-11 * planet.mass))
            
            # Create moon
            moon = CelestialBody(
                name=f"{planet.name} Moon {i+1}",
                mass=mass,
                radius=radius,
                position=position,
                velocity=velocity,
                color=(0.7, 0.7, 0.7),
                rotation_period=rotation_period,
                orbital_period=orbital_period,
                parent=planet
            )
            
            moons.append(moon)
            
        return moons 