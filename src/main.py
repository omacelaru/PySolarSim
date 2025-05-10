import sys
from PyQt6.QtWidgets import QApplication
from src.ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    # Load and apply QSS stylesheet
    try:
        with open("style.qss", "r") as f:
            app.setStyleSheet(f.read())
    except Exception as e:
        print("Could not load style.qss:", e)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 