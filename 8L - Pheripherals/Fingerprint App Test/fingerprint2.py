from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QTextEdit, QMessageBox
from PySide6.QtGui import QPixmap
from pyzkfp import ZKFP2
import sys
from PIL import Image
import numpy as np
import threading
import os

class FingerprintApp(QWidget):
    def __init__(self):
        super().__init__()
        self.zkfp2 = ZKFP2()
        self.light_colors = ["green", "red", "white"]
        self.current_light_index = -1  # Start at -1 so first press turns on green
        self.init_ui()
        self.initialize_device()
        self.running = True
        self.image_counter = 1
        self.capture_thread = threading.Thread(target=self.capture_fingerprint_loop, daemon=True)
        self.capture_thread.start()

    def init_ui(self):
        self.setWindowTitle("ZKTeco Live 20R GUI")
        self.setGeometry(100, 100, 400, 400)

        self.log = QTextEdit(self)
        self.log.setReadOnly(True)
        
        self.image_label = QLabel(self)
        
        self.register_btn = QPushButton("Register Fingerprint", self)
        self.register_btn.clicked.connect(self.register_fingerprint)
        
        self.compare_btn = QPushButton("Compare Fingerprint", self)
        self.compare_btn.clicked.connect(self.compare_fingerprint)
        
        self.light_btn = QPushButton("Turn On (Green)", self)
        self.light_btn.clicked.connect(self.toggle_light)
        self.update_light_button()
        
        layout = QVBoxLayout()
        layout.addWidget(self.register_btn)
        layout.addWidget(self.compare_btn)
        layout.addWidget(self.light_btn)
        layout.addWidget(QLabel("Fingerprint Image:"))
        layout.addWidget(self.image_label)
        layout.addWidget(QLabel("Log Output:"))
        layout.addWidget(self.log)

        self.setLayout(layout)

    def log_message(self, message):
        self.log.append(message)

    def initialize_device(self):
        self.zkfp2.Init()
        device_count = self.zkfp2.GetDeviceCount()
        if device_count > 0:
            self.zkfp2.OpenDevice(0)
            self.log_message(f"Device initialized. {device_count} device(s) found.")
        else:
            QMessageBox.warning(self, "Error", "No fingerprint devices found!")

    def capture_fingerprint_loop(self):
        while self.running:
            capture = self.zkfp2.AcquireFingerprint()
            if capture:
                tmp, img = capture
                self.log_message("Fingerprint captured successfully.")
                self.zkfp2.show_image(img)
                self.save_fingerprint_image(img)
                self.display_fingerprint()

    def save_fingerprint_image(self, img):
        try:
            fingerprint_dir = os.path.join(os.getcwd(), "fingerprint")
            os.makedirs(fingerprint_dir, exist_ok=True)
            file_path = os.path.join(fingerprint_dir, f"fingerprint{self.image_counter}.bmp")
            width, height = 300, 400
            img_array = np.frombuffer(img, dtype=np.uint8).reshape((height, width))
            image = Image.fromarray(img_array, mode='L')
            image.save(file_path, format="BMP")
            self.log_message(f"Fingerprint image saved to {file_path}")
            self.image_counter += 1
        except Exception as e:
            self.log_message(f"Error saving fingerprint image: {e}")

    def display_fingerprint(self):
        fingerprint_dir = os.path.join(os.getcwd(), "fingerprint")
        file_path = os.path.join(fingerprint_dir, f"fingerprint{self.image_counter - 1}.bmp")
        if os.path.exists(file_path):
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                self.image_label.setPixmap(pixmap.scaled(200, 200))
            else:
                self.log_message("Error: Loaded pixmap is null (corrupt image file).")
        else:
            self.log_message("Error: Fingerprint image file not found.")

    def toggle_light(self):
        self.current_light_index = (self.current_light_index + 1) % len(self.light_colors)
        current_color = self.light_colors[self.current_light_index]
        self.zkfp2.Light(current_color)
        self.log_message(f"Light switched to {current_color}.")
        self.update_light_button()

    def update_light_button(self):
        current_color = self.light_colors[self.current_light_index]
        next_color = self.light_colors[(self.current_light_index + 0) % len(self.light_colors)].capitalize()
        self.light_btn.setText(f"Turn On ({next_color})")
        text_color = "black" if current_color == "white" else "white"
        self.light_btn.setStyleSheet(f"background-color: {current_color}; color: {text_color};")

    def register_fingerprint(self):
        templates = []
        for i in range(3):
            capture = self.zkfp2.AcquireFingerprint()
            if capture:
                tmp, img = capture
                templates.append(tmp)
                self.log_message(f"Fingerprint sample {i+1} captured.")
        regTemp, _ = self.zkfp2.DBMerge(*templates)
        finger_id = 1
        self.zkfp2.DBAdd(finger_id, regTemp)
        self.log_message("Fingerprint registered successfully.")

    def compare_fingerprint(self):
        capture = self.zkfp2.AcquireFingerprint()
        if capture:
            tmp, _ = capture
            fingerprint_id, score = self.zkfp2.DBIdentify(tmp)
            self.log_message(f"Matched Fingerprint ID: {fingerprint_id}, Score: {score}")
        else:
            self.log_message("No match found.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FingerprintApp()
    window.show()
    sys.exit(app.exec())