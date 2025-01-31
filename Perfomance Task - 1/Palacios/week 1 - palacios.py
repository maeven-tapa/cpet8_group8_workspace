from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt
from ui_main import Ui_MainWindow  # Import the converted UI file

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 1️⃣ Set window opacity (Transparency)
        self.setWindowOpacity(0.9)

        # 2️⃣ Set label text alignment (Centered)
        self.ui.label.setAlignment(Qt.AlignCenter)

        # 3️⃣ Set placeholder text in QLineEdit
        self.ui.lineEdit.setPlaceholderText("Enter your name here...")

        # 4️⃣ Style the button (Purple background, white text, and hover effect)
        self.ui.pushButton.setStyleSheet("""
            QPushButton {
                background-color: #800080;  /* Purple background */
                color: white;               /* White text */
                font-size: 16px;            /* Font size */
                font-family: Arial;         /* Font family */
                padding: 10px 20px;         /* Padding for button */
                border-radius: 8px;         /* Rounded corners */
            }
            QPushButton:hover {
                background-color: #9b59b6;  /* Lighter purple on hover */
            }
            QPushButton:pressed {
                background-color: #6a2c8b;  /* Darker purple when pressed */
            }
        """)

        # 5️⃣ Set tooltip on the button
        self.ui.pushButton.setToolTip("UNO CUTIEEEE")

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
