from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSlider
from PyQt6.QtCore import Qt
from graphics.renderer import OpenGLWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySolarSim - Solar System Simulation")
        self.setMinimumSize(1024, 768)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Create OpenGL widget for 3D rendering
        self.gl_widget = OpenGLWidget()
        main_layout.addWidget(self.gl_widget, stretch=4)
        
        # Create control panel
        control_panel = QWidget()
        control_layout = QVBoxLayout(control_panel)
        
        # Add some basic controls
        self.info_label = QLabel("Select a celestial body to view information")
        control_layout.addWidget(self.info_label)
        
        # Add simulation controls
        self.pause_button = QPushButton("Pause/Resume")
        self.pause_button.clicked.connect(self.toggle_simulation)
        control_layout.addWidget(self.pause_button)
        
        self.reset_button = QPushButton("Reset Simulation")
        self.reset_button.clicked.connect(self.reset_simulation)
        control_layout.addWidget(self.reset_button)
        
        # Add time scale control
        time_scale_layout = QHBoxLayout()
        time_scale_layout.addWidget(QLabel("Time Scale:"))
        self.time_scale_slider = QSlider(Qt.Orientation.Horizontal)
        self.time_scale_slider.setMinimum(1)
        self.time_scale_slider.setMaximum(100)
        self.time_scale_slider.setValue(10)
        self.time_scale_slider.valueChanged.connect(self.update_time_scale)
        time_scale_layout.addWidget(self.time_scale_slider)
        control_layout.addLayout(time_scale_layout)
        
        control_layout.addStretch()
        main_layout.addWidget(control_panel, stretch=1)
    
    def toggle_simulation(self):
        self.gl_widget.toggle_simulation()
        self.pause_button.setText("Resume" if self.gl_widget.solar_system.paused else "Pause")
    
    def reset_simulation(self):
        self.gl_widget.reset_simulation()
    
    def update_time_scale(self, value):
        self.gl_widget.solar_system.time_scale = value / 10.0 