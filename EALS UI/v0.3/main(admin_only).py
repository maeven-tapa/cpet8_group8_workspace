import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QWidget, QStackedWidget, QTabWidget, QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Qt
from datetime import datetime

class EALS:
    def __init__(self):
        self.home = Home()
        global global_home_ui
        global_home_ui = self.home.home_ui
        global_home_ui.showMaximized()

class Home:
    admin_password = "defaultpassword"
    password_changed = False
    
    def __init__(self):
        self.loader = QUiLoader()
        self.home_ui = self.loader.load("home.ui")
        self.home_ui.main_page.setCurrentWidget(self.home_ui.home_page)
        self.admin_id = "admin-01-0001"
        self.update_date_today()
        self.home_ui.home_login_btn.clicked.connect(self.handle_login)
    
    def update_date_today(self):
        current_date = datetime.now()
        formatted_date = current_date.strftime("%a, %b %d, %Y")
        self.home_ui.date_today.setText(formatted_date)

    def handle_login(self):
        user_id = self.home_ui.home_id_box.text()
        password = self.home_ui.home_pass_box.text()
        if user_id == self.admin_id and password == Home.admin_password:
            if Home.password_changed:
                self.goto_admin_ui()
            else:
                self.goto_change_pass()
        else:
            error_msg = QMessageBox()
            error_msg.setIcon(QMessageBox.Critical)
            error_msg.setText("Invalid credentials")
            error_msg.setInformativeText("Please enter valid admin ID and password")
            error_msg.setWindowTitle("Login Error")
            error_msg.exec()
    
    def goto_change_pass(self):
        self.changepass = ChangePassword()
        self.changepass.change_pass_ui.show()
    
    def goto_admin_ui(self):
        global_home_ui.close()
        self.admin = Admin()
        self.admin.admin_ui.showMaximized()

class ChangePassword:
    def __init__(self):
        self.loader = QUiLoader()
        self.change_pass_ui = self.loader.load("admin_change_pass.ui")
        self.change_pass_ui.change_pass_note.setText("Please enter your current password and set a new one.")
        self.change_pass_ui.change_pass_note.setStyleSheet("color: black")
        self.change_pass_ui.admin_change_pass_btn.clicked.connect(self.validate_and_change_password)
        self.change_pass_ui.setWindowFlags(self.change_pass_ui.windowFlags() | Qt.WindowStaysOnTopHint)

    def validate_and_change_password(self):
        new_password = self.change_pass_ui.change_pass_np_box.text()
        confirm_password = self.change_pass_ui.change_pass_confirm_box.text()
        current_password = self.change_pass_ui.change_pass_cp_box.text()
        
        if current_password != Home.admin_password:
            self.change_pass_ui.change_pass_note.setText("Current password is incorrect!")
            self.change_pass_ui.change_pass_note.setStyleSheet("color: red")
            return
            
        if not current_password or not new_password or not confirm_password:
            self.change_pass_ui.change_pass_note.setText("All password fields are required!")
            self.change_pass_ui.change_pass_note.setStyleSheet("color: red")
            return
            
        if new_password != confirm_password:
            self.change_pass_ui.change_pass_note.setText("New password and confirmation don't match!")
            self.change_pass_ui.change_pass_note.setStyleSheet("color: red")
            return
            
        if len(new_password) < 8:
            self.change_pass_ui.change_pass_note.setText("New password must be at least 8 characters!")
            self.change_pass_ui.change_pass_note.setStyleSheet("color: red")
            return
            

        Home.admin_password = new_password
        Home.password_changed = True
        self.goto_admin_home()
        
    def goto_admin_home(self):
        global_home_ui.close()
        self.change_pass_ui.close()
        self.admin = Admin()
        self.admin.admin_ui.showMaximized()

