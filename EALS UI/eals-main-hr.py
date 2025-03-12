from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader

class EALS:
    def __init__(self):
        loader = QUiLoader()
        self.ui = loader.load("eals-main.ui")
        main_page_index = self.ui.stackedWidget.indexOf(self.ui.main_page)
        self.ui.stackedWidget.setCurrentIndex(main_page_index)
    
        self.ui.login_btn.clicked.connect(self.goto_hr_home)
        
        #for home page
        self.ui.hr_employee_btn.clicked.connect(self.goto_hr_employee)
        self.ui.hr_logout_btn.clicked.connect(self.goto_main_menu)
        self.ui.hr_create_feedback_btn.clicked.connect(self.goto_hr_feedback)
        self.ui.hr_employee_home_btn.clicked.connect(self.goto_hr_home)
        self.ui.cancel_feedback_btn.clicked.connect(self.goto_hr_home)
        self.ui.send_feedback_btn.clicked.connect(self.goto_hr_home)
        self.ui.hr_create_feedback_btn.clicked.connect(self.goto_hr_feedback)
        self.ui.hr_employee_view_btn.clicked.connect(self.goto_view_employee)
        self.ui.view_employee_back_btn.clicked.connect(self.goto_hr_employee)

        self.ui.show()
        
    def goto_main_menu(self):
        main_menu_index = self.ui.stackedWidget.indexOf(self.ui.main_page)
        self.ui.stackedWidget.setCurrentIndex(main_menu_index)

    
    def goto_hr_home(self):
        admin_home_index = self.ui.stackedWidget.indexOf(self.ui.hr_home_page)
        self.ui.stackedWidget.setCurrentIndex(admin_home_index)
    def goto_hr_employee(self):
        hr_employee_index = self.ui.stackedWidget.indexOf(self.ui.hr_employee_page)
        self.ui.stackedWidget.setCurrentIndex(hr_employee_index)
    def goto_hr_feedback(self):
        manage_hr_index = self.ui.stackedWidget.indexOf(self.ui.hr_feedback_page)
        self.ui.stackedWidget.setCurrentIndex(manage_hr_index)
    def goto_view_employee(self):
        view_employee_index = self.ui.stackedWidget.indexOf(self.ui.view_employee_page)
        self.ui.stackedWidget.setCurrentIndex(view_employee_index)
    def goto_veri1(self):
        veri1_index = self.ui.stackedWidget.indexOf(self.ui.employee_enroll_bio1_page)
        self.ui.stackedWidget.setCurrentIndex(veri1_index)
    def goto_veri2(self):
        veri2_index = self.ui.stackedWidget.indexOf(self.ui.employee_enroll_bio2_page)
        self.ui.stackedWidget.setCurrentIndex(veri2_index)
        
    
     

if __name__ == "__main__":
    app = QApplication([])
    window = EALS()
    app.exec()
