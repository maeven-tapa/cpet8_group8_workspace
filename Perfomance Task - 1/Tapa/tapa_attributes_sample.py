from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QApplication, QMainWindow
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.Sample_UI()

    def Sample_UI(self):
        self.setWindowTitle("PyQt6 UI Example")
        self.setGeometry(100, 100, 400, 200)
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QVBoxLayout(central_widget)
        self.tabWidget = QtWidgets.QTabWidget()
        layout.addWidget(self.tabWidget)

        # Tab 1
        self.tab1 = QtWidgets.QWidget()
        self.tabWidget.addTab(self.tab1, "Tab 1")
        tab1_layout = QtWidgets.QVBoxLayout(self.tab1)
        
        self.stackedWidget = QtWidgets.QStackedWidget()
        tab1_layout.addWidget(self.stackedWidget)
        
        # Page 1
        page1 = QtWidgets.QWidget()
        vbox = QtWidgets.QVBoxLayout(page1)
        label1 = QtWidgets.QLabel("Do you want to proceed?")
        label1.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        vbox.addWidget(label1)
        buttonBox1 = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel)
        vbox.addWidget(buttonBox1)
        self.stackedWidget.addWidget(page1)

        # Page 2
        page2 = QtWidgets.QWidget()
        hbox = QtWidgets.QHBoxLayout(page2)
        buttonBox2 = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel)
        hbox.addWidget(buttonBox2)
        label2 = QtWidgets.QLabel("Do you want to proceed?")
        hbox.addWidget(label2)
        self.stackedWidget.addWidget(page2)
        
        # Page 3
        page3 = QtWidgets.QWidget()
        form_layout = QtWidgets.QFormLayout(page3)
        label3 = QtWidgets.QLabel("Do you want to proceed?")
        buttonBox3 = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel)
        form_layout.addRow(label3, buttonBox3)
        self.stackedWidget.addWidget(page3)
        
        # Page 4
        page4 = QtWidgets.QWidget()
        grid_layout4 = QtWidgets.QGridLayout(page4)
        label4 = QtWidgets.QLabel("Do you want to proceed?")
        grid_layout4.addWidget(label4, 0, 0)
        buttonBox4 = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel)
        grid_layout4.addWidget(buttonBox4, 1, 0)
        self.stackedWidget.addWidget(page4)
        
        # Navigation Buttons for Tab 1
        nav_buttons1 = QtWidgets.QHBoxLayout()
        self.prev_button1 = QtWidgets.QPushButton("Previous")
        self.next_button1 = QtWidgets.QPushButton("Next")
        nav_buttons1.addWidget(self.prev_button1)
        nav_buttons1.addWidget(self.next_button1)
        tab1_layout.addLayout(nav_buttons1)
        
        self.prev_button1.clicked.connect(self.prev_page1)
        self.next_button1.clicked.connect(self.next_page1)

        # Tab 2
        self.tab2 = QtWidgets.QWidget()
        self.tabWidget.addTab(self.tab2, "Tab 2")
        tab2_layout = QtWidgets.QVBoxLayout(self.tab2)
        
        self.stackedWidget2 = QtWidgets.QStackedWidget()
        tab2_layout.addWidget(self.stackedWidget2)
        
        # Page 5
        page5 = QtWidgets.QWidget()
        grid_layout5 = QtWidgets.QGridLayout(page5)
        slider = QtWidgets.QSlider()
        slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        scrollbar = QtWidgets.QScrollBar()
        scrollbar.setOrientation(QtCore.Qt.Orientation.Horizontal)
        grid_layout5.addWidget(slider, 0, 0)
        grid_layout5.addWidget(scrollbar, 1, 0)
        self.stackedWidget2.addWidget(page5)
        
        # Page 6
        page6 = QtWidgets.QWidget()
        hbox_layout6 = QtWidgets.QHBoxLayout(page6)
        v_slider = QtWidgets.QSlider()
        v_slider.setOrientation(QtCore.Qt.Orientation.Vertical)
        v_scrollbar = QtWidgets.QScrollBar()
        v_scrollbar.setOrientation(QtCore.Qt.Orientation.Vertical)
        hbox_layout6.addWidget(v_slider)
        hbox_layout6.addWidget(v_scrollbar)
        self.stackedWidget2.addWidget(page6)
        
        # Navigation Buttons for Tab 2
        nav_buttons2 = QtWidgets.QHBoxLayout()
        self.prev_button2 = QtWidgets.QPushButton("Previous")
        self.next_button2 = QtWidgets.QPushButton("Next")
        nav_buttons2.addWidget(self.prev_button2)
        nav_buttons2.addWidget(self.next_button2)
        tab2_layout.addLayout(nav_buttons2)
        
        self.prev_button2.clicked.connect(self.prev_page2)
        self.next_button2.clicked.connect(self.next_page2)

    def prev_page1(self):
        index = self.stackedWidget.currentIndex()
        self.stackedWidget.setCurrentIndex((index - 1) % self.stackedWidget.count())
    
    def next_page1(self):
        index = self.stackedWidget.currentIndex()
        self.stackedWidget.setCurrentIndex((index + 1) % self.stackedWidget.count())
    
    def prev_page2(self):
        index = self.stackedWidget2.currentIndex()
        self.stackedWidget2.setCurrentIndex((index - 1) % self.stackedWidget2.count())
    
    def next_page2(self):
        index = self.stackedWidget2.currentIndex()
        self.stackedWidget2.setCurrentIndex((index + 1) % self.stackedWidget2.count())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
