from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QSlider, QComboBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

class OpenGLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(800, 600)
        self.last_mouse_pos = None
        self.is_dragging = False
        
    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        
    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, width / height, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        
    def paintGL(self):
        if hasattr(self.parent(), 'renderer'):
            self.parent().renderer.render(self.parent().solar_system.bodies)
            
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_dragging = True
            self.last_mouse_pos = event.pos()
            
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_dragging = False
            
    def mouseMoveEvent(self, event):
        if self.is_dragging and self.last_mouse_pos is not None:
            delta = event.pos() - self.last_mouse_pos
            if hasattr(self.parent(), 'renderer'):
                self.parent().renderer.update_camera(delta.x() * 0.5, delta.y() * 0.5)
            self.last_mouse_pos = event.pos()
            self.update()
            
    def wheelEvent(self, event):
        if hasattr(self.parent(), 'renderer'):
            delta = event.angleDelta().y()
            zoom_factor = 0.1 if delta > 0 else -0.1
            self.parent().renderer.update_zoom(zoom_factor)
            self.update()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Solar System Simulation")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)
        
        # Create OpenGL widget
        self.gl_widget = OpenGLWidget(self)
        layout.addWidget(self.gl_widget, stretch=1)
        
        # Create control panel
        control_panel = QWidget()
        control_layout = QVBoxLayout(control_panel)
        layout.addWidget(control_panel)
        
        # Add controls
        self.add_simulation_controls(control_layout)
        self.add_view_controls(control_layout)
        self.add_info_panel(control_layout)
        
        # Create animation timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start(16)  # ~60 FPS
        
        # Simulation state
        self.simulation_speed = 1.0
        self.is_paused = False
        
    def add_simulation_controls(self, layout):
        """Add simulation control buttons and sliders"""
        group = QWidget()
        group_layout = QVBoxLayout(group)
        
        # Speed control
        speed_label = QLabel("Simulation Speed:")
        speed_slider = QSlider(Qt.Orientation.Horizontal)
        speed_slider.setRange(1, 100)
        speed_slider.setValue(10)
        speed_slider.valueChanged.connect(self.update_speed)
        
        # Pause button
        pause_button = QPushButton("Pause")
        pause_button.setCheckable(True)
        pause_button.toggled.connect(self.toggle_pause)
        
        # Reset button
        reset_button = QPushButton("Reset")
        reset_button.clicked.connect(self.reset_simulation)
        
        group_layout.addWidget(speed_label)
        group_layout.addWidget(speed_slider)
        group_layout.addWidget(pause_button)
        group_layout.addWidget(reset_button)
        group_layout.addStretch()
        
        layout.addWidget(group)
        
    def add_view_controls(self, layout):
        """Add view control buttons"""
        group = QWidget()
        group_layout = QVBoxLayout(group)
        
        # View mode selector
        view_label = QLabel("View Mode:")
        view_combo = QComboBox()
        view_combo.addItems(["Free Camera", "Follow Planet", "Top View"])
        view_combo.currentIndexChanged.connect(self.change_view_mode)
        
        # Planet selector (for follow mode)
        planet_label = QLabel("Select Planet:")
        planet_combo = QComboBox()
        planet_combo.addItems(["Sun", "Planet 1", "Planet 2", "Planet 3"])
        planet_combo.currentIndexChanged.connect(self.select_planet)
        
        group_layout.addWidget(view_label)
        group_layout.addWidget(view_combo)
        group_layout.addWidget(planet_label)
        group_layout.addWidget(planet_combo)
        group_layout.addStretch()
        
        layout.addWidget(group)
        
    def add_info_panel(self, layout):
        """Add information display panel"""
        group = QWidget()
        group_layout = QVBoxLayout(group)
        
        # Info labels
        self.info_labels = {
            'time': QLabel("Time: 0.0 days"),
            'selected_body': QLabel("Selected: None"),
            'distance': QLabel("Distance: 0.0 AU"),
            'velocity': QLabel("Velocity: 0.0 km/s")
        }
        
        for label in self.info_labels.values():
            group_layout.addWidget(label)
            
        group_layout.addStretch()
        layout.addWidget(group)
        
    def update_simulation(self):
        """Update simulation state"""
        if not self.is_paused:
            dt = 0.016 * self.simulation_speed  # 16ms * speed
            if hasattr(self, 'solar_system'):
                self.solar_system.update(dt)
            self.update_info()
            self.gl_widget.update()
            
    def update_speed(self, value):
        """Update simulation speed"""
        self.simulation_speed = value / 10.0
        
    def toggle_pause(self, checked):
        """Toggle simulation pause state"""
        self.is_paused = checked
        
    def reset_simulation(self):
        """Reset simulation to initial state"""
        if hasattr(self, 'solar_system'):
            self.solar_system = None
            self.setup_simulation()
            
    def change_view_mode(self, index):
        """Change camera view mode"""
        if hasattr(self, 'renderer'):
            self.renderer.view_mode = index
            
    def select_planet(self, index):
        """Select a planet to follow"""
        if hasattr(self, 'renderer'):
            self.renderer.follow_planet = index
            
    def update_info(self):
        """Update information panel"""
        if hasattr(self, 'solar_system'):
            # Update time
            days = self.solar_system.time / (24 * 3600)
            self.info_labels['time'].setText(f"Time: {days:.1f} days")
            
            # Update selected body info
            if hasattr(self, 'renderer') and self.renderer.selected_body:
                body = self.renderer.selected_body
                self.info_labels['selected_body'].setText(f"Selected: {body.name}")
                
                # Calculate distance from sun
                sun = self.solar_system.bodies[0]
                distance = np.linalg.norm(body.position - sun.position) / 1.496e11  # Convert to AU
                self.info_labels['distance'].setText(f"Distance: {distance:.2f} AU")
                
                # Calculate velocity
                velocity = np.linalg.norm(body.velocity) / 1000  # Convert to km/s
                self.info_labels['velocity'].setText(f"Velocity: {velocity:.1f} km/s") 