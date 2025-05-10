from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
from typing import List, Tuple
import math

class Renderer:
    def __init__(self):
        self.camera_distance = 5.0
        self.camera_rotation_x = 30.0
        self.camera_rotation_y = 0.0
        self.light_position = (0.0, 0.0, 10.0, 1.0)
        self.ambient_light = (0.2, 0.2, 0.2, 1.0)
        self.diffuse_light = (1.0, 1.0, 1.0, 1.0)
        
        # Add view mode and selection attributes
        self.view_mode = 0  # 0: Free Camera, 1: Follow Planet, 2: Top View
        self.follow_planet = 0  # Index of planet to follow
        self.selected_body = None  # Currently selected celestial body
        
    def initialize(self):
        """Initialize OpenGL settings"""
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        # Set up light
        glLightfv(GL_LIGHT0, GL_POSITION, self.light_position)
        glLightfv(GL_LIGHT0, GL_AMBIENT, self.ambient_light)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, self.diffuse_light)
        
    def resize(self, width: int, height: int):
        """Handle window resize"""
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, width / height, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        
    def setup_camera(self):
        """Set up the camera position and orientation"""
        glLoadIdentity()
        
        # Calculate camera position
        x = self.camera_distance * math.cos(math.radians(self.camera_rotation_y)) * math.cos(math.radians(self.camera_rotation_x))
        y = self.camera_distance * math.sin(math.radians(self.camera_rotation_x))
        z = self.camera_distance * math.sin(math.radians(self.camera_rotation_y)) * math.cos(math.radians(self.camera_rotation_x))
        
        gluLookAt(x, y, z, 0, 0, 0, 0, 1, 0)
        
    def draw_celestial_body(self, body, scale_factor: float = 1e-4):
        """Draw a celestial body with proper lighting and materials"""
        glPushMatrix()
        
        # Set position
        glTranslatef(body.position[0] * scale_factor,
                    body.position[1] * scale_factor,
                    body.position[2] * scale_factor)
        
        # Set material properties
        glColor3f(*body.color)
        glMaterialfv(GL_FRONT, GL_AMBIENT, (*body.color, 0.2))
        glMaterialfv(GL_FRONT, GL_DIFFUSE, (*body.color, 1.0))
        glMaterialfv(GL_FRONT, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))
        glMaterialf(GL_FRONT, GL_SHININESS, 50.0)
        
        # Draw sphere
        sphere = gluNewQuadric()
        gluQuadricTexture(sphere, GL_TRUE)
        radius = body.radius * scale_factor
        gluSphere(sphere, radius, 32, 32)
        
        glPopMatrix()
        
    def draw_orbit(self, body, scale_factor: float = 1e-4):
        """Draw the orbital path of a celestial body"""
        if body.parent is None:
            return
            
        glPushMatrix()
        glColor3f(0.5, 0.5, 0.5)
        glBegin(GL_LINE_LOOP)
        
        # Calculate orbital radius
        radius = np.linalg.norm(body.position - body.parent.position) * scale_factor
        
        # Draw circle
        for i in range(360):
            angle = math.radians(i)
            x = radius * math.cos(angle)
            z = radius * math.sin(angle)
            glVertex3f(x, 0, z)
            
        glEnd()
        glPopMatrix()
        
    def render(self, bodies: List):
        """Render the entire scene"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        self.setup_camera()
        
        # Draw all bodies and their orbits
        for body in bodies:
            self.draw_orbit(body)
            self.draw_celestial_body(body)
            
    def update_camera(self, dx: float, dy: float):
        """Update camera rotation"""
        self.camera_rotation_y += dx
        self.camera_rotation_x += dy
        self.camera_rotation_x = max(-89, min(89, self.camera_rotation_x))
        
    def update_zoom(self, delta: float):
        """Update camera zoom"""
        self.camera_distance = max(2.0, min(20.0, self.camera_distance - delta)) 