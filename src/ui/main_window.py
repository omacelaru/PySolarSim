from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt, QTimer
from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from src.simulation.solar_system import SolarSystem
import math

class GLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(800, 600)
        self.solar_system = SolarSystem()
        self.rotation = 0.0
        
        # Setup animation timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(16)  # ~60 FPS
        
    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        
        # Set up light
        glLightfv(GL_LIGHT0, GL_POSITION, (0, 0, 10, 1))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))
        
    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, width/height, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        
    def draw_sphere(self, radius, slices=32, stacks=32):
        for i in range(stacks):
            lat0 = math.pi * (-0.5 + float(i) / stacks)
            z0 = math.sin(lat0)
            zr0 = math.cos(lat0)
            
            lat1 = math.pi * (-0.5 + float(i + 1) / stacks)
            z1 = math.sin(lat1)
            zr1 = math.cos(lat1)
            
            glBegin(GL_QUAD_STRIP)
            for j in range(slices + 1):
                lng = 2 * math.pi * float(j) / slices
                x = math.cos(lng)
                y = math.sin(lng)
                
                glNormal3f(x * zr0, y * zr0, z0)
                glVertex3f(x * zr0 * radius, y * zr0 * radius, z0 * radius)
                
                glNormal3f(x * zr1, y * zr1, z1)
                glVertex3f(x * zr1 * radius, y * zr1 * radius, z1 * radius)
            glEnd()
        
    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # Set up the camera
        glTranslatef(0.0, 0.0, -20.0)
        glRotatef(30.0, 1.0, 0.0, 0.0)
        glRotatef(self.rotation, 0.0, 1.0, 0.0)
        
        # Draw all celestial bodies
        for body in self.solar_system.get_bodies():
            glPushMatrix()
            pos = body.get_position()
            glTranslatef(pos[0], pos[1], pos[2])
            color = body.get_color()
            glColor3f(color[0], color[1], color[2])
            self.draw_sphere(body.radius)
            glPopMatrix()
            
    def animate(self):
        self.solar_system.update(0.016)  # Update with delta time
        self.rotation += 0.5
        self.update()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Solar System Simulation")
        self.setMinimumSize(1000, 800)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)
        
        # Create OpenGL widget
        self.gl_widget = GLWidget()
        layout.addWidget(self.gl_widget, stretch=2)
        
        # Create control panel
        control_panel = QWidget()
        control_layout = QVBoxLayout(control_panel)
        
        # Add some basic controls
        info_label = QLabel("Solar System Info")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        control_layout.addWidget(info_label)
        
        # Add buttons for basic controls
        reset_button = QPushButton("Reset View")
        reset_button.clicked.connect(self.reset_view)
        control_layout.addWidget(reset_button)
        
        control_layout.addStretch()
        layout.addWidget(control_panel, stretch=1)
        
    def reset_view(self):
        self.gl_widget.rotation = 0.0
        self.gl_widget.update() 