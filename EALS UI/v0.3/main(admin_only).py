import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QWidget, QStackedWidget, QTabWidget, QMessageBox, QTableWidgetItem
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
        self.employees = []

        self.admin_ui.admin_logout_btn.clicked.connect(self.goto_home)

        self.admin_ui.employee_edit_btn.clicked.connect(self.goto_employee_edit)
        self.admin_ui.employee_edit_back.clicked.connect(self.goto_employee_hr)
        self.admin_ui.employee_edit_deactivate.clicked.connect(self.goto_employee_hr)
        self.admin_ui.employee_edit_save.clicked.connect(self.goto_employee_hr)

        self.admin_ui.employee_enroll_btn.clicked.connect(self.goto_employee_enroll)
        self.admin_ui.employee_enroll_cancel.clicked.connect(self.goto_employee_hr)
        self.admin_ui.employee_enroll_1.clicked.connect(self.goto_employee_enroll_2_with_validation)
        self.admin_ui.employee_enroll_back1.clicked.connect(self.goto_employee_enroll)
        self.admin_ui.employee_enroll_2.clicked.connect(self.goto_employee_enroll_3)
        self.admin_ui.employee_enroll_back2.clicked.connect(self.goto_employee_enroll_2)
        self.admin_ui.employee_enroll_3.clicked.connect(self.finalize_employee_enrollment)

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
        self.load_employee_table()

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


    def validate_employee_data(self):
        first_name = self.admin_ui.employee_first_name.text().strip()
        last_name = self.admin_ui.employee_last_name.text().strip()
        mi = self.admin_ui.employee_mi.text().strip()
        id_pref = self.admin_ui.employee_id_pref.text().strip()
        id_year = self.admin_ui.employee_id_year.currentText()
        id_no = self.admin_ui.employee_id_no.currentText()
        password = self.admin_ui.employee_password.text()
        confirm_password = self.admin_ui.employee_confirm_password.text()
        
        gender = None
        if self.admin_ui.employee_male.isChecked():
            gender = "Male"
        elif self.admin_ui.employee_female.isChecked():
            gender = "Female"
        
        department = self.admin_ui.employee_department_box.currentText()
        position = self.admin_ui.employee_position_box.currentText()
        
        schedule = None
        if self.admin_ui.employee_sched_1.isChecked():
            schedule = "6am to 2pm"
        elif self.admin_ui.employee_sched_2.isChecked():
            schedule = "2pm to 10pm"
        elif self.admin_ui.employee_sched_3.isChecked():
            schedule = "10pm to 6am"
        
        missing_fields = []
        
        if not first_name:
            missing_fields.append("First Name")
        if not last_name:
            missing_fields.append("Last Name")
        if not id_pref:
            missing_fields.append("ID Prefix")
        if not password:
            missing_fields.append("Password")
        if not confirm_password:
            missing_fields.append("Confirm Password")
        if not gender:
            missing_fields.append("Gender")
        if not schedule:
            missing_fields.append("Schedule")
        
        if password and confirm_password and password != confirm_password:
            return False, "Password and Confirm Password do not match"
        
        if missing_fields:
            return False, f"Please fill in the following required fields: {', '.join(missing_fields)}"
        
        employee_data = {
            "first_name": first_name,
            "last_name": last_name,
            "middle_initial": mi,
            "employee_id": f"{id_pref}-{id_year}-{id_no}",
            "password": password,
            "gender": gender,
            "birthday": self.admin_ui.employee_birthday_edit.date().toString("yyyy-MM-dd"),
            "department": department,
            "position": position,
            "schedule": schedule
        }
        
        return True, employee_data

    def load_employee_table(self):
        self.admin_ui.employee_list_tbl.setRowCount(0)

        if hasattr(self, 'employees') and self.employees:
            for employee in self.employees:
                self.add_employee_to_table(employee)

    def add_employee_to_table(self, employee_data):
        row_position = self.admin_ui.employee_list_tbl.rowCount()
        self.admin_ui.employee_list_tbl.insertRow(row_position)
        middle_initial = f" {employee_data['middle_initial']}." if employee_data['middle_initial'] else ""
        full_name = f"{employee_data['last_name']}, {employee_data['first_name']}{middle_initial}"
        dept_pos = f"{employee_data['department']} / {employee_data['position']}"
        
        name_item = QTableWidgetItem(full_name)
        id_item = QTableWidgetItem(employee_data['employee_id'])
        dept_pos_item = QTableWidgetItem(dept_pos)
        status_item = QTableWidgetItem("Active")  # New employees are active by default
        
        name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
        id_item.setFlags(id_item.flags() & ~Qt.ItemIsEditable)
        dept_pos_item.setFlags(dept_pos_item.flags() & ~Qt.ItemIsEditable)
        status_item.setFlags(status_item.flags() & ~Qt.ItemIsEditable)
        
        self.admin_ui.employee_list_tbl.setItem(row_position, 0, name_item)
        self.admin_ui.employee_list_tbl.setItem(row_position, 1, id_item)
        self.admin_ui.employee_list_tbl.setItem(row_position, 2, dept_pos_item)
        self.admin_ui.employee_list_tbl.setItem(row_position, 3, status_item)
        
        self.admin_ui.employee_list_tbl.resizeColumnsToContents()

    def save_employee_data(self, employee_data):
        if not hasattr(self, 'employees'):
            self.employees = []

        self.employees.append(employee_data)
        
        print("Saving employee data:")
        for key, value in employee_data.items():
            print(f"{key}: {value}")
        
        if self.admin_ui.admin_employee_sc_pages.currentWidget() == self.admin_ui.employee_hr_page:
            self.add_employee_to_table(employee_data)
        
        return True

    def goto_employee_enroll_2_with_validation(self):
        valid, result = self.validate_employee_data()
        if valid:
            self.current_employee_data = result
            self.goto_employee_enroll_2()
        else:
            error_msg = QMessageBox()
            error_msg.setIcon(QMessageBox.Critical)
            error_msg.setText("Validation Error")
            error_msg.setInformativeText(result)
            error_msg.setWindowTitle("Enrollment Error")
            error_msg.exec()

    def finalize_employee_enrollment(self):
        if hasattr(self, 'current_employee_data'):
            success = self.save_employee_data(self.current_employee_data)
            
            if success:
                success_msg = QMessageBox()
                success_msg.setIcon(QMessageBox.Information)
                success_msg.setText("Employee Enrolled Successfully")
                success_msg.setInformativeText(f"Employee {self.current_employee_data['first_name']} {self.current_employee_data['last_name']} has been enrolled.")
                success_msg.setWindowTitle("Enrollment Success")
                success_msg.exec()
                self.goto_employee_hr()
                self.load_employee_table()
            else:
                error_msg = QMessageBox()
                error_msg.setIcon(QMessageBox.Critical)
                error_msg.setText("Enrollment Error")
                error_msg.setInformativeText("Failed to save employee data. Please try again.")
                error_msg.setWindowTitle("Enrollment Error")
                error_msg.exec()
        else:
            error_msg = QMessageBox()
            error_msg.setIcon(QMessageBox.Critical)
            error_msg.setText("Process Error")
            error_msg.setInformativeText("No employee data found. Please restart the enrollment process.")
            error_msg.setWindowTitle("Enrollment Error")
            error_msg.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = EALS()
    sys.exit(app.exec())