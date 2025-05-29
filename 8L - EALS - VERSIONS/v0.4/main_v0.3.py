import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QWidget, QStackedWidget, QTabWidget, QMessageBox, QTableWidgetItem, QAbstractItemView, QFileDialog, QLineEdit
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QPixmap
from datetime import datetime
import sqlite3
import threading
import os
import shutil

class DatabaseConnection:
    def __init__(self, db_name="eals_database.db"):
        self.db_name = db_name
        self.connection = None
        self.lock = threading.Lock()

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_name, check_same_thread=False)
            self.create_tables()
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")

    def create_tables(self):
        try:
            with self.lock:
                cursor = self.connection.cursor()
                cursor.executescript('''
                CREATE TABLE IF NOT EXISTS Admin (
                    admin_id VARCHAR(20) PRIMARY KEY,
                    password VARCHAR(255) NOT NULL,
                    password_changed BOOLEAN DEFAULT FALSE
                );

                CREATE TABLE IF NOT EXISTS Employee (
                    employee_id VARCHAR(20) PRIMARY KEY,
                    first_name VARCHAR(50) NOT NULL,
                    last_name VARCHAR(50) NOT NULL,
                    middle_initial CHAR(1),
                    birthday DATE NOT NULL,
                    gender VARCHAR(10) NOT NULL,
                    department VARCHAR(50) NOT NULL,
                    position VARCHAR(50) NOT NULL,
                    schedule VARCHAR(20) NOT NULL,
                    is_hr BOOLEAN DEFAULT FALSE,
                    status VARCHAR(10) DEFAULT 'Active',
                    password VARCHAR(255) NOT NULL,
                    profile_picture VARCHAR(255) NOT NULL
                );

                CREATE TABLE IF NOT EXISTS attendance_logs (
                    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    employee_id VARCHAR(20) NOT NULL,
                    date DATE NOT NULL,
                    time TIME NOT NULL,
                    remarks VARCHAR(10) NOT NULL,
                    FOREIGN KEY (employee_id) REFERENCES Employee(employee_id)
                );

                CREATE TABLE IF NOT EXISTS system_setting (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    backup_config INTEGER DEFAULT 2,
                    automatic_backup_config INTEGER DEFAULT 1,
                    archive_config INTEGER DEFAULT 1
                );

                CREATE TABLE IF NOT EXISTS system_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    path TEXT NOT NULL,
                    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );

                INSERT OR IGNORE INTO system_setting (id) VALUES (1);
                INSERT OR IGNORE INTO Admin (admin_id, password, password_changed) 
                VALUES ('admin-01-0001', 'defaultpassword', FALSE);
                ''')
                self.connection.commit()
                
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")

    def execute_query(self, query, params=()):
        try:
            with self.lock:
                cursor = self.connection.cursor()
                cursor.execute(query, params)
                self.connection.commit()
                return cursor
        except sqlite3.Error as e:
            print(f"Database query error: {e}")
            return None

    def close(self):
        if self.connection:
            self.connection.close()


class SystemLogs:
    def __init__(self, db):
        self.db = db

    def log_system_action(self, action):
        try:
            log_dir = "resources/logs"
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)

            log_file = os.path.join(log_dir, f"{datetime.now().strftime('%Y%m%d')}.txt")
            with open(log_file, "a") as file:
                file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {action}\n")

            # Check if the log file path already exists in the database
            cursor = self.db.execute_query("SELECT id FROM system_logs WHERE path = ?", (log_file,))
            if not cursor.fetchone():
                self.db.execute_query('''
                    INSERT INTO system_logs (path)
                    VALUES (?)
                ''', (log_file,))
        except Exception as e:
            print(f"Error logging system action: {e}")

class EALS:
    def __init__(self):
        self.db = DatabaseConnection()
        self.db.connect()
        self.home = Home(self.db)
        global global_home_ui
        global_home_ui = self.home.home_ui
        global_home_ui.showMaximized()

    def __del__(self):
        self.db.close()

    def goto_admin_ui(self):
        global_home_ui.close()
        self.admin = Admin(self.db)
        self.admin.admin_ui.showMaximized()