class Admin:
    def __init__(self):
        self.loader = QUiLoader()
        self.admin_ui = self.loader.load("admin.ui")
        self.admin_ui.home_tabs.setCurrentWidget(self.admin_ui.admin_dashboard)
        self.admin_ui.admin_employee_sc_pages.setCurrentWidget(self.admin_ui.employee_hr_page)

        self.admin_ui.admin_logout_btn.clicked.connect(self.goto_home)

        self.admin_ui.employee_edit_btn.clicked.connect(self.goto_employee_edit)
        self.admin_ui.employee_edit_back.clicked.connect(self.goto_employee_hr)
        self.admin_ui.employee_edit_deactivate.clicked.connect(self.goto_employee_hr)
        self.admin_ui.employee_edit_save.clicked.connect(self.goto_employee_hr)

        self.admin_ui.employee_enroll_btn.clicked.connect(self.goto_employee_enroll)
        self.admin_ui.employee_enroll_cancel.clicked.connect(self.goto_employee_hr)
        self.admin_ui.employee_enroll_1.clicked.connect(self.goto_employee_enroll_2)
        self.admin_ui.employee_enroll_back1.clicked.connect(self.goto_employee_enroll)
        self.admin_ui.employee_enroll_2.clicked.connect(self.goto_employee_enroll_3)
        self.admin_ui.employee_enroll_back2.clicked.connect(self.goto_employee_enroll_2)
        self.admin_ui.employee_enroll_3.clicked.connect(self.goto_employee_hr)

        self.admin_ui.employee_view_btn.clicked.connect(self.goto_employee_view)
        self.admin_ui.employee_view_back.clicked.connect(self.goto_employee_hr)

        self.admin_ui.hr_edit_btn.clicked.connect(self.goto_hr_edit)
        self.admin_ui.hr_edit_back.clicked.connect(self.goto_employee_hr)
        self.admin_ui.hr_edit_deactivate.clicked.connect(self.goto_employee_hr)
        self.admin_ui.hr_edit_save.clicked.connect(self.goto_employee_hr)

        self.admin_ui.hr_add_btn.clicked.connect(self.goto_hr_add)
        self.admin_ui.hr_add_cancel.clicked.connect(self.goto_employee_hr)
        self.admin_ui.hr_add_1.clicked.connect(self.goto_employee_enroll_2)

        self.admin_ui.hr_view_btn.clicked.connect(self.goto_hr_view)
        self.admin_ui.hr_view_back.clicked.connect(self.goto_employee_hr)
        
        self.update_date_today()


    def update_date_today(self):
        current_date = datetime.now()
        formatted_date = current_date.strftime("%a, %b %d, %Y")
        self.admin_ui.date_today.setText(formatted_date)

    def goto_home(self):
        global_home_ui.showMaximized()
        self.admin_ui.close()

    
    def goto_employee_hr(self):
        employee_hr_page = self.admin_ui.admin_employee_sc_pages.indexOf(self.admin_ui.employee_hr_page)
        self.admin_ui.admin_employee_sc_pages.setCurrentIndex(employee_hr_page)

    def goto_employee_edit(self):
        employee_edit_page = self.admin_ui.admin_employee_sc_pages.indexOf(self.admin_ui.employee_edit_page)
        self.admin_ui.admin_employee_sc_pages.setCurrentIndex(employee_edit_page)

    def goto_employee_enroll(self):
        employee_enroll_page = self.admin_ui.admin_employee_sc_pages.indexOf(self.admin_ui.employee_enroll_page)
        self.admin_ui.admin_employee_sc_pages.setCurrentIndex(employee_enroll_page)

    def goto_employee_enroll_2(self):
        employee_enroll_2_page = self.admin_ui.admin_employee_sc_pages.indexOf(self.admin_ui.employee_enroll2_page)
        self.admin_ui.admin_employee_sc_pages.setCurrentIndex(employee_enroll_2_page)

    def goto_employee_enroll_3(self):
        employee_enroll_3_page = self.admin_ui.admin_employee_sc_pages.indexOf(self.admin_ui.employee_enroll3_page)
        self.admin_ui.admin_employee_sc_pages.setCurrentIndex(employee_enroll_3_page)
        
    def goto_employee_view(self):
        employee_view_page = self.admin_ui.admin_employee_sc_pages.indexOf(self.admin_ui.employee_view_page)
        self.admin_ui.admin_employee_sc_pages.setCurrentIndex(employee_view_page)

    def goto_hr_edit(self):
        hr_edit_page = self.admin_ui.admin_employee_sc_pages.indexOf(self.admin_ui.hr_edit_page)
        self.admin_ui.admin_employee_sc_pages.setCurrentIndex(hr_edit_page)

    def goto_hr_add(self):
        hr_add_page = self.admin_ui.admin_employee_sc_pages.indexOf(self.admin_ui.hr_add_page)
        self.admin_ui.admin_employee_sc_pages.setCurrentIndex(hr_add_page)

    def goto_hr_view(self):
        hr_view_page = self.admin_ui.admin_employee_sc_pages.indexOf(self.admin_ui.hr_view_page)
        self.admin_ui.admin_employee_sc_pages.setCurrentIndex(hr_view_page)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = EALS()
    sys.exit(app.exec())