import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QWidget, QStackedWidget, QTabWidget, QMessageBox, QTableWidgetItem, QAbstractItemView
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Qt, QDate
from datetime import datetime
from admin import Admin
import globals

class EALS:
    def __init__(self):
        self.home = Home()
        globals.global_home_ui = self.home.home_ui
        globals.global_home_ui.showMaximized()

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
        globals.global_home_ui.close()
        self.admin = Admin()
        self.admin.admin_ui.showMaximized()

class ChangePassword:
    def __init__(self):
        self.loader = QUiLoader()
        self.change_pass_ui = self.loader.load("admin_change_pass.ui")
        self.change_pass_ui.change_pass_note.setText("For security purposes, please enter your current password below, then choose a new password and confirm it. Make sure your new password is at least 8 characters long.")
        self.change_pass_ui.change_pass_note.setStyleSheet("color: black")
        self.change_pass_ui.admin_change_pass_btn.clicked.connect(self.validate_and_change_password)
        self.change_pass_ui.setWindowTitle("Change Admin Password")
        self.change_pass_ui.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)

    def validate_and_change_password(self):
        new_password = self.change_pass_ui.change_pass_np_box.text()
        confirm_password = self.change_pass_ui.change_pass_confirm_box.text()
        current_password = self.change_pass_ui.change_pass_cp_box.text()
        
        if current_password != Home.admin_password:
            self.change_pass_ui.change_pass_note.setText( "The current password you entered is incorrect. Please double-check and try again. Passwords are case-sensitive, so make sure your Caps Lock is off.")
            self.change_pass_ui.change_pass_note.setStyleSheet("color: red")
            return
            
        if not current_password or not new_password or not confirm_password:
            self.change_pass_ui.change_pass_note.setText("All password fields are required. Please make sure to enter your current password, a new password, and confirm the new password before continuing.")
            self.change_pass_ui.change_pass_note.setStyleSheet("color: red")
            return
            
        if new_password != confirm_password:
            self.change_pass_ui.change_pass_note.setText("The new password and the confirmation password do not match. Please ensure that both fields contain exactly the same password.")
            self.change_pass_ui.change_pass_note.setStyleSheet("color: red")
            return
            
        if len(new_password) < 8:
            self.change_pass_ui.change_pass_note.setText("Your new password must be at least 8 characters long for security reasons. Please choose a stronger password that meets this requirement.")
            self.change_pass_ui.change_pass_note.setStyleSheet("color: red")
            return
            

        Home.admin_password = new_password
        Home.password_changed = True
        self.goto_admin_home()
        
    def goto_admin_home(self):
        globals.global_home_ui.close()
        self.change_pass_ui.close()
        self.admin = Admin()
        self.admin.admin_ui.showMaximized()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = EALS()
    sys.exit(app.exec())