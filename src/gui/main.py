import os
import sys
from PyQt6.QtWidgets import QApplication
from gui.game_window import GameWindow

def main():
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    # Add the parent directory to Python path
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if current_dir not in sys.path:
        sys.path.append(current_dir)
    
    main()