import sys
from PySide6.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout

#Qtable Widget Example
''' class TableExample(QWidget):
    def __init__(self):
        super().__init__()

        # Create QTableWidget
        self.table = QTableWidget()
        self.table.setRowCount(3)   # Set number of rows
        self.table.setColumnCount(3)  # Set number of columns

        # Set column headers
        self.table.setHorizontalHeaderLabels(["Name", "Age", "Section"])

        # Populate table with data
        data = [
            ("Raven", 20, "BET-COET-2A"),
            ("Maeven", 19, "BET-COET-2A"),
            ("Dona", 20, "BET-COET-2A"),
            ("Sieg", 21, "BET-COET-2A")
        ]

        for row, (name, age, country) in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(name))
            self.table.setItem(row, 1, QTableWidgetItem(str(age)))
            self.table.setItem(row, 2, QTableWidgetItem(country))

        # Layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.table)

        # Window properties
        self.setWindowTitle("QTableWidget Example - PySide6")
        self.resize(400, 300)

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TableExample()
    window.show()  # Ensure the window is shown
    sys.exit(app.exec())  # Start event loop'''

'''import sys
from PySide6.QtWidgets import QApplication, QWidget, QTreeWidget, QTreeWidgetItem, QVBoxLayout

#QtreeWidget
class TreeExample(QWidget):
    def __init__(self):
        super().__init__()

        # Create QTreeWidget
        self.tree = QTreeWidget()
        self.tree.setColumnCount(2)  # Number of columns
        self.tree.setHeaderLabels(["Item", "Details"])  # Set headers

        # Add top-level items
        parent1 = QTreeWidgetItem(self.tree, ["Fruits", "Category"])
        parent2 = QTreeWidgetItem(self.tree, ["Vegetables", "Category"])

        # Add children to "Fruits"
        apple = QTreeWidgetItem(parent1, ["Apple", "Red"])
        banana = QTreeWidgetItem(parent1, ["Banana", "Yellow"])

        # Add children to "Vegetables"
        carrot = QTreeWidgetItem(parent2, ["Carrot", "Orange"])
        broccoli = QTreeWidgetItem(parent2, ["Broccoli", "Green"])

        # Expand all items by default
        self.tree.expandAll()

        # Layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.tree)

        # Window properties
        self.setWindowTitle("QTreeWidget Example - PySide6")
        self.resize(400, 300)

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TreeExample()
    window.show()  # Ensure the window is shown
    sys.exit(app.exec())  # Start event loop'''
''''
#QGraphics 
import sys
from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PySide6.QtGui import QBrush, QColor, QPainter
from PySide6.QtCore import Qt

class GraphicsViewExample(QGraphicsView):
    def __init__(self):
        super().__init__()

        # Create the graphics scene
        scene = QGraphicsScene()
        self.setScene(scene)

        # Set the scene boundaries
        self.setSceneRect(0, 0, 400, 300)

        # Create and add a square item
        rect = QGraphicsRectItem(100, 100, 100, 100)  # (x, y, width, height)
        rect.setBrush(QBrush(QColor("pink")))  # Fill color
        rect.setFlag(QGraphicsRectItem.ItemIsMovable)  # Enable dragging
        scene.addItem(rect)

        # Enable anti-aliasing (Fixed)
        self.setRenderHint(QPainter.Antialiasing)  

# Run Application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Create main window
    window = GraphicsViewExample()
    window.setWindowTitle("QGraphicsView Example - PySide6")
    window.resize(500, 400)
    window.show()  # Ensure the window is displayed
    
    sys.exit(app.exec()) '''

'''''
import sys
from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget

#QMediaPlayer
class MediaPlayerExample(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize the player and the video widget
        self.mediaPlayer = QMediaPlayer()
        self.videoWidget = QVideoWidget()

        # Set up layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.videoWidget)

        # Add Play and Stop buttons
        self.playButton = QPushButton("Play")
        self.playButton.clicked.connect(self.play_video)
        layout.addWidget(self.playButton)

        self.stopButton = QPushButton("Stop")
        self.stopButton.clicked.connect(self.stop_video)
        layout.addWidget(self.stopButton)

        # Set up media player output
        self.mediaPlayer.setVideoOutput(self.videoWidget)

        # Window properties
        self.setWindowTitle("QMediaPlayer Example - PySide6")
        self.resize(640, 480)

    def play_video(self):
        # File dialog to open a video file
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Video File", "", "Video Files (*.mp4 *.avi *.mkv)")
        if file_name:
            # Use QMediaPlayer directly with the URL
            media_source = QUrl.fromLocalFile(file_name)
            self.mediaPlayer.setMedia(media_source)  # Set media directly
            self.mediaPlayer.play()  # Play the video

    def stop_video(self):
        self.mediaPlayer.stop()  # Stop the video playback

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MediaPlayerExample()
    window.show()
    sys.exit(app.exec())
'''''

import sys
from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from PySide6.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile

class WebEngineExample(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the WebEngineView
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://scholar.google.com/")) 

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(self.browser)

        # Set up the main window
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Window properties
        self.setWindowTitle("QWebEngineView Example - PySide6")
        self.resize(800, 600)

    def load_url(self, url: str):
        self.browser.setUrl(QUrl(url))

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Create and show the window
    window = WebEngineExample()
    window.show()
    
    sys.exit(app.exec())
