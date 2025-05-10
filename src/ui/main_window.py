from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QLabel, QSlider, QGroupBox, QSpinBox,
                            QComboBox, QCheckBox)
from PyQt6.QtCore import Qt, QTimer
from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from src.simulation.solar_system import SolarSystem
import math
import numpy as np

class GLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(800, 600)
        self.solar_system = SolarSystem()
        self.simulation_speed = 1.0
        self.is_running = True
        self.selected_body = None
        
        # Camera parameters
        self.camera_distance = 20.0
        self.camera_rotation_x = 30.0
        self.camera_rotation_y = 0.0
        self.camera_rotation_z = 0.0
        
        # Lighting parameters
        self.ambient_light = 0.2
        self.diffuse_light = 1.0
        
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
        glEnable(GL_NORMALIZE)
        
        # Set up light
        glLightfv(GL_LIGHT0, GL_POSITION, (0, 0, 10, 1))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (self.ambient_light, self.ambient_light, self.ambient_light, 1))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (self.diffuse_light, self.diffuse_light, self.diffuse_light, 1))
        
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
        glTranslatef(0.0, 0.0, -self.camera_distance)
        glRotatef(self.camera_rotation_x, 1.0, 0.0, 0.0)
        glRotatef(self.camera_rotation_y, 0.0, 1.0, 0.0)
        glRotatef(self.camera_rotation_z, 0.0, 0.0, 1.0)
        
        # Draw all celestial bodies
        for body in self.solar_system.get_bodies():
            glPushMatrix()
            pos = body.get_position()
            glTranslatef(pos[0], pos[1], pos[2])
            
            # Apply body's own rotation
            rot_matrix = body.get_rotation_matrix()
            glMultMatrixf(rot_matrix.flatten())
            
            color = body.get_color()
            glColor3f(color[0], color[1], color[2])
            
            # Highlight selected body
            if body == self.selected_body:
                glColor3f(1.0, 1.0, 1.0)  # White highlight
                
            self.draw_sphere(body.radius)
            glPopMatrix()
            
    def animate(self):
        if self.is_running:
            self.solar_system.update(0.016 * self.simulation_speed)
            self.update()
            
    def select_body(self, body_name):
        for body in self.solar_system.get_bodies():
            if body.name == body_name:
                self.selected_body = body
                break
        self.update()
        
    def set_simulation_speed(self, speed):
        self.simulation_speed = speed
        
    def toggle_simulation(self, running):
        self.is_running = running
        
    def set_camera_distance(self, distance):
        self.camera_distance = distance
        self.update()
        
    def set_camera_rotation(self, x, y, z):
        self.camera_rotation_x = x
        self.camera_rotation_y = y
        self.camera_rotation_z = z
        self.update()
        
    def set_lighting(self, ambient, diffuse):
        self.ambient_light = ambient
        self.diffuse_light = diffuse
        glLightfv(GL_LIGHT0, GL_AMBIENT, (ambient, ambient, ambient, 1))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (diffuse, diffuse, diffuse, 1))
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
        
        # Simulation Controls
        sim_group = QGroupBox("Simulation Controls")
        sim_layout = QVBoxLayout()
        
        # Play/Pause button
        self.play_button = QPushButton("Pause")
        self.play_button.setCheckable(True)
        self.play_button.setChecked(True)
        self.play_button.clicked.connect(self.toggle_simulation)
        sim_layout.addWidget(self.play_button)
        
        # Speed control
        speed_layout = QHBoxLayout()
        speed_layout.addWidget(QLabel("Speed:"))
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(10)
        self.speed_slider.setValue(1)
        self.speed_slider.valueChanged.connect(self.change_speed)
        speed_layout.addWidget(self.speed_slider)
        sim_layout.addLayout(speed_layout)
        
        sim_group.setLayout(sim_layout)
        control_layout.addWidget(sim_group)
        
        # Camera Controls
        camera_group = QGroupBox("Camera Controls")
        camera_layout = QVBoxLayout()
        
        # Distance control
        dist_layout = QHBoxLayout()
        dist_layout.addWidget(QLabel("Distance:"))
        self.dist_slider = QSlider(Qt.Orientation.Horizontal)
        self.dist_slider.setMinimum(10)
        self.dist_slider.setMaximum(50)
        self.dist_slider.setValue(20)
        self.dist_slider.valueChanged.connect(self.change_camera_distance)
        dist_layout.addWidget(self.dist_slider)
        camera_layout.addLayout(dist_layout)
        
        # Rotation controls
        rot_x_layout = QHBoxLayout()
        rot_x_layout.addWidget(QLabel("Rotate X:"))
        self.rot_x_slider = QSlider(Qt.Orientation.Horizontal)
        self.rot_x_slider.setMinimum(-180)
        self.rot_x_slider.setMaximum(180)
        self.rot_x_slider.setValue(30)
        self.rot_x_slider.valueChanged.connect(self.change_camera_rotation)
        rot_x_layout.addWidget(self.rot_x_slider)
        camera_layout.addLayout(rot_x_layout)
        
        rot_y_layout = QHBoxLayout()
        rot_y_layout.addWidget(QLabel("Rotate Y:"))
        self.rot_y_slider = QSlider(Qt.Orientation.Horizontal)
        self.rot_y_slider.setMinimum(-180)
        self.rot_y_slider.setMaximum(180)
        self.rot_y_slider.setValue(0)
        self.rot_y_slider.valueChanged.connect(self.change_camera_rotation)
        rot_y_layout.addWidget(self.rot_y_slider)
        camera_layout.addLayout(rot_y_layout)
        
        rot_z_layout = QHBoxLayout()
        rot_z_layout.addWidget(QLabel("Rotate Z:"))
        self.rot_z_slider = QSlider(Qt.Orientation.Horizontal)
        self.rot_z_slider.setMinimum(-180)
        self.rot_z_slider.setMaximum(180)
        self.rot_z_slider.setValue(0)
        self.rot_z_slider.valueChanged.connect(self.change_camera_rotation)
        rot_z_layout.addWidget(self.rot_z_slider)
        camera_layout.addLayout(rot_z_layout)
        
        camera_group.setLayout(camera_layout)
        control_layout.addWidget(camera_group)
        
        # Lighting Controls
        light_group = QGroupBox("Lighting Controls")
        light_layout = QVBoxLayout()
        
        # Ambient light control
        ambient_layout = QHBoxLayout()
        ambient_layout.addWidget(QLabel("Ambient:"))
        self.ambient_slider = QSlider(Qt.Orientation.Horizontal)
        self.ambient_slider.setMinimum(0)
        self.ambient_slider.setMaximum(100)
        self.ambient_slider.setValue(20)
        self.ambient_slider.valueChanged.connect(self.change_lighting)
        ambient_layout.addWidget(self.ambient_slider)
        light_layout.addLayout(ambient_layout)
        
        # Diffuse light control
        diffuse_layout = QHBoxLayout()
        diffuse_layout.addWidget(QLabel("Diffuse:"))
        self.diffuse_slider = QSlider(Qt.Orientation.Horizontal)
        self.diffuse_slider.setMinimum(0)
        self.diffuse_slider.setMaximum(100)
        self.diffuse_slider.setValue(100)
        self.diffuse_slider.valueChanged.connect(self.change_lighting)
        diffuse_layout.addWidget(self.diffuse_slider)
        light_layout.addLayout(diffuse_layout)
        
        light_group.setLayout(light_layout)
        control_layout.addWidget(light_group)
        
        # Body Selection
        body_group = QGroupBox("Celestial Body Info")
        body_layout = QVBoxLayout()
        
        self.body_combo = QComboBox()
        self.body_combo.addItems([body.name for body in self.gl_widget.solar_system.get_bodies()])
        self.body_combo.currentTextChanged.connect(self.select_body)
        body_layout.addWidget(self.body_combo)
        
        self.info_label = QLabel("Select a body to view its information")
        self.info_label.setWordWrap(True)
        body_layout.addWidget(self.info_label)
        
        body_group.setLayout(body_layout)
        control_layout.addWidget(body_group)
        
        control_layout.addStretch()
        layout.addWidget(control_panel, stretch=1)
        
    def toggle_simulation(self, checked):
        self.gl_widget.toggle_simulation(checked)
        self.play_button.setText("Play" if not checked else "Pause")
        
    def change_speed(self, value):
        self.gl_widget.set_simulation_speed(value)
        
    def change_camera_distance(self, value):
        self.gl_widget.set_camera_distance(value)
        
    def change_camera_rotation(self, _):
        x = self.rot_x_slider.value()
        y = self.rot_y_slider.value()
        z = self.rot_z_slider.value()
        self.gl_widget.set_camera_rotation(x, y, z)
        
    def change_lighting(self, _):
        ambient = self.ambient_slider.value() / 100.0
        diffuse = self.diffuse_slider.value() / 100.0
        self.gl_widget.set_lighting(ambient, diffuse)
        
    def select_body(self, body_name):
        self.gl_widget.select_body(body_name)
        # Update info label with body details
        for body in self.gl_widget.solar_system.get_bodies():
            if body.name == body_name:
                info = f"Name: {body.name}\n"
                info += f"Radius: {body.radius:.2f}\n"
                info += f"Distance: {body.distance:.2f}\n"
                info += f"Orbital Period: {body.orbital_period:.2f} years\n"
                info += f"Rotation Period: {body.rotation_period:.2f} days\n"
                info += f"Orbital Inclination: {math.degrees(body.orbital_inclination):.2f}°"
                self.info_label.setText(info)
                break 