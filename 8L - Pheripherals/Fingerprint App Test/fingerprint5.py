import sqlite3
import os
from pyzkfp import ZKFP2
from PIL import Image
import io

class FingerprintLogic:
    def __init__(self):
        self.zkfp = ZKFP2()
        self.device_open = False
        self.last_template = None
        self.db_conn = sqlite3.connect("fingerprints.db")
        self.templates_dir = "fingerprint_templates"
        os.makedirs(self.templates_dir, exist_ok=True)  # Ensure the directory exists
        self.init_db()

    def init_db(self):
        cursor = self.db_conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fingerprints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                template_path TEXT NOT NULL
            )
        """)
        self.db_conn.commit()

    def initialize_device(self):
        self.zkfp.Init()
        count = self.zkfp.GetDeviceCount()
        if count > 0:
            self.zkfp.OpenDevice(0)
            self.device_open = True
            print(f"Device initialized. {count} device(s) found.")
            self.zkfp.Light('white')
        else:
            print("No device found.")

    def capture_fingerprint(self):
        if not self.device_open:
            print("Device not initialized or opened.")
            return None

        try:
            while True:
                capture = self.zkfp.AcquireFingerprint()
                if capture:
                    self.last_template, image_data = capture
                    self.display_image(image_data)
                    print("Fingerprint captured.")
                    return self.last_template
        except Exception as e:
            print(f"Error capturing fingerprint: {str(e)}")
            return None

    def display_image(self, image_data):
        # Set fixed image dimensions
        width, height = 300, 400

        img = Image.frombytes('L', (width, height), image_data)
        img = img.resize((200, 200))
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        print("Image displayed (dimensions retained).")

    def compare_1_1(self):
        if not self.device_open:
            print("Device not initialized.")
            return

        try:
            while True:
                capture = self.zkfp.AcquireFingerprint()
                if capture:
                    captured_template, _ = capture
                    break
        except Exception as e:
            print(f"Error capturing fingerprint: {str(e)}")
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

                result = self.zkfp.DBMatch(captured_template, db_template)
                print(f"Match result: {result}")

                threshold = 50  # or adjust based on testing
                if result >= threshold:  # Check if result is above threshold
                    best_score = result
                    best_user_id = user_id

        if best_score > 0:
            self.zkfp.Light('green')
            print(f"1:1 Comparison Result: Match found with ID {best_user_id} (Score: {best_score})")
        else:
            self.zkfp.Light('red')
            print("No match found.")

    def register_fingerprint(self):
        if not self.device_open:
            print("Device not initialized.")
            return

        templates = []
        for i in range(3):
            while True:
                capture = self.zkfp.AcquireFingerprint()
                if capture:
                    tmp, _ = capture
                    templates.append(tmp)
                    print(f"Fingerprint {i + 1} captured.")
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

        print(f"Fingerprint registered with ID {user_id} and saved to {template_path}")

    def terminate_device(self):
        if self.device_open:
            self.zkfp.CloseDevice()
        self.zkfp.Terminate()
        self.db_conn.close()
        print("Device terminated and database connection closed.")

