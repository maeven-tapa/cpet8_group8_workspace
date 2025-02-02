from PySide6.QtWidgets import (QApplication, QWidget, QGridLayout, QCalendarWidget,
                               QDateEdit, QTimeEdit, QCheckBox, QFrame)
from PySide6.QtAxContainer import QAxWidget
from PySide6.QtCore import Qt
import sys

class Form(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Form")
        self.setGeometry(0, 0, 402, 499)
        
        layout = QGridLayout(self)
        
        self.calendarWidget = QCalendarWidget()
        layout.addWidget(self.calendarWidget, 0, 0, 1, 3)
        
        self.dateEdit = QDateEdit()
        layout.addWidget(self.dateEdit, 1, 0, 1, 3)
        
        self.timeEdit = QTimeEdit()
        layout.addWidget(self.timeEdit, 2, 0, 1, 3)
        
        self.checkBox1 = QCheckBox("To Do")
        layout.addWidget(self.checkBox1, 3, 0)
        
        self.checkBox2 = QCheckBox("Done")
        layout.addWidget(self.checkBox2, 3, 1)
        
        self.checkBox3 = QCheckBox("Late")
        layout.addWidget(self.checkBox3, 3, 2)
        
        self.line = QFrame()
        self.line.setFrameShape(QFrame.HLine)
        layout.addWidget(self.line, 4, 0, 1, 3)
        
        self.axWidget = QAxWidget("{6bf52a52-394a-11d3-b153-00c04f79faa6}")
        layout.addWidget(self.axWidget, 5, 0, 1, 3)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Form()
    window.show()
    sys.exit(app.exec())
