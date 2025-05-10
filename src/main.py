import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

from gui.main_window import MainWindow
from physics.solar_system import SolarSystem
from graphics.renderer import Renderer
from ai.celestial_generator import CelestialGenerator

class SolarSimulation:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.main_window = MainWindow()
        self.solar_system = SolarSystem()
        self.renderer = Renderer()
        self.celestial_generator = CelestialGenerator()
        
        # Initialize the simulation
        self.setup_simulation()
        
    def setup_simulation(self):
        """Initialize the solar system with default celestial bodies"""
        # Add the sun
        self.solar_system.add_sun()
        
        # Generate initial planets using AI
        planets = self.celestial_generator.generate_planets(8)
        for planet in planets:
            self.solar_system.add_planet(planet)
            
    def run(self):
        """Start the application"""
        self.main_window.show()
        return self.app.exec()

if __name__ == "__main__":
    simulation = SolarSimulation()
    sys.exit(simulation.run()) 