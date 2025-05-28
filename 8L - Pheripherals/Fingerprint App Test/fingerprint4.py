import sys
import sqlite3
import os
import wmi
from PySide6.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout,
                               QLabel, QFileDialog, QMessageBox)
from PySide6.QtGui import QPixmap, QImage
from pyzkfp import ZKFP2
from PIL import Image
import io

class FingerprintApp(QWidget):
    def __init__(self):
        super().__init__()
        self.zkfp = ZKFP2()
        self.init_ui()
        self.device_open = False
        self.last_template = None
        self.db_conn = sqlite3.connect("fingerprints.db")
        self.templates_dir = "fingerprint_templates"
        os.makedirs(self.templates_dir, exist_ok=True)  # Ensure the directory exists
        self.init_db()

    def init_ui(self):
        self.setWindowTitle("Fingerprint Reader App")
        layout = QVBoxLayout()

        self.status = QLabel("Status: Not initialized")
        layout.addWidget(self.status)

        self.device_name_label = QLabel("Device: Not connected")
        layout.addWidget(self.device_name_label)

        self.image_label = QLabel("Captured Fingerprint")
        layout.addWidget(self.image_label)

        self.init_btn = QPushButton("Initialize Device")
        self.init_btn.clicked.connect(self.initialize_device)
        layout.addWidget(self.init_btn)

        self.capture_btn = QPushButton("Capture Fingerprint")
        self.capture_btn.clicked.connect(self.capture_fingerprint)
        layout.addWidget(self.capture_btn)

        self.compare_btn = QPushButton("1:1 Compare")
        self.compare_btn.clicked.connect(self.compare_1_1)
        layout.addWidget(self.compare_btn)

        self.register_btn = QPushButton("Register Fingerprint")
        self.register_btn.clicked.connect(self.register_fingerprint)
        layout.addWidget(self.register_btn)

        self.setLayout(layout)

    def init_db(self):
        cursor = self.db_conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fingerprints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                template_path TEXT NOT NULL
            )
        """)
        self.db_conn.commit()

    def get_fingerprint_device_name(self):
        """Get the actual fingerprint device name from Windows Device Manager"""
        try:
            c = wmi.WMI()
            # Look for fingerprint devices in various categories
            for device in c.Win32_PnPEntity():
                if device.Name and any(keyword in device.Name.lower() for keyword in 
                    ['zkfp', 'zkteco', 'zk']):
                    return device.Name
            
            # If no specific fingerprint device found, look for USB devices with fingerprint keywords
            for device in c.Win32_USBHub():
                if device.Name and any(keyword in device.Name.lower() for keyword in 
                    ['zk', 'zkfp', 'zkteco']):
                    return device.Name
                    
            return "Unknown Fingerprint Device"
        except Exception as e:
            print(f"Error getting device name: {e}")
            return "Fingerprint Scanner"

    def initialize_device(self):
        self.zkfp.Init()
        count = self.zkfp.GetDeviceCount()
        if count > 0:
            self.zkfp.OpenDevice(0)
            self.device_open = True
            
            # Get actual device name from Windows Device Manager
            device_name = self.get_fingerprint_device_name()
            self.device_name_label.setText(f"Device: {device_name}")
            
            self.status.setText(f"Device initialized. {count} device(s) found.")
            self.zkfp.Light('white')
        else:
            self.status.setText("No device found.")
            self.device_name_label.setText("Device: Not connected")

    def capture_fingerprint(self):
        if not self.device_open:
            self.status.setText("Device not initialized or opened.")
            return

        try:
            while True:
                capture = self.zkfp.AcquireFingerprint()
                if capture:
                    self.last_template, image_data = capture
                    self.display_image(image_data)
                    self.status.setText("Fingerprint captured.")
                    break
        except Exception as e:
            self.status.setText(f"Error capturing fingerprint: {str(e)}")

    def display_image(self, image_data):
        # Set fixed image dimensions
        width, height = 300, 400

        img = Image.frombytes('L', (width, height), image_data)
        img = img.resize((200, 200))
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        qimg = QImage.fromData(buffer.getvalue())
        pixmap = QPixmap.fromImage(qimg)
        self.image_label.setPixmap(pixmap)

    def compare_1_1(self):
        if not self.device_open:
            self.status.setText("Device not initialized.")
            return

        try:
            while True:
                capture = self.zkfp.AcquireFingerprint()
                if capture:
                    captured_template, _ = capture
                    break
        except Exception as e:
            self.status.setText(f"Error capturing fingerprint: {str(e)}")
            return

        cursor = self.db_conn.cursor()
        cursor.execute("SELECT id, template_path FROM fingerprints")
        records = cursor.fetchall()  # Fetch all records

        best_score = -1
        best_user_id = -1
        for user_id, template_path in records:
            if os.path.exists(template_path):
                with open(template_path, "rb") as tpl_file:
                    db_template = tpl_file.read()

                print(f"Captured Template Length: {len(captured_template)}")
                print(f"Stored Template Length: {len(db_template)}")

                result = self.zkfp.DBMatch(captured_template, db_template)
                print(f"Match result: {result}")

                threshold = 50  # or adjust based on testing
                if result >= threshold:  # Check if result is above threshold
                    best_score = result
                    best_user_id = user_id

        if best_score > 0:
            self.zkfp.Light('green')
            self.status.setText(f"1:1 Comparison Result: Match found with ID {best_user_id} (Score: {best_score})")
        else:
            self.zkfp.Light('red')
            self.status.setText("No match found.")

    def register_fingerprint(self):
        if not self.device_open:
            self.status.setText("Device not initialized.")
            return

        templates = []
        for i in range(3):
            while True:
                capture = self.zkfp.AcquireFingerprint()
                if capture:
                    tmp, _ = capture
                    templates.append(tmp)
                    self.status.setText(f"Fingerprint {i + 1} captured.")
                    break

        reg_temp, _ = self.zkfp.DBMerge(*templates)
        reg_temp_bytes = bytes(reg_temp)  # Convert reg_temp to bytes

        cursor = self.db_conn.cursor()
        cursor.execute("INSERT INTO fingerprints (template_path) VALUES (?)", ("",))
        user_id = cursor.lastrowid

        template_path = os.path.join(self.templates_dir, f"template_{user_id}.tpl")
        with open(template_path, "wb") as tpl_file:
            tpl_file.write(reg_temp_bytes)

        cursor.execute("UPDATE fingerprints SET template_path = ? WHERE id = ?", (template_path, user_id))
        self.db_conn.commit()

        self.status.setText(f"Fingerprint registered with ID {user_id} and saved to {template_path}")

    def terminate_device(self, event):
        if self.device_open:
            self.zkfp.CloseDevice()
        self.zkfp.Terminate()
        self.db_conn.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = FingerprintApp()
    win.show()
    sys.exit(app.exec())