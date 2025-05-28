import sys
from PySide6.QtWidgets import QApplication, QSplashScreen, QLabel
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap, QPainter, QBrush, QColor, QPen

class EALS_SplashScreen(QSplashScreen):
    def __init__(self):
        pixmap = QPixmap(470, 270)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw shadow first (offset background)
        shadow_offset = 1
        painter.setBrush(QBrush(QColor(0, 0, 0, 60)))  # Semi-transparent black shadow
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(shadow_offset, shadow_offset, 470 - shadow_offset, 270 - shadow_offset, 10, 10)
        
        # Draw main background
        painter.setBrush(QBrush(QColor(255, 255, 255)))
        painter.setPen(QPen(QColor(128, 129, 130), 1))  # 1px border with specified color
        painter.drawRoundedRect(0, 0, 470 - shadow_offset, 270 - shadow_offset, 10, 10)
        painter.end()
        
        super().__init__(pixmap)
        
        # Set window flags for shadow effect
        self.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        
        # Add E/ALS label in top left
        eals_label = QLabel("E/ALS", self)
        eals_label.setStyleSheet("""
            background-color: rgb(0, 0, 0);
            color: rgb(255, 255, 255);
            border-radius: 5px;
            padding: 5px 10px;
            font-weight: bold;
        """)
        eals_label.move(10, 10)
        eals_label.adjustSize()
        
        # Status label that can be updated
        self.status_label = QLabel("Starting application...", self)
        self.status_label.setStyleSheet("""
            color: rgb(128, 128, 128);
            font-size: 10px;
            background-color: transparent;
        """)
        self.status_label.adjustSize()
        self.status_label.move(10, 270 - shadow_offset - self.status_label.height() - 10)
        
        # Load and center the logo
        try:
            logo = QPixmap("resources/logo-eals.png")
            if not logo.isNull():
                logo = logo.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                logo_label = QLabel(self)
                logo_label.setPixmap(logo)
                logo_label.setAlignment(Qt.AlignCenter)
                logo_label.resize(logo.size())
                logo_label.move(
                    ((470 - shadow_offset) - logo.width()) // 2,
                    ((270 - shadow_offset) - logo.height()) // 2
                )
        except Exception as e:
            print(f"Could not load logo-eals.png: {e}")
    
    def update_status(self, message):
        """Update the status message on the splash screen"""
        self.status_label.setText(message)
        self.status_label.adjustSize()
        self.status_label.move(10, 270 - 3 - self.status_label.height() - 10)
    
    def center_on_screen(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        splash_geometry = self.geometry()
        
        x = (screen_geometry.width() - splash_geometry.width()) // 2
        y = (screen_geometry.height() - splash_geometry.height()) // 2
        
        self.move(x, y)

def main():
    app = QApplication(sys.argv)
    splash = EALS_SplashScreen()
    splash.center_on_screen()
    splash.show()
    app.processEvents()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()