class HR:
    def __init__(self, db, hr_data):
        self.db = db
        self.system_logs = SystemLogs(db)
        self.hr_data = hr_data
        self.loader = QUiLoader()
        self.hr_ui = self.loader.load("hr.ui")
        self.hr_ui.hr_employee_sc_pages.setCurrentWidget(self.hr_ui.hr_employee_dashboard_page)
        self.hr_ui.hr_employee_tbl.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.hr_ui.hr_employee_tbl.setSelectionMode(QAbstractItemView.SingleSelection)
        self.hr_ui.hr_employee_search_box.textChanged.connect(self.filter_hr_employee_table)
        self.hr_ui.hr_employee_sort_box.currentIndexChanged.connect(self.sort_hr_employee_table)
        self.hr_ui.hr_employee_view_back.clicked.connect(self.goto_hr_dashboard)
        self.hr_ui.hr_logout_btn.clicked.connect(self.handle_logout)
        self.hr_ui.hr_employee_view_btn.clicked.connect(self.goto_hr_employee_view)

        self.hr_ui.hr_attedance_logs_tbl.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.hr_ui.hr_attedance_logs_tbl.setSelectionMode(QAbstractItemView.SingleSelection)

        self.hr_ui.hr_attedance_logs_search.textChanged.connect(self.filter_hr_attendance_logs_table)
        self.hr_ui.hr_attedance_logs_sort.currentIndexChanged.connect(self.sort_hr_attendance_logs_table)

        self.hr_ui.hr_employee_logs_tbl.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.hr_ui.hr_employee_logs_tbl.setSelectionMode(QAbstractItemView.SingleSelection)

        self.hr_employees = []
        self.load_hr_employee_table()
        self.load_hr_attendance_logs_table()
        self.update_date_today()


    def update_hr_dashboard_labels(self):
        try:
            cursor = self.db.execute_query("SELECT COUNT(*) FROM Employee")
            total_employees = cursor.fetchone()[0] if cursor else 0

            cursor = self.db.execute_query("SELECT COUNT(*) FROM Employee WHERE status = 'Active'")
            active_employees = cursor.fetchone()[0] if cursor else 0

            today_date = datetime.now().strftime("%Y-%m-%d")
            cursor = self.db.execute_query(
                "SELECT COUNT(DISTINCT employee_id) FROM attendance_logs "
                "WHERE date = ? AND employee_id IN (SELECT employee_id FROM Employee WHERE is_hr = 0)", 
                (today_date,)
            )
            logged_employees = cursor.fetchone()[0] if cursor else 0

            cursor = self.db.execute_query(
                "SELECT COUNT(DISTINCT employee_id) FROM attendance_logs "
                "WHERE date = ? AND remarks = 'late' AND employee_id IN (SELECT employee_id FROM Employee WHERE is_hr = 0)", 
                (today_date,)
            )
            late_employees = cursor.fetchone()[0] if cursor else 0

            cursor = self.db.execute_query(
                "SELECT COUNT(*) FROM Employee WHERE is_hr = 0 AND status = 'Active' AND employee_id NOT IN ("
                "SELECT DISTINCT employee_id FROM attendance_logs WHERE date = ?)", 
                (today_date,)
            )
            absent_employees = cursor.fetchone()[0] if cursor else 0

            self.hr_ui.hr_total_employee_lbl.setText(f"{total_employees}/{total_employees}")
            self.hr_ui.hr_active_employee_lbl.setText(str(active_employees))
            self.hr_ui.hr_logged_employee_lbl.setText(str(logged_employees))
            self.hr_ui.hr_late_employee_lbl.setText(str(late_employees))
            self.hr_ui.hr_absent_employee_lbl.setText(str(absent_employees))

        except sqlite3.Error as e:
            print(f"Database error while updating HR dashboard labels: {e}")

    def update_date_today(self):
        current_date = datetime.now()
        formatted_date = current_date.strftime("%a, %b %d, %Y")
        self.hr_ui.date_today.setText(formatted_date)

    def load_hr_employee_table(self):
        self.system_logs.log_system_action("Load employees into the HR employee table.")
        try:
            cursor = self.db.execute_query("SELECT * FROM Employee WHERE is_hr = 0")
            employees = cursor.fetchall() if cursor else []

            self.hr_employees = []
            self.hr_ui.hr_employee_tbl.setRowCount(0)
            for employee in employees:
                employee_data = {
                    "employee_id": employee[0],
                    "first_name": employee[1],
                    "last_name": employee[2],
                    "middle_initial": employee[3],
                    "department": employee[6],
                    "position": employee[7],
                    "status": employee[10]
                }
                self.hr_employees.append(employee_data)
                self.add_hr_employee_to_table(employee_data)
                self.update_hr_dashboard_labels()
        except sqlite3.Error as e:
            self.system_logs.log_system_action(f"Database error while loading HR employees: {e}")

    def add_hr_employee_to_table(self, employee_data):
        row_position = self.hr_ui.hr_employee_tbl.rowCount()
        self.hr_ui.hr_employee_tbl.insertRow(row_position)
        middle_initial = f" {employee_data['middle_initial']}." if employee_data['middle_initial'] else ""
        full_name = f"{employee_data['last_name']}, {employee_data['first_name']}{middle_initial}"
        dept_pos = f"{employee_data['department']} / {employee_data['position']}"

        name_item = QTableWidgetItem(full_name)
        dept_pos_item = QTableWidgetItem(dept_pos)
        status_item = QTableWidgetItem(employee_data.get('status', 'Active'))

        name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
        dept_pos_item.setFlags(dept_pos_item.flags() & ~Qt.ItemIsEditable)
        status_item.setFlags(status_item.flags() & ~Qt.ItemIsEditable)

        self.hr_ui.hr_employee_tbl.setItem(row_position, 0, name_item)
        self.hr_ui.hr_employee_tbl.setItem(row_position, 1, dept_pos_item)
        self.hr_ui.hr_employee_tbl.setItem(row_position, 2, status_item)

        self.hr_ui.hr_employee_tbl.resizeColumnsToContents()

    def filter_hr_employee_table(self):
        search_text = self.hr_ui.hr_employee_search_box.text().lower()
        for row in range(self.hr_ui.hr_employee_tbl.rowCount()):
            self.hr_ui.hr_employee_tbl.setRowHidden(row, False)

        if not search_text:
            return

        for row in range(self.hr_ui.hr_employee_tbl.rowCount()):
            match_found = False
            for col in range(self.hr_ui.hr_employee_tbl.columnCount()):
                item = self.hr_ui.hr_employee_tbl.item(row, col)
                if item and search_text in item.text().lower():
                    match_found = True
                    break
            self.hr_ui.hr_employee_tbl.setRowHidden(row, not match_found)

    def sort_hr_employee_table(self):
        sort_option = self.hr_ui.hr_employee_sort_box.currentText()
        if sort_option == "By Name:":
            self.hr_employees.sort(key=lambda x: (x["last_name"].lower(), x["first_name"].lower()))
        elif sort_option == "By Department:":
            self.hr_employees.sort(key=lambda x: x["department"].lower())
        elif sort_option == "By Position:":
            self.hr_employees.sort(key=lambda x: x["department"].lower())
        elif sort_option == "By Status:":
            self.hr_employees.sort(key=lambda x: 0 if x["status"].lower() == "active" else 1)

        self.hr_ui.hr_employee_tbl.setRowCount(0)
        for employee_data in self.hr_employees:
            self.add_hr_employee_to_table(employee_data)

    def goto_hr_employee_view(self):
        self.system_logs.log_system_action("The HR, has selected an employee to view.")
        if selected := self.hr_ui.hr_employee_tbl.selectedIndexes():
            row = selected[0].row()
            employee_data = self.hr_employees[row]
            self.display_hr_employee_view(employee_data)
            view_page = self.hr_ui.hr_employee_view_page
            page_index = self.hr_ui.hr_employee_sc_pages.indexOf(view_page)
            self.hr_ui.hr_employee_sc_pages.setCurrentIndex(page_index)

    def display_hr_employee_view(self, employee_data):
        self.hr_ui.hr_view_employee_first_name.setText(employee_data["first_name"])
        self.hr_ui.hr_view_employee_last_name.setText(employee_data["last_name"])
        self.hr_ui.hr_view_employee_mi.setText(employee_data["middle_initial"])
        self.hr_ui.hr_view_employee_department_box.setText(employee_data["department"])
        self.hr_ui.hr_view_employee_position_box.setText(employee_data["position"])
        self.hr_ui.hr_view_employee_accountid.setText(employee_data["employee_id"])
        self.load_hr_employee_attendance_logs(employee_data["employee_id"])

    def goto_hr_dashboard(self):
        self.system_logs.log_system_action("Going back to the HR Employee dashboard.")
        dashboard_page = self.hr_ui.hr_employee_sc_pages.indexOf(self.hr_ui.hr_employee_dashboard_page)
        self.hr_ui.hr_employee_sc_pages.setCurrentIndex(dashboard_page)

    def handle_logout(self):
        current_time = datetime.now()
        current_date = current_time.strftime("%Y-%m-%d")
        self.db.execute_query("INSERT INTO attendance_logs (employee_id, date, time, remarks) VALUES (?, ?, ?, ?)",
                              (self.hr_data["employee_id"], current_date, current_time.strftime("%H:%M:%S"), "out"))
        self.hr_ui.close()
        global_home_ui.showMaximized()
        self.system_logs.log_system_action("The HR logged out.")

    def load_hr_attendance_logs_table(self):
        self.system_logs.log_system_action("Load all attendance logs for employees only into the table.")
        try:
            cursor = self.db.execute_query(
                "SELECT employee_id, remarks, date, time FROM attendance_logs WHERE employee_id IN (SELECT employee_id FROM Employee WHERE is_hr = 0)"
            )
            logs = cursor.fetchall() if cursor else []

            self.hr_ui.hr_attedance_logs_tbl.setRowCount(0)
            for log in logs:
                self.add_attendance_log_to_table(self.hr_ui.hr_attedance_logs_tbl, log)
        except sqlite3.Error as e:
            self.system_logs.log_system_action(f"Database error while loading HR attendance logs: {e}")
            print(f"Database error while loading HR attendance logs: {e}")

    def add_attendance_log_to_table(self, table, log):
        """Add a single attendance log to the specified table."""
        row_position = table.rowCount()
        table.insertRow(row_position)

        account_id_item = QTableWidgetItem(log[0])
        remarks_item = QTableWidgetItem(log[1])
        date_item = QTableWidgetItem(log[2])
        time_item = QTableWidgetItem(log[3])

        account_id_item.setFlags(account_id_item.flags() & ~Qt.ItemIsEditable)
        remarks_item.setFlags(remarks_item.flags() & ~Qt.ItemIsEditable)
        date_item.setFlags(date_item.flags() & ~Qt.ItemIsEditable)
        time_item.setFlags(time_item.flags() & ~Qt.ItemIsEditable)

        table.setItem(row_position, 0, account_id_item)
        table.setItem(row_position, 1, remarks_item)
        table.setItem(row_position, 2, date_item)
        table.setItem(row_position, 3, time_item)

        table.resizeColumnsToContents()

    def filter_hr_attendance_logs_table(self):
        """Filter HR attendance logs based on the search bar input."""
        search_text = self.hr_ui.hr_attedance_logs_search.text().lower()
        for row in range(self.hr_ui.hr_attedance_logs_tbl.rowCount()):
            self.hr_ui.hr_attedance_logs_tbl.setRowHidden(row, False)

        if not search_text:
            return

        for row in range(self.hr_ui.hr_attedance_logs_tbl.rowCount()):
            match_found = False
            for col in range(self.hr_ui.hr_attedance_logs_tbl.columnCount()):
                item = self.hr_ui.hr_attedance_logs_tbl.item(row, col)
                if item and search_text in item.text().lower():
                    match_found = True
                    break
            self.hr_ui.hr_attedance_logs_tbl.setRowHidden(row, not match_found)

    def sort_hr_attendance_logs_table(self):
        """Sort HR attendance logs based on the selected sort option."""
        sort_option = self.hr_ui.hr_attedance_logs_sort.currentText()

        logs = []
        for row in range(self.hr_ui.hr_attedance_logs_tbl.rowCount()):
            log = [
                self.hr_ui.hr_attedance_logs_tbl.item(row, col).text()
                for col in range(self.hr_ui.hr_attedance_logs_tbl.columnCount())
            ]
            logs.append(log)

        if sort_option == "By Date:":
            logs.sort(key=lambda x: x[2])  # Sort by Date
        elif sort_option == "By Time:":
            logs.sort(key=lambda x: x[3])  # Sort by Time
        elif sort_option == "By Account ID:":
            logs.sort(key=lambda x: x[0])  # Sort by Account ID
        elif sort_option == "By Remarks:":
            logs.sort(key=lambda x: x[1])  # Sort by Remarks

        self.hr_ui.hr_attedance_logs_tbl.setRowCount(0)
        for log in logs:
            self.add_attendance_log_to_table(self.hr_ui.hr_attedance_logs_tbl, log)

    def load_hr_employee_attendance_logs(self, employee_id):
        self.system_logs.log_system_action("Load attendance logs for the selected employee.")
        try:
            cursor = self.db.execute_query(
                "SELECT date, time, remarks FROM attendance_logs WHERE employee_id = ?", (employee_id,)
            )
            logs = cursor.fetchall() if cursor else []

            self.hr_ui.hr_employee_logs_tbl.setRowCount(0)
            for log in logs:
                self.add_log_to_table(self.hr_ui.hr_employee_logs_tbl, log)
        except sqlite3.Error as e:
            self.system_logs.log_system_action(f"Database error while loading HR employee attendance logs: {e}")
            print(f"Database error while loading HR employee attendance logs: {e}")

    def add_log_to_table(self, table, log):
        """Add a single log entry to the specified table."""
        row_position = table.rowCount()
        table.insertRow(row_position)

        date_item = QTableWidgetItem(log[0])
        time_item = QTableWidgetItem(log[1])
        remarks_item = QTableWidgetItem(log[2])

        date_item.setFlags(date_item.flags() & ~Qt.ItemIsEditable)
        time_item.setFlags(time_item.flags() & ~Qt.ItemIsEditable)
        remarks_item.setFlags(remarks_item.flags() & ~Qt.ItemIsEditable)

        table.setItem(row_position, 0, date_item)
        table.setItem(row_position, 1, time_item)
        table.setItem(row_position, 2, remarks_item)

        table.resizeColumnsToContents()

