import pytest
import numpy as np
from src.simulation.solar_system import SolarSystem
from src.simulation.celestial_bodies import CelestialBody, Star

def test_solar_system_creation():
    system = SolarSystem()
    assert len(system.bodies) == 0
    
    system.create_solar_system()
    assert len(system.bodies) == 4  # Sun, Mercury, Venus, Earth
    
    # Test if Sun is created correctly
    sun = system.get_body_by_name("Sun")
    assert isinstance(sun, Star)
    assert sun.mass == 1.989e30
    assert sun.radius == 696340000
    
    # Test if Earth is created correctly
    earth = system.get_body_by_name("Earth")
    assert isinstance(earth, CelestialBody)
    assert earth.mass == 5.972e24
    assert earth.radius == 6371000

def test_simulation_update():
    system = SolarSystem()
    system.create_solar_system()
    
    # Store initial positions
    initial_positions = {body.name: body.position.copy() for body in system.bodies}
    
    # Update simulation
    system.update(1.0)  # Update for 1 second
    
    # Check if positions have changed
    for body in system.bodies:
        assert not np.array_equal(body.position, initial_positions[body.name])

def test_pause_functionality():
    system = SolarSystem()
    system.create_solar_system()
    
    # Store initial positions
    initial_positions = {body.name: body.position.copy() for body in system.bodies}
    
    # Pause simulation
    system.toggle_pause()
    assert system.paused
    
    # Update simulation
    system.update(1.0)
    
    # Check if positions haven't changed
    for body in system.bodies:
        assert np.array_equal(body.position, initial_positions[body.name])
    
    # Resume simulation
    system.toggle_pause()
    assert not system.paused
    
    # Update again
    system.update(1.0)
    
    # Check if positions have changed
    for body in system.bodies:
        assert not np.array_equal(body.position, initial_positions[body.name]) 