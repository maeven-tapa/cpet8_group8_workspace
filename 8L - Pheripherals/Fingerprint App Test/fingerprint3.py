from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QTextEdit, QMessageBox
from PySide6.QtGui import QPixmap
from pyzkfp import ZKFP2
import sys
from PIL import Image
import numpy as np
import os
import sqlite3

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
        # Initialize SQLite DB
        self.db_path = os.path.join(os.getcwd(), "fingerprints.db")
        self.init_db()

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

    def init_db(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS fingerprints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                template BLOB
            )
        ''')
        self.conn.commit()

    def save_template_to_db(self, template):
        try:
            self.cursor.execute("INSERT INTO fingerprints (template) VALUES (?)", (sqlite3.Binary(template),))
            self.conn.commit()
            self.log_message("Fingerprint template saved to SQLite DB.")
        except Exception as e:
            self.log_message(f"Error saving to DB: {e}")

    def load_templates_from_db(self):
        self.cursor.execute("SELECT id, template FROM fingerprints")
        return self.cursor.fetchall()

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
            self.log_message(f"Please place your finger for sample {i+1}...")
            while self.running:
                capture = self.zkfp2.AcquireFingerprint()
                if capture:
                    tmp, img = capture
                    templates.append(tmp)
                    self.log_message(f"Fingerprint sample {i+1} captured.")
                    break
            if not self.running:
                self.log_message("Registration aborted.")
                return
        if len(templates) < 3:
            self.log_message("Failed to capture 3 fingerprint samples. Registration aborted.")
            return
        regTemp, _ = self.zkfp2.DBMerge(templates[0], templates[1], templates[2])
        finger_id = 1
        self.zkfp2.DBAdd(finger_id, regTemp)
        self.log_message("Fingerprint registered successfully.")
        # Save to SQLite DB
        self.save_template_to_db(regTemp)

    def compare_fingerprint(self):
        capture = self.zkfp2.AcquireFingerprint()
        if not capture:
            self.log_message("No fingerprint captured.")
            return
        tmp, _ = capture
        # Load all templates from DB and compare
        matches = []
        for db_id, db_template in self.load_templates_from_db():
            try:
                score = self.zkfp2.DBMatch(tmp, db_template)
                if score > 0:  # Score > 0 means a match (adjust threshold as needed)
                    matches.append((db_id, score))
            except Exception as e:
                self.log_message(f"Error comparing with DB template {db_id}: {e}")
        if matches:
            best_match = max(matches, key=lambda x: x[1])
            self.log_message(f"Matched DB ID: {best_match[0]}, Score: {best_match[1]}")
        else:
            self.log_message("No match found in database.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FingerprintApp()
    window.show()
    sys.exit(app.exec())