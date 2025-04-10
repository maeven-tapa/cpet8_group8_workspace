import time
from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader

class EALS:
    def __init__(self):
        loader = QUiLoader()
        self.ui = loader.load("eals-main.ui")
        main_page_index = self.ui.stackedWidget.indexOf(self.ui.main_page)
        self.ui.stackedWidget.setCurrentIndex(main_page_index)
    
        self.ui.login_btn.clicked.connect(self.go_to_admin_changepass)
        self.ui.change_pass_btn.clicked.connect(self.go_to_home)   
        #for home page
        self.ui.home_employee_btn.clicked.connect(self.goto_employee)
        self.ui.home_settings_btn.clicked.connect(self.goto_settings)
        self.ui.home_logout_btn.clicked.connect(self.goto_main_menu)
        
        #for employee page
        self.ui.employee_home_btn.clicked.connect(self.goto_home)
        self.ui.employee_settings_btn.clicked.connect(self.goto_settings)
        self.ui.manage_hr_btn.clicked.connect(self.goto_manage_hr)
        self.ui.employee_edit_btn.clicked.connect(self.goto_edit_employee)
        self.ui.employee_add_btn.clicked.connect(self.goto_employee_add)
        self.ui.employee_view_btn.clicked.connect(self.goto_view_employee)
        
        #for admin - manage hr
        self.ui.manager_hr_back_btn.clicked.connect(self.goto_employee)
        
        #for admin - edit employee
        self.ui.save_employee_btn.clicked.connect(self.goto_employee)
        self.ui.edit_employee_back_btn.clicked.connect(self.goto_employee)
        
        #for admin - view employee
        self.ui.view_employee_back_btn.clicked.connect(self.goto_employee)
        
        #for admin - enroll emnployee
        self.ui.add_employee_btn.clicked.connect(self.goto_employee)
        self.ui.enroll_employee_btn.clicked.connect(self.goto_veri1)
        self.ui.bio_cancel_btn.clicked.connect(self.goto_veri2)
        self.ui.face_cancel_btn.clicked.connect(self.goto_employee)
        
        
        #for settings page
        self.ui.settings_home_btn.clicked.connect(self.goto_home)
        self.ui.settings_employee_btn.clicked.connect(self.goto_employee)
        
        self.ui.show()
    
    def delay(self):
        time.sleep(5)
        
    def goto_main_menu(self):
        self.delay()
        main_menu_index = self.ui.stackedWidget.indexOf(self.ui.main_page)
        self.ui.stackedWidget.setCurrentIndex(main_menu_index)

    def go_to_admin_changepass(self):
        self.delay()
        admin_page_index = self.ui.stackedWidget.indexOf(self.ui.admin_changpass_page)
        self.ui.stackedWidget.setCurrentIndex(admin_page_index)
    
    def go_to_home(self):
        self.delay()
        admin_home_index = self.ui.stackedWidget.indexOf(self.ui.admin_home_page)
        self.ui.stackedWidget.setCurrentIndex(admin_home_index)
    
    #for admin menu
    def goto_home(self):
        self.delay()
        employee_home_index = self.ui.stackedWidget.indexOf(self.ui.admin_home_page)
        self.ui.stackedWidget.setCurrentIndex(employee_home_index)
    def goto_settings(self):
        self.delay()
        admin_setting_index = self.ui.stackedWidget.indexOf(self.ui.admin_settings_page)
        self.ui.stackedWidget.setCurrentIndex(admin_setting_index) 
    def goto_employee(self):
        self.delay()
        home_employee_index = self.ui.stackedWidget.indexOf(self.ui.admin_employee_page)
        self.ui.stackedWidget.setCurrentIndex(home_employee_index) 
        
     #for admin - employee menu
    def goto_manage_hr(self):
        self.delay()
        manage_hr_index = self.ui.stackedWidget.indexOf(self.ui.admin_hr_page)
        self.ui.stackedWidget.setCurrentIndex(manage_hr_index)
    def goto_edit_employee(self):
        self.delay()
        edit_employee_index = self.ui.stackedWidget.indexOf(self.ui.edit_employee_page)
        self.ui.stackedWidget.setCurrentIndex(edit_employee_index)
    def goto_employee_add(self):
        self.delay()
        add_employee_index = self.ui.stackedWidget.indexOf(self.ui.employee_enroll_page)
        self.ui.stackedWidget.setCurrentIndex(add_employee_index)
    def goto_view_employee(self):
        self.delay()
        view_employee_index = self.ui.stackedWidget.indexOf(self.ui.view_employee_page)
        self.ui.stackedWidget.setCurrentIndex(view_employee_index)
        
    #for admin - enroll emnployee
    def goto_veri1(self):
        self.delay()
        veri1_index = self.ui.stackedWidget.indexOf(self.ui.employee_enroll_bio1_page)
        self.ui.stackedWidget.setCurrentIndex(veri1_index)
    def goto_veri2(self):
        self.delay()
        veri2_index = self.ui.stackedWidget.indexOf(self.ui.employee_enroll_bio2_page)
        self.ui.stackedWidget.setCurrentIndex(veri2_index)
        
    
     
    
if __name__ == "__main__":
    app = QApplication([])
    window = EALS()
    app.exec()
