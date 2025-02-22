import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, 
    QLabel, QFileDialog, QProgressBar
)
from PyQt6.QtCore import QThread, pyqtSignal
from HuffmanCoding import HuffmanCoding

class Worker(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(tuple)

    def __init__(self, task, *args):  
        super().__init__()
        self.task = task
        self.args = args

    def run(self):
        result = self.task(*self.args, self.progress.emit)
        self.finished.emit(result)

class HuffmanGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.current_task = None

    def init_ui(self):
        self.setWindowTitle("Huffman Kompresor")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()
        self.label = QLabel("Wybierz operację")
        layout.addWidget(self.label)

        self.btn_compress = QPushButton("Kompresuj plik")
        self.btn_compress.clicked.connect(self.start_compress)
        layout.addWidget(self.btn_compress)

        self.btn_decompress = QPushButton("Dekompresuj plik")
        self.btn_decompress.clicked.connect(self.start_decompress)
        layout.addWidget(self.btn_decompress)

        self.progress = QProgressBar()
        layout.addWidget(self.progress)

        self.setLayout(layout)

    def start_compress(self):
        input_path, _ = QFileDialog.getOpenFileName(self, "Wybierz plik do kompresji")
        if not input_path:
            return
        output_path, _ = QFileDialog.getSaveFileName(self, "Zapisz skompresowany plik", "", "Huffman Files (*.huff)")
        if not output_path:
            return
        
        self.current_task = Worker(HuffmanCoding.compress, input_path, output_path)
        self.current_task.progress.connect(self.update_progress)
        self.current_task.finished.connect(self.task_finished)
        self.current_task.start()

    def start_decompress(self):
        input_path, _ = QFileDialog.getOpenFileName(self, "Wybierz plik .huff", "", "Huffman Files (*.huff)")
        if not input_path:
            return
        output_path, _ = QFileDialog.getSaveFileName(self, "Zapisz odkompresowany plik")
        if not output_path:
            return
        
        self.current_task = Worker(HuffmanCoding.decompress, input_path, output_path)
        self.current_task.progress.connect(self.update_progress)
        self.current_task.finished.connect(self.task_finished)
        self.current_task.start()

    def update_progress(self, value):
        self.progress.setValue(value)

    def task_finished(self, result):
        self.label.setText(f"Operacja zakończona!\nRozmiar przed: {result[0][2]} B\nRozmiar po: {result[1]} B")
        self.progress.setValue(100)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HuffmanGUI()
    window.show()
    sys.exit(app.exec())