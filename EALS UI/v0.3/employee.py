import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QWidget, QStackedWidget, QTabWidget
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Qt

class EALS:
    def __init__(self):
        self.home = Home()
        global global_home_ui
        global_home_ui = self.home.home_ui
        global_home_ui.showMaximized()

class Home:
    def __init__(self):
        self.loader = QUiLoader()
        self.home_ui = self.loader.load("home.ui")
        self.home_ui.main_page.setCurrentWidget(self.home_ui.home_page)

        self.home_ui.home_login_btn.clicked.connect(self.goto_bio1)
        self.home_ui.bio1_next.clicked.connect(self.goto_bio2)
        self.home_ui.bio2_next.clicked.connect(self.goto_result_prompt)

    def goto_bio1(self):
        bio1_page = self.home_ui.main_page.indexOf(self.home_ui.bio1_page)
        self.home_ui.main_page.setCurrentIndex(bio1_page)

    def goto_bio2(self):
        bio2_page = self.home_ui.main_page.indexOf(self.home_ui.bio2_page)
        self.home_ui.main_page.setCurrentIndex(bio2_page)

    def goto_result_prompt(self):
        result_prompt = self.home_ui.main_page.indexOf(self.home_ui.result_page)
        self.home_ui.main_page.setCurrentIndex(result_prompt)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = EALS()
    sys.exit(app.exec())