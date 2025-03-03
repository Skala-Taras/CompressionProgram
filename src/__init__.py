from .UIApp import MainWindow
from PyQt6.QtWidgets import QApplication
import sys

def run():
    """
    Initialize and run the Huffman Compression application
    """
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    run()
