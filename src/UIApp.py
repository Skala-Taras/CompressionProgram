import os
import sys
from PyQt6.QtWidgets import QApplication, QPushButton, QLabel, QMessageBox, QMainWindow, QVBoxLayout, QWidget, QProgressBar, QFileDialog
from PyQt6.QtCore import QSize, QThread, pyqtSignal, Qt, pyqtSlot
from HuffmanCoding import HuffmanCoding
import sys 

class CompressionWorker(QThread):
    """
    Runs a counter thread.
    """
    progress_updated = pyqtSignal(int)
    finished = pyqtSignal()
    error_happened = pyqtSignal(str)

    def __init__(self, operation, input_path, output_path):
        super().__init__()
        self.operation = operation  # 'compress' or 'decompress'
        self.input_path = input_path
        self.output_path = output_path
        self.huffman = HuffmanCoding()

    def run(self):
        try:
            if self.operation == 'compress':
                self.huffman.compress_data(
                    self.input_path, 
                    self.output_path, 
                    self.update_progress
                    )
                
            else:
                self.huffman.decompress_data(
                    self.input_path, 
                    self.output_path, 
                    self.update_progress
                    )
                
            self.finished.emit()

        except Exception as e:
            self.error_happened.emit(str(e))
    
    def update_progress(self, value):
        self.progress_updated.emit(value)
        

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
        
    def init_ui(self):
        self.setWindowTitle("Compress/Decompress Data")
        self.setFixedSize(QSize(400, 300))

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # Operation Buttons
        self.btn_compress = QPushButton("📁 Compress File")
        self.btn_compress.clicked.connect(self.compress_file)
        self.btn_compress.setStyleSheet("""
            QPushButton {
                padding: 15px;
                font-size: 16px;
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover { background-color: #45a049; }
        """)
        layout.addWidget(self.btn_compress)

        self.btn_decompress = QPushButton("📤 Decompress File")
        self.btn_decompress.clicked.connect(self.decompress_file)
        self.btn_decompress.setStyleSheet("""
            QPushButton {
                padding: 15px;
                font-size: 16px;
                background-color: #2196F3;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover { background-color: #1976D2; }
        """)
        layout.addWidget(self.btn_decompress)

        # Progress Indicators
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setTextVisible(True)
        self.progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
                height: 20px;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                width: 10px;
            }
        """)
        layout.addWidget(self.progress)

        # Percentage Label
        self.percentage_label = QLabel("0%")
        self.percentage_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.percentage_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                color: #333;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.percentage_label)

        # Status Message
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #666;
                font-style: italic;
            }
        """)
        layout.addWidget(self.status_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def compress_file(self):
        self.start_operation("compress")

    def decompress_file(self):
        self.start_operation("decompress")
    
    def start_operation(self, operation):
        
        input_path, _ = (QFileDialog.getOpenFileName(self, "Decompres file")
                        if operation == 'decompress' else
                        QFileDialog.getOpenFileName(self, "Compres file"))

        if not input_path:
            return

        output_path, _ = (QFileDialog.getSaveFileName(self, "Compres file", "", "Text fail (*.txt)")
                         if operation == 'decompress' else
                         QFileDialog.getSaveFileName(self, "Decompres file", "", "Huffman Compress Files (*.huff)"))

        if not output_path:
            return

        self.toggle_buttons(False)
        self.progress.setValue(0)

        self.worker = CompressionWorker(operation, input_path, output_path)
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.finished.connect(self.on_operation_finished)
        self.worker.error_happened.connect(self.show_error)
        self.worker.start()

    @pyqtSlot(int)
    def update_progress(self, value):
        self.progress.setValue(value)
        self.percentage_label.setText(f"{value}%")
        if value == 100:
            self.status_label.setText("Finalizing...")

    @pyqtSlot()
    def on_operation_finished(self):
        self.toggle_buttons(True)
        self.progress.setValue(100)
        self.percentage_label.setText("100%")
        self.status_label.setText("✅ Operation Completed Successfully!")
        QMessageBox.information(self, "Success", "Operation completed successfully!")

    @pyqtSlot(str)
    def show_error(self, message):
        self.toggle_buttons(True)
        self.progress.setValue(0)
        self.percentage_label.setText("❌ Error")
        self.status_label.setText("Operation failed")
        QMessageBox.critical(self, "Error", f"Operation failed:\n{message}")

    def toggle_buttons(self, enabled):
        self.btn_compress.setEnabled(enabled)
        self.btn_decompress.setEnabled(enabled)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())