class Home:
    admin_password = "defaultpassword"
    password_changed = False
    
    def __init__(self, db):
        self.db = db
        self.system_logs = SystemLogs(db)
        self.loader = QUiLoader()
        self.home_ui = self.loader.load("home.ui")
        self.home_ui.main_page.setCurrentWidget(self.home_ui.home_page)
        self.admin_id = "admin-01-0001"
        self.update_date_today()
        self.home_ui.home_login_btn.clicked.connect(self.handle_login)
        self.home_ui.bio1_next.clicked.connect(self.goto_bio2)
        self.home_ui.bio2_next.clicked.connect(self.goto_result_prompt)
        self.employee_data = None  # Store logged-in employee data
        self.system_logs.log_system_action("The home UI has been loaded.")
        self.home_ui.pass_visibility_button.clicked.connect(self.toggle_password_visibility)
        self.password_visible = False
    
    def update_date_today(self):
        current_date = datetime.now()
        formatted_date = current_date.strftime("%a, %b %d, %Y")
        self.home_ui.date_today.setText(formatted_date)
        self.system_logs.log_system_action("Setting current date to the home UI.")

    def handle_login(self):
        user_id = self.home_ui.home_id_box.text()
        password = self.home_ui.home_pass_box.text()

        try:
            # Check if the user is an admin
            cursor = self.db.execute_query("SELECT password, password_changed FROM Admin WHERE admin_id = ?", (user_id,))
            admin_result = cursor.fetchone() if cursor else None

            if admin_result:
                db_password, password_changed = admin_result
                if password == db_password:
                    Home.password_changed = password_changed
                    if password_changed:
                        self.system_logs.log_system_action("The password is already changed, going to the admin UI.")
                        self.goto_admin_ui()
                    else:
                        self.system_logs.log_system_action("The password is not changed executing Change Password Prompt")
                        self.goto_change_pass()
                    return
                else:
                    self.show_error("Invalid credentials", "Please enter valid admin ID and password")
                    self.system_logs.log_system_action("An invalid Admin loggin attempt has been made.")
                    return

            # Check if the user is an employee
            cursor = self.db.execute_query("SELECT * FROM Employee WHERE employee_id = ? AND password = ?", (user_id, password))
            employee_result = cursor.fetchone() if cursor else None

            if employee_result:
                employee_data = {
                    "employee_id": employee_result[0],
                    "first_name": employee_result[1],
                    "last_name": employee_result[2],
                    "middle_initial": employee_result[3],
                    "birthday": employee_result[4],
                    "gender": employee_result[5],
                    "department": employee_result[6],
                    "position": employee_result[7],
                    "schedule": employee_result[8],
                    "is_hr": employee_result[9],
                    "profile_picture": employee_result[12]
                }
                if employee_data["is_hr"]:
                    self.goto_hr_ui(employee_data)
                    self.system_logs.log_system_action("A user is logged in as HR")
                    
                else:
                    self.employee_data = employee_data
                    if self.validate_attendance():
                        self.system_logs.log_system_action("A user is logged in as an employee")
                        self.goto_bio1()
            else:
                self.show_error("Invalid credentials", "Please enter valid employee ID and password")
                self.system_logs.log_system_action("An invalid loggin attempt has been made.")
        except sqlite3.Error as e:
            print(f"Database error during login: {e}")

    def validate_attendance(self):
        """Validate if the attendance log is valid based on schedule and previous logs."""
        if not self.employee_data:
            return False

        current_time = datetime.now()
        current_date = current_time.strftime("%Y-%m-%d")
        current_hour = current_time.hour

        # Check if the employee is logging in or out
        cursor = self.db.execute_query("SELECT time, remarks FROM attendance_logs WHERE employee_id = ? AND date = ?", 
                                       (self.employee_data["employee_id"], current_date))
        attendance = cursor.fetchone() if cursor else None

        if attendance:
            # Check if logging out is valid
            log_time = datetime.strptime(attendance[0], "%H:%M:%S")
            if attendance[1] == "in" and (current_time - log_time).total_seconds() < 8 * 3600:
                self.show_error("Invalid Logout", "You cannot log out less than 8 hours after logging in.")
                return False
            self.employee_data["remarks"] = "out"
        else:
            # Check if logging in is within schedule
            schedule_start, schedule_end = self.parse_schedule(self.employee_data["schedule"])
            if not self.is_within_schedule(schedule_start, schedule_end, current_hour):
                self.show_error("Invalid Login", "You cannot log in outside your scheduled shift.")
                return False
            self.employee_data["remarks"] = "in"

        return True

    def goto_hr_ui(self, hr_data):

        current_time = datetime.now()
        current_date = current_time.strftime("%Y-%m-%d")
        self.db.execute_query("INSERT INTO attendance_logs (employee_id, date, time, remarks) VALUES (?, ?, ?, ?)",
                              (hr_data["employee_id"], current_date, current_time.strftime("%H:%M:%S"), hr_data.get("remarks", "in")))
        global_home_ui.close()
        self.hr = HR(self.db, hr_data)
        self.hr.hr_ui.showMaximized()

    def goto_bio1(self):
        if self.employee_data:
            self.home_ui.bio1_employee_pic.setFixedSize(900, 600)
            self.home_ui.bio1_employee_pic.setPixmap(QPixmap(self.employee_data["profile_picture"]).scaled(
                self.home_ui.bio1_employee_pic.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.home_ui.bio1_employee_name.setText(f"<b>Name:</b> {self.employee_data['first_name']} {self.employee_data['last_name']}")
            self.home_ui.bio1_employee_department.setText(f"<b>Department:</b> {self.employee_data['department']}")
            self.home_ui.bio1_employee_position.setText(f"<b>Position:</b> {self.employee_data['position']}")
            self.home_ui.bio1_employee_shift.setText(f"<b>Shift:</b> {self.employee_data['schedule']}")

        bio1_page = self.home_ui.main_page.indexOf(self.home_ui.bio1_page)
        self.home_ui.main_page.setCurrentIndex(bio1_page)

    def goto_bio2(self):
        if self.employee_data:
            self.home_ui.bio2_employee_pic.setFixedSize(900, 600)
            self.home_ui.bio2_employee_pic.setPixmap(QPixmap(self.employee_data["profile_picture"]).scaled(
                self.home_ui.bio2_employee_pic.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.home_ui.bio2_employee_name.setText(f"<b>Name:</b> {self.employee_data['first_name']} {self.employee_data['last_name']}")
            self.home_ui.bio2_employee_department.setText(f"<b>Department:</b> {self.employee_data['department']}")
            self.home_ui.bio2_employee_position.setText(f"<b>Position:</b> {self.employee_data['position']}")
            self.home_ui.bio2_employee_shift.setText(f"<b>Shift:</b> {self.employee_data['schedule']}")

        bio2_page = self.home_ui.main_page.indexOf(self.home_ui.bio2_page)
        self.home_ui.main_page.setCurrentIndex(bio2_page)

    def goto_result_prompt(self):
        """Display the result of user authentication and log the action."""
        if self.employee_data:
            current_time = datetime.now()
            current_date = current_time.strftime("%Y-%m-%d")

            # Log attendance
            self.system_logs.log_system_action("A user logged.")
            self.db.execute_query("INSERT INTO attendance_logs (employee_id, date, time, remarks) VALUES (?, ?, ?, ?)", 
                                  (self.employee_data["employee_id"], current_date, current_time.strftime("%H:%M:%S"), self.employee_data.get("remarks", "in")))

        result_prompt = self.home_ui.main_page.indexOf(self.home_ui.result_page)
        self.home_ui.main_page.setCurrentIndex(result_prompt)

        # Return to home page after 5 seconds
        threading.Timer(2.0, lambda: self.home_ui.main_page.setCurrentWidget(self.home_ui.home_page)).start()

    def parse_schedule(self, schedule):
        """Parse schedule string like '10pm to 6am' into start and end hours."""
        try:
            start, end = schedule.lower().split(" to ")
            start_hour = self.convert_to_24_hour(start)
            end_hour = self.convert_to_24_hour(end)
            return start_hour, end_hour
        except Exception as e:
            print(f"Error parsing schedule: {e}")
            return 0, 24  # Default to full day if parsing fails

    def convert_to_24_hour(self, time_str):
        """Convert time string like '10pm' or '6am' to 24-hour format."""
        try:
            hour = int(time_str[:-2])
            if "pm" in time_str and hour != 12:
                hour += 12
            elif "am" in time_str and hour == 12:
                hour = 0
            return hour
        except ValueError as e:
            print(f"Error converting time to 24-hour format: {e}")
            return -1  # Return an invalid hour if conversion fails

    def is_within_schedule(self, start_hour, end_hour, current_hour):
        """Check if the current hour is within the schedule."""
        if start_hour < end_hour:  # Normal schedule (e.g., 6am to 2pm)
            return start_hour <= current_hour < end_hour
        else:  # Overnight schedule (e.g., 10pm to 6am)
            return current_hour >= start_hour or current_hour < end_hour

    def show_error(self, title, message):
        error_msg = QMessageBox()
        error_msg.setIcon(QMessageBox.Critical)
        error_msg.setText(title)
        error_msg.setInformativeText(message)
        error_msg.setWindowTitle("Error")
        error_msg.exec()
    
    def goto_change_pass(self):
        self.changepass = ChangePassword(self.db, self.admin_id)
        self.changepass.change_pass_ui.show()
    
    def goto_admin_ui(self):
        global_home_ui.close()
        self.admin = Admin(self.db)
        self.admin.admin_ui.showMaximized()

    def toggle_password_visibility(self):
        """Toggle the visibility of the password in the password input field."""
        if self.password_visible:
            self.home_ui.home_pass_box.setEchoMode(QLineEdit.Password)
            self.password_visible = False
        else:
            self.home_ui.home_pass_box.setEchoMode(QLineEdit.Normal)
            self.password_visible = True

class ChangePassword:
    def __init__(self, db, admin_id):
        self.db = db
        self.system_logs = SystemLogs(db)
        self.admin_id = admin_id
        self.loader = QUiLoader()
        self.change_pass_ui = self.loader.load("admin_change_pass.ui")
        self.change_pass_ui.change_pass_note.setText("For security purposes, please enter your current password below, then choose a new password and confirm it. Make sure your new password is at least 8 characters long.")
        self.change_pass_ui.change_pass_note.setStyleSheet("color: black")
        self.change_pass_ui.admin_change_pass_btn.clicked.connect(self.validate_and_change_password)
        self.change_pass_ui.setWindowTitle("Change Admin Password")
        self.change_pass_ui.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)
        self.system_logs.log_system_action("The change password prompt has been loaded.")

    def validate_and_change_password(self):
        new_password = self.change_pass_ui.change_pass_np_box.text()
        confirm_password = self.change_pass_ui.change_pass_confirm_box.text()
        current_password = self.change_pass_ui.change_pass_cp_box.text()

        try:
            cursor = self.db.execute_query("SELECT password FROM Admin WHERE admin_id = ?", (self.admin_id,))
            result = cursor.fetchone() if cursor else None

            if not result or current_password != result[0]:
                self.change_pass_ui.change_pass_note.setText("The current password you entered is incorrect. Please double-check and try again. Passwords are case-sensitive, so make sure your Caps Lock is off.")
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

            self.db.execute_query("UPDATE Admin SET password = ?, password_changed = TRUE WHERE admin_id = ?", (new_password, self.admin_id))

            success_msg = QMessageBox()
            success_msg.setIcon(QMessageBox.Information)
            self.system_logs.log_system_action("The admin password has been changed.")
            success_msg.setText("Password Changed Successfully")
            success_msg.setInformativeText("Your password has been updated. Please use the new password for future logins.")
            success_msg.setWindowTitle("Success")
            success_msg.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)
            success_msg.exec()

            self.change_pass_ui.close()

        except sqlite3.Error as e:
            self.system_logs.log_system_action("There was an Database error during password change")
            print(f"Database error during password change: {e}")
            

class Admin:
    def __init__(self, db):
        self.db = db
        self.system_logs = SystemLogs(db)
        self.loader = QUiLoader()
        self.admin_ui = self.loader.load("admin.ui")
        self.admin_ui.home_tabs.setCurrentWidget(self.admin_ui.admin_dashboard)
        self.admin_ui.admin_employee_sc_pages.setCurrentWidget(self.admin_ui.employee_hr_page)
        self.employees = []
        self.hr_employees = []
        self.current_employee_data = {}
        
        self.admin_ui.system_log_list.currentIndexChanged.connect(self.display_selected_log)
        self.load_system_logs()

        self.load_employee_table()
        self.load_hr_table()

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

        self.admin_ui.employee_picture_btn.clicked.connect(self.handle_enroll_picture)
        self.admin_ui.change_employee_picture.clicked.connect(self.handle_edit_picture)

        self.admin_ui.backup_btn.clicked.connect(self.save_backup_config)
        self.admin_ui.archive_btn.clicked.connect(self.save_archive_config)

        self.load_backup_and_archive_settings()

        self.admin_ui.admin_attedance_logs_tbl.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.admin_ui.admin_attedance_logs_tbl.setSelectionMode(QAbstractItemView.SingleSelection)

        self.admin_ui.admin_attedance_logs_search.textChanged.connect(self.filter_attendance_logs_table)
        self.admin_ui.admin_attedance_logs_sort.currentIndexChanged.connect(self.sort_attendance_logs_table)

        self.load_attendance_logs_table()

        self.admin_ui.view_employee_tbl.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.admin_ui.view_employee_tbl.setSelectionMode(QAbstractItemView.SingleSelection)

        self.admin_ui.view_hr_tbl.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.admin_ui.view_hr_tbl.setSelectionMode(QAbstractItemView.SingleSelection)

    def load_system_logs(self):
        """Load all log files into the system_log_list QComboBox."""
        log_dir = "resources/logs"
        self.admin_ui.system_log_list.clear()

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        log_files = [f for f in os.listdir(log_dir) if os.path.isfile(os.path.join(log_dir, f))]
        self.admin_ui.system_log_list.addItems(log_files)

    def display_selected_log(self):
        self.system_logs.log_system_action("A log file has been displayed.")
        selected_log = self.admin_ui.system_log_list.currentText()
        log_dir = "resources/logs"
        log_path = os.path.join(log_dir, selected_log)

        if os.path.exists(log_path):
            try:
                with open(log_path, "r") as file:
                    content = file.read()
                    self.admin_ui.system_log_browser.setText(content)
            except Exception as e:
                print(f"Error reading log file {log_path}: {e}")
                self.admin_ui.system_log_browser.setText("Error loading log file.")
        else:
            self.admin_ui.system_log_browser.setText("No log file selected or file does not exist.")

    def load_backup_and_archive_settings(self):
        try:
            cursor = self.db.execute_query("SELECT backup_config, automatic_backup_config, archive_config FROM system_setting WHERE id = 1")
            settings = cursor.fetchone() if cursor else None

            if settings:
                backup_config, auto_backup_config, archive_config = settings

                # Set backup configuration
                self.admin_ui.automatic_backup_btn.setChecked(backup_config == 1)

                # Set automatic backup configuration
                if auto_backup_config == 1:
                    self.admin_ui.auto_back_choice_1.setChecked(True)
                elif auto_backup_config == 2:
                    self.admin_ui.auto_back_choice_2.setChecked(True)
                elif auto_backup_config == 3:
                    self.admin_ui.auto_back_choice_3.setChecked(True)

                # Set archive configuration
                if archive_config == 1:
                    self.admin_ui.archive_choice_1.setChecked(True)
                elif archive_config == 2:
                    self.admin_ui.archive_choice_2.setChecked(True)
                elif archive_config == 3:
                    self.admin_ui.archive_choice_3.setChecked(True)
        except sqlite3.Error as e:
            print(f"Error loading backup and archive settings: {e}")

    def update_date_today(self):
        current_date = datetime.now()
        formatted_date = current_date.strftime("%a, %b %d, %Y")
        self.admin_ui.date_today.setText(formatted_date)

    def goto_home(self):
        self.system_logs.log_system_action("The Admin logged out.")
        global_home_ui.showMaximized()
        self.admin_ui.close()

    
    def goto_employee_hr(self):
        self.system_logs.log_system_action("Goes to the employee HR page.")
        employee_hr_page = self.admin_ui.admin_employee_sc_pages.indexOf(self.admin_ui.employee_hr_page)
        self.admin_ui.admin_employee_sc_pages.setCurrentIndex(employee_hr_page)
        self.load_employee_table()
        self.load_hr_table()

    def goto_employee_edit(self):
        self.system_logs.log_system_action("A selected employee is being edited.")
        employee_edit_page = self.admin_ui.admin_employee_sc_pages.indexOf(self.admin_ui.employee_edit_page)
        self.admin_ui.admin_employee_sc_pages.setCurrentIndex(employee_edit_page)

    def goto_employee_enroll(self):
        self.system_logs.log_system_action("The employee enrollment page has been opened.")
        employee_enroll_page = self.admin_ui.admin_employee_sc_pages.indexOf(self.admin_ui.employee_enroll_page)
        self.admin_ui.admin_employee_sc_pages.setCurrentIndex(employee_enroll_page)
        self.admin_ui.is_hr_no.setChecked(True)
        self.toggle_hr_fields()

    def goto_employee_enroll_2(self):
        self.system_logs.log_system_action("the enrollment proceed to the step 2.")
        employee_enroll_2_page = self.admin_ui.admin_employee_sc_pages.indexOf(self.admin_ui.employee_enroll2_page)
        self.admin_ui.admin_employee_sc_pages.setCurrentIndex(employee_enroll_2_page)

    def goto_employee_enroll_3(self):
        self.system_logs.log_system_action("the enrollment proceed to the step 3.")
        employee_enroll_3_page = self.admin_ui.admin_employee_sc_pages.indexOf(self.admin_ui.employee_enroll3_page)
        self.admin_ui.admin_employee_sc_pages.setCurrentIndex(employee_enroll_3_page)
        
    def filter_employee_table(self):
        search_text = self.admin_ui.employee_search_box.text().lower()
        
        for row in range(self.admin_ui.employee_list_tbl.rowCount()):
            self.admin_ui.employee_list_tbl.setRowHidden(row, False)
        
        if not search_text:
            return
        
        for row in range(self.admin_ui.employee_list_tbl.rowCount()):
            match_found = False
            
            for col in range(self.admin_ui.employee_list_tbl.columnCount()):
                item = self.admin_ui.employee_list_tbl.item(row, col)
                if item and search_text in item.text().lower():
                    match_found = True
                    break
                    
            self.admin_ui.employee_list_tbl.setRowHidden(row, not match_found)

    def filter_hr_table(self):
        search_text = self.admin_ui.hr_search_box.text().lower()
        
        for row in range(self.admin_ui.hr_list_tbl.rowCount()):
            self.admin_ui.hr_list_tbl.setRowHidden(row, False)
        
        if not search_text:
            return
        
        for row in range(self.admin_ui.hr_list_tbl.rowCount()):
            match_found = False
            
            for col in range(self.admin_ui.hr_list_tbl.columnCount()):
                item = self.admin_ui.hr_list_tbl.item(row, col)
                if item and search_text in item.text().lower():
                    match_found = True
                    break
                    
            self.admin_ui.hr_list_tbl.setRowHidden(row, not match_found)

    def sort_employee_table(self):
        sort_option = self.admin_ui.employee_sort_box.currentText()

        if sort_option == "By Name:":
            self.employees.sort(key=lambda x: (x["last_name"].lower(), x["first_name"].lower()))
        elif sort_option == "By Account ID:":
            self.employees.sort(key=lambda x: (x["employee_id"].split('-')[0], int(x["employee_id"].split('-')[2])))
        elif sort_option == "By Department:":
            self.employees.sort(key=lambda x: x["department"].lower())
        elif sort_option == "By Status:":
            self.employees.sort(key=lambda x: 0 if x["status"].lower() == "active" else 1)

        self.admin_ui.employee_list_tbl.setRowCount(0)
        for employee_data in self.employees:
            self.add_employee_to_table(employee_data)

    def sort_hr_table(self):
        sort_option = self.admin_ui.hr_sort_box.currentText()

        if sort_option == "By Name:":
            self.hr_employees.sort(key=lambda x: (x["last_name"].lower(), x["first_name"].lower()))
        elif sort_option == "By Account ID:":
            self.hr_employees.sort(key=lambda x: (x["employee_id"].split('-')[0], int(x["employee_id"].split('-')[2])))
        elif sort_option == "By Status:":
            self.employees.sort(key=lambda x: 0 if x["status"].lower() == "active" else 1)

        self.admin_ui.hr_list_tbl.setRowCount(0)
        for hr_data in self.hr_employees:
            self.add_hr_to_table(hr_data)

    def goto_employee_view(self):
        self.system_logs.log_system_action("A employee is selected to be viewed.")
        if selected := self.admin_ui.employee_list_tbl.selectedIndexes():
            row = selected[0].row()
            self.display_employee_view(self.employees[row])
            view_page = self.admin_ui.employee_view_page
        elif selected := self.admin_ui.hr_list_tbl.selectedIndexes():
            row = selected[0].row()
            self.display_hr_view(self.hr_employees[row])
            view_page = self.admin_ui.hr_view_page
        else:
            error_msg = QMessageBox()
            error_msg.setIcon(QMessageBox.Warning)
            error_msg.setText("No Selection")
            error_msg.setInformativeText("Please select an employee to view.")
            error_msg.setWindowTitle("View Error")
            error_msg.exec()
            return
            
        page_index = self.admin_ui.admin_employee_sc_pages.indexOf(view_page)
        self.admin_ui.admin_employee_sc_pages.setCurrentIndex(page_index)

    def display_employee_view(self, employee_data):
        self.system_logs.log_system_action("Loading all data of an employee for viewing.")
        self.admin_ui.view_employee_first_name.setText(employee_data["first_name"])
        self.admin_ui.view_employee_last_name.setText(employee_data["last_name"])
        self.admin_ui.view_employee_mi.setText(employee_data["middle_initial"])
        birthday_str = employee_data["birthday"]

        try:
            birthday_date = datetime.strptime(birthday_str, "%Y-%m-%d")
            formatted_birthday = birthday_date.strftime("%B %d, %Y")
            self.admin_ui.view_employee_birthday.setText(formatted_birthday)
            
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
        else:
            self.admin_ui.view_employee_sched_3.setChecked(True)

        self.display_picture(self.admin_ui.view_employee_picture, employee_data['profile_picture'])
        self.load_employee_attendance_logs(employee_data["employee_id"])

    def display_hr_view(self, hr_data):
        self.system_logs.log_system_action("Loading all data of an HR employee for viewing.")
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
        else:
            self.admin_ui.view_hr_sched_3.setChecked(True)

        self.display_picture(self.admin_ui.view_hr_picture, hr_data['profile_picture'])
        self.load_hr_attendance_logs(hr_data["employee_id"])

    def handle_edit_button(self):
        self.system_logs.log_system_action("The edit button has been clicked.")
        employee_selected_rows = self.admin_ui.employee_list_tbl.selectedIndexes()
        hr_selected_rows = self.admin_ui.hr_list_tbl.selectedIndexes()

        if employee_selected_rows:
            row = employee_selected_rows[0].row()
            if row < len(self.employees):
                self.selected_employee_index = row
                self.selected_employee_type = "employee"
                employee_data = self.employees[row]
                self.load_employee_to_edit_form(employee_data)
                self.goto_employee_edit()
            else:
                self.system_logs.log_system_action("Invalid selection has been made.")
                print("Invalid employee row selected.")

        elif hr_selected_rows:
            row = hr_selected_rows[0].row()
            if row < len(self.hr_employees):
                self.selected_employee_index = row
                self.selected_employee_type = "hr"
                hr_data = self.hr_employees[row]
                self.load_employee_to_edit_form(hr_data)
                self.goto_employee_edit()
            else:
                self.system_logs.log_system_action("Invalid selection has been made.")
                print("Invalid HR row selected.")

        else:
            self.system_logs.log_system_action("Invalid selection has been made. (No employee has been selected)")
            error_msg = QMessageBox()
            error_msg.setIcon(QMessageBox.Warning)
            error_msg.setText("No Selection")
            error_msg.setInformativeText("Please select an employee to edit.")
            error_msg.setWindowTitle("Edit Error")
            error_msg.exec()

    def load_employee_to_edit_form(self, employee_data):
        self.system_logs.log_system_action("Loading employee data to edit page.")
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
        else:
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

        self.display_picture(self.admin_ui.edit_emplyee_picture, employee_data['profile_picture'])

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
            "status": status,
            "profile_picture": self.current_employee_data.get('profile_picture', '')
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

        try:
            employee_name = f"{result['first_name']}_{result['last_name']}"
            picture_path = self.save_picture(result['profile_picture'], employee_name)
            if picture_path:
                result['profile_picture'] = picture_path

            self.db.execute_query('''
                UPDATE Employee
                SET first_name = ?, last_name = ?, middle_initial = ?, birthday = ?, gender = ?,
                    department = ?, position = ?, schedule = ?, is_hr = ?, status = ?, password = ?, profile_picture = ?
                WHERE employee_id = ?
            ''', (
                result['first_name'], result['last_name'], result['middle_initial'], result['birthday'],
                result['gender'], result['department'], result['position'], result['schedule'],
                result['is_hr'], result['status'], result['password'], result['profile_picture'], result['employee_id']
            ))

            self.system_logs.log_system_action("A successful edit of an employee has been made.")
            success_msg = QMessageBox()
            success_msg.setIcon(QMessageBox.Information)
            success_msg.setText("Employee Updated")
            success_msg.setInformativeText(f"Employee {result['first_name']} {result['last_name']} has been updated.")
            success_msg.setWindowTitle("Edit Success")
            success_msg.exec()

            self.load_employee_table()
            self.load_hr_table()
            self.goto_employee_hr()

        except sqlite3.Error as e:
            print(f"Database error while updating employee: {e}")

    def toggle_employee_status(self):
        if self.selected_employee_index is None or self.selected_employee_type is None:
            error_msg = QMessageBox()
            error_msg.setIcon(QMessageBox.Critical)
            error_msg.setText("Status Update Error")
            error_msg.setInformativeText("No employee selected.")
            error_msg.setWindowTitle("Status Error")
            error_msg.exec()
            return

        try:
            if self.selected_employee_type == "employee":
                employee = self.employees[self.selected_employee_index]
            else:
                employee = self.hr_employees[self.selected_employee_index]

            new_status = "Inactive" if employee["status"] == "Active" else "Active"

            self.db.execute_query("UPDATE Employee SET status = ? WHERE employee_id = ?", (new_status, employee["employee_id"]))

            employee["status"] = new_status

            success_msg = QMessageBox()
            success_msg.setIcon(QMessageBox.Information)
            success_msg.setText("Status Updated")
            success_msg.setInformativeText(f"Employee {employee['first_name']} {employee['last_name']} has been {new_status.lower()}.")
            success_msg.setWindowTitle("Status Update")
            success_msg.exec()

            self.load_employee_table()
            self.load_hr_table()

        except sqlite3.Error as e:
            print(f"Database error while updating status: {e}")

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
            "status": "Active",
            "profile_picture": self.current_employee_data.get('profile_picture', '')
        }
        
        return True, employee_data

    def load_employee_table(self):
        self.system_logs.log_system_action("Loading all employees to the employee table.")
        try:
            cursor = self.db.execute_query("SELECT * FROM Employee WHERE is_hr = 0")
            employees = cursor.fetchall() if cursor else []

            self.employees = []
            self.admin_ui.employee_list_tbl.setRowCount(0)
            for employee in employees:
                employee_data = {
                    "employee_id": employee[0],
                    "first_name": employee[1],
                    "last_name": employee[2],
                    "middle_initial": employee[3],
                    "birthday": employee[4],
                    "gender": employee[5],
                    "department": employee[6],
                    "position": employee[7],
                    "schedule": employee[8],
                    "is_hr": employee[9],
                    "status": employee[10],
                    "password": employee[11],
                    "profile_picture": employee[12]
                }
                self.employees.append(employee_data)
                self.add_employee_to_table(employee_data)

            self.update_dashboard_labels()

        except sqlite3.Error as e:
            print(f"Database error while loading employees: {e}")

    def load_hr_table(self):
        self.system_logs.log_system_action("Loading all HR employees to the HR table.")
        try:
            cursor = self.db.execute_query("SELECT * FROM Employee WHERE is_hr = 1")
            hr_employees = cursor.fetchall() if cursor else []

            self.hr_employees = []
            self.admin_ui.hr_list_tbl.setRowCount(0)
            for hr_employee in hr_employees:
                hr_data = {
                    "employee_id": hr_employee[0],
                    "first_name": hr_employee[1],
                    "last_name": hr_employee[2],
                    "middle_initial": hr_employee[3],
                    "birthday": hr_employee[4],
                    "gender": hr_employee[5],
                    "department": hr_employee[6],
                    "position": hr_employee[7],
                    "schedule": hr_employee[8],
                    "is_hr": hr_employee[9],
                    "status": hr_employee[10],
                    "password": hr_employee[11],
                    "profile_picture": hr_employee[12]
                }
                self.hr_employees.append(hr_data)
                self.add_hr_to_table(hr_data)

        except sqlite3.Error as e:
            print(f"Database error while loading HR employees: {e}")

    def add_employee_to_table(self, employee_data):
        row_position = self.admin_ui.employee_list_tbl.rowCount()
        self.admin_ui.employee_list_tbl.insertRow(row_position)
        middle_initial = f" {employee_data['middle_initial']}." if employee_data['middle_initial'] else ""
        full_name = f"{employee_data['last_name']}, {employee_data['first_name']}{middle_initial}"
        dept_pos = f"{employee_data['department']} / {employee_data['position']}"
        
        name_item = QTableWidgetItem(full_name)
        id_item = QTableWidgetItem(employee_data['employee_id'])
        dept_pos_item = QTableWidgetItem(dept_pos)
        status_item = QTableWidgetItem(employee_data.get('status', 'Active'))
        
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
        status_item = QTableWidgetItem(hr_data.get('status', 'Active'))
        
        name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
        id_item.setFlags(id_item.flags() & ~Qt.ItemIsEditable)
        status_item.setFlags(status_item.flags() & ~Qt.ItemIsEditable)
        
        self.admin_ui.hr_list_tbl.setItem(row_position, 0, name_item)
        self.admin_ui.hr_list_tbl.setItem(row_position, 1, id_item)
        self.admin_ui.hr_list_tbl.setItem(row_position, 2, status_item)
        
        self.admin_ui.hr_list_tbl.resizeColumnsToContents()

    def save_employee_data(self, employee_data):
        self.system_logs.log_system_action("Saving employee data to the database.")
        try:
            cursor = self.db.execute_query("SELECT employee_id FROM Employee WHERE employee_id = ?", (employee_data['employee_id'],))
            result = cursor.fetchone() if cursor else None

            if result:
                self.db.execute_query('''
                    UPDATE Employee
                    SET first_name = ?, last_name = ?, middle_initial = ?, birthday = ?, gender = ?,
                        department = ?, position = ?, schedule = ?, is_hr = ?, status = ?, password = ?, profile_picture = ?
                    WHERE employee_id = ?
                ''', (
                    employee_data['first_name'], employee_data['last_name'], employee_data['middle_initial'],
                    employee_data['birthday'], employee_data['gender'], employee_data['department'],
                    employee_data['position'], employee_data['schedule'], employee_data['is_hr'],
                    employee_data['status'], employee_data['password'], employee_data['profile_picture'], employee_data['employee_id']
                ))
            else:
                self.db.execute_query('''
                    INSERT INTO Employee (employee_id, first_name, last_name, middle_initial, birthday, gender,
                                          department, position, schedule, is_hr, status, password, profile_picture)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    employee_data['employee_id'], employee_data['first_name'], employee_data['last_name'],
                    employee_data['middle_initial'], employee_data['birthday'], employee_data['gender'],
                    employee_data['department'], employee_data['position'], employee_data['schedule'],
                    employee_data['is_hr'], employee_data['status'], employee_data['password'], employee_data['profile_picture']
                ))

            return True

        except sqlite3.Error as e:
            print(f"Database error while saving employee data: {e}")
            return False

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
            employee_name = f"{self.current_employee_data['first_name']}_{self.current_employee_data['last_name']}"
            picture_path = self.save_picture(self.current_employee_data['profile_picture'], employee_name)
            if picture_path:
                self.current_employee_data['profile_picture'] = picture_path

            success = self.save_employee_data(self.current_employee_data)
            
            if success:
                self.system_logs.log_system_action("A new employee has been enrolled.")
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
                self.system_logs.log_system_action("Failed to save employee data.")
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

    def toggle_hr_fields(self):
        is_hr = self.admin_ui.is_hr_yes.isChecked()
        self.admin_ui.employee_department_box.setDisabled(is_hr)
        self.admin_ui.employee_position_box.setDisabled(is_hr)
        if is_hr:
            self.admin_ui.employee_department_box.setCurrentText("Human Resources")
            self.admin_ui.employee_position_box.setCurrentText("HR Staff")

    def update_dashboard_labels(self):
        try:
            cursor = self.db.execute_query("SELECT COUNT(*) FROM Employee")
            total_employees = cursor.fetchone()[0] if cursor else 0

            cursor = self.db.execute_query("SELECT COUNT(*) FROM Employee WHERE status = 'Active'")
            active_employees = cursor.fetchone()[0] if cursor else 0

            today_date = datetime.now().strftime("%Y-%m-%d")
            cursor = self.db.execute_query(
                "SELECT COUNT(DISTINCT employee_id) FROM attendance_logs "
                "WHERE date = ? AND employee_id IN (SELECT employee_id FROM Employee WHERE is_hr = 0)", 
                (today_date,)
            )
            logged_employees = cursor.fetchone()[0] if cursor else 0

            cursor = self.db.execute_query(
                "SELECT COUNT(DISTINCT employee_id) FROM attendance_logs "
                "WHERE date = ? AND remarks = 'late' AND employee_id IN (SELECT employee_id FROM Employee WHERE is_hr = 0)", 
                (today_date,)
            )
            late_employees = cursor.fetchone()[0] if cursor else 0

            cursor = self.db.execute_query(
                "SELECT COUNT(*) FROM Employee WHERE is_hr = 0 AND status = 'Active' AND employee_id NOT IN ("
                "SELECT DISTINCT employee_id FROM attendance_logs WHERE date = ?)", 
                (today_date,)
            )
            absent_employees = cursor.fetchone()[0] if cursor else 0

            self.system_logs.log_system_action("Dashboard labels have been updated.")
            self.admin_ui.total_employee_lbl.setText(f"{total_employees}/{total_employees}")
            self.admin_ui.active_employee_lbl.setText(str(active_employees))
            self.admin_ui.logged_employee_lbl.setText(str(logged_employees))
            self.admin_ui.late_employee_lbl.setText(str(late_employees))
            self.admin_ui.absent_employee_lbl.setText(str(absent_employees))

        except sqlite3.Error as e:
            print(f"Database error while updating dashboard labels: {e}")

    def select_picture(self, label):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.bmp *.gif)")
        if file_dialog.exec():
            selected_file = file_dialog.selectedFiles()[0]
            pixmap = QPixmap(selected_file)
            label.setPixmap(pixmap.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            return selected_file
        return None

    def save_picture(self, file_path, employee_name):
        if not os.path.exists("resources/profile_pictures"):
            os.makedirs("resources/profile_pictures")

        file_extension = os.path.splitext(file_path)[1]
        destination = os.path.join("resources/profile_pictures", f"{employee_name}{file_extension}")
        try:
            shutil.copy(file_path, destination)
            return destination
        except Exception as e:
            print(f"Error saving picture: {e}")
            return None

    def handle_enroll_picture(self):
        file_path = self.select_picture(self.admin_ui.enroll_employee_picture)
        if file_path:
            self.current_employee_data['profile_picture'] = file_path

    def handle_edit_picture(self):
        file_path = self.select_picture(self.admin_ui.edit_emplyee_picture)
        if file_path:
            self.current_employee_data['profile_picture'] = file_path

    def display_picture(self, label, picture_path):
        if picture_path and os.path.exists(picture_path):
            pixmap = QPixmap(picture_path)
            pixmap = pixmap.scaled(170, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            label.setPixmap(pixmap)
        else:
            label.setPixmap(QPixmap())

    def save_backup_config(self):
        try:
            backup_config = 1 if self.admin_ui.automatic_backup_btn.isChecked() else 2
            auto_backup_config = 1 if self.admin_ui.auto_back_choice_1.isChecked() else \
                                2 if self.admin_ui.auto_back_choice_2.isChecked() else 3

            self.db.execute_query('''
                UPDATE system_setting
                SET backup_config = ?, automatic_backup_config = ?
                WHERE id = 1
            ''', (backup_config, auto_backup_config))

            self.system_logs.log_system_action("Backup configuration saved.")
            
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Backup configuration saved successfully.")
            msg.setWindowTitle("Configuration Saved")
            msg.exec_()
            
        except sqlite3.Error as e:
            print(f"Error saving backup configuration: {e}")
            error_msg = QMessageBox()
            error_msg.setIcon(QMessageBox.Critical)
            error_msg.setText(f"Failed to save backup configuration.")
            error_msg.setDetailedText(f"Database error: {e}")
            error_msg.setWindowTitle("Configuration Error")
            error_msg.exec_()

    def save_archive_config(self):
        try:
            archive_config = 1 if self.admin_ui.archive_choice_1.isChecked() else \
                            2 if self.admin_ui.archive_choice_2.isChecked() else 3

            self.db.execute_query('''
                UPDATE system_setting
                SET archive_config = ?
                WHERE id = 1
            ''', (archive_config,))

            self.system_logs.log_system_action("Archive configuration saved.")
            
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Archive configuration saved successfully.")
            msg.setWindowTitle("Configuration Saved")
            msg.exec_()
            
        except sqlite3.Error as e:
            print(f"Error saving archive configuration: {e}")
            error_msg = QMessageBox()
            error_msg.setIcon(QMessageBox.Critical)
            error_msg.setText(f"Failed to save archive configuration.")
            error_msg.setDetailedText(f"Database error: {e}")
            error_msg.setWindowTitle("Configuration Error")
            error_msg.exec_()

    def load_attendance_logs_table(self):
        """Load all attendance logs into the table."""
        try:
            cursor = self.db.execute_query("SELECT employee_id, remarks, date, time FROM attendance_logs")
            logs = cursor.fetchall() if cursor else []

            self.admin_ui.admin_attedance_logs_tbl.setRowCount(0)
            for log in logs:
                self.add_attendance_log_to_table(log)
        except sqlite3.Error as e:
            print(f"Database error while loading attendance logs: {e}")

    def add_attendance_log_to_table(self, log):
        """Add a single attendance log to the table."""
        row_position = self.admin_ui.admin_attedance_logs_tbl.rowCount()
        self.admin_ui.admin_attedance_logs_tbl.insertRow(row_position)

        account_id_item = QTableWidgetItem(log[0])
        remarks_item = QTableWidgetItem(log[1])
        date_item = QTableWidgetItem(log[2])
        time_item = QTableWidgetItem(log[3])

        account_id_item.setFlags(account_id_item.flags() & ~Qt.ItemIsEditable)
        remarks_item.setFlags(remarks_item.flags() & ~Qt.ItemIsEditable)
        date_item.setFlags(date_item.flags() & ~Qt.ItemIsEditable)
        time_item.setFlags(time_item.flags() & ~Qt.ItemIsEditable)

        self.admin_ui.admin_attedance_logs_tbl.setItem(row_position, 0, account_id_item)
        self.admin_ui.admin_attedance_logs_tbl.setItem(row_position, 1, remarks_item)
        self.admin_ui.admin_attedance_logs_tbl.setItem(row_position, 2, date_item)
        self.admin_ui.admin_attedance_logs_tbl.setItem(row_position, 3, time_item)

        self.admin_ui.admin_attedance_logs_tbl.resizeColumnsToContents()

    def filter_attendance_logs_table(self):
        """Filter attendance logs based on the search bar input."""
        search_text = self.admin_ui.admin_attedance_logs_search.text().lower()
        for row in range(self.admin_ui.admin_attedance_logs_tbl.rowCount()):
            self.admin_ui.admin_attedance_logs_tbl.setRowHidden(row, False)

        if not search_text:
            return

        for row in range(self.admin_ui.admin_attedance_logs_tbl.rowCount()):
            match_found = False
            for col in range(self.admin_ui.admin_attedance_logs_tbl.columnCount()):
                item = self.admin_ui.admin_attedance_logs_tbl.item(row, col)
                if item and search_text in item.text().lower():
                    match_found = True
                    break
            self.admin_ui.admin_attedance_logs_tbl.setRowHidden(row, not match_found)

    def sort_attendance_logs_table(self):
        """Sort attendance logs based on the selected sort option."""
        sort_option = self.admin_ui.admin_attedance_logs_sort.currentText()

        logs = []
        for row in range(self.admin_ui.admin_attedance_logs_tbl.rowCount()):
            log = [
                self.admin_ui.admin_attedance_logs_tbl.item(row, col).text()
                for col in range(self.admin_ui.admin_attedance_logs_tbl.columnCount())
            ]
            logs.append(log)

        if sort_option == "By Date:":
            logs.sort(key=lambda x: x[2])  # Sort by Date
        elif sort_option == "By Time:":
            logs.sort(key=lambda x: x[3])  # Sort by Time
        elif sort_option == "By Account ID:":
            logs.sort(key=lambda x: x[0])  # Sort by Account ID
        elif sort_option == "By Remarks:":
            logs.sort(key=lambda x: x[1])  # Sort by Remarks

        self.admin_ui.admin_attedance_logs_tbl.setRowCount(0)
        for log in logs:
            self.add_attendance_log_to_table(log)

    def load_employee_attendance_logs(self, employee_id):
        """Load attendance logs for the selected employee."""
        try:
            cursor = self.db.execute_query(
                "SELECT date, time, remarks FROM attendance_logs WHERE employee_id = ?", (employee_id,)
            )
            logs = cursor.fetchall() if cursor else []

            self.admin_ui.view_employee_tbl.setRowCount(0)
            for log in logs:
                self.add_log_to_table(self.admin_ui.view_employee_tbl, log)
        except sqlite3.Error as e:
            print(f"Database error while loading employee attendance logs: {e}")

    def load_hr_attendance_logs(self, hr_id):
        """Load attendance logs for the selected HR."""
        try:
            cursor = self.db.execute_query(
                "SELECT date, time, remarks FROM attendance_logs WHERE employee_id = ?", (hr_id,)
            )
            logs = cursor.fetchall() if cursor else []

            self.admin_ui.view_hr_tbl.setRowCount(0)
            for log in logs:
                self.add_log_to_table(self.admin_ui.view_hr_tbl, log)
        except sqlite3.Error as e:
            print(f"Database error while loading HR attendance logs: {e}")

    def add_log_to_table(self, table, log):
        """Add a single log entry to the specified table."""
        row_position = table.rowCount()
        table.insertRow(row_position)

        date_item = QTableWidgetItem(log[0])
        time_item = QTableWidgetItem(log[1])
        remarks_item = QTableWidgetItem(log[2])

        date_item.setFlags(date_item.flags() & ~Qt.ItemIsEditable)
        time_item.setFlags(time_item.flags() & ~Qt.ItemIsEditable)
        remarks_item.setFlags(remarks_item.flags() & ~Qt.ItemIsEditable)

        table.setItem(row_position, 0, date_item)
        table.setItem(row_position, 1, time_item)
        table.setItem(row_position, 2, remarks_item)

        table.resizeColumnsToContents()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = EALS()
    sys.exit(app.exec())
