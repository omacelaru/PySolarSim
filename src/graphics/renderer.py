from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QSurfaceFormat
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from simulation.solar_system import SolarSystem

class OpenGLWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        
        # Set up OpenGL format
        format = QSurfaceFormat()
        format.setVersion(3, 3)
        format.setProfile(QSurfaceFormat.OpenGLContextProfile.CoreProfile)
        QSurfaceFormat.setDefaultFormat(format)
        
        # Camera settings
        self.camera_distance = 200.0
        self.camera_rotation = [0.0, 0.0, 0.0]
        
        # Create solar system
        self.solar_system = SolarSystem()
        self.solar_system.create_solar_system()
        
        # Scale factor for visualization
        self.scale_factor = 1e-9  # Scale down to reasonable size
        
        # Animation timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start(16)  # ~60 FPS
        
        # Initialize OpenGL context
        self.context = None
        self.initializeGL()
    
    def initializeGL(self):
        if self.context is None:
            self.context = QSurfaceFormat()
            self.context.setVersion(3, 3)
            self.context.setProfile(QSurfaceFormat.OpenGLContextProfile.CoreProfile)
            QSurfaceFormat.setDefaultFormat(self.context)
        
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        
        # Set up light
        glLightfv(GL_LIGHT0, GL_POSITION, (0, 0, 0, 1))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))
    
    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, width / height, 0.1, 1000.0)
        glMatrixMode(GL_MODELVIEW)
    
    def update_simulation(self):
        self.solar_system.update(1/60)  # Update with 60 FPS
        self.update()
    
    def paintEvent(self, event):
        self.paintGL()
    
    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # Set up camera
        glTranslatef(0, 0, -self.camera_distance)
        glRotatef(self.camera_rotation[0], 1, 0, 0)
        glRotatef(self.camera_rotation[1], 0, 1, 0)
        glRotatef(self.camera_rotation[2], 0, 0, 1)
        
        # Draw all celestial bodies
        for body in self.solar_system.bodies:
            # Scale position for visualization
            pos = body.position * self.scale_factor
            radius = body.radius * self.scale_factor * 100  # Scale radius for better visibility
            
            # Draw the body
            self.draw_sphere(pos[0], pos[1], pos[2], radius, body.color)
            
            # Draw orbit trail
            if len(body.orbit_points) > 1:
                self.draw_orbit(body.get_orbit_points() * self.scale_factor)
    
    def draw_sphere(self, x, y, z, radius, color):
        glPushMatrix()
        glTranslatef(x, y, z)
        glColor3f(*color)
        
        quad = gluNewQuadric()
        gluSphere(quad, radius, 32, 32)
        gluDeleteQuadric(quad)
        
        glPopMatrix()
    
    def draw_orbit(self, points):
        glDisable(GL_LIGHTING)
        glBegin(GL_LINE_STRIP)
        glColor3f(0.5, 0.5, 0.5)
        for point in points:
            glVertex3f(point[0], point[1], point[2])
        glEnd()
        glEnable(GL_LIGHTING)
    
    def mousePressEvent(self, event):
        self.last_pos = event.pos()
    
    def mouseMoveEvent(self, event):
        dx = event.pos().x() - self.last_pos.x()
        dy = event.pos().y() - self.last_pos.y()
        
        if event.buttons() & Qt.MouseButton.LeftButton:
            self.camera_rotation[1] += dx
            self.camera_rotation[0] += dy
        
        self.last_pos = event.pos()
    
    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        self.camera_distance -= delta * 0.1
        self.camera_distance = max(10, min(200, self.camera_distance))
    
    def toggle_simulation(self):
        self.solar_system.toggle_pause()
    
    def reset_simulation(self):
        self.solar_system.reset() 