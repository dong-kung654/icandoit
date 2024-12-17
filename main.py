from gui import SimpleGUI
import sys
from PyQt6.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)
    window = SimpleGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
