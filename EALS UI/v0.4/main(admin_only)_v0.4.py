import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QWidget, QStackedWidget, QTabWidget, QMessageBox, QTableWidgetItem, QAbstractItemView
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Qt, QDate
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
        self.hr_employees = []

        self.admin_ui.admin_logout_btn.clicked.connect(self.goto_home)

        self.admin_ui.employee_list_tbl.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.admin_ui.employee_list_tbl.setSelectionMode(QAbstractItemView.SingleSelection)
        self.admin_ui.hr_list_tbl.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.admin_ui.hr_list_tbl.setSelectionMode(QAbstractItemView.SingleSelection)

        self.admin_ui.employee_edit_btn.clicked.connect(self.handle_edit_button)
        self.admin_ui.employee_edit_save.clicked.connect(self.save_edited_employee)
        self.admin_ui.employee_edit_deactivate.clicked.connect(self.toggle_employee_status)
        self.admin_ui.employee_edit_back.clicked.connect(self.goto_employee_hr)

        self.admin_ui.employee_enroll_btn.clicked.connect(self.goto_employee_enroll)
        self.admin_ui.employee_enroll_cancel.clicked.connect(self.goto_employee_hr)
        self.admin_ui.employee_enroll_1.clicked.connect(self.goto_employee_enroll_2_with_validation)
        self.admin_ui.employee_enroll_back1.clicked.connect(self.goto_employee_enroll)
        self.admin_ui.employee_enroll_2.clicked.connect(self.goto_employee_enroll_3)
        self.admin_ui.employee_enroll_back2.clicked.connect(self.goto_employee_enroll_2)
        self.admin_ui.employee_enroll_3.clicked.connect(self.finalize_employee_enrollment)

        self.admin_ui.employee_view_btn.clicked.connect(self.goto_employee_view)
        self.admin_ui.employee_view_back.clicked.connect(self.goto_employee_hr)
        self.admin_ui.hr_view_back.clicked.connect(self.goto_employee_hr)
        
        self.admin_ui.is_hr_yes.toggled.connect(self.toggle_hr_fields)
        self.admin_ui.is_hr_no.toggled.connect(self.toggle_hr_fields)

        self.admin_ui.employee_search_box.textChanged.connect(self.filter_employee_table)
        self.admin_ui.hr_search_box.textChanged.connect(self.filter_hr_table)
        
        self.admin_ui.employee_sort_box.currentIndexChanged.connect(self.sort_employee_table)
        self.admin_ui.hr_sort_box.currentIndexChanged.connect(self.sort_hr_table)
        
        self.selected_employee_index = None
        self.selected_employee_type = None
        
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
        self.load_hr_table()

    def goto_employee_edit(self):
        employee_edit_page = self.admin_ui.admin_employee_sc_pages.indexOf(self.admin_ui.employee_edit_page)
        self.admin_ui.admin_employee_sc_pages.setCurrentIndex(employee_edit_page)

    def goto_employee_enroll(self):
        employee_enroll_page = self.admin_ui.admin_employee_sc_pages.indexOf(self.admin_ui.employee_enroll_page)
        self.admin_ui.admin_employee_sc_pages.setCurrentIndex(employee_enroll_page)
        # Reset the HR radio buttons and fields
        self.admin_ui.is_hr_no.setChecked(True)
        self.toggle_hr_fields()

    def goto_employee_enroll_2(self):
        employee_enroll_2_page = self.admin_ui.admin_employee_sc_pages.indexOf(self.admin_ui.employee_enroll2_page)
        self.admin_ui.admin_employee_sc_pages.setCurrentIndex(employee_enroll_2_page)

    def goto_employee_enroll_3(self):
        employee_enroll_3_page = self.admin_ui.admin_employee_sc_pages.indexOf(self.admin_ui.employee_enroll3_page)
        self.admin_ui.admin_employee_sc_pages.setCurrentIndex(employee_enroll_3_page)
        
    def filter_employee_table(self):
        search_text = self.admin_ui.employee_search_box.text().lower()
        
        # Show all rows first
        for row in range(self.admin_ui.employee_list_tbl.rowCount()):
            self.admin_ui.employee_list_tbl.setRowHidden(row, False)
        
        if not search_text:
            return
        
        # Hide rows that don't match the search
        for row in range(self.admin_ui.employee_list_tbl.rowCount()):
            match_found = False
            
            # Search in each column
            for col in range(self.admin_ui.employee_list_tbl.columnCount()):
                item = self.admin_ui.employee_list_tbl.item(row, col)
                if item and search_text in item.text().lower():
                    match_found = True
                    break
                    
            self.admin_ui.employee_list_tbl.setRowHidden(row, not match_found)

    def filter_hr_table(self):
        search_text = self.admin_ui.hr_search_box.text().lower()
        
        # Show all rows first
        for row in range(self.admin_ui.hr_list_tbl.rowCount()):
            self.admin_ui.hr_list_tbl.setRowHidden(row, False)
        
        if not search_text:
            return
        
        # Hide rows that don't match the search
        for row in range(self.admin_ui.hr_list_tbl.rowCount()):
            match_found = False
            
            # Search in each column
            for col in range(self.admin_ui.hr_list_tbl.columnCount()):
                item = self.admin_ui.hr_list_tbl.item(row, col)
                if item and search_text in item.text().lower():
                    match_found = True
                    break
                    
            self.admin_ui.hr_list_tbl.setRowHidden(row, not match_found)

    def sort_employee_table(self):
        sort_option = self.admin_ui.employee_sort_box.currentText()
        
        # Store current data
        data = []
        for row in range(self.admin_ui.employee_list_tbl.rowCount()):
            row_data = []
            for col in range(self.admin_ui.employee_list_tbl.columnCount()):
                item = self.admin_ui.employee_list_tbl.item(row, col)
                row_data.append(item.text() if item else "")
            # Add the index of the employee in the self.employees list for reference
            row_data.append(row)
            data.append(row_data)
        
        # Sort the data based on the selected option
        if sort_option == "By Name":
            data.sort(key=lambda x: x[0])  # Sort by Name (column 0)
        elif sort_option == "By Account ID":
            data.sort(key=lambda x: x[1])  # Sort by Account ID (column 1)
        elif sort_option == "By Department":
            data.sort(key=lambda x: x[2])  # Sort by Department (column 2)
        elif sort_option == "By Status":
            data.sort(key=lambda x: x[3])  # Sort by Status (column 3)
        
        # Update the table with sorted data
        self.admin_ui.employee_list_tbl.setRowCount(0)
        for row_data in data:
            original_index = row_data[-1]  # Get the original index
            employee_data = self.employees[original_index]
            self.add_employee_to_table(employee_data)

    def sort_hr_table(self):
        sort_option = self.admin_ui.hr_sort_box.currentText()
        
        # Store current data
        data = []
        for row in range(self.admin_ui.hr_list_tbl.rowCount()):
            row_data = []
            for col in range(self.admin_ui.hr_list_tbl.columnCount()):
                item = self.admin_ui.hr_list_tbl.item(row, col)
                row_data.append(item.text() if item else "")
            # Add the index of the employee in the self.hr_employees list for reference
            row_data.append(row)
            data.append(row_data)
        
        # Sort the data based on the selected option
        if sort_option == "By Name":
            data.sort(key=lambda x: x[0])  # Sort by Name (column 0)
        elif sort_option == "By Account ID":
            data.sort(key=lambda x: x[1])  # Sort by Account ID (column 1)
        elif sort_option == "By Status":
            data.sort(key=lambda x: x[2])  # Sort by Status (column 2)
        
        # Update the table with sorted data
        self.admin_ui.hr_list_tbl.setRowCount(0)
        for row_data in data:
            original_index = row_data[-1]  # Get the original index
            hr_data = self.hr_employees[original_index]
            self.add_hr_to_table(hr_data)

    def goto_employee_view(self):
        employee_selected_rows = self.admin_ui.employee_list_tbl.selectedIndexes()
        hr_selected_rows = self.admin_ui.hr_list_tbl.selectedIndexes()
        
        if employee_selected_rows:
            row = employee_selected_rows[0].row()
            employee_data = self.employees[row]
            self.display_employee_view(employee_data)
            
            employee_view_page = self.admin_ui.admin_employee_sc_pages.indexOf(self.admin_ui.employee_view_page)
            self.admin_ui.admin_employee_sc_pages.setCurrentIndex(employee_view_page)
            
        elif hr_selected_rows:
            row = hr_selected_rows[0].row()
            hr_data = self.hr_employees[row]
            self.display_hr_view(hr_data)
            
            hr_view_page = self.admin_ui.admin_employee_sc_pages.indexOf(self.admin_ui.hr_view_page)
            self.admin_ui.admin_employee_sc_pages.setCurrentIndex(hr_view_page)
            
        else:
            error_msg = QMessageBox()
            error_msg.setIcon(QMessageBox.Warning)
            error_msg.setText("No Selection")
            error_msg.setInformativeText("Please select an employee to view.")
            error_msg.setWindowTitle("View Error")
            error_msg.exec()

    def display_employee_view(self, employee_data):
        self.admin_ui.view_employee_first_name.setText(employee_data["first_name"])
        self.admin_ui.view_employee_last_name.setText(employee_data["last_name"])
        self.admin_ui.view_employee_mi.setText(employee_data["middle_initial"])
        birthday_str = employee_data["birthday"]

        try:
            birthday_date = datetime.strptime(birthday_str, "%Y-%m-%d")
            formatted_birthday = birthday_date.strftime("%B %d, %Y")
            self.admin_ui.view_employee_birthday.setText(formatted_birthday)
            
            # Calculate age
            today = datetime.now()
            age = today.year - birthday_date.year - ((today.month, today.day) < (birthday_date.month, birthday_date.day))
            self.admin_ui.view_employee_age.setText(str(age))
        except Exception as e:
            print(f"Error formatting birthday: {e}")
            self.admin_ui.view_employee_birthday.setText(birthday_str)
            self.admin_ui.view_employee_age.setText("N/A")
        
        if employee_data["gender"] == "Male":
            self.admin_ui.view_employee_male.setChecked(True)
        else:
            self.admin_ui.view_employee_female.setChecked(True)
        
        self.admin_ui.view_employee_department_box.setText(employee_data["department"])
        self.admin_ui.view_employee_position_box.setText(employee_data["position"])
        self.admin_ui.view_employee_accountid.setText(employee_data["employee_id"])
        
        if employee_data["schedule"] == "6am to 2pm":
            self.admin_ui.view_employee_sched_1.setChecked(True)
        elif employee_data["schedule"] == "2pm to 10pm":
            self.admin_ui.view_employee_sched_2.setChecked(True)
        else:  # 10pm to 6am
            self.admin_ui.view_employee_sched_3.setChecked(True)

    def display_hr_view(self, hr_data):
        self.admin_ui.view_hr_first_name.setText(hr_data["first_name"])
        self.admin_ui.view_hr_last_name.setText(hr_data["last_name"])
        self.admin_ui.view_hr_mi.setText(hr_data["middle_initial"])
        birthday_str = hr_data["birthday"]

        try:
            birthday_date = datetime.strptime(birthday_str, "%Y-%m-%d")
            formatted_birthday = birthday_date.strftime("%B %d, %Y")
            self.admin_ui.view_hr_birthday.setText(formatted_birthday)
            today = datetime.now()
            age = today.year - birthday_date.year - ((today.month, today.day) < (birthday_date.month, birthday_date.day))
            self.admin_ui.view_hr_age.setText(str(age))
        except Exception as e:
            print(f"Error formatting birthday: {e}")
            self.admin_ui.view_hr_birthday.setText(birthday_str)
            self.admin_ui.view_hr_age.setText("N/A")
        
        if hr_data["gender"] == "Male":
            self.admin_ui.view_hr_male.setChecked(True)
        else:
            self.admin_ui.view_hr_female.setChecked(True)
        
        self.admin_ui.view_hr_accountid.setText(hr_data["employee_id"])
        
        if hr_data["schedule"] == "6am to 2pm":
            self.admin_ui.view_hr_sched_1.setChecked(True)
        elif hr_data["schedule"] == "2pm to 10pm":
            self.admin_ui.view_hr_sched_2.setChecked(True)
        else:  # 10pm to 6am
            self.admin_ui.view_hr_sched_3.setChecked(True)


    def handle_edit_button(self):
        employee_selected_rows = self.admin_ui.employee_list_tbl.selectedIndexes()
        hr_selected_rows = self.admin_ui.hr_list_tbl.selectedIndexes()
        
        if employee_selected_rows:
            row = employee_selected_rows[0].row() 
            self.selected_employee_index = row
            self.selected_employee_type = "employee"
            employee_data = self.employees[row]
            self.load_employee_to_edit_form(employee_data)
            self.goto_employee_edit()
            
        elif hr_selected_rows:
            row = hr_selected_rows[0].row()
            self.selected_employee_index = row
            self.selected_employee_type = "hr"
            hr_data = self.hr_employees[row]
            self.load_employee_to_edit_form(hr_data)
            self.goto_employee_edit()
            
        else:
            error_msg = QMessageBox()
            error_msg.setIcon(QMessageBox.Warning)
            error_msg.setText("No Selection")
            error_msg.setInformativeText("Please select an employee to edit.")
            error_msg.setWindowTitle("Edit Error")
            error_msg.exec()

    def load_employee_to_edit_form(self, employee_data):
        self.admin_ui.edit_employee_first_name.setText(employee_data["first_name"])
        self.admin_ui.edit_employee_last_name.setText(employee_data["last_name"])
        self.admin_ui.edit_employee_mi.setText(employee_data["middle_initial"])
        
        date_parts = employee_data["birthday"].split("-")
        if len(date_parts) == 3:
            year, month, day = int(date_parts[0]), int(date_parts[1]), int(date_parts[2])
            self.admin_ui.edit_employee_birthday_edit.setDate(QDate(year, month, day))
        
        if employee_data["gender"] == "Male":
            self.admin_ui.edit_employee_male.setChecked(True)
        else:
            self.admin_ui.edit_employee_female.setChecked(True)
        
        is_hr = employee_data.get("is_hr", False)
        if is_hr:
            self.admin_ui.edit_is_hr_yes.setChecked(True)
        else:
            self.admin_ui.edit_is_hr_no.setChecked(True)
        
        self.toggle_edit_hr_fields()
        
        try:
            index = self.admin_ui.edit_employee_department_box.findText(employee_data["department"])
            if index >= 0:
                self.admin_ui.edit_employee_department_box.setCurrentIndex(index)
                
            index = self.admin_ui.edit_employee_position_box.findText(employee_data["position"])
            if index >= 0:
                self.admin_ui.edit_employee_position_box.setCurrentIndex(index)
        except Exception as e:
            print(f"Error setting department/position: {e}")
        
        id_parts = employee_data["employee_id"].split("-")
        if len(id_parts) == 3:
            self.admin_ui.edit_employee_id_pref.setText(id_parts[0])
            try:
                index = self.admin_ui.edit_employee_id_year.findText(id_parts[1])
                if index >= 0:
                    self.admin_ui.edit_employee_id_year.setCurrentIndex(index)
            except Exception as e:
                print(f"Error setting ID year: {e}")
            try:
                index = self.admin_ui.edit_employee_id_no.findText(id_parts[2])
                if index >= 0:
                    self.admin_ui.edit_employee_id_no.setCurrentIndex(index)
            except Exception as e:
                print(f"Error setting ID number: {e}")
        
        self.admin_ui.edit_employee_password.setText(employee_data["password"])
        self.admin_ui.edit_employee_confirm_password.setText(employee_data["password"])
        
        if employee_data["schedule"] == "6am to 2pm":
            self.admin_ui.edit_employee_sched_1.setChecked(True)
        elif employee_data["schedule"] == "2pm to 10pm":
            self.admin_ui.edit_employee_sched_2.setChecked(True)
        else:  # 10pm to 6am
            self.admin_ui.edit_employee_sched_3.setChecked(True)
        
        status = "Active"
        if self.selected_employee_type == "employee":
            row = self.selected_employee_index
            status_item = self.admin_ui.employee_list_tbl.item(row, 3)
            if status_item:
                status = status_item.text()
        else:
            row = self.selected_employee_index
            status_item = self.admin_ui.hr_list_tbl.item(row, 2)
            if status_item:
                status = status_item.text()
        
        if status == "Active":
            self.admin_ui.employee_edit_deactivate.setText("Deactivate")
        else:
            self.admin_ui.employee_edit_deactivate.setText("Activate")

    def toggle_edit_hr_fields(self):
        try:
            self.admin_ui.edit_is_hr_yes.toggled.connect(self.toggle_edit_hr_fields)
            self.admin_ui.edit_is_hr_no.toggled.connect(self.toggle_edit_hr_fields)
        except:
            pass
        
        is_hr = self.admin_ui.edit_is_hr_yes.isChecked()
        self.admin_ui.edit_employee_department_box.setDisabled(is_hr)
        self.admin_ui.edit_employee_position_box.setDisabled(is_hr)
        
        if is_hr:
            self.admin_ui.edit_employee_department_box.setCurrentText("Human Resources")
            self.admin_ui.edit_employee_position_box.setCurrentText("HR Staff")

    def validate_edited_employee_data(self):
        first_name = self.admin_ui.edit_employee_first_name.text().strip()
        last_name = self.admin_ui.edit_employee_last_name.text().strip()
        mi = self.admin_ui.edit_employee_mi.text().strip()
        id_pref = self.admin_ui.edit_employee_id_pref.text().strip()
        id_year = self.admin_ui.edit_employee_id_year.currentText()
        id_no = self.admin_ui.edit_employee_id_no.currentText()
        password = self.admin_ui.edit_employee_password.text()
        confirm_password = self.admin_ui.edit_employee_confirm_password.text()
        
        gender = None
        if self.admin_ui.edit_employee_male.isChecked():
            gender = "Male"
        elif self.admin_ui.edit_employee_female.isChecked():
            gender = "Female"
        
        is_hr = self.admin_ui.edit_is_hr_yes.isChecked()
        
        department = self.admin_ui.edit_employee_department_box.currentText()
        position = self.admin_ui.edit_employee_position_box.currentText()
        if is_hr:
            department = "Human Resources"
            position = "HR Staff"
        
        schedule = None
        if self.admin_ui.edit_employee_sched_1.isChecked():
            schedule = "6am to 2pm"
        elif self.admin_ui.edit_employee_sched_2.isChecked():
            schedule = "2pm to 10pm"
        elif self.admin_ui.edit_employee_sched_3.isChecked():
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
        
        status = "Active"
        if self.selected_employee_type == "employee" and self.selected_employee_index is not None:
            status_item = self.admin_ui.employee_list_tbl.item(self.selected_employee_index, 3)
            if status_item:
                status = status_item.text()
        elif self.selected_employee_type == "hr" and self.selected_employee_index is not None:
            status_item = self.admin_ui.hr_list_tbl.item(self.selected_employee_index, 2)
            if status_item:
                status = status_item.text()
        
        employee_data = {
            "first_name": first_name,
            "last_name": last_name,
            "middle_initial": mi,
            "employee_id": f"{id_pref}-{id_year}-{id_no}",
            "password": password,
            "gender": gender,
            "birthday": self.admin_ui.edit_employee_birthday_edit.date().toString("yyyy-MM-dd"),
            "department": department,
            "position": position,
            "schedule": schedule,
            "is_hr": is_hr,
            "status": status
        }
        
        return True, employee_data

    def save_edited_employee(self):
        if self.selected_employee_index is None or self.selected_employee_type is None:
            error_msg = QMessageBox()
            error_msg.setIcon(QMessageBox.Critical)
            error_msg.setText("Edit Error")
            error_msg.setInformativeText("No employee selected for editing.")
            error_msg.setWindowTitle("Edit Error")
            error_msg.exec()
            return
        
        valid, result = self.validate_edited_employee_data()
        if not valid:
            error_msg = QMessageBox()
            error_msg.setIcon(QMessageBox.Critical)
            error_msg.setText("Validation Error")
            error_msg.setInformativeText(result)
            error_msg.setWindowTitle("Edit Error")
            error_msg.exec()
            return
        
        current_type = self.selected_employee_type
        new_type = "hr" if result["is_hr"] else "employee"
        index = self.selected_employee_index
        
        if current_type != new_type:
            if current_type == "employee":
                employee_data = self.employees.pop(index)
                if not hasattr(self, 'hr_employees'):
                    self.hr_employees = []
                self.hr_employees.append(result)
            else:
                employee_data = self.hr_employees.pop(index)
                if not hasattr(self, 'employees'):
                    self.employees = []
                self.employees.append(result)
        else:
            if current_type == "employee":
                self.employees[index] = result
            else:  # HR
                self.hr_employees[index] = result
        
        self.load_employee_table()
        self.load_hr_table()

        success_msg = QMessageBox()
        success_msg.setIcon(QMessageBox.Information)
        success_msg.setText("Employee Updated")
        success_msg.setInformativeText(f"Employee {result['first_name']} {result['last_name']} has been updated.")
        success_msg.setWindowTitle("Edit Success")
        success_msg.exec()

        self.goto_employee_hr()

    def toggle_hr_fields(self):
        is_hr = self.admin_ui.is_hr_yes.isChecked()
        self.admin_ui.employee_department_box.setDisabled(is_hr)
        self.admin_ui.employee_position_box.setDisabled(is_hr)
        if is_hr:
            self.admin_ui.employee_department_box.setCurrentText("Human Resources")
            self.admin_ui.employee_position_box.setCurrentText("HR Staff")

    def toggle_employee_status(self):
        if self.selected_employee_index is None or self.selected_employee_type is None:
            error_msg = QMessageBox()
            error_msg.setIcon(QMessageBox.Critical)
            error_msg.setText("Status Update Error")
            error_msg.setInformativeText("No employee selected.")
            error_msg.setWindowTitle("Status Error")
            error_msg.exec()
            return
        
        current_status = "Active"
        if self.selected_employee_type == "employee":
            status_item = self.admin_ui.employee_list_tbl.item(self.selected_employee_index, 3)
            if status_item:
                current_status = status_item.text()
            
            new_status = "Inactive" if current_status == "Active" else "Active"
            self.employees[self.selected_employee_index]["status"] = new_status
            status_item.setText(new_status)
            
        else:
            status_item = self.admin_ui.hr_list_tbl.item(self.selected_employee_index, 2)
            if status_item:
                current_status = status_item.text()

            new_status = "Inactive" if current_status == "Active" else "Active"
            self.hr_employees[self.selected_employee_index]["status"] = new_status
            status_item.setText(new_status)
        
        if new_status == "Active":
            self.admin_ui.employee_edit_deactivate.setText("Deactivate")
        else:
            self.admin_ui.employee_edit_deactivate.setText("Activate")
        
        action = "activated" if new_status == "Active" else "deactivated"
        
        employee_name = ""
        if self.selected_employee_type == "employee":
            employee = self.employees[self.selected_employee_index]
            employee_name = f"{employee['first_name']} {employee['last_name']}"
        else:
            employee = self.hr_employees[self.selected_employee_index]
            employee_name = f"{employee['first_name']} {employee['last_name']}"
        
        success_msg = QMessageBox()
        success_msg.setIcon(QMessageBox.Information)
        success_msg.setText("Status Updated")
        success_msg.setInformativeText(f"Employee {employee_name} has been {action}.")
        success_msg.setWindowTitle("Status Update")
        success_msg.exec()

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
        
        is_hr = self.admin_ui.is_hr_yes.isChecked()
        
        department = self.admin_ui.employee_department_box.currentText()
        position = self.admin_ui.employee_position_box.currentText()
        
        if is_hr:
            department = "Human Resources"
            position = "HR Staff"
        
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
            "schedule": schedule,
            "is_hr": is_hr,
            "status": "Active"
        }
        
        return True, employee_data

    def load_employee_table(self):
        self.admin_ui.employee_list_tbl.setRowCount(0)

        if hasattr(self, 'employees') and self.employees:
            for employee in self.employees:
                if not employee.get('is_hr', False):  # Only regular employees
                    self.add_employee_to_table(employee)
        
        # Apply current sort if a sort option is selected
        if self.admin_ui.employee_sort_box.currentIndex() > 0:  # If not the default option
            self.sort_employee_table()
        
        # Apply current filter if there is search text
        if self.admin_ui.employee_search_box.text():
            self.filter_employee_table()

    def load_hr_table(self):
        self.admin_ui.hr_list_tbl.setRowCount(0)

        if hasattr(self, 'hr_employees') and self.hr_employees:
            for hr_employee in self.hr_employees:
                self.add_hr_to_table(hr_employee)
        
        # Apply current sort if a sort option is selected
        if self.admin_ui.hr_sort_box.currentIndex() > 0:  # If not the default option
            self.sort_hr_table()
        
        # Apply current filter if there is search text
        if self.admin_ui.hr_search_box.text():
            self.filter_hr_table()

    def add_employee_to_table(self, employee_data):
        row_position = self.admin_ui.employee_list_tbl.rowCount()
        self.admin_ui.employee_list_tbl.insertRow(row_position)
        middle_initial = f" {employee_data['middle_initial']}." if employee_data['middle_initial'] else ""
        full_name = f"{employee_data['last_name']}, {employee_data['first_name']}{middle_initial}"
        dept_pos = f"{employee_data['department']} / {employee_data['position']}"
        
        name_item = QTableWidgetItem(full_name)
        id_item = QTableWidgetItem(employee_data['employee_id'])
        dept_pos_item = QTableWidgetItem(dept_pos)
        status_item = QTableWidgetItem(employee_data.get('status', 'Active'))  # Get status or default to Active
        
        name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
        id_item.setFlags(id_item.flags() & ~Qt.ItemIsEditable)
        dept_pos_item.setFlags(dept_pos_item.flags() & ~Qt.ItemIsEditable)
        status_item.setFlags(status_item.flags() & ~Qt.ItemIsEditable)
        
        self.admin_ui.employee_list_tbl.setItem(row_position, 0, name_item)
        self.admin_ui.employee_list_tbl.setItem(row_position, 1, id_item)
        self.admin_ui.employee_list_tbl.setItem(row_position, 2, dept_pos_item)
        self.admin_ui.employee_list_tbl.setItem(row_position, 3, status_item)
        
        self.admin_ui.employee_list_tbl.resizeColumnsToContents()

    def add_hr_to_table(self, hr_data):
        row_position = self.admin_ui.hr_list_tbl.rowCount()
        self.admin_ui.hr_list_tbl.insertRow(row_position)
        middle_initial = f" {hr_data['middle_initial']}." if hr_data['middle_initial'] else ""
        full_name = f"{hr_data['last_name']}, {hr_data['first_name']}{middle_initial}"
        
        name_item = QTableWidgetItem(full_name)
        id_item = QTableWidgetItem(hr_data['employee_id'])
        status_item = QTableWidgetItem(hr_data.get('status', 'Active'))  # Get status or default to Active
        
        name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
        id_item.setFlags(id_item.flags() & ~Qt.ItemIsEditable)
        status_item.setFlags(status_item.flags() & ~Qt.ItemIsEditable)
        
        self.admin_ui.hr_list_tbl.setItem(row_position, 0, name_item)
        self.admin_ui.hr_list_tbl.setItem(row_position, 1, id_item)
        self.admin_ui.hr_list_tbl.setItem(row_position, 2, status_item)
        
        self.admin_ui.hr_list_tbl.resizeColumnsToContents()

    def save_employee_data(self, employee_data):
        is_hr = employee_data.get('is_hr', False)
        
        if is_hr:
            if not hasattr(self, 'hr_employees'):
                self.hr_employees = []
            self.hr_employees.append(employee_data)
            
            print("Saving HR employee data:")
            for key, value in employee_data.items():
                print(f"{key}: {value}")
                
            if self.admin_ui.admin_employee_sc_pages.currentWidget() == self.admin_ui.employee_hr_page:
                self.add_hr_to_table(employee_data)
        else:
            if not hasattr(self, 'employees'):
                self.employees = []
            self.employees.append(employee_data)
            
            print("Saving regular employee data:")
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
                employee_type = "HR Employee" if self.current_employee_data.get('is_hr', False) else "Employee"
                success_msg.setInformativeText(f"{employee_type} {self.current_employee_data['first_name']} {self.current_employee_data['last_name']} has been enrolled.")
                success_msg.setWindowTitle("Enrollment Success")
                success_msg.exec()
                self.goto_employee_hr()
                self.load_employee_table()
                self.load_hr_table()
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