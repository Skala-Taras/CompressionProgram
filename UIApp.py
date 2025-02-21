import os
from PyQt6.QtWidgets import QApplication, QPushButton, QMainWindow, QVBoxLayout, QWidget, QProgressBar, QFileDialog
from PyQt6.QtCore import QSize
from HuffmanCoding import HuffmanCoding
import sys 

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_UI()
        
        
    def init_UI(self): 
        """
        Initializes the user interface components.
        
        Creates and arranges the main UI elements including:
        - Compression button
        - Decompression button
        - Progress bar
        - Layout management
        """
        self.setWindowTitle("Compress/Decompress Data")
        self.setFixedSize(QSize(400, 300))

        pagelayout = QVBoxLayout()
        # optional_layout = QVBoxLayout()

        btn_compress = QPushButton("Comprase data \nchose a file")
        btn_compress.pressed.connect(self.compress_file)
        pagelayout.addWidget(btn_compress)


        btn_decompress = QPushButton("Decompress data \nchose a file")
        btn_decompress.pressed.connect(self.decompress_file)
        pagelayout.addWidget(btn_decompress)
        
        self.progressBar = QProgressBar(self)
        self.progressBar.setGeometry(25, 45, 300, 30)
        pagelayout.addWidget(self.progressBar)

        widget = QWidget()
        widget.setLayout(pagelayout)
        self.setCentralWidget(widget)

    def compress_file(self):
        """
        Handles the file compression operation.
        
        Opens two file dialogs:
        1. First to select the input file to compress
        2. Second to choose the save location for the compressed file (.huffc)
        
        Returns:
            None
        """
        print("##########")
        file_diretion, _ = QFileDialog.getOpenFileName(self, "Compres file")
        if not file_diretion:
            return
        sava_directories, _ = QFileDialog.getSaveFileName(self, "Decompres file", "", "Huffman Compress Files (*.huffc)")
        if not sava_directories:
            return
        # ad = HuffmanCoding()
        # a =ad.compress_data(file_diretion)
        # print(f"--->{file_diretion}")
        # print(a)
        # print(sava_directories)
        # # for file in files:

    def decompress_file(self):
        pass


    
    

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    #exec()