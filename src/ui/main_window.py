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
from PyQt6.QtGui import QMouseEvent, QWheelEvent, QKeyEvent
import random

class GLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(800, 600)
        self.solar_system = SolarSystem()
        self.simulation_speed = 1.0
        self.is_running = True
        self.selected_body = None
        
        # Camera parameters
        self.camera_distance = 43.0  # Large enough to see all planets
        self.camera_rotation_x = 30.0
        self.camera_rotation_y = 0.0
        self.camera_rotation_z = 0.0
        
        # Lighting parameters
        self.ambient_light = 0.2
        self.diffuse_light = 1.0
        
        # View mode
        self.view_mode = 'Oblic View'
        self.follow_distance = 8.0
        
        # Setup animation timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(16)  # ~60 FPS
        
        self.last_mouse_pos = None
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        
        self.stars = [
            (random.uniform(-60, 60), random.uniform(-60, 60), random.uniform(-60, 60))
            for _ in range(300)
        ]
        
        self.show_orbits = True
        
    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_NORMALIZE)
        self.update_lighting()
        
        # Select Sun by default
        if self.selected_body is None:
            self.selected_body = self.solar_system.get_bodies()[0]
        
    def update_lighting(self):
        # Place light at the sun's position
        sun = self.solar_system.get_bodies()[0]
        sun_pos = sun.get_position()
        glLightfv(GL_LIGHT0, GL_POSITION, (sun_pos[0], sun_pos[1], sun_pos[2], 1.0))
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
        
    def draw_selection_ring(self, radius, color):
        glColor3f(*color)  # Use planet's own color
        glLineWidth(2.0)
        glBegin(GL_LINE_LOOP)
        for i in range(64):
            angle = 2 * math.pi * i / 64
            x = math.cos(angle) * (radius * 1.15)
            y = math.sin(angle) * (radius * 1.15)
            glVertex3f(x, y, 0)
        glEnd()
        glLineWidth(1.0)

    def draw_saturn_rings(self, radius):
        glPushAttrib(GL_ENABLE_BIT)
        glDisable(GL_LIGHTING)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(0.8, 0.8, 0.5, 0.4)
        inner = radius * 1.3
        outer = radius * 2.2
        glBegin(GL_TRIANGLE_STRIP)
        for i in range(65):
            angle = 2 * math.pi * i / 64
            x_in = math.cos(angle) * inner
            y_in = math.sin(angle) * inner
            x_out = math.cos(angle) * outer
            y_out = math.sin(angle) * outer
            glVertex3f(x_in, y_in, 0)
            glVertex3f(x_out, y_out, 0)
        glEnd()
        glDisable(GL_BLEND)
        glEnable(GL_LIGHTING)
        glPopAttrib()

    def draw_orbit(self, body):
        glDisable(GL_LIGHTING)
        glColor4f(0.7, 0.7, 0.7, 0.5)
        glLineWidth(1.0)
        glBegin(GL_LINE_LOOP)
        for i in range(128):
            angle = 2 * math.pi * i / 128
            x = body.distance * math.cos(angle)
            y = body.distance * math.sin(angle) * math.cos(body.orbital_inclination)
            z = body.distance * math.sin(angle) * math.sin(body.orbital_inclination)
            z += getattr(body, 'z_offset', 0.0)
            glVertex3f(x, y, z)
        glEnd()
        glEnable(GL_LIGHTING)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # Camera logic based on view mode
        if self.view_mode == 'Free Camera':
            glTranslatef(0.0, 0.0, -self.camera_distance)
            glRotatef(self.camera_rotation_x, 1.0, 0.0, 0.0)
            glRotatef(self.camera_rotation_y, 0.0, 1.0, 0.0)
            glRotatef(self.camera_rotation_z, 0.0, 0.0, 1.0)
        elif self.view_mode == 'Top View':
            gluLookAt(0, 0, self.camera_distance, 0, 0, 0, 0, 1, 0)
        elif self.view_mode == 'Lateral View':
            gluLookAt(self.camera_distance, 0, 0, 0, 0, 0, 0, 0, 1)
        elif self.view_mode == 'Oblic View':
            d = self.camera_distance / math.sqrt(3)
            gluLookAt(d, d, d, 0, 0, 0, 0, 0, 1)
        elif self.view_mode == 'Follow Planet' and self.selected_body is not None:
            pos = self.selected_body.get_position()
            if self.selected_body.name.lower() == 'sun':
                cam_pos = pos + np.array([0.0, 0.0, self.follow_distance])
                up = np.array([0, 1, 0])
            else:
                offset = np.array([1.0, 1.0, 1.0])
                offset = offset / np.linalg.norm(offset) * self.follow_distance
                cam_pos = pos + offset
                up = np.array([0, 0, 1])
            gluLookAt(cam_pos[0], cam_pos[1], cam_pos[2],
                      pos[0], pos[1], pos[2],
                      up[0], up[1], up[2])
        
        # Draw starry background
        glDisable(GL_LIGHTING)
        glPointSize(1.5)
        glBegin(GL_POINTS)
        glColor3f(1.0, 1.0, 1.0)
        for x, y, z in self.stars:
            glVertex3f(x, y, z)
        glEnd()
        glEnable(GL_LIGHTING)
        self.update_lighting()
        
        # Draw all orbital trajectories if enabled (read directly from MainWindow)
        mainwindow = self.parent().parent()
        if hasattr(mainwindow, 'orbit_checkbox') and mainwindow.orbit_checkbox.isChecked():
            for body in self.solar_system.get_bodies():
                self.draw_orbit(body)
        
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
            
            # Draw selection ring if selected
            if body == self.selected_body:
                glDisable(GL_LIGHTING)
                self.draw_selection_ring(body.radius, color)
                glEnable(GL_LIGHTING)
            
            self.draw_sphere(body.radius)
            # Draw Saturn's rings if this is Saturn
            if body.name.lower() == 'saturn':
                self.draw_saturn_rings(body.radius)
            # Draw satellites (e.g., Moon for Earth)
            for moon in self.solar_system.get_satellites(body.name):
                glPushMatrix()
                moon_pos = moon.get_position()
                glTranslatef(moon_pos[0], moon_pos[1], moon_pos[2])
                moon_color = moon.get_color()
                glColor3f(moon_color[0], moon_color[1], moon_color[2])
                self.draw_sphere(moon.radius)
                if moon == self.selected_body:
                    glDisable(GL_LIGHTING)
                    self.draw_selection_ring(moon.radius, moon_color)
                    glEnable(GL_LIGHTING)
                glPopMatrix()
            glPopMatrix()
            
    def animate(self):
        if self.is_running:
            self.solar_system.update(0.016 * self.simulation_speed)
            self.update()
            
    def select_body(self, body_name):
        # Search in planets
        found = False
        for body in self.solar_system.get_bodies():
            if body.name == body_name:
                self.selected_body = body
                color = body.get_color()
                info = f"Name: {body.name}\n"
                info += f"Radius: {body.radius:.2f}\n"
                info += f"Distance: {body.distance:.2f}\n"
                info += f"Orbital Period: {body.orbital_period:.2f} years\n"
                info += f"Rotation Period: {body.rotation_period:.2f} days\n"
                info += f"Orbital Inclination: {math.degrees(body.orbital_inclination):.2f}°"
                self.selected_body = body
                self.info_label.setText(info)
                found = True
                break
        # Search in satellites if not found
        if not found:
            for planet in self.solar_system.get_bodies():
                for sat in self.solar_system.get_satellites(planet.name):
                    if sat.name == body_name:
                        self.selected_body = sat
                        color = sat.get_color()
                        info = f"Name: {sat.name}\n"
                        info += f"Radius: {sat.radius:.2f}\n"
                        info += f"Distance: {sat.distance:.2f} (from planet)\n"
                        info += f"Orbital Period: {sat.orbital_period:.2f} years\n"
                        info += f"Rotation Period: {sat.rotation_period:.2f} days\n"
                        info += f"Orbital Inclination: {math.degrees(sat.orbital_inclination):.2f}°"
                        self.selected_body = sat
                        self.info_label.setText(info)
                        found = True
                        break
                if found:
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
        self.update_lighting()
        self.update()

    def set_view_mode(self, mode):
        self.view_mode = mode
        self.update()

    def set_follow_distance(self, distance):
        self.follow_distance = distance
        self.update()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.last_mouse_pos = event.position()
    def mouseMoveEvent(self, event: QMouseEvent):
        if self.last_mouse_pos is not None and self.parent().parent().view_combo.currentText() == 'Free Camera':
            delta = event.position() - self.last_mouse_pos
            self.last_mouse_pos = event.position()
            self.camera_rotation_x += delta.y() * 0.12
            self.camera_rotation_y += delta.x() * 0.12
            # Clamp X rotation
            self.camera_rotation_x = max(-90, min(90, self.camera_rotation_x))
            # Sync sliders if present
            mw = self.parent().parent()
            mw.rot_x_slider.setValue(int(self.camera_rotation_x))
            mw.rot_y_slider.setValue(int(self.camera_rotation_y))
            self.update()
    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.last_mouse_pos = None
    def wheelEvent(self, event: QWheelEvent):
        if self.parent().parent().view_combo.currentText() in ['Free Camera', 'Top View']:
            delta = event.angleDelta().y() / 120  # 1 step per notch
            self.camera_distance -= delta
            self.camera_distance = max(2, min(100, self.camera_distance))
            # Sync slider
            mw = self.parent().parent()
            mw.dist_slider.setValue(int(self.camera_distance))
            self.update()
        elif self.parent().parent().view_combo.currentText() == 'Follow Planet':
            delta = event.angleDelta().y() / 120
            self.follow_distance -= delta
            self.follow_distance = max(2, min(30, self.follow_distance))
            mw = self.parent().parent()
            mw.follow_dist_slider.setValue(int(self.follow_distance))
            self.update()
    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
        step = 5
        zstep = 5
        zoomstep = 1
        mode = self.parent().parent().view_combo.currentText()
        if mode in ['Free Camera', 'Top View']:
            if key in [Qt.Key.Key_W, Qt.Key.Key_Up]:
                self.camera_rotation_x -= step
                self.camera_rotation_x = max(-90, min(90, self.camera_rotation_x))
                self.parent().parent().rot_x_slider.setValue(int(self.camera_rotation_x))
            elif key in [Qt.Key.Key_S, Qt.Key.Key_Down]:
                self.camera_rotation_x += step
                self.camera_rotation_x = max(-90, min(90, self.camera_rotation_x))
                self.parent().parent().rot_x_slider.setValue(int(self.camera_rotation_x))
            elif key in [Qt.Key.Key_A, Qt.Key.Key_Left]:
                self.camera_rotation_y -= step
                self.parent().parent().rot_y_slider.setValue(int(self.camera_rotation_y))
            elif key in [Qt.Key.Key_D, Qt.Key.Key_Right]:
                self.camera_rotation_y += step
                self.parent().parent().rot_y_slider.setValue(int(self.camera_rotation_y))
            elif key == Qt.Key.Key_Q:
                self.camera_rotation_z -= zstep
                self.parent().parent().rot_z_slider.setValue(int(self.camera_rotation_z))
            elif key == Qt.Key.Key_E:
                self.camera_rotation_z += zstep
                self.parent().parent().rot_z_slider.setValue(int(self.camera_rotation_z))
            elif key in [Qt.Key.Key_Plus, Qt.Key.Key_Equal, Qt.Key.Key_PageUp]:
                self.camera_distance -= zoomstep
                self.camera_distance = max(2, min(100, self.camera_distance))
                self.parent().parent().dist_slider.setValue(int(self.camera_distance))
            elif key in [Qt.Key.Key_Minus, Qt.Key.Key_PageDown]:
                self.camera_distance += zoomstep
                self.camera_distance = max(2, min(100, self.camera_distance))
                self.parent().parent().dist_slider.setValue(int(self.camera_distance))
            self.update()
        elif mode == 'Follow Planet':
            if key in [Qt.Key.Key_Plus, Qt.Key.Key_Equal, Qt.Key.Key_PageUp]:
                self.follow_distance -= zoomstep
                self.follow_distance = max(2, min(30, self.follow_distance))
                self.parent().parent().follow_dist_slider.setValue(int(self.follow_distance))
            elif key in [Qt.Key.Key_Minus, Qt.Key.Key_PageDown]:
                self.follow_distance += zoomstep
                self.follow_distance = max(2, min(30, self.follow_distance))
                self.parent().parent().follow_dist_slider.setValue(int(self.follow_distance))
            self.update()

    def toggle_orbits(self, state):
        self.show_orbits = (state == Qt.CheckState.Checked)
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
        self.play_button = QPushButton("Pause")
        self.play_button.setCheckable(True)
        self.play_button.setChecked(True)
        self.play_button.clicked.connect(self.toggle_simulation)
        sim_layout.addWidget(self.play_button)
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
        
        # View Mode Controls
        view_group = QGroupBox("View Mode")
        view_layout = QVBoxLayout()
        view_layout.addWidget(QLabel("View Mode:"))
        self.view_combo = QComboBox()
        self.view_combo.addItems(["Free Camera", "Follow Planet", "Top View", "Lateral View", "Oblic View"])
        self.view_combo.currentTextChanged.connect(self.change_view_mode)
        view_layout.addWidget(self.view_combo)
        
        # Follow Distance slider (hidden by default)
        self.follow_dist_layout = QHBoxLayout()
        self.follow_dist_label = QLabel("Follow Distance:")
        self.follow_dist_slider = QSlider(Qt.Orientation.Horizontal)
        self.follow_dist_slider.setMinimum(2)
        self.follow_dist_slider.setMaximum(30)
        self.follow_dist_slider.setValue(8)
        self.follow_dist_slider.valueChanged.connect(self.change_follow_distance)
        self.follow_dist_layout.addWidget(self.follow_dist_label)
        self.follow_dist_layout.addWidget(self.follow_dist_slider)
        view_layout.addLayout(self.follow_dist_layout)
        view_group.setLayout(view_layout)
        control_layout.addWidget(view_group)
        
        # Lighting Controls
        light_group = QGroupBox("Lighting Controls")
        light_layout = QVBoxLayout()
        ambient_layout = QHBoxLayout()
        ambient_layout.addWidget(QLabel("Ambient:"))
        self.ambient_slider = QSlider(Qt.Orientation.Horizontal)
        self.ambient_slider.setMinimum(0)
        self.ambient_slider.setMaximum(100)
        self.ambient_slider.setValue(20)
        self.ambient_slider.valueChanged.connect(self.change_lighting)
        ambient_layout.addWidget(self.ambient_slider)
        light_layout.addLayout(ambient_layout)
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
        # Add all main bodies and satellites to the dropdown (Moon after Earth)
        all_bodies = [body.name for body in self.gl_widget.solar_system.get_bodies()]
        moon_inserted = False
        result_bodies = []
        for name in all_bodies:
            result_bodies.append(name)
            if name == 'Earth':
                # Insert Moon right after Earth
                for sat in self.gl_widget.solar_system.get_satellites('Earth'):
                    if sat.name not in result_bodies:
                        result_bodies.append(sat.name)
        self.body_combo = QComboBox()
        self.body_combo.addItems(result_bodies)
        self.body_combo.currentTextChanged.connect(self.select_body)
        body_layout.addWidget(self.body_combo)
        self.info_label = QLabel("Select a body to view its information")
        self.info_label.setWordWrap(True)
        body_layout.addWidget(self.info_label)
        body_group.setLayout(body_layout)
        control_layout.addWidget(body_group)
        # Create Show Orbits checkbox ONCE here
        self.orbit_checkbox = QCheckBox("Show Orbits")
        self.orbit_checkbox.setChecked(True)
        self.orbit_checkbox.stateChanged.connect(self.gl_widget.update)
        # Camera Controls (moved to bottom)
        camera_group = QGroupBox("Camera Controls")
        camera_layout = QVBoxLayout()
        dist_layout = QHBoxLayout()
        dist_layout.addWidget(QLabel("Distance:"))
        self.dist_slider = QSlider(Qt.Orientation.Horizontal)
        self.dist_slider.setMinimum(10)
        self.dist_slider.setMaximum(50)
        self.dist_slider.setValue(20)
        self.dist_slider.valueChanged.connect(self.change_camera_distance)
        dist_layout.addWidget(self.dist_slider)
        camera_layout.addLayout(dist_layout)
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
        # Add widgets in order
        control_layout.addWidget(self.orbit_checkbox)
        control_layout.addWidget(camera_group)
        control_layout.addStretch()
        layout.addWidget(control_panel, stretch=1)
        # Set default view mode after all controls are created
        self.view_combo.setCurrentText("Oblic View")
        
        # Initial UI state
        self.update_view_mode_ui('Free Camera')
        
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
        # Search in planets
        found = False
        for body in self.gl_widget.solar_system.get_bodies():
            if body.name == body_name:
                self.gl_widget.selected_body = body
                color = body.get_color()
                info = f"Name: {body.name}\n"
                info += f"Radius: {body.radius:.2f}\n"
                info += f"Distance: {body.distance:.2f}\n"
                info += f"Orbital Period: {body.orbital_period:.2f} years\n"
                info += f"Rotation Period: {body.rotation_period:.2f} days\n"
                info += f"Orbital Inclination: {math.degrees(body.orbital_inclination):.2f}°"
                self.info_label.setText(info)
                found = True
                break
        # Search in satellites if not found
        if not found:
            for planet in self.gl_widget.solar_system.get_bodies():
                for sat in self.gl_widget.solar_system.get_satellites(planet.name):
                    if sat.name == body_name:
                        self.gl_widget.selected_body = sat
                        color = sat.get_color()
                        info = f"Name: {sat.name}\n"
                        info += f"Radius: {sat.radius:.2f}\n"
                        info += f"Distance: {sat.distance:.2f} (from planet)\n"
                        info += f"Orbital Period: {sat.orbital_period:.2f} years\n"
                        info += f"Rotation Period: {sat.rotation_period:.2f} days\n"
                        info += f"Orbital Inclination: {math.degrees(sat.orbital_inclination):.2f}°"
                        self.info_label.setText(info)
                        found = True
                        break
                if found:
                    break
        self.gl_widget.update()

    def change_view_mode(self, mode):
        self.gl_widget.set_view_mode(mode)
        self.update_view_mode_ui(mode)

    def update_view_mode_ui(self, mode):
        # Show/hide controls based on view mode
        is_free = (mode == 'Free Camera')
        is_follow = (mode == 'Follow Planet')
        is_top = (mode == 'Top View')
        # Camera controls
        self.dist_slider.setEnabled(is_free or is_top)
        self.rot_x_slider.setEnabled(is_free)
        self.rot_y_slider.setEnabled(is_free)
        self.rot_z_slider.setEnabled(is_free)
        # Follow distance slider
        self.follow_dist_label.setVisible(is_follow)
        self.follow_dist_slider.setVisible(is_follow)
        for i in range(self.follow_dist_layout.count()):
            widget = self.follow_dist_layout.itemAt(i).widget()
            if widget:
                widget.setVisible(is_follow)

    def change_follow_distance(self, value):
        self.gl_widget.set_follow_distance(value)
        