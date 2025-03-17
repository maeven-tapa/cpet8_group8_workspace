from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader

class EALS:
    def __init__(self):
        loader = QUiLoader()
        self.ui = loader.load("eals-main.ui")
        main_page_index = self.ui.stackedWidget.indexOf(self.ui.main_page)
        self.ui.stackedWidget.setCurrentIndex(main_page_index)
    
        self.ui.login_btn.clicked.connect(self.goto_veri1)
        self.ui.veri1_cancel_btn.clicked.connect(self.goto_veri2)
        self.ui.veri2_cancel_btn.clicked.connect(self.goto_main_menu)
        
        self.ui.show()
        
    def goto_main_menu(self):
        main_menu_index = self.ui.stackedWidget.indexOf(self.ui.main_page)
        self.ui.stackedWidget.setCurrentIndex(main_menu_index)
        
    def goto_veri1(self):
        veri1_index = self.ui.stackedWidget.indexOf(self.ui.veri1_employee_page)
        self.ui.stackedWidget.setCurrentIndex(veri1_index)
    def goto_veri2(self):
        veri2_index = self.ui.stackedWidget.indexOf(self.ui.veri2_employee_page)
        self.ui.stackedWidget.setCurrentIndex(veri2_index)

if __name__ == "__main__":
    app = QApplication([])
    window = EALS()
    app.exec()
