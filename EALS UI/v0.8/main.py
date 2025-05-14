import sys
import random
import os
import sqlite3
import threading
import shutil
import smtplib
import socket
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage  # Add this import
from PySide6.QtWidgets import QApplication,QMessageBox, QTableWidgetItem, QAbstractItemView, QFileDialog, QLineEdit,QVBoxLayout, QPushButton, QRadioButton, QWidget, QHBoxLayout, QLabel, QListWidget, QListWidgetItem  # add QListWidget, QListWidgetItem
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Qt, QDate, QCoreApplication, QProcess, QTimer, QRegularExpression
from PySide6.QtGui import QPixmap, QRegularExpressionValidator, QIcon, QColor, QPainter
from datetime import datetime, timedelta
from pyqttoast import Toast, ToastPreset, ToastPosition
import argon2
import secrets
import string
import chime
from PySide6.QtCharts import QChart, QChartView, QAreaSeries, QLineSeries, QValueAxis, QCategoryAxis, QBarSeries, QBarSet, QPieSeries
from PySide6.QtCharts import QHorizontalBarSeries, QBarCategoryAxis 
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import matplotlib.pyplot as plt
import tempfile
import pandas as pd
import io
import json


PASSWORD_HASHER = argon2.PasswordHasher()

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
                    default_pass VARCHAR(255) NOT NULL,
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
                    password_changed BOOLEAN DEFAULT FALSE,
                    profile_picture VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    created_by VARCHAR(20) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_modified_by VARCHAR(20),
                    last_modified_at TIMESTAMP,
                    attedance_count CHAR(1),
                    late_count CHAR(2),
                    absent_count CHAR(2),
                    FOREIGN KEY (created_by) REFERENCES Admin(admin_id),
                    FOREIGN KEY (last_modified_by) REFERENCES Admin(admin_id)
                );

                CREATE TABLE IF NOT EXISTS attendance_logs (
                    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    employee_id VARCHAR(20) NOT NULL,
                    date DATE NOT NULL,
                    time TIME NOT NULL,
                    remarks VARCHAR(10) NOT NULL,
                    is_late BOOLEAN,
                    FOREIGN KEY (employee_id) REFERENCES Employee(employee_id)
                );

                CREATE TABLE IF NOT EXISTS feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title VARCHAR(50) NOT NULL,
                    message TEXT NOT NULL, 
                    created_by VARCHAR(20) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (created_by) REFERENCES Employee(employee_id)
                );
                
                CREATE TABLE IF NOT EXISTS announcements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    subject VARCHAR(100) NOT NULL,
                    message TEXT NOT NULL,
                    sending_type VARCHAR(20) NOT NULL,
                    involved_employee VARCHAR(20),
                    schedule_enabled BOOLEAN DEFAULT FALSE,
                    schedule_frequency INTEGER,
                    theme_enabled BOOLEAN DEFAULT FALSE,
                    theme_type VARCHAR(50),
                    attached_files_count INTEGER,
                    files_path TEXT,
                    created_by VARCHAR(20) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (created_by) REFERENCES Employee(employee_id)
                );
                                
                CREATE TABLE IF NOT EXISTS system_settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    backup_type VARCHAR(10),
                    backup_frequency INTEGER,
                    backup_unit VARCHAR(10),
                    retention_enabled BOOLEAN,
                    retention_frequency INTEGER,
                    retention_unit VARCHAR(10),
                    created_by VARCHAR(20) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_modified_by VARCHAR(20),
                    last_modified_at TIMESTAMP,
                    FOREIGN KEY (created_by) REFERENCES Admin(admin_id),
                    FOREIGN KEY (last_modified_by) REFERENCES Admin(admin_id)
                );

                CREATE TABLE IF NOT EXISTS system_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    path TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_modified_at TIMESTAMP,
                    entity_started VARCHAR(20), -- ID of the entity that initiated the action
                    stopped_to_the_entity VARCHAR(20), -- ID of the entity where the action stopped
                    present_count INTEGER DEFAULT 0,
                    absent_count INTEGER DEFAULT 0,
                    late_count INTEGER DEFAULT 0,
                    average_work_hours REAL DEFAULT 0, -- Added column
                    FOREIGN KEY (entity_started) REFERENCES Employee(employee_id),
                    FOREIGN KEY (entity_started) REFERENCES Admin(admin_id),
                    FOREIGN KEY (entity_started) REFERENCES Feedback(id),
                    FOREIGN KEY (entity_started) REFERENCES attendance_logs(log_id),
                    FOREIGN KEY (entity_started) REFERENCES system_settings(id),
                    FOREIGN KEY (stopped_to_the_entity) REFERENCES Employee(employee_id),
                    FOREIGN KEY (stopped_to_the_entity) REFERENCES Admin(admin_id),
                    FOREIGN KEY (stopped_to_the_entity) REFERENCES Feedback(id),
                    FOREIGN KEY (stopped_to_the_entity) REFERENCES attendance_logs(log_id),
                    FOREIGN KEY (stopped_to_the_entity) REFERENCES system_settings(id)
                );
                ''')
                self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")

    def is_initial_setup(self):
        try:
            cursor = self.execute_query("SELECT COUNT(*) FROM Admin")
            result = cursor.fetchone()
            return result[0] == 0 if result else True
        except sqlite3.Error as e:
            print(f"Database error during initial setup check: {e}")
            return True

    def create_initial_admin(self):
        try:
            admin_id = f"admin-01-0001"
            admin_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            hashed_password = PASSWORD_HASHER.hash(admin_password)
            hashed_default_pass = PASSWORD_HASHER.hash(admin_password)  # Hash the default password
            self.execute_query('''
                INSERT INTO Admin (admin_id, password, default_pass, password_changed)
                VALUES (?, ?, ?, FALSE)
            ''', (admin_id, hashed_password, hashed_default_pass))  # Store the hashed default password
            self.connection.commit()
            system_logs = SystemLogs(self)
            system_logs.log_system_action(f"Initial admin account {admin_id} created", "Admin")
            return admin_id, admin_password
        except sqlite3.Error as e:
            print(f"Database error during initial admin creation: {e}")
            return None, None

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

    def get_average_work_hours(self, date_str):
        """
        Calculate the average work hours for all employees for a given date.
        Only considers employees (is_hr = 0) who have both a Clock In and Clock Out on that date.
        """
        try:
            cursor = self.db.execute_query(
                '''
                SELECT employee_id FROM attendance_logs
                WHERE date = ? AND remarks = 'Clock In'
                AND employee_id IN (SELECT employee_id FROM Employee WHERE is_hr = 0)
                ''', (date_str,)
            )
            employee_ids = [row[0] for row in cursor.fetchall()] if cursor else []
            total_hours = 0
            count = 0
            for emp_id in employee_ids:
                # Get Clock In and Clock Out times for this employee on this date
                cur = self.db.execute_query(
                    '''
                    SELECT time, remarks FROM attendance_logs
                    WHERE employee_id = ? AND date = ?
                    ORDER BY time ASC
                    ''', (emp_id, date_str)
                )
                logs = cur.fetchall() if cur else []
                clock_in_time = None
                clock_out_time = None
                for log in logs:
                    if log[1] == "Clock In" and not clock_in_time:
                        clock_in_time = log[0]
                    elif log[1] == "Clock Out":
                        clock_out_time = log[0]
                if clock_in_time and clock_out_time:
                    try:
                        t1 = datetime.strptime(f"{date_str} {clock_in_time}", "%Y-%m-%d %H:%M:%S")
                        t2 = datetime.strptime(f"{date_str} {clock_out_time}", "%Y-%m-%d %H:%M:%S")
                        hours = (t2 - t1).total_seconds() / 3600
                        if hours > 0:
                            total_hours += hours
                            count += 1
                    except Exception:
                        continue
            return round(total_hours / count, 2) if count > 0 else 0
        except Exception as e:
            print(f"Error calculating average work hours: {e}")
            return 0

    def log_system_action(self, action, entity_type):
        """
        entities = Employee, Admin, Feedback, AttendanceLog, SystemSettings
        sample usage = self.system_logs.log_system_action(f"HR discarded feedback draft", "Employee")
        """
        try:
            log_dir = "resources/logs"
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)

            log_file = os.path.join(log_dir, f"{datetime.now().strftime('%Y%m%d')}.txt")
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            with open(log_file, "a") as file:
                file.write(f"{current_time} - {action}\n")

            entity_id = None
            if entity_type == "Employee" and hasattr(self, "employee_data"):
                entity_id = self.employee_data.get("employee_id")
            elif entity_type == "Admin" and hasattr(self, "admin_id"):
                entity_id = self.admin_id
            elif entity_type == "Feedback":
                cursor = self.db.execute_query("SELECT id FROM feedback ORDER BY created_at DESC LIMIT 1")
                result = cursor.fetchone()
                entity_id = result[0] if result else None
            elif entity_type == "AttendanceLog":
                cursor = self.db.execute_query("SELECT log_id FROM attendance_logs ORDER BY date DESC, time DESC LIMIT 1")
                result = cursor.fetchone()
                entity_id = result[0] if result else None
            elif entity_type == "SystemSettings":
                cursor = self.db.execute_query("SELECT id FROM system_settings ORDER BY last_modified_at DESC LIMIT 1")
                result = cursor.fetchone()
                entity_id = result[0] if result else None

            if entity_id is None:
                entity_id = entity_type

            today = datetime.now().strftime('%Y-%m-%d')
            present_count = 0
            absent_count = 0
            late_count = 0
            try:
                # Present: employees who have attendance log today
                cursor = self.db.execute_query(
                    "SELECT COUNT(DISTINCT employee_id) FROM attendance_logs WHERE date = ? AND employee_id IN (SELECT employee_id FROM Employee WHERE is_hr = 0)",
                    (today,)
                )
                present_count = cursor.fetchone()[0] if cursor else 0

                # Late: employees who have is_late=1 today
                cursor = self.db.execute_query(
                    "SELECT COUNT(DISTINCT employee_id) FROM attendance_logs WHERE date = ? AND is_late = 1 AND employee_id IN (SELECT employee_id FROM Employee WHERE is_hr = 0)",
                    (today,)
                )
                late_count = cursor.fetchone()[0] if cursor else 0

                # Absent: active employees with no attendance log today
                cursor = self.db.execute_query(
                    "SELECT COUNT(*) FROM Employee WHERE is_hr = 0 AND status = 'Active' AND employee_id NOT IN (SELECT DISTINCT employee_id FROM attendance_logs WHERE date = ?)",
                    (today,)
                )
                absent_count = cursor.fetchone()[0] if cursor else 0
                
                # Calculate average work hours for today
                average_work_hours = self.get_average_work_hours(today)
            except Exception as e:
                print(f"Error computing attendance counts for system logs: {e}")

            cursor = self.db.execute_query(
                "SELECT id FROM system_logs WHERE date(created_at) = ?",
                (today,)
            )
            existing_log = cursor.fetchone()

            if existing_log:
                self.db.execute_query(
                    '''
                    UPDATE system_logs
                    SET last_modified_at = ?, 
                        stopped_to_the_entity = ?,
                        present_count = ?, 
                        absent_count = ?, 
                        late_count = ?,
                        average_work_hours = ?
                    WHERE id = ?
                    ''',
                    (current_time, entity_id, present_count, absent_count, late_count, average_work_hours, existing_log[0])
                )
            else:
                self.db.execute_query(
                    '''
                    INSERT INTO system_logs (path, created_at, last_modified_at, entity_started, stopped_to_the_entity, present_count, absent_count, late_count, average_work_hours)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''',
                    (log_file, current_time, current_time, entity_id, entity_id, present_count, absent_count, late_count, average_work_hours)
                )

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

class Feedback:
    def __init__(self, db, hr_data):
        self.db = db
        self.system_logs = SystemLogs(db)
        self.hr_data = hr_data
        self.loader = QUiLoader()
        self.feedback_ui = self.loader.load("ui/feedback.ui")
        self.feedback_ui.setWindowTitle("Send Feedback")
        self.feedback_ui.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)
        self.feedback_ui.setWindowModality(Qt.ApplicationModal)
        
        # Connect save button
        self.feedback_ui.save_feedback_btn.clicked.connect(self.save_feedback)
        self.feedback_ui.discard_feedback_btn.clicked.connect(self.discard_feedback)
        
        
    def discard_feedback(self):
        self.system_logs.log_system_action("HR discarded feedback draft", "Employee")

        self.feedback_ui.feedback_title_box.clear()
        self.feedback_ui.feedback_box.clear()

        self.feedback_ui.close()
        
    def save_feedback(self):
        title = self.feedback_ui.feedback_title_box.text().strip()
        message = self.feedback_ui.feedback_box.toPlainText().strip()
        
        # Validate title length
        if len(title) < 5 or len(title) > 50:
            self.show_error("Invalid Title", "Title must be between 5 and 50 characters long.")
            return
            
        # Validate message length
        if len(message) < 20 or len(message) > 500:
            self.show_error("Invalid Message", "Message must be between 20 and 500 characters long.")
            return
                
        try:
            self.db.execute_query('''
                INSERT INTO feedback (title, message, created_by)
                VALUES (?, ?, ?)
            ''', (title, message, self.hr_data["employee_id"]))
            
            self.feedback_ui.feedback_title_box.clear()
            self.feedback_ui.feedback_box.clear()
            self.feedback_ui.close()
            self.system_logs.log_system_action(f"HR submitted feedback: {title}", "Employee")
            self.show_success( "Success", "Feedback submitted successfully.")
            
        except sqlite3.Error as e:
            print(f"Database error while saving feedback: {e}")
            self.show_error("Error", "Failed to save feedback. Please try again.")
            
    def show_success(self, title, message):
        chime.theme('chime')
        chime.success()
        toast = Toast(self.feedback_ui)
        toast.setTitle(title)
        toast.setText(message)
        toast.setDuration(2000)  # Duration in milliseconds
        toast.setOffset(25, 35)  
        toast.setBorderRadius(6)  
        toast.applyPreset(ToastPreset.SUCCESS)  
        toast.setBackgroundColor(QColor('#FFFFFF')) 
        toast.setPosition(ToastPosition.TOP_RIGHT)  
        toast.show() 
            
    def show_error(self, title, message):
        chime.theme('big-sur')
        chime.warning()
        toast = Toast(self.feedback_ui)
        toast.setTitle(title)
        toast.setText(message)
        toast.setDuration(2000)  # Duration in milliseconds
        toast.setOffset(25, 35)  
        toast.setBorderRadius(6)  
        toast.applyPreset(ToastPreset.ERROR)  
        toast.setBackgroundColor(QColor('#FFFFFF'))
        toast.setPosition(ToastPosition.TOP_RIGHT)  
        toast.show()  

class HR:
    def __init__(self, db, hr_data):
        self.db = db
        self.system_logs = SystemLogs(db)
        self.hr_data = hr_data
        self.loader = QUiLoader()
        self.hr_ui = self.loader.load("ui/hr.ui")
        self.hr_ui.setWindowIcon(QIcon('resources/logo.ico'))
        self.hr_ui.setWindowTitle("EALS - HR")
        self.hr_ui.hr_home_tabs.setCurrentWidget(self.hr_ui.hr_dashboard)
        self.hr_ui.hr_employee_sc_pages.setCurrentWidget(self.hr_ui.hr_employee_dashboard_page)
        self.hr_ui.hr_employee_tbl.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.hr_ui.hr_employee_tbl.setSelectionMode(QAbstractItemView.SingleSelection)
        self.hr_ui.hr_employee_search_box.textChanged.connect(self.filter_hr_employee_table)
        self.hr_ui.hr_employee_sort_box.currentIndexChanged.connect(self.sort_hr_employee_table)
        self.hr_ui.hr_employee_view_back.clicked.connect(self.goto_hr_dashboard)
        self.hr_ui.hr_logout_btn.clicked.connect(self.handle_logout)
        self.hr_ui.hr_employee_view_btn.clicked.connect(self.goto_hr_employee_view)
        self.hr_ui.send_feedback_btn.clicked.connect(self.show_feedback_form)

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
        self.check_net()

        self.hr_ui.dashboard_nav_btn.clicked.connect(self.handle_hr_dashboard_nav)
        self.hr_ui.hr_dashboard_pages.setCurrentWidget(self.hr_ui.db_page_1)
        self.hr_ui.dashboard_nav_btn.setText("Next")

        # --- HR CHARTS SETUP ---
        self.chart_view = None
        self.setup_attendance_area_chart()
        if hasattr(self.hr_ui, "chart_layout1") and self.chart_view:
            self.hr_ui.chart_layout1.addWidget(self.chart_view, 0, 0)

        self.avg_work_hours_chart_view = None
        self.setup_avg_work_hours_line_chart()
        if hasattr(self.hr_ui, "chart_layout2") and self.avg_work_hours_chart_view:
            self.hr_ui.chart_layout2.addWidget(self.avg_work_hours_chart_view, 0, 0)

        self.pie_chart_view = None
        self.setup_attendance_pie_chart()
        if hasattr(self.hr_ui, "chart_layout3") and self.pie_chart_view:
            self.hr_ui.chart_layout3.addWidget(self.pie_chart_view, 0, 0)

        # Change: Top 10 Presents Bar Chart (chart_layout4)
        self.top_present_chart_view = None
        self.setup_top_present_bar_chart()
        if hasattr(self.hr_ui, "chart_layout4") and self.top_present_chart_view:
            self.hr_ui.chart_layout4.addWidget(self.top_present_chart_view, 0, 0)

        # Add: Top 10 Late Bar Chart (chart_layout5)
        self.top_late_chart_view = None
        self.setup_top_late_bar_chart()
        if hasattr(self.hr_ui, "chart_layout5") and self.top_late_chart_view:
            self.hr_ui.chart_layout5.addWidget(self.top_late_chart_view, 0, 0)
        # --- END HR CHARTS SETUP ---

        self.announcement = Announcement(db, hr_data, self.hr_ui)

        # Add report generation button connection
        self.hr_ui.generate_report_btn.clicked.connect(self.generate_report)
        self.report_generator = ReportGeneration(self.db)

    def generate_report(self):
        file_dialog = QFileDialog()
        file_dialog.setDefaultSuffix("pdf")
        output_path, _ = file_dialog.getSaveFileName(
            self.hr_ui,
            "Save Report",
            "",
            "PDF Files (*.pdf)"
        )
        
        if output_path:
            try:
                self.report_generator.generate_report(output_path)
                self.system_logs.log_system_action(f"HR generated report: {output_path}", "Employee")
                self.show_success("Report Generated", "The report has been generated successfully!")
            except Exception as e:
                print(f"Error generating report: {e}")
                self.show_error("Report Generation Failed", "Failed to generate the report. Please try again.")

    def setup_attendance_area_chart(self):
        self.chart = QChart()
        self.present_series = QLineSeries()
        self.absent_series = QLineSeries()
        self.present_series.setName("Present")
        self.absent_series.setName("Absent")

        self.present_area = QAreaSeries(self.present_series)
        self.present_area.setName("Present")
        self.present_area.setColor(QColor(128, 173, 246, 180))
        self.present_area.setBorderColor(QColor(128, 173, 246))
        self.present_area.setOpacity(0.6)

        self.absent_area = QAreaSeries(self.absent_series)
        self.absent_area.setName("Absent")
        self.absent_area.setColor(QColor(48, 9, 154, 180))
        self.absent_area.setBorderColor(QColor(48, 9, 154))
        self.absent_area.setOpacity(0.6)

        self.chart.setBackgroundBrush(QColor(239, 239, 239))

        self.chart.addSeries(self.present_area)
        self.chart.addSeries(self.absent_area)

        self.axis_x = QValueAxis()
        self.axis_x.setTitleText("Day of Month")
        self.axis_x.setLabelFormat("%d")
        self.axis_y = QValueAxis()
        self.axis_y.setTitleText("Count")
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)
        self.present_area.attachAxis(self.axis_x)
        self.present_area.attachAxis(self.axis_y)
        self.absent_area.attachAxis(self.axis_x)
        self.absent_area.attachAxis(self.axis_y)

        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        self.update_attendance_area_chart()

    def update_attendance_area_chart(self):
        self.present_series.clear()
        self.absent_series.clear()
        try:
            cursor = self.db.execute_query(
                """
                SELECT date(created_at) as log_date, present_count, absent_count
                FROM system_logs
                WHERE date(created_at) >= date('now', '-6 days')
                ORDER BY date(created_at)
                """
            )
            data = cursor.fetchall() if cursor else []
            if not data:
                return

            dates = []
            presents = []
            absents = []
            max_y = 1

            for row in data:
                date_str, present, absent = row
                try:
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                    dates.append(date_obj.strftime("%d"))
                    presents.append(int(present))
                    absents.append(int(absent))
                    max_y = max(max_y, int(present), int(absent))
                except Exception:
                    continue

            if not dates:
                return

            self.chart.removeAxis(self.axis_x)
            axis_x = QCategoryAxis()
            axis_x.setTitleText("Day of Month")
            axis_x.setLabelsPosition(QCategoryAxis.AxisLabelsPositionOnValue)
            self.axis_x = axis_x

            point_count = len(dates)
            for i in range(point_count):
                self.present_series.append(i, presents[i])
                self.absent_series.append(i, absents[i])
                axis_x.append(dates[i], i)

            self.axis_x.setRange(0, point_count - 1)
            self.axis_y.setRange(0, max_y)
            self.axis_y.setTickCount(max_y + 1)
            self.axis_y.setLabelFormat("%d")

            self.chart.addAxis(self.axis_x, Qt.AlignBottom)
            self.present_area.attachAxis(self.axis_x)
            self.absent_area.attachAxis(self.axis_x)
        except Exception as e:
            print(f"Error updating HR attendance area chart: {e}")

    def setup_avg_work_hours_line_chart(self):
        self.avg_chart = QChart()
        self.bar_series = QBarSeries()
        self.line_series = QLineSeries()
        self.bar_set = QBarSet("Actual")
        self.bar_series.append(self.bar_set)
        self.line_series.setName("Average")

        pen = self.line_series.pen()
        pen.setWidth(3)
        pen.setColor(QColor(255, 140, 0))
        self.line_series.setPen(pen)

        self.avg_chart.addSeries(self.bar_series)
        self.avg_chart.addSeries(self.line_series)
        self.avg_chart.setBackgroundBrush(QColor(239, 239, 239))

        self.avg_axis_x = QCategoryAxis()
        self.avg_axis_x.setTitleText("Day")
        self.avg_axis_x.setLabelsPosition(QCategoryAxis.AxisLabelsPositionOnValue)

        self.avg_axis_y = QValueAxis()
        self.avg_axis_y.setTitleText("Hours")
        self.avg_axis_y.setLabelFormat("%.1f")
        self.avg_axis_y.setRange(0, 12)

        self.avg_chart.addAxis(self.avg_axis_x, Qt.AlignBottom)
        self.avg_chart.addAxis(self.avg_axis_y, Qt.AlignLeft)
        self.bar_series.attachAxis(self.avg_axis_x)
        self.bar_series.attachAxis(self.avg_axis_y)
        self.line_series.attachAxis(self.avg_axis_x)
        self.line_series.attachAxis(self.avg_axis_y)

        self.avg_chart.legend().setVisible(True)
        self.avg_chart.legend().setAlignment(Qt.AlignBottom)

        self.avg_work_hours_chart_view = QChartView(self.avg_chart)
        self.avg_work_hours_chart_view.setRenderHint(QPainter.Antialiasing)

        self.update_avg_work_hours_line_chart()

    def update_avg_work_hours_line_chart(self):
        self.bar_set.remove(0, self.bar_set.count())
        self.line_series.clear()
        self.avg_chart.removeAxis(self.avg_axis_x)
        self.avg_axis_x = QCategoryAxis()
        self.avg_axis_x.setTitleText("Day")
        self.avg_axis_x.setLabelsPosition(QCategoryAxis.AxisLabelsPositionOnValue)

        try:
            cursor = self.db.execute_query(
                """
                SELECT date(created_at) as log_date, average_work_hours
                FROM system_logs
                WHERE date(created_at) >= date('now', '-6 days')
                ORDER BY date(created_at)
                """
            )
            data = cursor.fetchall() if cursor else []
            if not data:
                return

            days = []
            hours = []
            max_hour = 1

            for idx, row in enumerate(data):
                date_str, avg_hours = row
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                day_label = date_obj.strftime("%a")
                days.append(day_label)
                hours_val = float(avg_hours) if avg_hours is not None else 0
                hours.append(hours_val)
                max_hour = max(max_hour, hours_val)

            for val in hours:
                self.bar_set << val

            color = QColor(112, 205, 152)
            color.setAlphaF(0.6)
            self.bar_set.setColor(color)

            avg_val = sum(hours) / len(hours) if hours else 0

            for i in range(len(days)):
                self.line_series.append(i, avg_val)

            for i, label in enumerate(days):
                self.avg_axis_x.append(label, i)

            self.avg_axis_x.setRange(0, len(days) - 1)
            self.avg_chart.addAxis(self.avg_axis_x, Qt.AlignBottom)
            self.bar_series.attachAxis(self.avg_axis_x)
            self.line_series.attachAxis(self.avg_axis_x)
            self.avg_axis_y.setRange(0, max(8, int(max_hour + 1)))
            self.avg_axis_y.setTickCount(min(13, int(max_hour + 2)))
        except Exception as e:
            print(f"Error updating HR avg work hours line chart: {e}")

    def setup_attendance_pie_chart(self):
        self.pie_chart = QChart()
        self.pie_series = QPieSeries()
        self.pie_chart.addSeries(self.pie_series)
        self.pie_chart.setBackgroundBrush(QColor(239, 239, 239))
        self.pie_chart.legend().setVisible(True)
        self.pie_chart.legend().setAlignment(Qt.AlignBottom)
        self.pie_chart_view = QChartView(self.pie_chart)
        self.pie_chart_view.setRenderHint(QPainter.Antialiasing)
        self.update_attendance_pie_chart()

    def update_attendance_pie_chart(self):
        self.pie_series.clear()
        try:
            today_date = datetime.now().strftime("%Y-%m-%d")
            cursor = self.db.execute_query(
                "SELECT COUNT(DISTINCT employee_id) FROM attendance_logs WHERE date = ? AND employee_id IN (SELECT employee_id FROM Employee WHERE is_hr = 0)",
                (today_date,)
            )
            present = cursor.fetchone()[0] if cursor else 0

            cursor = self.db.execute_query(
                "SELECT COUNT(*) FROM Employee WHERE is_hr = 0 AND status = 'Active' AND employee_id NOT IN (SELECT DISTINCT employee_id FROM attendance_logs WHERE date = ?)",
                (today_date,)
            )
            absent = cursor.fetchone()[0] if cursor else 0

            total = present + absent
            if total == 0:
                self.pie_series.append("No Data", 1)
                self.pie_series.slices()[0].setColor(QColor(200, 200, 200))
                self.pie_series.slices()[0].setLabelVisible(True)
            else:
                present_pct = (present / total) * 100
                absent_pct = (absent / total) * 100
                present_slice = self.pie_series.append(f"Present ({present_pct:.1f}%)", present)
                absent_slice = self.pie_series.append(f"Absent ({absent_pct:.1f}%)", absent)
                present_slice.setColor(QColor(255, 174, 53))
                absent_slice.setColor(QColor(240, 86, 68))
                present_slice.setLabelVisible(True)
                absent_slice.setLabelVisible(True)
        except Exception as e:
            print(f"Error updating HR attendance pie chart: {e}")

    def setup_top_present_bar_chart(self):
        # Top 10 employees by presence count (horizontal bar chart, modern look, 60% transparency)
        self.top_present_chart = QChart()
        self.top_present_series = QHorizontalBarSeries()
        self.top_present_set = QBarSet("Presents")
        self.top_present_series.append(self.top_present_set)
        # Modern color with 60% transparency
        present_color = QColor(76, 175, 80)  # Material green
        present_color.setAlphaF(0.6)
        self.top_present_set.setColor(present_color)
        self.top_present_chart.addSeries(self.top_present_series)
        self.top_present_chart.setBackgroundBrush(QColor(245, 245, 245))
        self.top_present_chart.setTitleFont(self.hr_ui.font())
        self.top_present_chart.setDropShadowEnabled(True)

        self.top_present_axis_y = QBarCategoryAxis()
        self.top_present_axis_x = QValueAxis()
        self.top_present_axis_x.setTitleText("Presence Count")
        self.top_present_axis_x.setLabelFormat("%d")
        self.top_present_chart.addAxis(self.top_present_axis_y, Qt.AlignLeft)
        self.top_present_chart.addAxis(self.top_present_axis_x, Qt.AlignBottom)
        self.top_present_series.attachAxis(self.top_present_axis_y)
        self.top_present_series.attachAxis(self.top_present_axis_x)
        self.top_present_chart.legend().setVisible(False)

        self.top_present_chart_view = QChartView(self.top_present_chart)
        self.top_present_chart_view.setRenderHint(QPainter.Antialiasing)
        self.update_top_present_bar_chart()

    def update_top_present_bar_chart(self):
        self.top_present_set.remove(0, self.top_present_set.count())
        self.top_present_axis_y.clear()
        try:
            cursor = self.db.execute_query(
                """
                SELECT e.last_name, e.first_name, e.middle_initial, COUNT(a.log_id) as present_count
                FROM Employee e
                LEFT JOIN attendance_logs a ON e.employee_id = a.employee_id AND a.remarks = 'Clock In'
                WHERE e.is_hr = 0
                GROUP BY e.employee_id
                ORDER BY present_count DESC
                LIMIT 10
                """
            )
            data = cursor.fetchall() if cursor else []
            categories = []
            max_present = 1
            for row in data:
                last, first, mi, count = row
                name = f"{last}, {first} {mi or ''}".strip()
                categories.append(name)
                val = int(count or 0)
                self.top_present_set << val
                max_present = max(max_present, val)
            self.top_present_axis_y.append(categories)
            self.top_present_axis_x.setRange(0, max(1, max_present))
        except Exception as e:
            print(f"Error updating top present bar chart: {e}")

    def setup_top_late_bar_chart(self):
        # Top 10 employees by lateness count (horizontal bar chart, modern look, 60% transparency)
        self.top_late_chart = QChart()
        self.top_late_series = QHorizontalBarSeries()
        self.top_late_set = QBarSet("Lates")
        self.top_late_series.append(self.top_late_set)
        # Modern color with 60% transparency
        late_color = QColor(244, 67, 54)  # Material red
        late_color.setAlphaF(0.6)
        self.top_late_set.setColor(late_color)
        self.top_late_chart.addSeries(self.top_late_series)
        self.top_late_chart.setBackgroundBrush(QColor(245, 245, 245))
        self.top_late_chart.setTitleFont(self.hr_ui.font())
        self.top_late_chart.setDropShadowEnabled(True)

        self.top_late_axis_y = QBarCategoryAxis()
        self.top_late_axis_x = QValueAxis()
        self.top_late_axis_x.setTitleText("Lateness Count")
        self.top_late_axis_x.setLabelFormat("%d")
        self.top_late_chart.addAxis(self.top_late_axis_y, Qt.AlignLeft)
        self.top_late_chart.addAxis(self.top_late_axis_x, Qt.AlignBottom)
        self.top_late_series.attachAxis(self.top_late_axis_y)
        self.top_late_series.attachAxis(self.top_late_axis_x)
        self.top_late_chart.legend().setVisible(False)

        self.top_late_chart_view = QChartView(self.top_late_chart)
        self.top_late_chart_view.setRenderHint(QPainter.Antialiasing)
        self.update_top_late_bar_chart()

    def update_top_late_bar_chart(self):
        self.top_late_set.remove(0, self.top_late_set.count())
        self.top_late_axis_y.clear()
        try:
            cursor = self.db.execute_query(
                "SELECT last_name, first_name, middle_initial, late_count FROM Employee WHERE is_hr = 0 ORDER BY CAST(late_count AS INTEGER) DESC LIMIT 10"
            )
            data = cursor.fetchall() if cursor else []
            categories = []
            max_late = 1
            for row in data:
                last, first, mi, count = row
                name = f"{last}, {first} {mi or ''}".strip()
                categories.append(name)
                val = int(count or 0)
                self.top_late_set << val
                max_late = max(max_late, val)
            self.top_late_axis_y.append(categories)
            self.top_late_axis_x.setRange(0, max(1, max_late))
        except Exception as e:
            print(f"Error updating top late bar chart: {e}")

    def show_feedback_form(self):
        self.system_logs.log_system_action("HR opened feedback form", "Employee")
        self.feedback = Feedback(self.db, self.hr_data)
        self.feedback.feedback_ui.show()
        
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
                "WHERE date = ? AND is_late = 1 AND employee_id IN (SELECT employee_id FROM Employee WHERE is_hr = 0)", 
                (today_date,)
            )
            late_employees = cursor.fetchone()[0] if cursor else 0

            cursor = self.db.execute_query(
                "SELECT COUNT(*) FROM Employee WHERE is_hr = 0 AND status = 'Active' AND employee_id NOT IN ("
                "SELECT DISTINCT employee_id FROM attendance_logs WHERE date = ?)", 
                (today_date,)
            )
            absent_employees = cursor.fetchone()[0] if cursor else 0

            # --- NEW: Shift and overtime labels (copied from Admin) ---
            # Morning shift
            cursor = self.db.execute_query(
                "SELECT COUNT(*) FROM Employee WHERE is_hr = 0 AND status = 'Active' AND schedule = '6am to 2pm'"
            )
            morning_total = cursor.fetchone()[0] if cursor else 0
            cursor = self.db.execute_query(
                "SELECT COUNT(DISTINCT e.employee_id) FROM Employee e "
                "JOIN attendance_logs a ON e.employee_id = a.employee_id "
                "WHERE e.is_hr = 0 AND e.status = 'Active' AND e.schedule = '6am to 2pm' AND a.date = ? AND a.remarks = 'Clock In'",
                (today_date,)
            )
            morning_present = cursor.fetchone()[0] if cursor else 0

            # Afternoon shift
            cursor = self.db.execute_query(
                "SELECT COUNT(*) FROM Employee WHERE is_hr = 0 AND status = 'Active' AND schedule = '2pm to 10pm'"
            )
            afternoon_total = cursor.fetchone()[0] if cursor else 0
            cursor = self.db.execute_query(
                "SELECT COUNT(DISTINCT e.employee_id) FROM Employee e "
                "JOIN attendance_logs a ON e.employee_id = a.employee_id "
                "WHERE e.is_hr = 0 AND e.status = 'Active' AND e.schedule = '2pm to 10pm' AND a.date = ? AND a.remarks = 'Clock In'",
                (today_date,)
            )
            afternoon_present = cursor.fetchone()[0] if cursor else 0

            # Night shift
            cursor = self.db.execute_query(
                "SELECT COUNT(*) FROM Employee WHERE is_hr = 0 AND status = 'Active' AND schedule = '10pm to 6am'"
            )
            night_total = cursor.fetchone()[0] if cursor else 0
            cursor = self.db.execute_query(
                "SELECT COUNT(DISTINCT e.employee_id) FROM Employee e "
                "JOIN attendance_logs a ON e.employee_id = a.employee_id "
                "WHERE e.is_hr = 0 AND e.status = 'Active' AND e.schedule = '10pm to 6am' AND a.date = ? AND a.remarks = 'Clock In'",
                (today_date,)
            )
            night_present = cursor.fetchone()[0] if cursor else 0

            # --- NEW: Average overtime calculation ---
            cursor = self.db.execute_query(
                "SELECT employee_id FROM attendance_logs WHERE date = ? AND remarks = 'Clock In' AND employee_id IN (SELECT employee_id FROM Employee WHERE is_hr = 0)",
                (today_date,)
            )
            employee_ids = [row[0] for row in cursor.fetchall()] if cursor else []
            total_overtime = 0
            overtime_count = 0
            for emp_id in employee_ids:
                cur = self.db.execute_query(
                    "SELECT time, remarks FROM attendance_logs WHERE employee_id = ? AND date = ? ORDER BY time ASC",
                    (emp_id, today_date)
                )
                logs = cur.fetchall() if cur else []
                clock_in_time = None
                clock_out_time = None
                for log in logs:
                    if log[1] == "Clock In" and not clock_in_time:
                        clock_in_time = log[0]
                    elif log[1] == "Clock Out":
                        clock_out_time = log[0]
                if clock_in_time and clock_out_time:
                    try:
                        t1 = datetime.strptime(f"{today_date} {clock_in_time}", "%Y-%m-%d %H:%M:%S")
                        t2 = datetime.strptime(f"{today_date} {clock_out_time}", "%Y-%m-%d %H:%M:%S")
                        worked_hours = (t2 - t1).total_seconds() / 3600
                        overtime = worked_hours - 8
                        if overtime > 0:
                            total_overtime += overtime
                            overtime_count += 1
                    except Exception:
                        continue
            ave_overtime = round(total_overtime / overtime_count, 2) if overtime_count > 0 else 0

            # --- Set HR dashboard labels ---
            self.hr_ui.hr_total_employee_lbl.setText(f"{total_employees}/{total_employees}")
            self.hr_ui.hr_active_employee_lbl.setText(str(active_employees))
            self.hr_ui.hr_logged_employee_lbl.setText(str(logged_employees))
            self.hr_ui.hr_late_employee_lbl.setText(str(late_employees))
            self.hr_ui.hr_absent_employee_lbl.setText(str(absent_employees))

            # --- Set new shift and overtime labels ---
            if hasattr(self.hr_ui, "morning_shift_lbl"):
                self.hr_ui.morning_shift_lbl.setText(f"{morning_present}/{morning_total}")
            if hasattr(self.hr_ui, "afternoon_shift_lbl"):
                self.hr_ui.afternoon_shift_lbl.setText(f"{afternoon_present}/{afternoon_total}")
            if hasattr(self.hr_ui, "night_shift_lbl"):
                self.hr_ui.night_shift_lbl.setText(f"{night_present}/{night_total}")
            if hasattr(self.hr_ui, "ave_overtime_lbl"):
                self.hr_ui.ave_overtime_lbl.setText(str(ave_overtime))

        except sqlite3.Error as e:
            print(f"Database error while updating HR dashboard labels: {e}")

    def update_date_today(self):
        current_date = datetime.now()
        formatted_date = current_date.strftime("%a, %b %d, %Y")
        self.hr_ui.date_today.setText(formatted_date)

    def load_hr_employee_table(self):
        self.system_logs.log_system_action("Load employees into the HR employee table.", "Employee")
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
                    "status": employee[10],
                    "profile_picture": employee[13]
                }
                self.hr_employees.append(employee_data)
                self.add_hr_employee_to_table(employee_data)
                self.update_hr_dashboard_labels()
        except sqlite3.Error as e:
            self.system_logs.log_system_action(f"Database error while loading HR employees: {e}", "Employee")

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
        self.system_logs.log_system_action("The HR, has selected an employee to view.", "Employee")
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
        self.display_picture(self.hr_ui.hr_view_employee_picture, employee_data['profile_picture'])
        
    def display_picture(self, label, picture_path):
        if (picture_path and os.path.exists(picture_path)):
            pixmap = QPixmap(picture_path)
            pixmap = pixmap.scaled(170, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            label.setPixmap(pixmap)
        else:
            label.setPixmap(QPixmap())

    def goto_hr_dashboard(self):
        self.system_logs.log_system_action("Going back to the HR Employee dashboard.", "Employee")
        dashboard_page = self.hr_ui.hr_employee_sc_pages.indexOf(self.hr_ui.hr_employee_dashboard_page)
        self.hr_ui.hr_employee_sc_pages.setCurrentIndex(dashboard_page)

    def handle_logout(self):
        current_time = datetime.now()
        current_date = current_time.strftime("%Y-%m-%d")
        self.db.execute_query("INSERT INTO attendance_logs (employee_id, date, time, remarks) VALUES (?, ?, ?, ?)",
                              (self.hr_data["employee_id"], current_date, current_time.strftime("%H:%M:%S"), "Clock Out"))
        self.hr_ui.close()
        global_home_ui.showMaximized()
        self.system_logs.log_system_action("The HR logged out.", "Employee")

    def load_hr_attendance_logs_table(self):
        self.system_logs.log_system_action("Load all attendance logs for employees only into the table.", "AttendanceLog")
        try:
            cursor = self.db.execute_query(
                "SELECT employee_id, remarks, date, time FROM attendance_logs WHERE employee_id IN (SELECT employee_id FROM Employee WHERE is_hr = 0)"
            )
            logs = cursor.fetchall() if cursor else []

            self.hr_ui.hr_attedance_logs_tbl.setRowCount(0)
            for log in logs:
                self.add_attendance_log_to_table(self.hr_ui.hr_attedance_logs_tbl, log)
        except sqlite3.Error as e:
            self.system_logs.log_system_action(f"Database error while loading HR attendance logs: {e}", "AttendanceLog")
            print(f"Database error while loading HR attendance logs: {e}")

    def add_attendance_log_to_table(self, table, log):
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
        sort_option = self.hr_ui.hr_attedance_logs_sort.currentText()

        logs = []
        for row in range(self.hr_ui.hr_attedance_logs_tbl.rowCount()):
            log = [
                self.hr_ui.hr_attedance_logs_tbl.item(row, col).text()
                for col in range(self.hr_ui.hr_attedance_logs_tbl.columnCount())
            ]
            logs.append(log)

        if sort_option == "By Date:":
            logs.sort(key=lambda x: x[2]) 
        elif sort_option == "By Time:":
            logs.sort(key=lambda x: x[3]) 
        elif sort_option == "By Account ID:":
            logs.sort(key=lambda x: x[0])  
        elif sort_option == "By Remarks:":
            logs.sort(key=lambda x: x[1])  

        self.hr_ui.hr_attedance_logs_tbl.setRowCount(0)
        for log in logs:
            self.add_attendance_log_to_table(self.hr_ui.hr_attedance_logs_tbl, log)

    def load_hr_employee_attendance_logs(self, employee_id):
        self.system_logs.log_system_action("Load attendance logs for the selected employee.", "AttendanceLog")
        try:
            cursor = self.db.execute_query(
                "SELECT date, time, remarks FROM attendance_logs WHERE employee_id = ?", (employee_id,)
            )
            logs = cursor.fetchall() if cursor else []

            self.hr_ui.hr_employee_logs_tbl.setRowCount(0)
            for log in logs:
                self.add_log_to_table(self.hr_ui.hr_employee_logs_tbl, log)
        except sqlite3.Error as e:
            self.system_logs.log_system_action(f"Database error while loading HR employee attendance logs: {e}", "AttendanceLog")
            print(f"Database error while loading HR employee attendance logs: {e}")

    def add_log_to_table(self, table, log):

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
        
    def check_net(self):
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=5)
            return True
        except OSError:
            toast = Toast(self.admin_ui)
            toast.setTitle("No Internet Connection")
            toast.setText("Please check your internet connection and try again.")
            toast.setOffset(40, 45)
            toast.setBorderRadius(6)
            toast.applyPreset(ToastPreset.ERROR)
            toast.setBackgroundColor(QColor('#ffb7b6'))
            toast.setPosition(ToastPosition.TOP_RIGHT)
            toast.setShowDurationBar(False)
            toast.setDuration(0) 
            toast.show()
            return False

    def handle_hr_dashboard_nav(self):

        current_widget = self.hr_ui.hr_dashboard_pages.currentWidget()
        if current_widget == self.hr_ui.db_page_1:
            self.hr_ui.hr_dashboard_pages.setCurrentWidget(self.hr_ui.db_page_2)
            self.hr_ui.dashboard_nav_btn.setText("Back")
        else:
            self.hr_ui.hr_dashboard_pages.setCurrentWidget(self.hr_ui.db_page_1)
            self.hr_ui.dashboard_nav_btn.setText("Next")
            
    def show_success(self, title, message):
        chime.theme('chime')
        chime.success()
        toast = Toast(self.hr_ui)
        toast.setTitle(title)
        toast.setText(message)
        toast.setDuration(2000)
        toast.setOffset(25, 35)
        toast.setBorderRadius(6)
        toast.applyPreset(ToastPreset.SUCCESS)
        toast.setBackgroundColor(QColor('#FFFFFF'))
        toast.setPositionRelativeToWidget(self.hr_ui.hr_home_tabs)
        toast.setPosition(ToastPosition.TOP_RIGHT)
        toast.show()

    def show_error(self, title, message):
        chime.theme('big-sur')
        chime.warning()
        toast = Toast(self.hr_ui)
        toast.setTitle(title)
        toast.setText(message)
        toast.setDuration(2000)
        toast.setOffset(25, 35)
        toast.setBorderRadius(6)
        toast.applyPreset(ToastPreset.ERROR)
        toast.setBackgroundColor(QColor('#FFFFFF'))
        toast.setPositionRelativeToWidget(self.hr_ui.hr_home_tabs)
        toast.setPosition(ToastPosition.TOP_RIGHT)
        toast.show()

class Home:
    password_changed = False
    failed_attempts = 0 

    def __init__(self, db):
        self.db = db
        self.system_logs = SystemLogs(db)
        self.loader = QUiLoader()
        self.home_ui = self.loader.load("ui/home.ui")
        self.home_ui.setWindowIcon(QIcon('resources/logo.ico'))
        self.home_ui.setWindowTitle("EALS")
        self.home_ui.main_page.setCurrentWidget(self.home_ui.home_page)
        self.admin_id = None
        self.admin_password = None
        self.check_initial_setup()
        self.update_date_today()
        self.home_ui.home_login_btn.clicked.connect(self.handle_login)
        self.home_ui.bio1_next.clicked.connect(self.goto_bio2)
        self.home_ui.bio2_next.clicked.connect(self.goto_result_prompt)
        self.employee_data = None  
        self.system_logs.log_system_action("The home UI has been loaded.", "SystemSettings")
        self.home_ui.pass_visibility_button.clicked.connect(self.toggle_password_visibility)
        self.home_ui.forgot_pass_btn.clicked.connect(self.goto_forgot_password)
        self.password_visible = False
        
    def update_date_today(self):
        current_date = datetime.now()
        formatted_date = current_date.strftime("%a, %b %d, %Y")
        self.home_ui.date_today.setText(formatted_date)
        self.system_logs.log_system_action("Setting current date to the home UI.", "SystemSettings")

    def validate_hr_attendance(self, hr_data):
        current_time = datetime.now()
        current_date = current_time.strftime("%Y-%m-%d")
        current_hour = current_time.hour

        
        cursor = self.db.execute_query("SELECT time, remarks FROM attendance_logs WHERE employee_id = ? AND date = ?", 
                                       (hr_data["employee_id"], current_date))
        attendance = cursor.fetchone() if cursor else None

        if attendance:
            
            return True
        else:
           
            schedule_start, schedule_end = self.parse_schedule(hr_data["schedule"])
            if not self.is_within_schedule(schedule_start, schedule_end, current_hour):
                self.show_error("Invalid Login", "You cannot log in outside your scheduled shift.")
                return False

        return True

    def handle_login(self):
        user_id = self.home_ui.home_id_box.text()
        password = self.home_ui.home_pass_box.text()

        try:
            cursor = self.db.execute_query("SELECT password, password_changed FROM Admin WHERE admin_id = ?", (user_id,))
            admin_result = cursor.fetchone() if cursor else None

            if admin_result:
                db_password, password_changed = admin_result
                try:
                    PASSWORD_HASHER.verify(db_password, password)
                    Home.failed_attempts = 0  
                    Home.password_changed = password_changed
                    if password_changed:
                        self.system_logs.log_system_action("The password is already changed, going to the admin UI.", "Admin")
                        self.show_success("Login Successful", "Welcome back, Admin!")
                        self.goto_admin_ui()
                    else:
                        self.system_logs.log_system_action("The password is not changed executing Change Password Prompt", "Admin")
                        self.goto_change_pass()
                    self.home_ui.home_id_box.clear() 
                    self.home_ui.home_pass_box.clear()
                    self.home_ui.home_pass_box.setEchoMode(QLineEdit.Password)
                    return
                except argon2.exceptions.VerifyMismatchError:
                    Home.failed_attempts += 1
                    self.system_logs.log_system_action("An invalid Admin login attempt has been made.", "Admin")
                    if Home.failed_attempts >= 3:
                        self.prompt_password_change()
                    else:
                        self.show_error("Invalid credentials", "Please enter valid admin ID and password")
                    return

            cursor = self.db.execute_query("SELECT * FROM Employee WHERE employee_id = ?", (user_id,))
            employee_result = cursor.fetchone() if cursor else None

            if employee_result:
                if employee_result[10] == "Inactive":
                    self.show_error("Invalid credentials", "Please enter valid employee ID and password")
                    self.system_logs.log_system_action("An inactive employee attempted to log in.", "Employee")
                    return
                    
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
                    "password_changed": employee_result[12],
                    "profile_picture": employee_result[13],
                    "email": employee_result[14],
                }
                
                db_password = employee_result[11]
                try:
                    PASSWORD_HASHER.verify(db_password, password)
                    if not employee_data["password_changed"]:
                        self.changepass = ChangePassword(self.db, employee_data["employee_id"], "employee")
                        self.changepass.change_pass_ui.show()
                        return
                        
                    if employee_data["is_hr"]:
                        if self.validate_hr_attendance(employee_data):
                            self.goto_hr_ui(employee_data)
                            self.home_ui.home_id_box.clear() 
                            self.home_ui.home_pass_box.clear()
                            self.home_ui.home_pass_box.setEchoMode(QLineEdit.Password)
                            self.show_success("Login Successful", "Welcome back, HR!")
                            self.system_logs.log_system_action("A user is logged in as HR", "Employee")
                    else:
                        self.employee_data = employee_data
                        if self.validate_attendance():
                            self.system_logs.log_system_action("A user is logged in as an employee", "Employee")
                            self.goto_bio1()
                except argon2.exceptions.VerifyMismatchError:
                    self.show_error("Invalid credentials", "Please enter valid employee ID and password")
                    self.system_logs.log_system_action("An invalid login attempt has been made.", "Employee")
            else:
                self.show_error("Invalid credentials", "Please enter valid employee ID and password")
                self.system_logs.log_system_action("An invalid login attempt has been made.", "Employee")
        except sqlite3.Error as e:
            print(f"Database error during login: {e}")

    def prompt_password_change(self):
        dialog = QMessageBox()
        dialog.setIcon(QMessageBox.Warning)
        dialog.setText("Too Many Failed Attempts")
        dialog.setInformativeText("You have entered the wrong password 3 times. Would you like to change your password?")
        dialog.setWindowTitle("Change Password")
        dialog.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)
        dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dialog.setDefaultButton(QMessageBox.Yes)

        response = dialog.exec()
        if response == QMessageBox.Yes:
            self.goto_admin_change_pass_ui()  # Redirect to the new admin change password UI
        else:
            Home.failed_attempts = 0
            
    def goto_admin_change_pass_ui(self):
        self.admin_change_pass_ui = QUiLoader().load("ui/admin_change_pass.ui")
        self.admin_change_pass_ui.setWindowTitle("Admin Change Password")
        self.admin_change_pass_ui.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)
        self.admin_change_pass_ui.setWindowModality(Qt.ApplicationModal)
        
        self.admin_id = self.home_ui.home_id_box.text()

        self.admin_change_pass_ui.change_pass_note.setText("For security purposes, please enter the admin default password below, then choose a new password and confirm it. Make sure your new password is at least 8 characters long.")
        self.admin_change_pass_ui.default_visibility_btn.clicked.connect(self.toggle_default_visibility)
        self.admin_change_pass_ui.np_visibility_btn.clicked.connect(self.toggle_np_visibility)
        self.admin_change_pass_ui.changepass_visibility_btn.clicked.connect(self.toggle_changepass_visibility)

        # Connect the change password button
        self.admin_change_pass_ui.admin_change_pass_btn.clicked.connect(self.validate_and_change_admin_password)

        self.admin_change_pass_ui.show()
        
    def toggle_default_visibility(self):
        if self.admin_change_pass_ui.default_pass_cp_box.echoMode() == QLineEdit.Password:
            self.admin_change_pass_ui.default_pass_cp_box.setEchoMode(QLineEdit.Normal)
        else:
            self.admin_change_pass_ui.default_pass_cp_box.setEchoMode(QLineEdit.Password)

    def toggle_np_visibility(self):
        if self.admin_change_pass_ui.change_pass_np_box.echoMode() == QLineEdit.Password:
            self.admin_change_pass_ui.change_pass_np_box.setEchoMode(QLineEdit.Normal)
        else:
            self.admin_change_pass_ui.change_pass_np_box.setEchoMode(QLineEdit.Password)

    def toggle_changepass_visibility(self):
        if self.admin_change_pass_ui.change_pass_confirm_box.echoMode() == QLineEdit.Password:
            self.admin_change_pass_ui.change_pass_confirm_box.setEchoMode(QLineEdit.Normal)
        else:
            self.admin_change_pass_ui.change_pass_confirm_box.setEchoMode(QLineEdit.Password)

    def validate_and_change_admin_password(self):
        default_password = self.admin_change_pass_ui.default_pass_cp_box.text()
        new_password = self.admin_change_pass_ui.change_pass_np_box.text()
        confirm_password = self.admin_change_pass_ui.change_pass_confirm_box.text()

        try:
            
            if not self.admin_id:
                self.admin_change_pass_ui.change_pass_note.setText("Error: Admin ID is not set. Please log in again.")
                self.admin_change_pass_ui.change_pass_note.setStyleSheet("color: red; border: none;")
                return
            
            # Fetch the default password from the database
            cursor = self.db.execute_query("SELECT default_pass FROM Admin WHERE admin_id = ?", (self.admin_id,))
            result = cursor.fetchone()

            if not result:
                self.admin_change_pass_ui.change_pass_note.setText("Error: Failed to fetch admin data. Please try again.")
                self.admin_change_pass_ui.change_pass_note.setStyleSheet("color: red; border: none;")
                return

            db_default_password = result[0]

            # Verify the default password
            try:
                PASSWORD_HASHER.verify(db_default_password, default_password)
            except argon2.exceptions.VerifyMismatchError:
                self.admin_change_pass_ui.change_pass_note.setText("Invalid Password: The default password you entered is incorrect.")
                self.admin_change_pass_ui.change_pass_note.setStyleSheet("color: red; border: none;")
                return

            # Validate new password
            if not new_password or not confirm_password:
                self.admin_change_pass_ui.change_pass_note.setText("Error: All fields are required.")
                self.admin_change_pass_ui.change_pass_note.setStyleSheet("color: red; border: none;")
                return

            if new_password != confirm_password:
                self.admin_change_pass_ui.change_pass_note.setText("Mismatch: The new password and confirmation password do not match.")
                self.admin_change_pass_ui.change_pass_note.setStyleSheet("color: red; border: none;")
                return

            if len(new_password) < 8:
                self.admin_change_pass_ui.change_pass_note.setText("Weak Password: The new password must be at least 8 characters long.")
                self.admin_change_pass_ui.change_pass_note.setStyleSheet("color: red; border: none;")
                return

            # Hash the new password and update the database
            hashed_password = PASSWORD_HASHER.hash(new_password)
            self.db.execute_query(
                "UPDATE Admin SET password = ?, password_changed = TRUE WHERE admin_id = ?",
                (hashed_password, self.admin_id)
            )

            self.system_logs.log_system_action("Admin password changed successfully.", "Admin")
            self.show_success("Password Changed Successfully", "Your password has been updated. Please use the new password for future logins.")

            self.admin_change_pass_ui.close()

        except sqlite3.Error as e:
            self.system_logs.log_system_action(f"Database error during admin password change: {e}", "Admin")
            print(f"Database error during password change: {e}")
            self.show_error("Database Error", "An error occurred while changing the password. Please try again.")
            
    def validate_attendance(self):
        if not self.employee_data:
            return False

        current_time = datetime.now()
        current_date = current_time.strftime("%Y-%m-%d")
        current_hour = current_time.hour

        cursor = self.db.execute_query(
            "SELECT attedance_count FROM Employee WHERE employee_id = ?",
            (self.employee_data["employee_id"],)
        )
        if cursor:
            result = cursor.fetchone()
            attendance_count = int(result[0]) if result and result[0] else 0
        else:
            attendance_count = 0

        if self.employee_data["schedule"] == "10pm to 6am":
            if current_hour >= 22:
                cursor = self.db.execute_query(
                    "SELECT COUNT(*) FROM attendance_logs WHERE employee_id = ? AND date = ? AND time >= '22:00:00'",
                    (self.employee_data["employee_id"], current_date)
                )
                night_logs = cursor.fetchone()[0] if cursor else 0
                if night_logs >= 2:
                    self.show_warning("Attendance Error", "You have already completed your attendance for tonight's shift.")
                    return False
            elif current_hour < 6:
                previous_date = (current_time - timedelta(days=1)).strftime("%Y-%m-%d")
                cursor = self.db.execute_query(
                    "SELECT COUNT(*) FROM attendance_logs WHERE employee_id = ? AND date = ? AND time >= '22:00:00'",
                    (self.employee_data["employee_id"], previous_date)
                )
                previous_night_logs = cursor.fetchone()[0] if cursor else 0
                
                cursor = self.db.execute_query(
                    "SELECT COUNT(*) FROM attendance_logs WHERE employee_id = ? AND date = ? AND time <= '06:00:00'",
                    (self.employee_data["employee_id"], current_date)
                )
                early_morning_logs = cursor.fetchone()[0] if cursor else 0
                
                total_logs = previous_night_logs + early_morning_logs
                if total_logs >= 2:
                    self.show_warning("Attendance Error", "You have already completed your attendance for this shift.")
                    return False
        else:
            cursor = self.db.execute_query(
                "SELECT COUNT(*) FROM attendance_logs WHERE employee_id = ? AND date = ?",
                (self.employee_data["employee_id"], current_date)
            )
            attendance_count = cursor.fetchone()[0] if cursor else 0
            
            if attendance_count >= 2:
                self.show_warning("Attendance Error", "You have already logged your attendance twice today.")
                return False

        cursor = self.db.execute_query(
            "SELECT time, remarks FROM attendance_logs WHERE employee_id = ? AND date = ?",
            (self.employee_data["employee_id"], current_date)
        )
        attendance = cursor.fetchone() if cursor else None

        if attendance:
            log_time_str = attendance[0]
            log_time = datetime.strptime(f"{current_date} {log_time_str}", "%Y-%m-%d %H:%M:%S")

            if attendance[1] == "Clock In" and (current_time - log_time).total_seconds() < 8 * 3600:
                dialog = QMessageBox()
                dialog.setIcon(QMessageBox.Warning)
                dialog.setText("Clock Out Warning")
                dialog.setInformativeText("You have logged in less than 8 hours ago. Are you sure you want to clock out?")
                dialog.setWindowTitle("Warning")
                dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                dialog.setDefaultButton(QMessageBox.No)

                response = dialog.exec()
                if response == QMessageBox.No:
                    return False
            self.employee_data["remarks"] = "Clock Out"
        else:
            schedule_start, schedule_end = self.parse_schedule(self.employee_data["schedule"])
            current_hour = current_time.hour
            if not self.is_within_schedule(schedule_start, schedule_end, current_hour):
                self.show_warning("Invalid Login", "You cannot log in outside your scheduled shift.")
                return False

            if self.employee_data["schedule"] == "10pm to 6am":
                if current_hour < 6:
                    scheduled_date = (current_time - timedelta(days=1)).date()
                else:
                    scheduled_date = current_time.date()
                scheduled_time = datetime.combine(scheduled_date, datetime.min.time()).replace(hour=22, minute=0, second=0, microsecond=0)
            else:
                scheduled_time = current_time.replace(hour=schedule_start, minute=0, second=0, microsecond=0)
                    
            late_threshold = scheduled_time + timedelta(minutes=15)
            is_late = current_time > late_threshold

            self.employee_data["remarks"] = "Clock In"
            self.employee_data["is_late"] = is_late
            self.employee_data["was_late"] = is_late

            if is_late:
                cursor = self.db.execute_query(
                    "SELECT late_count FROM Employee WHERE employee_id = ?",
                    (self.employee_data["employee_id"],)
                )
                late_count = int(cursor.fetchone()[0] or 0) if cursor else 0
                late_count += 1
                self.db.execute_query(
                    "UPDATE Employee SET late_count = ? WHERE employee_id = ?",
                    (late_count, self.employee_data["employee_id"])
                )

        new_count = attendance_count + 1
        self.db.execute_query(
            "UPDATE Employee SET attedance_count = ? WHERE employee_id = ?",
            (new_count, self.employee_data["employee_id"])
        )

        return True

    def goto_hr_ui(self, hr_data):

        current_time = datetime.now()
        current_date = current_time.strftime("%Y-%m-%d")
        self.db.execute_query("INSERT INTO attendance_logs (employee_id, date, time, remarks) VALUES (?, ?, ?, ?)",
                              (hr_data["employee_id"], current_date, current_time.strftime("%H:%M:%S"), hr_data.get("remarks", "Clock In")))
        global_home_ui.close()
        self.hr = HR(self.db, hr_data)
        self.hr.hr_ui.showMaximized()

    def goto_bio1(self):
        if self.employee_data:
            def update_picture():
                pixmap = QPixmap(self.employee_data["profile_picture"])
                pixmap = pixmap.scaled(self.home_ui.bio1_employee_pic.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.home_ui.bio1_employee_pic.setPixmap(pixmap)

            QTimer.singleShot(0, update_picture)

            self.home_ui.bio1_employee_name.setText(f"<b>Name:</b> {self.employee_data['first_name']} {self.employee_data['last_name']}")
            self.home_ui.bio1_employee_department.setText(f"<b>Department:</b> {self.employee_data['department']}")
            self.home_ui.bio1_employee_position.setText(f"<b>Position:</b> {self.employee_data['position']}")
            self.home_ui.bio1_employee_shift.setText(f"<b>Shift:</b> {self.employee_data['schedule']}")

        bio1_page = self.home_ui.main_page.indexOf(self.home_ui.bio1_page)
        self.home_ui.main_page.setCurrentIndex(bio1_page)

    def goto_bio2(self):
        if self.employee_data:
            def update_picture():
                pixmap = QPixmap(self.employee_data["profile_picture"])
                pixmap = pixmap.scaled(self.home_ui.bio2_employee_pic.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.home_ui.bio2_employee_pic.setPixmap(pixmap)

            QTimer.singleShot(0, update_picture)

            self.home_ui.bio2_employee_name.setText(f"<b>Name:</b> {self.employee_data['first_name']} {self.employee_data['last_name']}")
            self.home_ui.bio2_employee_department.setText(f"<b>Department:</b> {self.employee_data['department']}")
            self.home_ui.bio2_employee_position.setText(f"<b>Position:</b> {self.employee_data['position']}")
            self.home_ui.bio2_employee_shift.setText(f"<b>Shift:</b> {self.employee_data['schedule']}")

        bio2_page = self.home_ui.main_page.indexOf(self.home_ui.bio2_page)
        self.home_ui.main_page.setCurrentIndex(bio2_page)

    def send_attendance_email(self, employee_data, current_time, remarks):
        try:
            sender_email = "eals.tupc@gmail.com"
            sender_password = "buwl tszg dghr exln"  
            recipient_email = employee_data["email"]

            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = recipient_email
            message["Subject"] = f"EALS Attendance Record: {remarks}"

            header_img = os.path.join("resources", "theme_images", "default_theme_header.jpg")
            footer_img = os.path.join("resources", "theme_images", "default_theme_footer.jpg")

            formatted_time = current_time.strftime("%B %d, %Y at %I:%M:%S %p")

            html_content = f"""
                <div style="margin: 20px auto; padding: 20px; max-width: 600px; font-family: Arial, sans-serif;">
                    <div style="background-color: #4285f4; color: white; padding: 20px; border-radius: 8px 8px 0 0;">
                        <h2 style="margin: 0; text-align: center;">Attendance Record</h2>
                    </div>
                    <div style="background-color: #ffffff; padding: 20px; border-radius: 0 0 8px 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        <div style="text-align: center; margin-bottom: 20px;">
                            <img src="cid:profileimg" style="width: 150px; height: 150px; border-radius: 75px; object-fit: cover; margin: 0 auto;">
                        </div>
                        <p style="color: #202124; font-size: 16px;">Dear {employee_data['first_name']} {employee_data['last_name']},</p>
                        
                        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; margin: 20px 0;">
                            <p style="color: #666666; margin: 5px 0;">This email confirms that you have <strong>{remarks.lower()}ed</strong> on {formatted_time}.</p>
                        </div>

                        <div style="background-color: #e8f0fe; padding: 15px; border-radius: 8px; margin: 20px 0;">
                            <h3 style="color: #1967d2; margin-top: 0;">Attendance Details:</h3>
                            <p style="color: #666666; margin: 5px 0;">Employee ID: <strong>{employee_data['employee_id']}</strong></p>
                            <p style="color: #666666; margin: 5px 0;">Department: <strong>{employee_data['department']}</strong></p>
                            <p style="color: #666666; margin: 5px 0;">Position: <strong>{employee_data['position']}</strong></p>
                            <p style="color: #666666; margin: 5px 0;">Schedule: <strong>{employee_data['schedule']}</strong></p>
                        </div>

                        <p style="color: #666666; font-style: italic;">This is a system-generated email. Please do not reply.</p>
                        <br>
                        <p style="color: #666666; margin-bottom: 0;">Best regards,<br>EALS System</p>
                    </div>
                </div>
            """

            if os.path.exists(header_img):
                with open(header_img, "rb") as f:
                    img = MIMEImage(f.read())
                    img.add_header("Content-ID", "<headerimg>")
                    img.add_header("Content-Disposition", "inline", filename=os.path.basename(header_img))
                    message.attach(img)

            if os.path.exists(employee_data['profile_picture']):
                with open(employee_data['profile_picture'], "rb") as f:
                    img = MIMEImage(f.read())
                    img.add_header("Content-ID", "<profileimg>")
                    img.add_header("Content-Disposition", "inline", filename=os.path.basename(employee_data['profile_picture']))
                    message.attach(img)

            if os.path.exists(footer_img):
                with open(footer_img, "rb") as f:
                    img = MIMEImage(f.read())
                    img.add_header("Content-ID", "<footerimg>")
                    img.add_header("Content-Disposition", "inline", filename=os.path.basename(footer_img))
                    message.attach(img)

            html_header = '<img src="cid:headerimg" style="display:block; margin:auto; width:100%;"><br>' if os.path.exists(header_img) else ""
            html_footer = '<br><img src="cid:footerimg" style="display:block; margin:auto; width:100%;">' if os.path.exists(footer_img) else ""
            
            html_content = f"{html_header}{html_content}{html_footer}"
            message.attach(MIMEText(html_content, "html"))

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, sender_password)
                server.send_message(message)

            self.system_logs.log_system_action(f"Attendance email sent to {recipient_email}", "Employee")
            return True
        except Exception as e:
            print(f"Error sending attendance email: {e}")
            return False

    def goto_result_prompt(self):
        if self.employee_data:
            current_time = datetime.now()
            current_date = current_time.strftime("%Y-%m-%d")

            self.system_logs.log_system_action("A user logged.", "AttendanceLog")
            remarks = self.employee_data.get("remarks", "Clock In")
            is_late = self.employee_data.get("is_late", False)
            self.db.execute_query(
                "INSERT INTO attendance_logs (employee_id, date, time, remarks, is_late) VALUES (?, ?, ?, ?, ?)", 
                (self.employee_data["employee_id"], current_date, current_time.strftime("%H:%M:%S"), remarks, is_late)
            )

            if self.check_internet_connection():
                self.show_success("Email Notification", "Attendance email notification is being sent.")
                threading.Thread(
                    target=lambda: self.send_attendance_email(self.employee_data, current_time, remarks),
                    daemon=True
                ).start()
            
            if self.employee_data:
                current_time = datetime.now()
                current_date = current_time.strftime("%Y-%m-%d")

                hour = current_time.hour
                if 5 <= hour < 12:
                    greeting = "Good Morning"
                elif 12 <= hour < 18:
                    greeting = "Good Afternoon"
                else:
                    greeting = "Good Evening"
                self.home_ui.result_greetings_lbl.setText(f"{greeting}, {self.employee_data['first_name']}!")

                messages = [
                    "Keep up the excellent work!",
                    "Your dedication is appreciated!",
                    "You are making a difference every day!",
                    "Thank you for your hard work and commitment!"
                ]
                cursor = self.db.execute_query(
                    "SELECT is_late FROM attendance_logs WHERE employee_id = ? ORDER BY date DESC, time DESC LIMIT 1",
                    (self.employee_data["employee_id"],)
                )
                was_late = False
                if cursor:
                    result = cursor.fetchone()
                    was_late = bool(result[0]) if result and result[0] is not None else False
                if was_late:
                    messages.insert(0, "You were late for your shift today. Please be punctual next time.")
                    
                cursor = self.db.execute_query("SELECT date, time, remarks FROM attendance_logsWHERE employee_id = ?ORDER BY date DESC, time DESCLIMIT 10",
                (self.employee_data["employee_id"],)
                )
                logs = cursor.fetchall() if cursor else []

                clock_in_time = None
                clock_out_time = None

                for log in logs:
                    if log[2] == "Clock Out" and not clock_out_time:
                        clock_out_time = datetime.strptime(f"{log[0]} {log[1]}", "%Y-%m-%d %H:%M:%S")
                    elif log[2] == "Clock In" and not clock_in_time:
                        clock_in_time = datetime.strptime(f"{log[0]} {log[1]}", "%Y-%m-%d %H:%M:%S")
                    if clock_in_time and clock_out_time:
                        break

                if clock_in_time and clock_out_time:
                    worked_hours = (clock_out_time - clock_in_time).total_seconds() / 3600
                    if worked_hours > 8:
                        overtime_hours = worked_hours - 8
                        messages.insert(0, f"You worked {overtime_hours:.2f} hours extra from your scheduled hours! Great job!")
                    elif worked_hours >= 7.5:
                        messages.append("Almost a full shift! Keep up the consistency!")
                    elif worked_hours < 7:
                        messages.append("Try to complete your full shift next time. You can do it!")

                messages.extend([
                    "Your reliability is valued by the team!",
                    "Every extra effort counts. Thank you!",
                    "Your positive attitude makes a difference!",
                ])
                    
                random_message = random.choice(messages)
                self.home_ui.result_message_lbl.setText(random_message)

                try:
                    cursor = self.db.execute_query(
                        "SELECT remarks, date, time FROM attendance_logs WHERE employee_id = ?", 
                        (self.employee_data["employee_id"],)
                    )
                    logs = cursor.fetchall() if cursor else []

                    self.home_ui.result_employee_attendance_tbl.setRowCount(0)
                    for log in logs:
                        row_position = self.home_ui.result_employee_attendance_tbl.rowCount()
                        self.home_ui.result_employee_attendance_tbl.insertRow(row_position)

                        remarks_item = QTableWidgetItem(log[0])
                        date_item = QTableWidgetItem(log[1])
                        time_item = QTableWidgetItem(log[2])

                        remarks_item.setFlags(remarks_item.flags() & ~Qt.ItemIsEditable)
                        date_item.setFlags(date_item.flags() & ~Qt.ItemIsEditable)
                        time_item.setFlags(time_item.flags() & ~Qt.ItemIsEditable)

                        self.home_ui.result_employee_attendance_tbl.setItem(row_position, 0, remarks_item)
                        self.home_ui.result_employee_attendance_tbl.setItem(row_position, 1, date_item)
                        self.home_ui.result_employee_attendance_tbl.setItem(row_position, 2, time_item)

                    self.home_ui.result_employee_attendance_tbl.resizeColumnsToContents()
                except sqlite3.Error as e:
                    print(f"Database error while loading attendance logs: {e}")

            result_prompt = self.home_ui.main_page.indexOf(self.home_ui.result_page)
            self.home_ui.main_page.setCurrentIndex(result_prompt)
            self.home_ui.home_id_box.clear() 
            self.home_ui.home_pass_box.clear()
            self.home_ui.home_pass_box.setEchoMode(QLineEdit.Password)

            QTimer.singleShot(5000, lambda: self.home_ui.main_page.setCurrentWidget(self.home_ui.home_page))

    def parse_schedule(self, schedule):
        
        try:
            start, end = schedule.lower().split(" to ")
            start_hour = self.convert_to_24_hour(start)
            end_hour = self.convert_to_24_hour(end)
            return start_hour, end_hour
        except Exception as e:
            print(f"Error parsing schedule: {e}")
            return 0, 24 

    def convert_to_24_hour(self, time_str):
        
        try:
            hour = int(time_str[:-2])
            if "pm" in time_str and hour != 12:
                hour += 12
            elif "am" in time_str and hour == 12:
                hour = 0
            return hour
        except ValueError as e:
            print(f"Error converting time to 24-hour format: {e}")
            return -1  

    def is_within_schedule(self, start_hour, end_hour, current_hour):

        if start_hour < end_hour: 
            return start_hour <= current_hour < end_hour
        else:  
            return current_hour >= start_hour or current_hour < end_hour

    def show_success(self, title, message):
        chime.theme('chime')
        chime.success()
        toast = Toast(self.home_ui)
        toast.setTitle(title)
        toast.setText(message)
        toast.setDuration(2000)
        toast.setOffset(30, 70)
        toast.setBorderRadius(6) 
        toast.applyPreset(ToastPreset.SUCCESS)
        toast.setBackgroundColor(QColor('#FFFFFF'))
        toast.setPositionRelativeToWidget(self.home_ui.home_page)
        toast.setPosition(ToastPosition.TOP_RIGHT)
        toast.show()

    def show_error(self, title, message):
        chime.theme('big-sur')
        chime.warning()
        toast = Toast(self.home_ui)
        toast.setTitle(title)
        toast.setText(message)
        toast.setDuration(2000)
        toast.setOffset(30, 70)
        toast.setBorderRadius(6) 
        toast.applyPreset(ToastPreset.ERROR)
        toast.setBackgroundColor(QColor('#FFFFFF'))
        toast.setPositionRelativeToWidget(self.home_ui.home_page)
        toast.setPosition(ToastPosition.TOP_RIGHT)
        toast.show()
        
    def show_warning(self, title, message):
        chime.warning()
        toast = Toast(self.home_ui)
        toast.setTitle(title)
        toast.setText(message)
        toast.setDuration(2000)
        toast.setOffset(30, 70)
        toast.setBorderRadius(6) 
        toast.applyPreset(ToastPreset.WARNING)
        toast.setBackgroundColor(QColor('#FFFFFF'))
        toast.setPositionRelativeToWidget(self.home_ui.home_page)
        toast.setPosition(ToastPosition.TOP_RIGHT)
        toast.show()
    
    def goto_change_pass(self):
        self.changepass = ChangePassword(self.db, self.admin_id)
        self.changepass.change_pass_ui.show()
    
    def goto_admin_ui(self):
        global_home_ui.close()
        self.admin = Admin(self.db)
        self.admin.admin_ui.showMaximized()

    def toggle_password_visibility(self):
       
        if self.password_visible:
            self.home_ui.home_pass_box.setEchoMode(QLineEdit.Password)
            self.password_visible = False
        else:
            self.home_ui.home_pass_box.setEchoMode(QLineEdit.Normal)
            self.password_visible = True

    def goto_forgot_password(self):
        if not self.check_internet_connection():
            return  

        self.forgot_password = ForgotPassword(self.db)
        self.forgot_password.forgot_pass_ui.show()
        self.system_logs.log_system_action("User opened forgot password form", "SystemSettings")

    def check_internet_connection(self):
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=5)
            return True
        except OSError:
            toast = Toast(self.home_ui)
            toast.setTitle("No Internet Connection")
            toast.setText("Please check your internet connection and try again.")
            toast.setOffset(30, 70)
            toast.setBorderRadius(6)
            toast.applyPreset(ToastPreset.ERROR)
            toast.setBackgroundColor(QColor('#ffb7b6'))
            toast.setPositionRelativeToWidget(self.home_ui.home_page)
            toast.setPosition(ToastPosition.TOP_RIGHT)
            toast.setShowDurationBar(False)
            toast.setDuration(0)
            toast.show()
            return False

    def check_initial_setup(self):
        if self.db.is_initial_setup():
            self.admin_id, self.admin_password = self.db.create_initial_admin()
            if self.admin_id and self.admin_password:
                self.home_ui.main_page.setCurrentWidget(self.home_ui.start1_page)
                self.home_ui.start1_next_btn.clicked.connect(self.goto_start2_page)
                self.home_ui.start2_done_btn.clicked.connect(self.goto_home_page)
                self.home_ui.admin_userid_lbl.setText(self.admin_id)
                self.home_ui.admin_pass_lbl.setText(self.admin_password)
            else:
                QMessageBox.critical(None, "Error", "Failed to create initial admin. Please restart the application.")

    def goto_start2_page(self):
        self.home_ui.main_page.setCurrentWidget(self.home_ui.start2_page)

    def goto_home_page(self):
        self.home_ui.main_page.setCurrentWidget(self.home_ui.home_page)

    def send_email_notif(self):
        pass
    
class ChangePassword:
    def __init__(self, db, user_id, user_type="admin"):
        self.db = db
        self.system_logs = SystemLogs(db)
        self.user_id = user_id
        self.user_type = user_type  
        self.loader = QUiLoader()
        self.change_pass_ui = self.loader.load("ui/change_pass.ui")
        
        self.cp_visible = False
        self.np_visible = False
        self.changepass_visible = False
        
        if user_type == "admin":
            self.change_pass_ui.setWindowTitle("Change Admin Password")
            self.system_logs.log_system_action("The admin change password prompt has been loaded.", "Admin")
        else:
            self.change_pass_ui.setWindowTitle("Change Employee Password")
            self.system_logs.log_system_action("The employee change password prompt has been loaded.", "Employee")
            
        self.change_pass_ui.change_pass_note.setText("For security purposes, please enter your current password below, then choose a new password and confirm it. Make sure your new password is at least 8 characters long.")
        self.change_pass_ui.change_pass_note.setStyleSheet("color: black; border: none;")
        self.change_pass_ui.cp_visibility_btn.clicked.connect(self.toggle_cp_visibility)
        self.change_pass_ui.np_visibility_btn.clicked.connect(self.toggle_np_visibility)
        self.change_pass_ui.changepass_visibility_btn.clicked.connect(self.toggle_changepass_visibility)
        self.change_pass_ui.admin_change_pass_btn.clicked.connect(self.validate_and_change_password)
        self.change_pass_ui.admin_change_cancel_btn.clicked.connect(self.cancel_change_password)
        self.change_pass_ui.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)
        self.change_pass_ui.setWindowModality(Qt.ApplicationModal)

    def cancel_change_password(self):
        self.system_logs.log_system_action(f"Password change cancelled by {self.user_type}.", "Admin" if self.user_type == "admin" else "Employee")
        self.change_pass_ui.close()

    def toggle_cp_visibility(self):
        if self.cp_visible:
            self.change_pass_ui.change_pass_cp_box.setEchoMode(QLineEdit.Password)
        else:
            self.change_pass_ui.change_pass_cp_box.setEchoMode(QLineEdit.Normal)
        self.cp_visible = not self.cp_visible

    def toggle_np_visibility(self):
        if self.np_visible:
            self.change_pass_ui.change_pass_np_box.setEchoMode(QLineEdit.Password)
        else:
            self.change_pass_ui.change_pass_np_box.setEchoMode(QLineEdit.Normal)
        self.np_visible = not self.np_visible

    def toggle_changepass_visibility(self):
        if self.changepass_visible:
            self.change_pass_ui.change_pass_confirm_box.setEchoMode(QLineEdit.Password)
        else:
            self.change_pass_ui.change_pass_confirm_box.setEchoMode(QLineEdit.Normal)
        self.changepass_visible = not self.changepass_visible

    def validate_and_change_password(self):
        new_password = self.change_pass_ui.change_pass_np_box.text()
        confirm_password = self.change_pass_ui.change_pass_confirm_box.text()
        current_password = self.change_pass_ui.change_pass_cp_box.text()

        try:
            if self.user_type == "admin":
                table = "Admin"
                id_field = "admin_id"
            else:
                table = "Employee"
                id_field = "employee_id"

            cursor = self.db.execute_query(
                "SELECT password FROM {} WHERE {} = ?".format(table, id_field),
                (self.user_id,)
            )
            result = cursor.fetchone()

            if not result:
                chime.warning()
                self.change_pass_ui.change_pass_note.setText("The current password you entered is incorrect.")
                self.change_pass_ui.change_pass_note.setStyleSheet("color: red; border: none;")
                return
            
            try:
                PASSWORD_HASHER.verify(result[0], current_password)
            except argon2.exceptions.VerifyMismatchError:
                chime.warning()
                self.change_pass_ui.change_pass_note.setText("The current password you entered is incorrect.")
                self.change_pass_ui.change_pass_note.setStyleSheet("color: red; border: none;")
                return

            if not current_password or not new_password or not confirm_password:
                chime.warning()
                self.change_pass_ui.change_pass_note.setText("All password fields are required.")
                self.change_pass_ui.change_pass_note.setStyleSheet("color: red; border: none;")
                return

            if new_password != confirm_password:
                chime.warning()
                self.change_pass_ui.change_pass_note.setText("The new password and confirmation password do not match.")
                self.change_pass_ui.change_pass_note.setStyleSheet("color: red; border: none;")
                return

            if len(new_password) < 8:
                chime.warning()
                self.change_pass_ui.change_pass_note.setText("Your new password must be at least 8 characters long.")
                self.change_pass_ui.change_pass_note.setStyleSheet("color: red; border: none;")
                return

            hashed_password = PASSWORD_HASHER.hash(new_password)

            self.db.execute_query(
                "UPDATE {} SET password = ?, password_changed = TRUE WHERE {} = ?".format(table, id_field),
                (hashed_password, self.user_id)
            )

            self.system_logs.log_system_action(f"The {self.user_type} password has been changed.", "Admin" if self.user_type == "admin" else "Employee")
            chime.theme('chime')
            chime.success()
            toast = Toast(self.change_pass_ui)
            toast.setTitle("Password Changed Successfully")
            toast.setText("Your password has been updated. Please use the new password for future logins.")
            toast.setDuration(2000)
            toast.setOffset(30, 70) 
            toast.setBorderRadius(6) 
            toast.applyPreset(ToastPreset.SUCCESS)  
            toast.setBackgroundColor(QColor('#FFFFFF')) 
            toast.setPosition(ToastPosition.TOP_RIGHT) 
            toast.show()


            self.change_pass_ui.close()

        except sqlite3.Error as e:
            self.system_logs.log_system_action(
                f"Database error during {self.user_type} password change", 
                "Admin" if self.user_type == "admin" else "Employee"
            )
            print(f"Database error during password change: {e}")           

class ForgotPassword:
    def __init__(self, db):
        self.db = db
        self.system_logs = SystemLogs(db)
        self.loader = QUiLoader()
        self.forgot_pass_ui = self.loader.load("ui/forgot_password.ui")
        self.forgot_pass_ui.setWindowTitle("Forgot Password")
        self.forgot_pass_ui.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)
        self.forgot_pass_ui.setWindowModality(Qt.ApplicationModal)

        self.forgot_pass_ui.confirm_btn.clicked.connect(self.validate_account)
        self.forgot_pass_ui.verify_code_btn.clicked.connect(self.verify_code)
        self.forgot_pass_ui.fp_back_btn.clicked.connect(self.close_window)
        self.forgot_pass_ui.fp_back2_btn.clicked.connect(self.go_back_to_page1)
        
        self.current_employee = None
        self.verification_code = None
        
        self.setup_pin_inputs()
    
    def setup_pin_inputs(self):
        self.forgot_pass_ui.pin_1.setMaxLength(1)
        self.forgot_pass_ui.pin_2.setMaxLength(1)
        self.forgot_pass_ui.pin_3.setMaxLength(1)
        self.forgot_pass_ui.pin_4.setMaxLength(1)
        
        validator = QRegularExpressionValidator(QRegularExpression("[0-9]"))
        self.forgot_pass_ui.pin_1.setValidator(validator)
        self.forgot_pass_ui.pin_2.setValidator(validator)
        self.forgot_pass_ui.pin_3.setValidator(validator)
        self.forgot_pass_ui.pin_4.setValidator(validator)
        
        self.forgot_pass_ui.pin_1.textChanged.connect(lambda: self.move_focus_to_next(self.forgot_pass_ui.pin_1, self.forgot_pass_ui.pin_2))
        self.forgot_pass_ui.pin_2.textChanged.connect(lambda: self.move_focus_to_next(self.forgot_pass_ui.pin_2, self.forgot_pass_ui.pin_3))
        self.forgot_pass_ui.pin_3.textChanged.connect(lambda: self.move_focus_to_next(self.forgot_pass_ui.pin_3, self.forgot_pass_ui.pin_4))
        self.forgot_pass_ui.pin_4.textChanged.connect(lambda: self.check_verification_ready())
    
    def move_focus_to_next(self, current, next_input):
        if current.text():
            next_input.setFocus()
    
    def check_verification_ready(self):

        all_filled = bool(self.forgot_pass_ui.pin_1.text() and 
                         self.forgot_pass_ui.pin_2.text() and 
                         self.forgot_pass_ui.pin_3.text() and 
                         self.forgot_pass_ui.pin_4.text())
        self.forgot_pass_ui.verify_code_btn.setEnabled(all_filled)

    def validate_account(self):
        account_id = self.forgot_pass_ui.forgot_pass_id_box.text().strip()
        birthday = self.forgot_pass_ui.forgot_pass_birthday_box.date().toString("yyyy-MM-dd")
        email = self.forgot_pass_ui.forgot_pass_email_box.text().strip()

        if not account_id or not birthday or not email:
            missing_fields = []
            if not account_id:
                missing_fields.append("Account ID")
            if not birthday:
                missing_fields.append("Birthday")
            if not email:
                missing_fields.append("Email Address")
            self.forgot_pass_ui.fp_page1_note.setText(f"Warning: Please fill in the following fields: {', '.join(missing_fields)}.")
            self.forgot_pass_ui.fp_page1_note.setStyleSheet("color: black; background-color: rgb(255, 249, 245); border: 1px solid rgb(138, 55, 7);")
            return

        try:
            cursor = self.db.execute_query(
                "SELECT * FROM Employee WHERE employee_id = ?", 
                (account_id,)
            )
            employee = cursor.fetchone()

            if not employee:
                self.forgot_pass_ui.fp_page1_note.setText("Warning: The provided Account ID does not exist.")
                self.forgot_pass_ui.fp_page1_note.setStyleSheet("color: black; background-color: rgb(255, 249, 245); border: 1px solid rgb(138, 55, 7);")
                return

            if employee[4] != birthday or employee[14] != email:
                self.forgot_pass_ui.fp_page1_note.setText("Warning: The provided information does not match our records. Please check your inputs.")
                self.forgot_pass_ui.fp_page1_note.setStyleSheet("color: black; background-color: rgb(255, 249, 245); border: 1px solid rgb(138, 55, 7);")
                return

            self.current_employee = {
                "employee_id": employee[0],
                "email": employee[14]
            }
            
            self.verification_code = ''.join([str(secrets.randbelow(10)) for _ in range(4)])
            self.system_logs.log_system_action(
                f"Password reset verification code generated for employee {account_id}", 
                "Employee"
            )
            

            chime.theme('chime')
            chime.success()
            toast = Toast(self.forgot_pass_ui)
            toast.setTitle("Email Sent")
            toast.setText(f"A verification code has been sent to {email}.")
            toast.setDuration(2000)
            toast.setOffset(30, 70)
            toast.setBorderRadius(6)
            toast.applyPreset(ToastPreset.SUCCESS)
            toast.setBackgroundColor(QColor('#FFFFFF'))
            toast.setPosition(ToastPosition.TOP_RIGHT)
            toast.show()
            
            threading.Thread(
                target=lambda: self.send_verification_email(self.current_employee["email"], self.verification_code),
                daemon=True
            ).start()


            self.forgot_pass_ui.fp_stackedWidget.setCurrentWidget(self.forgot_pass_ui.fp_page_2)
            
            self.forgot_pass_ui.pin_1.clear()
            self.forgot_pass_ui.pin_2.clear()
            self.forgot_pass_ui.pin_3.clear()
            self.forgot_pass_ui.pin_4.clear()
            self.forgot_pass_ui.pin_1.setFocus()

        except sqlite3.Error as e:
            print(f"Database error during account validation: {e}")
            self.forgot_pass_ui.fp_page1_note.setText("Error: An error occurred while validating your account. Please try again later.")
            self.forgot_pass_ui.fp_page1_note.setStyleSheet("color: black; background-color: rgb(255, 249, 245); border: 1px solid rgb(138, 55, 7);")
            
    def send_verification_email(self, email, code):
        try:
            sender_email = "eals.tupc@gmail.com"  
            sender_password = "buwl tszg dghr exln"  

            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = email
            message["Subject"] = "EALS Verification Code"

            # Get default header and footer images
            header_img = os.path.join("resources", "theme_images", "default_theme_header.jpg")
            footer_img = os.path.join("resources", "theme_images", "default_theme_footer.jpg")

            # Create HTML email content with Google-like styling
            html_header = '<img src="cid:headerimg" style="display:block; margin:auto; width:100%;"><br>' if os.path.exists(header_img) else ""
            html_footer = '<br><img src="cid:footerimg" style="display:block; margin:auto; width:100%;">' if os.path.exists(footer_img) else ""
            
            html_content = f"""
                <div style="margin: 20px auto; padding: 20px; max-width: 600px; font-family: Arial, sans-serif;">
                    <div style="background-color: #4285f4; color: white; padding: 20px; border-radius: 8px 8px 0 0;">
                        <h2 style="margin: 0; text-align: center;">EALS Verification Code</h2>
                    </div>
                    <div style="background-color: #ffffff; padding: 20px; border-radius: 0 0 8px 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        <p style="color: #666666;">This verification code was sent to help you reset your EALS account password:</p>
                        <div style="text-align: center; padding: 20px;">
                            <span style="font-size: 32px; font-weight: bold; letter-spacing: 8px; color: #202124;">{code}</span>
                        </div>
                        <p style="color: #666666;">Don't know why you received this?</p>
                        <p style="color: #666666;">Someone requested a password reset for your EALS account. If this wasn't you, you can safely ignore this email.</p>
                        <p style="color: #666666;">To protect your account, don't forward this email or give this code to anyone.</p>
                        <br>
                        <p style="color: #666666; margin-bottom: 0;">Best regards,<br>EALS Team</p>
                    </div>
                </div>
            """

            html_content = f"{html_header}{html_content}{html_footer}"

            # Attach HTML content
            message.attach(MIMEText(html_content, "html"))

            # Attach header image if exists
            if os.path.exists(header_img):
                with open(header_img, "rb") as f:
                    img = MIMEImage(f.read())
                    img.add_header("Content-ID", "<headerimg>")
                    img.add_header("Content-Disposition", "inline", filename=os.path.basename(header_img))
                    message.attach(img)

            # Attach footer image if exists
            if os.path.exists(footer_img):
                with open(footer_img, "rb") as f:
                    img = MIMEImage(f.read())
                    img.add_header("Content-ID", "<footerimg>")
                    img.add_header("Content-Disposition", "inline", filename=os.path.basename(footer_img))
                    message.attach(img)

            # Send email
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, sender_password)
                server.send_message(message)

            print(f"Verification code sent to {email}")
            return True
        except Exception as e:
            print(f"Error sending verification email: {e}")
            return False

    def verify_code(self):
        entered_code = ''.join([
            self.forgot_pass_ui.pin_1.text(),
            self.forgot_pass_ui.pin_2.text(),
            self.forgot_pass_ui.pin_3.text(),
            self.forgot_pass_ui.pin_4.text()
        ])

        if entered_code == self.verification_code:
            self.change_pass_ui = QUiLoader().load("ui/employee_change_pass.ui")
            self.change_pass_ui.setWindowTitle("Change Password")
            self.change_pass_ui.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)

            self.change_pass_ui.employee_change_pass_btn.clicked.connect(self.validate_and_change_password)
            self.np_visible = False
            self.cp_visible = False
            self.change_pass_ui.np_visibility_btn.clicked.connect(self.toggle_np_visibility)
            self.change_pass_ui.cp_visibility_btn.clicked.connect(self.toggle_cp_visibility)
            self.forgot_pass_ui.close()
            self.change_pass_ui.show()
        else:
            self.forgot_pass_ui.fp_page2_note.setText("Warning: The verification code you entered is incorrect. Please try again.")
            self.forgot_pass_ui.fp_page2_note.setStyleSheet("color: black; background-color: yellow;")
            
    def toggle_np_visibility(self):
        if self.np_visible:
            self.change_pass_ui.change_pass_np_box.setEchoMode(QLineEdit.Password)
        else:
            self.change_pass_ui.change_pass_np_box.setEchoMode(QLineEdit.Normal)
        self.np_visible = not self.np_visible

    def toggle_cp_visibility(self):
        if self.cp_visible:
            self.change_pass_ui.change_pass_confirm_box.setEchoMode(QLineEdit.Password)
        else:
            self.change_pass_ui.change_pass_confirm_box.setEchoMode(QLineEdit.Normal)
        self.cp_visible = not self.cp_visible

    def validate_and_change_password(self):
        new_password = self.change_pass_ui.change_pass_np_box.text()
        confirm_password = self.change_pass_ui.change_pass_confirm_box.text()

        if not new_password or not confirm_password:
            chime.warning()
            self.change_pass_ui.change_pass_note.setText("Note: All fields are required.")
            self.change_pass_ui.change_pass_note.setStyleSheet("color: red")
            return

        if new_password != confirm_password:
            chime.warning()
            self.change_pass_ui.change_pass_note.setText("Note: Passwords do not match.")
            self.change_pass_ui.change_pass_note.setStyleSheet("color: red")
            return

        if len(new_password) < 8:
            chime.warning()
            self.change_pass_ui.change_pass_note.setText("Note: Password must be at least 8 characters long.")
            self.change_pass_ui.change_pass_note.setStyleSheet("color: red")
            return

        try:
            hashed_password = PASSWORD_HASHER.hash(new_password)

            self.db.execute_query(
                "UPDATE Employee SET password = ?, password_changed = TRUE WHERE employee_id = ?",
                (hashed_password, self.current_employee["employee_id"])
            )
            self.change_pass_ui.close()
            
            
            chime.theme('chime')
            chime.success()
            toast = Toast(self.forgot_pass_ui)
            toast.setTitle("Success")
            toast.setText("Password changed successfully.")
            toast.setDuration(2000)
            toast.setOffset(30, 70)
            toast.setBorderRadius(6)
            toast.applyPreset(ToastPreset.SUCCESS)
            toast.setBackgroundColor(QColor('#FFFFFF'))
            toast.setPosition(ToastPosition.TOP_RIGHT)
            toast.show()

        except sqlite3.Error as e:
            print(f"Database error during password change: {e}")
            QMessageBox.critical(None, "Error", "Failed to change password. Please try again.")

    def go_back_to_page1(self):
        self.forgot_pass_ui.fp_stackedWidget.setCurrentWidget(self.forgot_pass_ui.fp_page_1)

    def close_window(self):
        self.forgot_pass_ui.close()

class Admin:
    def __init__(self, db):
        self.db = db
        self.system_logs = SystemLogs(db)
        self.loader = QUiLoader()
        self.admin_ui = self.loader.load("ui/admin.ui")
        self.admin_ui.setWindowIcon(QIcon('resources/logo.ico'))
        self.admin_ui.setWindowTitle("EALS - Admin")
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
        
        self.admin_ui.employee_delete_btn.clicked.connect(self.handle_delete_employee)

        self.admin_ui.employee_picture_btn.clicked.connect(self.handle_enroll_picture)
        self.admin_ui.change_employee_picture.clicked.connect(self.handle_edit_picture)

        self.admin_ui.admin_attedance_logs_tbl.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.admin_ui.admin_attedance_logs_tbl.setSelectionMode(QAbstractItemView.SingleSelection)

        self.admin_ui.admin_attedance_logs_search.textChanged.connect(self.filter_attendance_logs_table)
        self.admin_ui.admin_attedance_logs_sort.currentIndexChanged.connect(self.sort_attendance_logs_table)

        self.load_attendance_logs_table()
        
        self.admin_ui.feedbacks_box.currentIndexChanged.connect(self.display_selected_feedback)
        self.load_feedback_titles()

        self.admin_ui.view_employee_tbl.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.admin_ui.view_employee_tbl.setSelectionMode(QAbstractItemView.SingleSelection)

        self.admin_ui.view_hr_tbl.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.admin_ui.view_hr_tbl.setSelectionMode(QAbstractItemView.SingleSelection)
    
        self.admin_ui.backup_btn.clicked.connect(self.handle_backup)
        self.admin_ui.restore_btn.clicked.connect(self.restore_backup)

        self.start_backup_scheduler()
        self.load_backup_table()
        self.load_backup_configuration()
        self.check_net()
        
        self.admin_ui.dashboard_pages.setCurrentWidget(self.admin_ui.db_page_1)
        self.admin_ui.dashboard_nav_btn.setText("Next")
        self.admin_ui.dashboard_nav_btn.clicked.connect(self.handle_dashboard_nav)
        
        self.chart_view = None
        self.setup_attendance_area_chart()
        if hasattr(self.admin_ui, "chart_layout1") and self.chart_view:
            self.admin_ui.chart_layout1.addWidget(self.chart_view, 0, 0)

        self.avg_work_hours_chart_view = None
        self.setup_avg_work_hours_line_chart()
        if hasattr(self.admin_ui, "chart_layout2") and self.avg_work_hours_chart_view:
            self.admin_ui.chart_layout2.addWidget(self.avg_work_hours_chart_view, 0, 0)
        
        # --- PIE CHART SETUP ---
        self.pie_chart_view = None
        self.setup_attendance_pie_chart()
        if hasattr(self.admin_ui, "chart_layout3") and self.pie_chart_view:
            self.admin_ui.chart_layout3.addWidget(self.pie_chart_view, 0, 0)

    def handle_dashboard_nav(self):
        current_widget = self.admin_ui.dashboard_pages.currentWidget()
        if current_widget == self.admin_ui.db_page_1:
            self.admin_ui.dashboard_pages.setCurrentWidget(self.admin_ui.db_page_2)
            self.admin_ui.dashboard_nav_btn.setText("Back")
        else:
            self.admin_ui.dashboard_pages.setCurrentWidget(self.admin_ui.db_page_1)
            self.admin_ui.dashboard_nav_btn.setText("Next")
        
    def get_current_admin(self):
        try:
            cursor = self.db.execute_query("SELECT admin_id FROM Admin LIMIT 1")
            result = cursor.fetchone()
            return result[0] if result else None
        except sqlite3.Error as e:
            print(f"Database error while fetching current admin: {e}")
            return None

    def load_system_logs(self):
        log_dir = "resources/logs"
        self.admin_ui.system_log_list.clear()

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        log_files = [f for f in os.listdir(log_dir) if os.path.isfile(os.path.join(log_dir, f))]
        self.admin_ui.system_log_list.addItems(log_files)

        try:
            cursor = self.db.execute_query(
                "SELECT created_at, present_count, absent_count, late_count FROM system_logs ORDER BY created_at DESC"
            )
            logs = cursor.fetchall() if cursor else []
            if hasattr(self.admin_ui, "system_log_summary_tbl"):
                tbl = self.admin_ui.system_log_summary_tbl
                tbl.setRowCount(0)
                for log in logs:
                    row = tbl.rowCount()
                    tbl.insertRow(row)
                    for col, val in enumerate(log):
                        item = QTableWidgetItem(str(val))
                        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                        tbl.setItem(row, col, item)
        except Exception as e:
            print(f"Error loading system log summary: {e}")

    def display_selected_log(self):
        self.system_logs.log_system_action("A log file has been displayed.", "SystemSettings")
        selected_log = self.admin_ui.system_log_list.currentText()
        log_dir = "resources/logs"
        log_path = os.path.join(log_dir, selected_log)

        if os.path.exists(log_path):
            try:
                with open(log_path, "r") as file:
                    content = file.read()
                    cursor = self.db.execute_query(
                        "SELECT present_count, absent_count, late_count FROM system_logs WHERE path = ? ORDER BY created_at DESC LIMIT 1",
                        (log_path,)
                    )
                    summary = cursor.fetchone() if cursor else None
                    if summary:
                        content += (
                            f"\n\n--- Attendance Summary ---\n"
                            f"Present: {summary[0]}\n"
                            f"Absent: {summary[1]}\n"
                            f"Late: {summary[2]}"
                        )
                    self.admin_ui.system_log_browser.setText(content)
            except Exception as e:
                print(f"Error reading log file {log_path}: {e}")
                self.admin_ui.system_log_browser.setText("Error loading log file.")
        else:
            self.admin_ui.system_log_browser.setText("No log file selected or file does not exist.")

    def update_date_today(self):
        current_date = datetime.now()
        formatted_date = current_date.strftime("%a, %b %d, %Y")
        self.admin_ui.date_today.setText(formatted_date)

    def goto_home(self):
        self.system_logs.log_system_action("The Admin logged out.", "Admin")
        global_home_ui.showMaximized()
        self.admin_ui.close()

    def load_feedback_titles(self):
        try:
            cursor = self.db.execute_query('''
                SELECT title FROM feedback 
                ORDER BY created_at DESC
            ''')
            titles = [row[0] for row in cursor.fetchall()]
            
            self.admin_ui.feedbacks_box.clear()
            self.admin_ui.feedbacks_box.addItems(titles)
            
        except sqlite3.Error as e:
            print(f"Database error while loading feedback titles: {e}")

    def display_selected_feedback(self):
        selected_title = self.admin_ui.feedbacks_box.currentText()
        if not selected_title:
            self.admin_ui.feedbacks_text_box.clear()
            return
            
        try:
            cursor = self.db.execute_query('''
                SELECT f.message, f.created_at, e.first_name, e.last_name 
                FROM feedback f
                JOIN Employee e ON f.created_by = e.employee_id
                WHERE f.title = ?
            ''', (selected_title,))
            
            result = cursor.fetchone()
            if result:
                message, created_at, first_name, last_name = result
                formatted_text = f"From: {first_name} {last_name}\n"
                formatted_text += f"Date: {created_at}\n\n"
                formatted_text += message
                
                self.admin_ui.feedbacks_text_box.setText(formatted_text)
            else:
                self.admin_ui.feedbacks_text_box.clear()
                
        except sqlite3.Error as e:
            print(f"Database error while loading feedback message: {e}")
            self.admin_ui.feedbacks_text_box.clear()
    
    def goto_employee_hr(self):
        self.system_logs.log_system_action("Goes to the employee HR page.", "Employee")
        employee_hr_page = self.admin_ui.admin_employee_sc_pages.indexOf(self.admin_ui.employee_hr_page)
        self.admin_ui.admin_employee_sc_pages.setCurrentIndex(employee_hr_page)


    def goto_employee_edit(self):
        self.system_logs.log_system_action("A selected employee is being edited.", "Employee")
        employee_edit_page = self.admin_ui.admin_employee_sc_pages.indexOf(self.admin_ui.employee_edit_page)
        self.admin_ui.admin_employee_sc_pages.setCurrentIndex(employee_edit_page)

    def goto_employee_enroll(self):
        self.system_logs.log_system_action("The employee enrollment page has been opened.", "Employee")
        employee_enroll_page = self.admin_ui.admin_employee_sc_pages.indexOf(self.admin_ui.employee_enroll_page)
        self.admin_ui.admin_employee_sc_pages.setCurrentIndex(employee_enroll_page)
        self.admin_ui.is_hr_no.setChecked(True)
        self.toggle_hr_fields()

    def goto_employee_enroll_2(self):
        self.system_logs.log_system_action("the enrollment proceed to the step 2.", "Employee")
        employee_enroll_2_page = self.admin_ui.admin_employee_sc_pages.indexOf(self.admin_ui.employee_enroll2_page)
        self.admin_ui.admin_employee_sc_pages.setCurrentIndex(employee_enroll_2_page)

    def goto_employee_enroll_3(self):
        self.system_logs.log_system_action("the enrollment proceed to the step 3.", "Employee")
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
        self.system_logs.log_system_action("A employee is selected to be viewed.", "Employee")
        if selected := self.admin_ui.employee_list_tbl.selectedIndexes():
            row = selected[0].row()
            self.display_employee_view(self.employees[row])
            view_page = self.admin_ui.employee_view_page
        elif selected := self.admin_ui.hr_list_tbl.selectedIndexes():
            row = selected[0].row()
            self.display_hr_view(self.hr_employees[row])
            view_page = self.admin_ui.hr_view_page
        else:
            self.show_error("Viewing Error", "No employee selected for viewing.")
            return
            
        page_index = self.admin_ui.admin_employee_sc_pages.indexOf(view_page)
        self.admin_ui.admin_employee_sc_pages.setCurrentIndex(page_index)

    def display_employee_view(self, employee_data):
        self.system_logs.log_system_action("Loading all data of an employee for viewing.", "Employee")
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
        self.admin_ui.view_employee_email.setText(employee_data.get("email", ""))
        
        if employee_data["schedule"] == "6am to 2pm":
            self.admin_ui.view_employee_sched_1.setChecked(True)
        elif employee_data["schedule"] == "2pm to 10pm":
            self.admin_ui.view_employee_sched_2.setChecked(True)
        else:
            self.admin_ui.view_employee_sched_3.setChecked(True)

        self.display_picture(self.admin_ui.view_employee_picture, employee_data['profile_picture'])
        self.load_employee_attendance_logs(employee_data["employee_id"])

    def display_hr_view(self, hr_data):
        self.system_logs.log_system_action("Loading all data of an HR employee for viewing.", "Employee")
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
        self.admin_ui.view_hr_email.setText(hr_data.get("email", ""))
        
        if hr_data["schedule"] == "6am to 2pm":
            self.admin_ui.view_hr_sched_1.setChecked(True)
        elif hr_data["schedule"] == "2pm to 10pm":
            self.admin_ui.view_hr_sched_2.setChecked(True)
        else:
            self.admin_ui.view_hr_sched_3.setChecked(True)

        self.display_picture(self.admin_ui.view_hr_picture, hr_data['profile_picture'])
        self.load_hr_attendance_logs(hr_data["employee_id"])

    def handle_edit_button(self):
        self.system_logs.log_system_action("The edit button has been clicked.", "Employee")
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
                self.system_logs.log_system_action("Invalid selection has been made.", "Employee")
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
                self.system_logs.log_system_action("Invalid selection has been made.", "Employee")
                print("Invalid HR row selected.")

        else:
            self.system_logs.log_system_action("Invalid selection has been made. (No employee has been selected)", "Employee")
            self.show_error("Edit Error", "No employee selected for editing.")

    def load_employee_to_edit_form(self, employee_data):
        self.system_logs.log_system_action("Loading employee data to edit page.", "Employee")
        self.current_employee_data = employee_data
        self.admin_ui.edit_employee_first_name.setText(employee_data["first_name"])
        self.admin_ui.edit_employee_last_name.setText(employee_data["last_name"])
        self.admin_ui.edit_employee_mi.setText(employee_data["middle_initial"])
        self.admin_ui.edit_employee_email.setText(employee_data.get("email"))
        
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
        email = self.admin_ui.edit_employee_email.text().strip()

        if not first_name:
            self.show_error("Validation Error", "First Name is required")
            return False, "First Name is required"
        if not all(part.isalpha() for part in first_name.split()):
            self.show_error("Validation Error", "Valid First Name (letters only, multiple names allowed)")
            return False, "Valid First Name (letters only, multiple names allowed)"

        if not last_name:
            self.show_error("Validation Error", "Last Name is required")
            return False, "Last Name is required"
        if not all(part.isalpha() for part in last_name.split()):
            self.show_error("Validation Error", "Valid Last Name (letters only, multiple names allowed)")
            return False, "Valid Last Name (letters only, multiple names allowed)"

        if mi and (len(mi) > 1 or not mi.isalpha()):
            self.show_error("Validation Error", "Valid Middle Initial (single letter only)")
            return False, "Valid Middle Initial (single letter only)"

        if not id_pref:
            self.show_error("Validation Error", "ID Prefix is required")
            return False, "ID Prefix is required"

        gender = None
        if self.admin_ui.edit_employee_male.isChecked():
            gender = "Male"
        elif self.admin_ui.edit_employee_female.isChecked():
            gender = "Female"
        if not gender:
            self.show_error("Validation Error", "Please select a Gender")
            return False, "Please select a Gender"

        schedule = None
        if self.admin_ui.edit_employee_sched_1.isChecked():
            schedule = "6am to 2pm"
        elif self.admin_ui.edit_employee_sched_2.isChecked():
            schedule = "2pm to 10pm"
        elif self.admin_ui.edit_employee_sched_3.isChecked():
            schedule = "10pm to 6am"
        if not schedule:
            self.show_error("Validation Error", "Please select a Schedule")
            return False, "Please select a Schedule"

        if not email:
            self.show_error("Validation Error", "Email Address is required")
            return False, "Email Address is required"
        if "@" not in email or "." not in email.split("@")[1]:
            self.show_error("Validation Error", "Valid Email Address (must contain @ and domain)")
            return False, "Valid Email Address (must contain @ and domain)"

        birthday = self.admin_ui.edit_employee_birthday_edit.date().toString("yyyy-MM-dd")
        try:
            birthday_date = datetime.strptime(birthday, "%Y-%m-%d")
            today = datetime.now()
            age = today.year - birthday_date.year - ((today.month, today.day) < (birthday_date.month, birthday_date.day))
            if age < 18:
                self.show_error("Validation Error", "Employee must be at least 18 years old")
                return False, "Employee must be at least 18 years old"
        except ValueError:
            self.show_error("Validation Error", "Invalid Birthday format")
            return False, "Invalid Birthday format"

        is_hr = self.admin_ui.edit_is_hr_yes.isChecked()
        department = self.admin_ui.edit_employee_department_box.currentText()
        position = self.admin_ui.edit_employee_position_box.currentText()
        
        if is_hr:
            department = "Human Resources"
            position = "HR Staff"

        employee_id = f"{id_pref}-{id_year}-{id_no}"
        try:
            cursor = self.db.execute_query(
                "SELECT employee_id FROM Employee WHERE employee_id = ? AND employee_id != ?",
                (employee_id, self.current_employee_data["employee_id"])
            )
            if cursor.fetchone():
                self.show_error("Validation Error", f"Employee ID {employee_id} already exists in the database")
                return False, f"Employee ID {employee_id} already exists in the database"

            cursor = self.db.execute_query(
                "SELECT first_name, last_name FROM Employee WHERE first_name = ? AND last_name = ? AND employee_id != ?",
                (first_name, last_name, self.current_employee_data["employee_id"])
            )
            if cursor.fetchone():
                self.show_error("Validation Error", f"An employee with the name {first_name} {last_name} already exists")
                return False, f"An employee with the name {first_name} {last_name} already exists"
        except sqlite3.Error as e:
            self.show_error("Database Error", "An error occurred while validating the data")
            return False, "Database error during validation"

        status = "Active"
        if self.selected_employee_type == "employee":
            status_item = self.admin_ui.employee_list_tbl.item(self.selected_employee_index, 3)
            if status_item:
                status = status_item.text()
        elif self.selected_employee_type == "hr":
            status_item = self.admin_ui.hr_list_tbl.item(self.selected_employee_index, 2)
            if status_item:
                status = status_item.text()

        employee_data = {
            "first_name": first_name,
            "last_name": last_name,
            "middle_initial": mi,
            "employee_id": employee_id,
            "gender": gender,
            "birthday": birthday,
            "department": department,
            "position": position,
            "schedule": schedule,
            "is_hr": is_hr,
            "status": status,
            "profile_picture": self.current_employee_data.get('profile_picture', ''),
            "email": email
        }

        return True, employee_data

    def save_edited_employee(self):
        if self.selected_employee_index is None or self.selected_employee_type is None:
            self.show_error("Edit Error", "No employee selected for editing.")
            return

        valid, result = self.validate_edited_employee_data()
        if not valid:
            self.show_error("Edit Error", "Validation Error.")
            return

        try:
            current_admin = self.get_current_admin()
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            if result['profile_picture'] != self.current_employee_data.get('profile_picture', ''):
                employee_name = f"{result['first_name']}_{result['last_name']}"
                picture_path = self.save_picture(result['profile_picture'], employee_name)
                if picture_path:
                    result['profile_picture'] = picture_path
            else:
                result['profile_picture'] = self.current_employee_data.get('profile_picture', '')

            self.db.execute_query('''
                UPDATE Employee
                SET first_name = ?, last_name = ?, middle_initial = ?, birthday = ?, gender = ?,
                    department = ?, position = ?, schedule = ?, is_hr = ?, status = ?, 
                    profile_picture = ?, email = ?, last_modified_by = ?, last_modified_at = ?
                WHERE employee_id = ?
            ''', (
                result['first_name'], result['last_name'], result['middle_initial'], result['birthday'],
                result['gender'], result['department'], result['position'], result['schedule'],
                result['is_hr'], result['status'], result['profile_picture'],
                result['email'], current_admin, current_time,  
                result['employee_id']
            ))

            self.system_logs.log_system_action(f"Employee {result['employee_id']} was modified by {current_admin}", "Employee")
            self.show_success("Employee Updated", f"Employee {result['first_name']} {result['last_name']} has been updated.")

            self.load_employee_table()
            self.load_hr_table()
            self.goto_employee_hr()

        except sqlite3.Error as e:
            print(f"Database error while updating employee: {e}")
            self.show_error("Edit Error", "Failed to update employee record.")

    def toggle_employee_status(self):
        if self.selected_employee_index is None or self.selected_employee_type is None:
            self.show_error("Status Update Error", "FNo employee is determined.")
            return

        try:
            if self.selected_employee_type == "employee":
                employee = self.employees[self.selected_employee_index]
                row = self.selected_employee_index
                status_column = 3 
            else:
                employee = self.hr_employees[self.selected_employee_index]
                row = self.selected_employee_index
                status_column = 2 

            new_status = "Inactive" if employee["status"] == "Active" else "Active"
            self.db.execute_query("UPDATE Employee SET status = ? WHERE employee_id = ?", (new_status, employee["employee_id"]))
            employee["status"] = new_status

            status_item = QTableWidgetItem(new_status)
            status_item.setFlags(status_item.flags() & ~Qt.ItemIsEditable)
            if self.selected_employee_type == "employee":
                self.admin_ui.employee_list_tbl.setItem(row, status_column, status_item)
            else:
                self.admin_ui.hr_list_tbl.setItem(row, status_column, status_item)

            if new_status == "Active":
                self.admin_ui.employee_edit_deactivate.setText("Deactivate")
            else:
                self.admin_ui.employee_edit_deactivate.setText("Activate")
                
            self.show_success("Status Updated", f"Employee {employee['first_name']} {employee['last_name']} has been {new_status.lower()}.")

        except sqlite3.Error as e:
            print(f"Database error while updating status: {e}")
            self.show_error("Database Error", "Failed to update employee status.")

    def validate_employee_data(self):
        first_name = self.admin_ui.employee_first_name.text().strip()
        last_name = self.admin_ui.employee_last_name.text().strip()
        mi = self.admin_ui.employee_mi.text().strip()
        id_pref = self.admin_ui.employee_id_pref.text().strip()
        id_year = self.admin_ui.employee_id_year.currentText()
        id_no = self.admin_ui.employee_id_no.currentText()
        profile_picture = self.current_employee_data.get('profile_picture', '')
        email = self.admin_ui.employee_email.text().strip()

        if not first_name:
            self.show_error("Validation Error", "First Name is required")
            return False, "First Name is required"
        if not all(part.isalpha() for part in first_name.split()):
            self.show_error("Validation Error", "Valid First Name (letters only, multiple names allowed)")
            return False, "Valid First Name (letters only, multiple names allowed)"

        if not last_name:
            self.show_error("Validation Error", "Last Name is required")
            return False, "Last Name is required"
        if not all(part.isalpha() for part in last_name.split()):
            self.show_error("Validation Error", "Valid Last Name (letters only, multiple names allowed)")
            return False, "Valid Last Name (letters only, multiple names allowed)"

        if mi and (len(mi) > 1 or not mi.isalpha()):
            self.show_error("Validation Error", "Valid Middle Initial (single letter only)")
            return False, "Valid Middle Initial (single letter only)"

        if not id_pref:
            self.show_error("Validation Error", "ID Prefix is required")
            return False, "ID Prefix is required"

        gender = None
        if self.admin_ui.employee_male.isChecked():
            gender = "Male"
        elif self.admin_ui.employee_female.isChecked():
            gender = "Female"
        if not gender:
            self.show_error("Validation Error", "Please select a Gender")
            return False, "Please select a Gender"

        schedule = None
        if self.admin_ui.employee_sched_1.isChecked():
            schedule = "6am to 2pm"
        elif self.admin_ui.employee_sched_2.isChecked():
            schedule = "2pm to 10pm"
        elif self.admin_ui.employee_sched_3.isChecked():
            schedule = "10pm to 6am"
        if not schedule:
            self.show_error("Validation Error", "Please select a Schedule")
            return False, "Please select a Schedule"

        if not profile_picture:
            self.show_error("Validation Error", "Profile Picture is required")
            return False, "Profile Picture is required"

        if not email:
            self.show_error("Validation Error", "Email Address is required")
            return False, "Email Address is required"
        if "@" not in email or "." not in email.split("@")[1]:
            self.show_error("Validation Error", "Valid Email Address (must contain @ and domain)")
            return False, "Valid Email Address (must contain @ and domain)"

        birthday = self.admin_ui.employee_birthday_edit.date().toString("yyyy-MM-dd")
        try:
            birthday_date = datetime.strptime(birthday, "%Y-%m-%d")
            today = datetime.now()
            age = today.year - birthday_date.year - ((today.month, today.day) < (birthday_date.month, birthday_date.day))
            if age < 18:
                self.show_error("Validation Error", "Employee must be at least 18 years old")
                return False, "Employee must be at least 18 years old"
        except ValueError:
            self.show_error("Validation Error", "Invalid Birthday format")
            return False, "Invalid Birthday format"

        is_hr = self.admin_ui.is_hr_yes.isChecked()
        department = self.admin_ui.employee_department_box.currentText()
        position = self.admin_ui.employee_position_box.currentText()

        if is_hr:
            department = "Human Resources"
            position = "HR Staff"

        employee_id = f"{id_pref}-{id_year}-{id_no}"
        try:
            cursor = self.db.execute_query("SELECT employee_id FROM Employee WHERE employee_id = ?", (employee_id,))
            if cursor.fetchone():
                self.show_error("Validation Error", f"Employee ID {employee_id} already exists in the database")
                return False, f"Employee ID {employee_id} already exists in the database"

            cursor = self.db.execute_query(
                "SELECT first_name, last_name FROM Employee WHERE first_name = ? AND last_name = ?",
                (first_name, last_name)
            )
            if cursor.fetchone():
                self.show_error("Validation Error", f"An employee with the name {first_name} {last_name} already exists")
                return False, f"An employee with the name {first_name} {last_name} already exists"
        except sqlite3.Error as e:
            self.show_error("Database Error", "An error occurred while validating the data")
            return False, "Database error during validation"

        password = ' '.join(word.upper() for word in last_name.split())
        hashed_password = PASSWORD_HASHER.hash(password)

        employee_data = {
            "first_name": first_name,
            "last_name": last_name,
            "middle_initial": mi,
            "employee_id": employee_id,
            "password": hashed_password,
            "gender": gender,
            "birthday": birthday,
            "department": department,
            "position": position,
            "schedule": schedule,
            "is_hr": is_hr,
            "status": "Active",
            "password_changed": False,
            "profile_picture": profile_picture,
            "email": email
        }

        return True, employee_data

    def load_employee_table(self):
        self.system_logs.log_system_action("Loading all employees to the employee table.", "Employee")
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
                    "password_changed": employee[12],  
                    "profile_picture": employee[13],
                    "email": employee[14]
                }
                self.employees.append(employee_data)
                self.add_employee_to_table(employee_data)

            self.update_dashboard_labels()

        except sqlite3.Error as e:
            print(f"Database error while loading employees: {e}")

    def load_hr_table(self):
        self.system_logs.log_system_action("Loading all HR employees to the HR table.", "Employee")
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
                    "password_changed": hr_employee[12],  
                    "profile_picture": hr_employee[13],
                    "email": hr_employee[14]
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
        
    def handle_delete_employee(self):
        employee_selected = self.admin_ui.employee_list_tbl.selectedIndexes()
        hr_selected = self.admin_ui.hr_list_tbl.selectedIndexes()
        
        if not employee_selected and not hr_selected:
            self.show_error("Delete Error", "Please select an employee to delete.")
            return

        if employee_selected:
            row = employee_selected[0].row()
            employee_data = self.employees[row]
            employee_type = "Employee"
        else:
            row = hr_selected[0].row()
            employee_data = self.hr_employees[row]
            employee_type = "HR Employee"


        confirm_msg = QMessageBox()
        confirm_msg.setIcon(QMessageBox.Warning)
        confirm_msg.setText("Confirm Deletion")
        confirm_msg.setInformativeText(f"Are you sure you want to delete {employee_type} {employee_data['first_name']} {employee_data['last_name']}?\n\nThis action cannot be undone.")
        confirm_msg.setWindowTitle("Delete Confirmation")
        confirm_msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm_msg.setDefaultButton(QMessageBox.No)

        if confirm_msg.exec() == QMessageBox.Yes:
            try:
                self.db.execute_query("DELETE FROM attendance_logs WHERE employee_id = ?", 
                                    (employee_data['employee_id'],))
                
                self.db.execute_query("DELETE FROM feedback WHERE created_by = ?", 
                                    (employee_data['employee_id'],))
                
                self.db.execute_query("DELETE FROM Employee WHERE employee_id = ?", 
                                    (employee_data['employee_id'],))

                if os.path.exists(employee_data['profile_picture']):
                    os.remove(employee_data['profile_picture'])

                self.system_logs.log_system_action(
                    f"{employee_type} {employee_data['employee_id']} has been deleted by {self.get_current_admin()}", 
                    "Employee"
                )
                
                self.show_success("Delete Success", f"{employee_type} {employee_data['first_name']} {employee_data['last_name']} has been deleted.")

                self.load_employee_table()
                self.load_hr_table()
                self.update_dashboard_labels()

            except sqlite3.Error as e:
                print(f"Database error while deleting employee: {e}")
                QMessageBox.critical(None, "Delete Error", 
                    "An error occurred while deleting the employee record.")
                
            except Exception as e:
                print(f"Error during employee deletion: {e}")
                QMessageBox.critical(None, "Delete Error", 
                    "An unexpected error occurred during deletion.")
        
    def get_employee_history(self, employee_id):
        try:
            cursor = self.db.execute_query('''
                SELECT 
                    created_by,
                    created_at,
                    last_modified_by,
                    last_modified_at
                FROM Employee
                WHERE employee_id = ?
            ''', (employee_id,))
            
            result = cursor.fetchone() if cursor else None
            if result:
                return {
                    'created_by': result[0],
                    'created_at': result[1],
                    'last_modified_by': result[2],
                    'last_modified_at': result[3]
                }
            return None
            
        except sqlite3.Error as e:
            print(f"Database error while fetching employee history: {e}")
            return None

    def save_employee_data(self, employee_data):
        self.system_logs.log_system_action("Saving employee data to the database.", "Employee")
        try:
            current_admin = self.get_current_admin()
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            cursor = self.db.execute_query("SELECT employee_id FROM Employee WHERE employee_id = ?", 
                                        (employee_data['employee_id'],))
            result = cursor.fetchone() if cursor else None

            if result:
                self.db.execute_query('''
                    UPDATE Employee
                    SET first_name = ?, last_name = ?, middle_initial = ?, birthday = ?, gender = ?,
                        department = ?, position = ?, schedule = ?, is_hr = ?, status = ?, 
                        password = ?, profile_picture = ?, email = ?, last_modified_by = ?, last_modified_at = ?
                    WHERE employee_id = ?
                ''', (
                    employee_data['first_name'], employee_data['last_name'], employee_data['middle_initial'],
                    employee_data['birthday'], employee_data['gender'], employee_data['department'],
                    employee_data['position'], employee_data['schedule'], employee_data['is_hr'],
                    employee_data['status'], employee_data['password'], employee_data['profile_picture'],
                    employee_data['email'], current_admin, current_time,
                    employee_data['employee_id']
                ))
                self.system_logs.log_system_action(f"Employee {employee_data['employee_id']} modified by {current_admin}", "Employee")
            else:
                self.db.execute_query('''
                    INSERT INTO Employee (
                        employee_id, first_name, last_name, middle_initial, birthday, gender,
                        department, position, schedule, is_hr, status, password, profile_picture, email,
                        created_by, created_at, last_modified_by, last_modified_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    employee_data['employee_id'], employee_data['first_name'], employee_data['last_name'],
                    employee_data['middle_initial'], employee_data['birthday'], employee_data['gender'],
                    employee_data['department'], employee_data['position'], employee_data['schedule'],
                    employee_data['is_hr'], employee_data['status'], employee_data['password'],
                    employee_data['profile_picture'], employee_data['email'], current_admin, current_time, current_admin, current_time
                ))
                self.system_logs.log_system_action(f"New employee {employee_data['employee_id']} created by {current_admin}", "Employee")

            return True

        except sqlite3.Error as e:
            print(f"Database error while saving employee data: {e}")
            return False

    def goto_employee_enroll_2_with_validation(self):
        valid, result = self.validate_employee_data()
        if valid:
            self.current_employee_data = result
            self.goto_employee_enroll_2()

    def finalize_employee_enrollment(self):
        if hasattr(self, 'current_employee_data'):
            employee_name = f"{self.current_employee_data['first_name']}_{self.current_employee_data['last_name']}"
            picture_path = self.save_picture(self.current_employee_data['profile_picture'], employee_name)
            if picture_path:
                self.current_employee_data['profile_picture'] = picture_path

            success = self.save_employee_data(self.current_employee_data)
            
            if success:
                self.system_logs.log_system_action("A new employee has been enrolled.", "Employee")
                employee_type = "HR Employee" if self.current_employee_data.get('is_hr', False) else "Employee"
                self.show_success("Enrollment Success", f"{employee_type} {self.current_employee_data['first_name']} {self.current_employee_data['last_name']} has been enrolled.")
                threading.Thread(target=lambda: self.send_welcome_email(self.current_employee_data), daemon=True).start()
                self.clear_employee_enrollment_fields()
                self.goto_employee_hr()
                self.load_employee_table()
                self.load_hr_table()
            else:
                self.system_logs.log_system_action("Failed to save employee data.", "Employee")
                self.show_error("Enrollment Error", "Failed to save employee data. Please try again.")
        else:
            self.show_error("Process Error", "No employee data found. Please restart the enrollment process.")

    def send_welcome_email(self, employee_data):
        try:
            sender_email = "eals.tupc@gmail.com"
            sender_password = "buwl tszg dghr exln" 
            recipient_email = employee_data["email"]

            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = recipient_email
            message["Subject"] = "EALS - Welcome and Account Details"

            header_img = os.path.join("resources", "theme_images", "default_theme_header.jpg")
            footer_img = os.path.join("resources", "theme_images", "default_theme_footer.jpg")

            html_content = f"""
                <div style="margin: 20px auto; padding: 20px; max-width: 600px; font-family: Arial, sans-serif;">
                    <div style="background-color: #4285f4; color: white; padding: 20px; border-radius: 8px 8px 0 0;">
                        <h2 style="margin: 0; text-align: center;">Welcome to EALS</h2>
                    </div>
                    <div style="background-color: #ffffff; padding: 20px; border-radius: 0 0 8px 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        <div style="text-align: center; margin-bottom: 20px;">
                            <img src="cid:profileimg" style="width: 150px; height: 150px; border-radius: 75px; object-fit: cover; margin: 0 auto;">
                        </div>
                        <p style="color: #202124; font-size: 16px;">Dear {employee_data['first_name']} {employee_data['last_name']},</p>
                        <p style="color: #666666;">Welcome to EALS! Your employee account has been successfully registered.</p>
                        
                        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; margin: 20px 0;">
                            <h3 style="color: #202124; margin-top: 0;">Account Details:</h3>
                            <p style="color: #666666; margin: 5px 0;">Employee ID: <strong>{employee_data['employee_id']}</strong></p>
                            <p style="color: #666666; margin: 5px 0;">Department: <strong>{employee_data['department']}</strong></p>
                            <p style="color: #666666; margin: 5px 0;">Position: <strong>{employee_data['position']}</strong></p>
                            <p style="color: #666666; margin: 5px 0;">Schedule: <strong>{employee_data['schedule']}</strong></p>
                            <p style="color: #666666; margin: 5px 0;">Email: <strong>{employee_data['email']}</strong></p>
                        </div>

                        <div style="background-color: #fff3e0; padding: 15px; border-radius: 8px; margin: 20px 0;">
                            <p style="color: #e65100; margin: 0;"><strong>Important:</strong></p>
                            <p style="color: #ff6f00; margin: 5px 0;">Your default password is your surname in ALL CAPS: <strong>{employee_data['last_name'].upper()}</strong></p>
                            <p style="color: #666666;">Please change your password upon your first login for security purposes.</p>
                        </div>

                        <p style="color: #666666;">This is a system-generated email. Please do not reply.</p>
                        <br>
                        <p style="color: #666666; margin-bottom: 0;">Best regards,<br>EALS System</p>
                    </div>
                </div>
            """

            if os.path.exists(header_img):
                with open(header_img, "rb") as f:
                    img = MIMEImage(f.read())
                    img.add_header("Content-ID", "<headerimg>")
                    img.add_header("Content-Disposition", "inline", filename=os.path.basename(header_img))
                    message.attach(img)

            if os.path.exists(employee_data['profile_picture']):
                with open(employee_data['profile_picture'], "rb") as f:
                    img = MIMEImage(f.read())
                    img.add_header("Content-ID", "<profileimg>")
                    img.add_header("Content-Disposition", "inline", filename=os.path.basename(employee_data['profile_picture']))
                    message.attach(img)

            if os.path.exists(footer_img):
                with open(footer_img, "rb") as f:
                    img = MIMEImage(f.read())
                    img.add_header("Content-ID", "<footerimg>")
                    img.add_header("Content-Disposition", "inline", filename=os.path.basename(footer_img))
                    message.attach(img)

            html_header = '<img src="cid:headerimg" style="display:block; margin:auto; width:100%;"><br>' if os.path.exists(header_img) else ""
            html_footer = '<br><img src="cid:footerimg" style="display:block; margin:auto; width:100%;">' if os.path.exists(footer_img) else ""
            
            html_content = f"{html_header}{html_content}{html_footer}"
            message.attach(MIMEText(html_content, "html"))

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, sender_password)
                server.send_message(message)

            self.system_logs.log_system_action(f"Welcome email sent to {recipient_email}", "Employee")
        except Exception as e:
            print(f"Error sending welcome email: {e}")

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
                "WHERE date = ? AND is_late = 1 AND employee_id IN (SELECT employee_id FROM Employee WHERE is_hr = 0)", 
                (today_date,)
            )
            late_employees = cursor.fetchone()[0] if cursor else 0

            cursor = self.db.execute_query(
                "SELECT COUNT(*) FROM Employee WHERE is_hr = 0 AND status = 'Active' AND employee_id NOT IN ("
                "SELECT DISTINCT employee_id FROM attendance_logs WHERE date = ?)", 
                (today_date,)
            )
            absent_employees = cursor.fetchone()[0] if cursor else 0

            cursor = self.db.execute_query(
                "SELECT COUNT(*) FROM Employee WHERE is_hr = 0 AND status = 'Active' AND schedule = '6am to 2pm'"
            )
            morning_total = cursor.fetchone()[0] if cursor else 0
            cursor = self.db.execute_query(
                "SELECT COUNT(DISTINCT e.employee_id) FROM Employee e "
                "JOIN attendance_logs a ON e.employee_id = a.employee_id "
                "WHERE e.is_hr = 0 AND e.status = 'Active' AND e.schedule = '6am to 2pm' AND a.date = ? AND a.remarks = 'Clock In'",
                (today_date,)
            )
            morning_present = cursor.fetchone()[0] if cursor else 0

            # Afternoon shift
            cursor = self.db.execute_query(
                "SELECT COUNT(*) FROM Employee WHERE is_hr = 0 AND status = 'Active' AND schedule = '2pm to 10pm'"
            )
            afternoon_total = cursor.fetchone()[0] if cursor else 0
            cursor = self.db.execute_query(
                "SELECT COUNT(DISTINCT e.employee_id) FROM Employee e "
                "JOIN attendance_logs a ON e.employee_id = a.employee_id "
                "WHERE e.is_hr = 0 AND e.status = 'Active' AND e.schedule = '2pm to 10pm' AND a.date = ? AND a.remarks = 'Clock In'",
                (today_date,)
            )
            afternoon_present = cursor.fetchone()[0] if cursor else 0

            # Night shift
            cursor = self.db.execute_query(
                "SELECT COUNT(*) FROM Employee WHERE is_hr = 0 AND status = 'Active' AND schedule = '10pm to 6am'"
            )
            night_total = cursor.fetchone()[0] if cursor else 0
            cursor = self.db.execute_query(
                "SELECT COUNT(DISTINCT e.employee_id) FROM Employee e "
                "JOIN attendance_logs a ON e.employee_id = a.employee_id "
                "WHERE e.is_hr = 0 AND e.status = 'Active' AND e.schedule = '10pm to 6am' AND a.date = ? AND a.remarks = 'Clock In'",
                (today_date,)
            )
            night_present = cursor.fetchone()[0] if cursor else 0

            # --- NEW: Average overtime calculation ---
            cursor = self.db.execute_query(
                "SELECT employee_id FROM attendance_logs WHERE date = ? AND remarks = 'Clock In' AND employee_id IN (SELECT employee_id FROM Employee WHERE is_hr = 0)",
                (today_date,)
            )
            employee_ids = [row[0] for row in cursor.fetchall()] if cursor else []
            total_overtime = 0
            overtime_count = 0
            for emp_id in employee_ids:
                cur = self.db.execute_query(
                    "SELECT time, remarks FROM attendance_logs WHERE employee_id = ? AND date = ? ORDER BY time ASC",
                    (emp_id, today_date)
                )
                logs = cur.fetchall() if cur else []
                clock_in_time = None
                clock_out_time = None
                for log in logs:
                    if log[1] == "Clock In" and not clock_in_time:
                        clock_in_time = log[0]
                    elif log[1] == "Clock Out":
                        clock_out_time = log[0]
                if clock_in_time and clock_out_time:
                    try:
                        t1 = datetime.strptime(f"{today_date} {clock_in_time}", "%Y-%m-%d %H:%M:%S")
                        t2 = datetime.strptime(f"{today_date} {clock_out_time}", "%Y-%m-%d %H:%M:%S")
                        worked_hours = (t2 - t1).total_seconds() / 3600
                        overtime = worked_hours - 8
                        if overtime > 0:
                            total_overtime += overtime
                            overtime_count += 1
                    except Exception:
                        continue
            ave_overtime = round(total_overtime / overtime_count, 2) if overtime_count > 0 else 0

            self.system_logs.log_system_action("Dashboard labels have been updated.", "SystemSettings")
            self.admin_ui.total_employee_lbl.setText(f"{total_employees}/{total_employees}")
            self.admin_ui.active_employee_lbl.setText(str(active_employees))
            self.admin_ui.logged_employee_lbl.setText(str(logged_employees))
            self.admin_ui.late_employee_lbl.setText(str(late_employees))
            self.admin_ui.absent_employee_lbl.setText(str(absent_employees))

            # --- Set new shift and overtime labels ---
            if hasattr(self.admin_ui, "morning_shift_lbl"):
                self.admin_ui.morning_shift_lbl.setText(f"{morning_present}/{morning_total}")
            if hasattr(self.admin_ui, "afternoon_shift_lbl"):
                self.admin_ui.afternoon_shift_lbl.setText(f"{afternoon_present}/{afternoon_total}")
            if hasattr(self.admin_ui, "night_shift_lbl"):
                self.admin_ui.night_shift_lbl.setText(f"{night_present}/{night_total}")
            if hasattr(self.admin_ui, "ave_overtime_lbl"):
                self.admin_ui.ave_overtime_lbl.setText(str(ave_overtime))

        except sqlite3.Error as e:
            print(f"Database error while updating dashboard labels: {e}")

    def select_picture(self, label):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("JPEG Images (*.jpeg *.jpg)")
        if file_dialog.exec():
            selected_file = file_dialog.selectedFiles()[0]
            
            if os.path.getsize(selected_file) > 20 * 1024 * 1024:
                QMessageBox.warning(None, "File Size Error", "The selected file exceeds the 20MB size limit.")
                return None
            
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
        def update_picture():
            if picture_path and os.path.exists(picture_path):
                pixmap = QPixmap(picture_path)
                pixmap = pixmap.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                label.setPixmap(pixmap)
            else:
                label.clear()

        QTimer.singleShot(0, update_picture)

    def clear_employee_enrollment_fields(self):
        self.admin_ui.enroll_employee_picture.clear()
        self.admin_ui.employee_first_name.clear()
        self.admin_ui.employee_last_name.clear()
        self.admin_ui.employee_mi.clear()
        self.admin_ui.employee_id_pref.clear()
        self.admin_ui.employee_email.clear()
        self.admin_ui.employee_id_year.setCurrentIndex(0)
        self.admin_ui.employee_id_no.setCurrentIndex(0)
        self.admin_ui.employee_birthday_edit.setDate(QDate.currentDate())
        self.admin_ui.employee_male.setChecked(False)
        self.admin_ui.employee_female.setChecked(False)
        self.admin_ui.is_hr_no.setChecked(True)
        self.admin_ui.employee_department_box.setCurrentIndex(0)
        self.admin_ui.employee_position_box.setCurrentIndex(0)
        self.admin_ui.employee_sched_1.setChecked(False)
        self.admin_ui.employee_sched_2.setChecked(False)
        self.admin_ui.employee_sched_3.setChecked(False)

    def load_attendance_logs_table(self):

        try:
            cursor = self.db.execute_query("SELECT employee_id, remarks, date, time FROM attendance_logs")
            logs = cursor.fetchall() if cursor else []

            self.admin_ui.admin_attedance_logs_tbl.setRowCount(0)
            for log in logs:
                self.add_attendance_log_to_table(log)
        except sqlite3.Error as e:
            print(f"Database error while loading attendance logs: {e}")

    def add_attendance_log_to_table(self, log):
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
        sort_option = self.admin_ui.admin_attedance_logs_sort.currentText()

        logs = []
        for row in range(self.admin_ui.admin_attedance_logs_tbl.rowCount()):
            log = [
                self.admin_ui.admin_attedance_logs_tbl.item(row, col).text()
                for col in range(self.admin_ui.admin_attedance_logs_tbl.columnCount())
            ]
            logs.append(log)

        if sort_option == "By Date:":
            logs.sort(key=lambda x: x[2])  
        elif sort_option == "By Time:":
            logs.sort(key=lambda x: x[3]) 
        elif sort_option == "By Account ID:":
            logs.sort(key=lambda x: x[0]) 
        elif sort_option == "By Remarks:":
            logs.sort(key=lambda x: x[1]) 

        self.admin_ui.admin_attedance_logs_tbl.setRowCount(0)
        for log in logs:
            self.add_attendance_log_to_table(log)

    def load_employee_attendance_logs(self, employee_id):
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
        
    def handle_backup(self):
        try:
            current_admin = self.get_current_admin()
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            if self.admin_ui.backup_basic_btn.isChecked():
                backup_type = "Basic"
                backup_frequency = 1
                backup_unit = self.admin_ui.backup_basic_box.currentText()
            elif self.admin_ui.backup_custom_btn.isChecked():
                backup_type = "Custom"
                backup_frequency = self.admin_ui.backup_custom_number.text().strip()
                backup_unit = self.admin_ui.backup_custom_box.currentText()
                if not backup_frequency.isdigit() or int(backup_frequency) <= 0:
                    QMessageBox.warning(None, "Invalid Input", "Please enter a valid frequency for custom backup.")
                    return
                backup_frequency = int(backup_frequency)
            else:
                QMessageBox.warning(None, "Invalid Input", "Please select a backup type.")
                return

            retention_enabled = self.admin_ui.backup_retention_btn.isChecked()
            if retention_enabled:
                retention_frequency = self.admin_ui.backup_retention_numbers.text().strip()
                retention_unit = self.admin_ui.backup_retention_box.currentText()
                if not retention_frequency.isdigit() or int(retention_frequency) <= 0:
                    QMessageBox.warning(None, "Invalid Input", "Please enter a valid retention frequency.")
                    return
                retention_frequency = int(retention_frequency)
            else:
                retention_frequency = None
                retention_unit = None

            cursor = self.db.execute_query("SELECT id FROM system_settings LIMIT 1")
            config_exists = cursor.fetchone() is not None

            if config_exists:
                self.db.execute_query('''
                    UPDATE system_settings 
                    SET backup_type = ?, backup_frequency = ?, backup_unit = ?,
                        retention_enabled = ?, retention_frequency = ?, retention_unit = ?,
                        last_modified_by = ?, last_modified_at = ?
                    WHERE id = 1
                ''', (
                    backup_type, backup_frequency, backup_unit,
                    retention_enabled, retention_frequency, retention_unit,
                    current_admin, current_time
                ))
                self.system_logs.log_system_action(f"Backup configuration updated by {current_admin}", "SystemSettings")
            else:
                self.db.execute_query('''
                    INSERT INTO system_settings (
                        backup_type, backup_frequency, backup_unit,
                        retention_enabled, retention_frequency, retention_unit,
                        created_by, created_at, last_modified_by, last_modified_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    backup_type, backup_frequency, backup_unit,
                    retention_enabled, retention_frequency, retention_unit,
                    current_admin, current_time, current_admin, current_time
                ))
                self.system_logs.log_system_action(f"New backup configuration created by {current_admin}", "SystemSettings")

            QMessageBox.information(None, "Backup Configuration", "Backup configuration saved successfully.")

            backup_dir = "resources/backups"
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(backup_dir, f"backup_{timestamp}.db")

            shutil.copy(self.db.db_name, backup_file)
            self.system_logs.log_system_action(f"Database backup created by {current_admin}: {backup_file}", "SystemSettings")

            QMessageBox.information(None, "Backup", f"Backup created successfully: {backup_file}")

            if retention_enabled:
                self.handle_retention(backup_dir, retention_frequency, retention_unit)

            self.load_backup_table()
            self.start_backup_scheduler()

        except sqlite3.Error as e:
            self.system_logs.log_system_action(f"Database error during backup configuration: {e}", "SystemSettings")
            self.show_error("Database Error", "An error occurred while saving the backup configuration.")
        except Exception as e:
            self.system_logs.log_system_action(f"Error during backup process: {e}", "SystemSettings")
            self.show_error("Backup Error", "An unexpected error occurred during the backup process.")
            
    def load_backup_table(self):
        backup_dir = "resources/backups"
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        backup_files = [f for f in os.listdir(backup_dir) if os.path.isfile(os.path.join(backup_dir, f))]
        self.admin_ui.backup_tbl.setRowCount(0)

        for backup_file in backup_files:
            row_position = self.admin_ui.backup_tbl.rowCount()
            self.admin_ui.backup_tbl.insertRow(row_position)

            file_name_item = QTableWidgetItem(backup_file)
            file_name_item.setFlags(file_name_item.flags() & ~Qt.ItemIsEditable)
            self.admin_ui.backup_tbl.setItem(row_position, 0, file_name_item)

            try:
                if backup_file.startswith("backup_") and backup_file.endswith(".db"):
                    timestamp_part = backup_file[len("backup_"):].split(".")[0]
                    backup_date = datetime.strptime(timestamp_part, "%Y%m%d_%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
                else:
                    raise ValueError("Invalid file name format")
            except (IndexError, ValueError):
                backup_date = "Invalid format"

            date_item = QTableWidgetItem(backup_date)
            date_item.setFlags(date_item.flags() & ~Qt.ItemIsEditable)
            self.admin_ui.backup_tbl.setItem(row_position, 1, date_item)

    def restore_backup(self):
        selected_rows = self.admin_ui.backup_tbl.selectedIndexes()
        if not selected_rows:
            self.show_error("Restore Error", "Please select a backup to restore.")
            return

        row = selected_rows[0].row()
        backup_file = self.admin_ui.backup_tbl.item(row, 0).text()
        backup_path = os.path.join("resources/backups", backup_file)

        try:
            shutil.copy(backup_path, self.db.db_name)
            QMessageBox.information(None, "Restore", "Database restored successfully. The application will now restart.")

            QProcess.startDetached(sys.executable, sys.argv)
            QCoreApplication.quit()
        except Exception as e:
            print(f"Error restoring backup: {e}")
            
    def scheduled_backup(self):
        try:
            cursor = self.db.execute_query("SELECT backup_type, backup_frequency, backup_unit, retention_enabled, retention_frequency, retention_unit FROM system_settings")
            config = cursor.fetchone()

            if not config:
                QMessageBox.warning(None, "Backup Error", "No backup configuration found. Please configure the backup settings first.")
                return

            backup_type, backup_frequency, backup_unit, retention_enabled, retention_frequency, retention_unit = config

            backup_dir = "resources/backups"
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(backup_dir, f"backup_{timestamp}.db")

            shutil.copy(self.db.db_name, backup_file)
            QMessageBox.information(None, "Backup", f"Backup created successfully: {backup_file}")

            if retention_enabled:
                self.handle_retention(backup_dir, retention_frequency, retention_unit)

        except sqlite3.Error as e:
            print(f"Database error while performing scheduled backup: {e}")
        except Exception as e:
            print(f"Error during scheduled backup: {e}")
            
    def handle_retention(self, backup_dir, retention_frequency, retention_unit):
        try:
            now = datetime.now()
            if retention_unit == "Hours":
                threshold = now - timedelta(hours=retention_frequency)
            elif retention_unit == "Days":
                threshold = now - timedelta(days=retention_frequency)
            elif retention_unit == "Weeks":
                threshold = now - timedelta(weeks=retention_frequency)
            elif retention_unit == "Months":
                threshold = now - timedelta(days=retention_frequency * 30)  
            else:
                return

            for backup_file in os.listdir(backup_dir):
                if backup_file.startswith("backup_") and backup_file.endswith(".db"):
                    timestamp_part = backup_file[len("backup_"):].split(".")[0]
                    try:
                        backup_date = datetime.strptime(timestamp_part, "%Y%m%d_%H%M%S")
                        if backup_date < threshold:
                            os.remove(os.path.join(backup_dir, backup_file))
                            print(f"Deleted old backup: {backup_file}")
                    except ValueError:
                        continue

        except Exception as e:
            print(f"Error during retention handling: {e}")
            
    def start_backup_scheduler(self):
        self.backup_timer = QTimer()
        self.backup_timer.timeout.connect(self.scheduled_backup)

        self.backup_timer.start(3600000)  

    def load_backup_configuration(self):
        try:
            cursor = self.db.execute_query("SELECT backup_type, backup_frequency, backup_unit, retention_enabled, retention_frequency, retention_unit FROM system_settings")
            config = cursor.fetchone()

            if not config:
                self.admin_ui.backup_basic_btn.setChecked(True)
                self.admin_ui.backup_basic_box.setCurrentIndex(0)
                self.admin_ui.backup_custom_number.clear()
                self.admin_ui.backup_custom_box.setCurrentIndex(0)
                self.admin_ui.backup_retention_btn.setChecked(False)
                self.admin_ui.backup_retention_numbers.clear()
                self.admin_ui.backup_retention_box.setCurrentIndex(0)
                return

            backup_type, backup_frequency, backup_unit, retention_enabled, retention_frequency, retention_unit = config

            if backup_type == "Basic":
                self.admin_ui.backup_basic_btn.setChecked(True)
                self.admin_ui.backup_basic_box.setCurrentText(backup_unit)
            elif backup_type == "Custom":
                self.admin_ui.backup_custom_btn.setChecked(True)
                self.admin_ui.backup_custom_number.setText(str(backup_frequency))
                self.admin_ui.backup_custom_box.setCurrentText(backup_unit)

            self.admin_ui.backup_retention_btn.setChecked(bool(retention_enabled))
            if retention_enabled:
                self.admin_ui.backup_retention_numbers.setText(str(retention_frequency))
                self.admin_ui.backup_retention_box.setCurrentText(retention_unit)

        except sqlite3.Error as e:
            print(f"Database error while loading backup configuration: {e}")

    def show_success(self, title, message):
        chime.theme('chime')
        chime.success()
        toast = Toast(self.admin_ui)
        toast.setTitle(title)
        toast.setText(message)
        toast.setDuration(2000)  
        toast.setOffset(25, 35)  
        toast.setBorderRadius(6)  
        toast.applyPreset(ToastPreset.SUCCESS)  
        toast.setBackgroundColor(QColor('#FFFFFF')) 
        toast.setPositionRelativeToWidget(self.admin_ui.home_tabs)
        toast.setPosition(ToastPosition.TOP_RIGHT)  
        toast.show() 

    def show_error(self, title, message):
        chime.theme('big-sur')
        chime.warning()
        toast = Toast(self.admin_ui)
        toast.setTitle(title)
        toast.setText(message)
        toast.setDuration(2000)  
        toast.setOffset(25, 35)  
        toast.setBorderRadius(6)  
        toast.applyPreset(ToastPreset.ERROR)  
        toast.setBackgroundColor(QColor('#FFFFFF'))  
        toast.setPositionRelativeToWidget(self.admin_ui.home_tabs)
        toast.setPosition(ToastPosition.TOP_RIGHT)  
        toast.show()  
        
    def check_net(self):
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=5)
            return True
        except OSError:
            toast = Toast(self.admin_ui)
            toast.setTitle("No Internet Connection")
            toast.setText("Please check your internet connection and try again.")
            toast.setOffset(40, 45)
            toast.setBorderRadius(6)
            toast.applyPreset(ToastPreset.ERROR)
            toast.setBackgroundColor(QColor('#ffb7b6'))
            toast.setPosition(ToastPosition.TOP_RIGHT)
            toast.setShowDurationBar(False)
            toast.setDuration(0) 
            toast.show()
            return False
        
    def setup_attendance_area_chart(self):
        self.chart = QChart()
        self.present_series = QLineSeries()
        self.absent_series = QLineSeries()
        self.present_series.setName("Present")
        self.absent_series.setName("Absent")

        self.present_area = QAreaSeries(self.present_series)
        self.present_area.setName("Present")
        self.present_area.setColor(QColor(128, 173, 246, 180))  
        self.present_area.setBorderColor(QColor(128, 173, 246))  
        self.present_area.setOpacity(0.6)  

        self.absent_area = QAreaSeries(self.absent_series)
        self.absent_area.setName("Absent")
        self.absent_area.setColor(QColor(48, 9, 154, 180))  
        self.absent_area.setBorderColor(QColor(48, 9, 154))  
        self.absent_area.setOpacity(0.6)  

        self.chart.setBackgroundBrush(QColor(239, 239, 239))

        self.chart.addSeries(self.present_area)
        self.chart.addSeries(self.absent_area)

        self.axis_x = QValueAxis()
        self.axis_x.setTitleText("Day of Month")
        self.axis_x.setLabelFormat("%d")
        self.axis_y = QValueAxis()
        self.axis_y.setTitleText("Count")
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)
        self.present_area.attachAxis(self.axis_x)
        self.present_area.attachAxis(self.axis_y)
        self.absent_area.attachAxis(self.axis_x)
        self.absent_area.attachAxis(self.axis_y)

        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        self.update_attendance_area_chart()


    def update_attendance_area_chart(self):
        self.present_series.clear()
        self.absent_series.clear()

        try:
            cursor = self.db.execute_query(
                """
                SELECT date(created_at) as log_date, present_count, absent_count
                FROM system_logs
                WHERE date(created_at) >= date('now', '-6 days')
                ORDER BY date(created_at)
                """
            )
            data = cursor.fetchall() if cursor else []
            if not data:
                return

            dates = []
            presents = []
            absents = []
            max_y = 1  

            for row in data:
                date_str, present, absent = row
                try:
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                    dates.append(date_obj.strftime("%d"))  
                    presents.append(int(present))
                    absents.append(int(absent))
                    max_y = max(max_y, int(present), int(absent))
                except Exception:
                    continue

            if not dates:
                return

            self.chart.removeAxis(self.axis_x)
            
            axis_x = QCategoryAxis()
            axis_x.setTitleText("Day of Month")
            axis_x.setLabelsPosition(QCategoryAxis.AxisLabelsPositionOnValue) 
            self.axis_x = axis_x
            
            point_count = len(dates)
            for i in range(point_count):
                self.present_series.append(i, presents[i])
                self.absent_series.append(i, absents[i])
                axis_x.append(dates[i], i)
            
            self.axis_x.setRange(0, point_count - 1)
            self.axis_y.setRange(0, max_y)
            self.axis_y.setTickCount(max_y + 1)  
            self.axis_y.setLabelFormat("%d")
            
            self.chart.addAxis(self.axis_x, Qt.AlignBottom)
            self.present_area.attachAxis(self.axis_x)
            self.absent_area.attachAxis(self.axis_x)

        except Exception as e:
            print(f"Error updating attendance area chart: {e}")
   
    def setup_avg_work_hours_line_chart(self):
        self.avg_chart = QChart()
        self.bar_series = QBarSeries()
        self.line_series = QLineSeries()
        self.bar_set = QBarSet("Actual")
        self.bar_series.append(self.bar_set)
        self.line_series.setName("Average")

        pen = self.line_series.pen()
        pen.setWidth(3)
        pen.setColor(QColor(255, 140, 0))
        self.line_series.setPen(pen)

        self.avg_chart.addSeries(self.bar_series)
        self.avg_chart.addSeries(self.line_series)
        self.avg_chart.setBackgroundBrush(QColor(239, 239, 239))

        self.avg_axis_x = QCategoryAxis()
        self.avg_axis_x.setTitleText("Day")
        self.avg_axis_x.setLabelsPosition(QCategoryAxis.AxisLabelsPositionOnValue)

        self.avg_axis_y = QValueAxis()
        self.avg_axis_y.setTitleText("Hours")
        self.avg_axis_y.setLabelFormat("%.1f")
        self.avg_axis_y.setRange(0, 12)

        self.avg_chart.addAxis(self.avg_axis_x, Qt.AlignBottom)
        self.avg_chart.addAxis(self.avg_axis_y, Qt.AlignLeft)
        self.bar_series.attachAxis(self.avg_axis_x)
        self.bar_series.attachAxis(self.avg_axis_y)
        self.line_series.attachAxis(self.avg_axis_x)
        self.line_series.attachAxis(self.avg_axis_y)

        self.avg_chart.legend().setVisible(True)
        self.avg_chart.legend().setAlignment(Qt.AlignBottom)

        self.avg_work_hours_chart_view = QChartView(self.avg_chart)
        self.avg_work_hours_chart_view.setRenderHint(QPainter.Antialiasing)

        self.update_avg_work_hours_line_chart()

    def update_avg_work_hours_line_chart(self):
        self.bar_set.remove(0, self.bar_set.count())
        self.line_series.clear()
        self.avg_chart.removeAxis(self.avg_axis_x)
        self.avg_axis_x = QCategoryAxis()
        self.avg_axis_x.setTitleText("Day")
        self.avg_axis_x.setLabelsPosition(QCategoryAxis.AxisLabelsPositionOnValue)

        try:
            cursor = self.db.execute_query(
                """
                SELECT date(created_at) as log_date, average_work_hours
                FROM system_logs
                WHERE date(created_at) >= date('now', '-6 days')
                ORDER BY date(created_at)
                """
            )
            data = cursor.fetchall() if cursor else []
            if not data:
                return

            days = []
            hours = []
            max_hour = 1

            for idx, row in enumerate(data):
                date_str, avg_hours = row
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                day_label = date_obj.strftime("%a")
                days.append(day_label)
                hours_val = float(avg_hours) if avg_hours is not None else 0
                hours.append(hours_val)
                max_hour = max(max_hour, hours_val)

            # Add bar values
            for val in hours:
                self.bar_set << val
                
            color = QColor(112, 205, 152)
            color.setAlphaF(0.6)  # 0.6 opacity
            self.bar_set.setColor(color)

            avg_val = sum(hours) / len(hours) if hours else 0

            for i in range(len(days)):
                self.line_series.append(i, avg_val)

            for i, label in enumerate(days):
                self.avg_axis_x.append(label, i)

            self.avg_axis_x.setRange(0, len(days) - 1)
            self.avg_chart.addAxis(self.avg_axis_x, Qt.AlignBottom)
            self.bar_series.attachAxis(self.avg_axis_x)
            self.line_series.attachAxis(self.avg_axis_x)
            self.avg_axis_y.setRange(0, max(8, int(max_hour + 1)))
            self.avg_axis_y.setTickCount(min(13, int(max_hour + 2)))
        except Exception as e:
            print(f"Error updating avg work hours line chart: {e}")

    def setup_attendance_pie_chart(self):
        self.pie_chart = QChart()
        self.pie_series = QPieSeries()
        self.pie_chart.addSeries(self.pie_series)
        self.pie_chart.setBackgroundBrush(QColor(239, 239, 239))
        self.pie_chart.legend().setVisible(True)
        self.pie_chart.legend().setAlignment(Qt.AlignBottom)
        self.pie_chart_view = QChartView(self.pie_chart)
        self.pie_chart_view.setRenderHint(QPainter.Antialiasing)
        self.update_attendance_pie_chart()

    def update_attendance_pie_chart(self):
        self.pie_series.clear()
        try:
            today_date = datetime.now().strftime("%Y-%m-%d")
            cursor = self.db.execute_query(
                "SELECT COUNT(DISTINCT employee_id) FROM attendance_logs WHERE date = ? AND employee_id IN (SELECT employee_id FROM Employee WHERE is_hr = 0)",
                (today_date,)
            )
            present = cursor.fetchone()[0] if cursor else 0

            cursor = self.db.execute_query(
                "SELECT COUNT(*) FROM Employee WHERE is_hr = 0 AND status = 'Active' AND employee_id NOT IN (SELECT DISTINCT employee_id FROM attendance_logs WHERE date = ?)",
                (today_date,)
            )
            absent = cursor.fetchone()[0] if cursor else 0

            total = present + absent
            if total == 0:
                self.pie_series.append("No Data", 1)
                self.pie_series.slices()[0].setColor(QColor(200, 200, 200))
                self.pie_series.slices()[0].setLabelVisible(True)
            else:
                present_pct = (present / total) * 100
                absent_pct = (absent / total) * 100
                present_slice = self.pie_series.append(f"Present ({present_pct:.1f}%)", present)
                absent_slice = self.pie_series.append(f"Absent ({absent_pct:.1f}%)", absent)
                present_slice.setColor(QColor(255, 174, 53))
                absent_slice.setColor(QColor(240, 86, 68))
                present_slice.setLabelVisible(True)
                absent_slice.setLabelVisible(True)
        except Exception as e:
            print(f"Error updating attendance pie chart: {e}")

class Announcement:
    def __init__(self, db, hr_data, hr_ui):
        self.db = db
        self.hr_data = hr_data
        self.hr_ui = hr_ui
        self.attachments = []
        self.edit_radio_buttons = []
        
        self.hr_ui.hr_announcements_pages.setCurrentWidget(self.hr_ui.email_page)

        self.hr_ui.employee_send_all_btn.toggled.connect(self.toggle_send_all)
        self.hr_ui.employee_choose_btn.toggled.connect(self.toggle_choose_employee)
        self.hr_ui.email_employee_search_box.textChanged.connect(self.filter_employee_table)
        self.hr_ui.email_employee_sort_box.currentIndexChanged.connect(self.sort_employee_table)
        self.hr_ui.save_as_template_btn.clicked.connect(self.save_as_template)
        self.hr_ui.import_btn.clicked.connect(self.import_template)
        self.hr_ui.attach_btn.clicked.connect(self.attach_files)
        self.hr_ui.send_email_btn.clicked.connect(self.send_announcement_email)
        self.hr_ui.email_view_btn.clicked.connect(self.view_selected_sched_email)
        self.hr_ui.edit_email_btn.clicked.connect(self.edit_selected_sched_email)
        self.hr_ui.delete_email_btn.clicked.connect(self.delete_selected_sched_email)
        self.hr_ui.view_email_back_btn.clicked.connect(self.back_from_view_email)
        self.hr_ui.edit_email_back_btn.clicked.connect(self.back_from_edit_email)
        self.hr_ui.save_email_btn.clicked.connect(self.save_edited_email)

        self.hr_ui.view_employee_send_all_btn.toggled.connect(self.toggle_view_send_all)
        self.hr_ui.view_employee_choose_btn.toggled.connect(self.toggle_view_choose_employee)
        self.hr_ui.edit_employee_send_all_btn.toggled.connect(self.toggle_edit_send_all)
        self.hr_ui.edit_employee_choose_btn.toggled.connect(self.toggle_edit_choose_employee)

        self.radio_buttons = []  # Track radio buttons for single selection

        self.load_employee_table()
        self.toggle_send_all()  # Set initial state

        # --- Scheduled emails UI connections ---
        self.hr_ui.sched_email_search_box.textChanged.connect(self.filter_sched_email_table)
        self.hr_ui.sched_email_sort_box.currentIndexChanged.connect(self.sort_sched_email_table)
        self.load_sched_email_table()

        # Ensure table is only enabled when choose is checked
        self.hr_ui.selectable_employee_list_tbl.setEnabled(self.hr_ui.employee_choose_btn.isChecked())
        self.hr_ui.employee_choose_btn.toggled.connect(self.toggle_choose_employee)

    def show_success(self, title, message):
        chime.theme('chime')
        chime.success()
        toast = Toast(self.hr_ui)
        toast.setTitle(title)
        toast.setText(message)
        toast.setDuration(2000)
        toast.setOffset(25, 35)
        toast.setBorderRadius(6)
        toast.applyPreset(ToastPreset.SUCCESS)
        toast.setBackgroundColor(QColor('#FFFFFF'))
        toast.setPositionRelativeToWidget(self.hr_ui.hr_home_tabs)
        toast.setPosition(ToastPosition.TOP_RIGHT)
        toast.show()

    def show_error(self, title, message):
        chime.theme('big-sur')
        chime.warning()
        toast = Toast(self.hr_ui)
        toast.setTitle(title)
        toast.setText(message)
        toast.setDuration(2000)
        toast.setOffset(25, 35)
        toast.setBorderRadius(6)
        toast.applyPreset(ToastPreset.ERROR)
        toast.setBackgroundColor(QColor('#FFFFFF'))
        toast.setPositionRelativeToWidget(self.hr_ui.hr_home_tabs)
        toast.setPosition(ToastPosition.TOP_RIGHT)
        toast.show()

    def show_warning(self, title, message):
        chime.warning()
        toast = Toast(self.hr_ui)
        toast.setTitle(title)
        toast.setText(message)
        toast.setDuration(2000)
        toast.setOffset(25, 35)
        toast.setBorderRadius(6)
        toast.applyPreset(ToastPreset.WARNING)
        toast.setBackgroundColor(QColor('#FFFFFF'))
        toast.setPositionRelativeToWidget(self.hr_ui.hr_home_tabs)
        toast.setPosition(ToastPosition.TOP_RIGHT)
        toast.show()

    def toggle_view_send_all(self):
        self.hr_ui.view_email_employee_list_tbl.setDisabled(self.hr_ui.view_employee_send_all_btn.isChecked())
        if self.hr_ui.view_employee_send_all_btn.isChecked():
            self.load_view_email_employee_table("All")

    def toggle_view_choose_employee(self):
        self.hr_ui.view_email_employee_list_tbl.setEnabled(self.hr_ui.view_employee_choose_btn.isChecked())
        if self.hr_ui.view_employee_choose_btn.isChecked():
            self.load_view_email_employee_table("Selected")

    def toggle_edit_send_all(self):
        self.hr_ui.edit_email_employee_list_tbl.setDisabled(self.hr_ui.edit_employee_send_all_btn.isChecked())
        if self.hr_ui.edit_employee_send_all_btn.isChecked():
            self.load_edit_email_employee_table("All")
    
    def toggle_edit_choose_employee(self):
        self.hr_ui.edit_email_employee_list_tbl.setEnabled(self.hr_ui.edit_employee_choose_btn.isChecked())
        if self.hr_ui.edit_employee_choose_btn.isChecked():
            self.load_edit_email_employee_table("Selected")

    def load_view_email_employee_table(self, sending_type):
        tbl = self.hr_ui.view_email_employee_list_tbl
        tbl.setRowCount(0)
        if sending_type == "All":
            cursor = self.db.execute_query("SELECT employee_id, first_name, last_name, middle_initial, department, position FROM Employee WHERE is_hr = 0 AND status = 'Active'")
        else:
            cursor = self.db.execute_query("SELECT employee_id, first_name, last_name, middle_initial, department, position FROM Employee WHERE employee_id = ?", (self.hr_data["employee_id"],))
        employees = cursor.fetchall() if cursor else []
        for emp in employees:
            row = tbl.rowCount()
            tbl.insertRow(row)
            mi = f" {emp[3]}." if emp[3] else ""
            name = f"{emp[2]}, {emp[1]}{mi}"
            tbl.setItem(row, 0, QTableWidgetItem(name))
            tbl.setItem(row, 1, QTableWidgetItem(emp[0]))
            tbl.setItem(row, 2, QTableWidgetItem(f"{emp[4]} / {emp[5]}"))
        tbl.resizeColumnsToContents()

    def load_edit_email_employee_table(self, sending_type):
        tbl = self.hr_ui.edit_email_employee_list_tbl
        tbl.setRowCount(0)
        if sending_type == "All":
            cursor = self.db.execute_query("SELECT employee_id, first_name, last_name, middle_initial, department, position FROM Employee WHERE is_hr = 0 AND status = 'Active'")
        else:
            cursor = self.db.execute_query("SELECT employee_id, first_name, last_name, middle_initial, department, position FROM Employee WHERE employee_id = ?", (self.hr_data["employee_id"],))
        employees = cursor.fetchall() if cursor else []
        for emp in employees:
            row = tbl.rowCount()
            tbl.insertRow(row)
            mi = f" {emp[3]}." if emp[3] else ""
            name = f"{emp[2]}, {emp[1]}{mi}"
            tbl.setItem(row, 0, QTableWidgetItem(name))
            tbl.setItem(row, 1, QTableWidgetItem(emp[0]))
            tbl.setItem(row, 2, QTableWidgetItem(f"{emp[4]} / {emp[5]}"))
        tbl.resizeColumnsToContents()

    def toggle_send_all(self):
        # If send all is checked, disable table
        self.hr_ui.selectable_employee_list_tbl.setDisabled(self.hr_ui.employee_send_all_btn.isChecked())
        # If send all is checked, also unselect all radios
        if self.hr_ui.employee_send_all_btn.isChecked():
            for radio in self.radio_buttons:
                radio.setChecked(False)

    def toggle_choose_employee(self):
        # Only enable table if choose is checked
        enabled = self.hr_ui.employee_choose_btn.isChecked()
        self.hr_ui.selectable_employee_list_tbl.setEnabled(enabled)
        if not enabled:
            for radio in self.radio_buttons:
                radio.setChecked(False)

    def load_sched_email_table(self):
        tbl = self.hr_ui.sched_email_list_tbl
        tbl.setRowCount(0)
        cursor = self.db.execute_query(
            "SELECT subject, created_at, schedule_frequency FROM announcements WHERE schedule_enabled = 1 ORDER BY created_at DESC"
        )
        self.sched_email_entries = cursor.fetchall() if cursor else []
        for entry in self.sched_email_entries:
            row = tbl.rowCount()
            tbl.insertRow(row)
            tbl.setItem(row, 0, QTableWidgetItem(entry[0]))  # Subject
            tbl.setItem(row, 1, QTableWidgetItem(str(entry[1])))  # Created at
            tbl.setItem(row, 2, QTableWidgetItem(str(entry[2])))  # Frequency

    def filter_sched_email_table(self):
        search_text = self.hr_ui.sched_email_search_box.text().lower()
        tbl = self.hr_ui.sched_email_list_tbl
        for row in range(tbl.rowCount()):
            show = False
            for col in range(tbl.columnCount()):
                item = tbl.item(row, col)
                if item and search_text in item.text().lower():
                    show = True
                    break
            tbl.setRowHidden(row, not show)

    def sort_sched_email_table(self):
        sort_option = self.hr_ui.sched_email_sort_box.currentText()
        tbl = self.hr_ui.sched_email_list_tbl
        # Gather all rows
        rows = []
        for row in range(tbl.rowCount()):
            row_data = [tbl.item(row, col).text() if tbl.item(row, col) else "" for col in range(tbl.columnCount())]
            rows.append(row_data)
        # Sort
        if sort_option == "By Subject:":
            rows.sort(key=lambda x: x[0].lower())
        elif sort_option == "By Created Date:":
            rows.sort(key=lambda x: x[1], reverse=True)
        elif sort_option == "By Frequency:":
            rows.sort(key=lambda x: x[2].lower())
        # Repopulate
        tbl.setRowCount(0)
        for row_data in rows:
            row = tbl.rowCount()
            tbl.insertRow(row)
            for col, val in enumerate(row_data):
                tbl.setItem(row, col, QTableWidgetItem(val))
        tbl.resizeColumnsToContents()
    
    def load_employee_table(self):
        cursor = self.db.execute_query("SELECT employee_id, first_name, last_name, middle_initial, department, position FROM Employee WHERE is_hr = 0 AND status = 'Active'")
        employees = cursor.fetchall() if cursor else []
        tbl = self.hr_ui.selectable_employee_list_tbl
        tbl.setRowCount(0)
        self.employee_list = []
        self.radio_buttons = []
        for emp in employees:
            emp_data = {
                "employee_id": emp[0],
                "first_name": emp[1],
                "last_name": emp[2],
                "middle_initial": emp[3],
                "department": emp[4],
                "position": emp[5]
            }
            self.employee_list.append(emp_data)
            row = tbl.rowCount()
            tbl.insertRow(row)
            # Add radio button for selection
            radio = QRadioButton()
            radio.setStyleSheet("background-color: white;")  # Set white background
            radio.toggled.connect(lambda checked, r=row: self.handle_radio_selected(r, checked))
            self.radio_buttons.append(radio)
            tbl.setCellWidget(row, 0, radio)
            # Name
            mi = f" {emp_data['middle_initial']}." if emp_data['middle_initial'] else ""
            name = f"{emp_data['last_name']}, {emp_data['first_name']}{mi}"
            tbl.setItem(row, 1, QTableWidgetItem(name))
            tbl.setItem(row, 2, QTableWidgetItem(emp_data['employee_id']))
            tbl.setItem(row, 3, QTableWidgetItem(f"{emp_data['department']} / {emp_data['position']}"))
        tbl.resizeColumnsToContents()

    def handle_radio_selected(self, row, checked):
        if checked:
            # Uncheck all other radios
            for idx, radio in enumerate(self.radio_buttons):
                if idx != row:
                    radio.setChecked(False)

    def filter_employee_table(self):
        search_text = self.hr_ui.email_employee_search_box.text().lower()
        tbl = self.hr_ui.selectable_employee_list_tbl
        for row in range(tbl.rowCount()):
            show = False
            for col in range(1, tbl.columnCount()):
                item = tbl.item(row, col)
                if item and search_text in item.text().lower():
                    show = True
                    break
            tbl.setRowHidden(row, not show)

    def sort_employee_table(self):
        sort_option = self.hr_ui.email_employee_sort_box.currentText()
        if sort_option == "By Name:":
            self.employee_list.sort(key=lambda x: (x["last_name"].lower(), x["first_name"].lower()))
        elif sort_option == "By Account ID:":
            self.employee_list.sort(key=lambda x: x["employee_id"])
        elif sort_option == "By Department:":
            self.employee_list.sort(key=lambda x: x["department"].lower())
        # Re-populate table
        self.hr_ui.selectable_employee_list_tbl.setRowCount(0)
        self.radio_buttons = []
        for emp_data in self.employee_list:
            row = self.hr_ui.selectable_employee_list_tbl.rowCount()
            self.hr_ui.selectable_employee_list_tbl.insertRow(row)
            radio = QRadioButton()
            radio.setStyleSheet("background-color: white;")  # Set white background
            radio.toggled.connect(lambda checked, r=row: self.handle_radio_selected(r, checked))
            self.radio_buttons.append(radio)
            self.hr_ui.selectable_employee_list_tbl.setCellWidget(row, 0, radio)
            mi = f" {emp_data['middle_initial']}." if emp_data['middle_initial'] else ""
            name = f"{emp_data['last_name']}, {emp_data['first_name']}{mi}"
            self.hr_ui.selectable_employee_list_tbl.setItem(row, 1, QTableWidgetItem(name))
            self.hr_ui.selectable_employee_list_tbl.setItem(row, 2, QTableWidgetItem(emp_data["employee_id"]))
            self.hr_ui.selectable_employee_list_tbl.setItem(row, 3, QTableWidgetItem(f"{emp_data['department']} / {emp_data['position']}"))
        self.hr_ui.selectable_employee_list_tbl.resizeColumnsToContents()

    def get_theme_images(self):

        theme_map = {
            "Default": ("default_theme_header.jpg", "default_theme_footer.jpg"),
            "Christmass Design": ("xmass_theme_header.jpg", "xmass_theme_footer.jpg"),
            "Design 1": ("theme1_header.jpg", "theme1_footer.jpg"),
            "Design 2": ("theme2_header.jpg", "theme2_footer.jpg"),
        }
        theme = "Default"  
        if self.hr_ui.set_theme_btn.isChecked():
            theme = self.hr_ui.theme_design_box.currentText()
        header, footer = theme_map.get(theme, theme_map["Default"])
        header_path = os.path.join("resources", "theme_images", header)
        footer_path = os.path.join("resources", "theme_images", footer)
        return header_path, footer_path

    def attach_files(self):
        valid_exts = ('.pdf', '.jpg', '.jpeg', '.png', '.doc', '.docx', '.xls', '.xlsx', '.txt', '.csv', '.zip')
        files, _ = QFileDialog.getOpenFileNames(self.hr_ui, "Select Attachments", "", 
            "Allowed Files (*.pdf *.jpg *.jpeg *.png *.doc *.docx *.xls *.xlsx *.txt *.csv *.zip)")
        if files:
            valid_files = [f for f in files if os.path.splitext(f)[1].lower() in valid_exts]
            if len(valid_files) < len(files):
                QMessageBox.warning(self.hr_ui, "Attachment Error", "Some files were not added because they are not supported by Gmail.")
            for f in valid_files:
                if f not in self.attachments:
                    self.attachments.append(f)
            self.update_attachments_list()

    def update_attachments_list(self):
        lw: QListWidget = self.hr_ui.attachments_list
        lw.clear()
        for file_path in self.attachments:
            fname = os.path.basename(file_path)
            item_widget = QWidget()
            hbox = QHBoxLayout(item_widget)
            hbox.setContentsMargins(0, 0, 0, 0)
            label = QLabel(fname)
            btn = QPushButton("✕")
            btn.setFixedSize(20, 20)
            btn.setStyleSheet("color: red; background: transparent; border: none; font-weight: bold;")
            btn.clicked.connect(lambda _, f=file_path: self.remove_attachment(f))
            hbox.addWidget(label)
            hbox.addWidget(btn)
            hbox.addStretch()
            item_widget.setLayout(hbox)
            item = QListWidgetItem()
            item.setSizeHint(item_widget.sizeHint())
            lw.addItem(item)
            lw.setItemWidget(item, item_widget)

    def remove_attachment(self, file_path):
        if file_path in self.attachments:
            if os.path.commonpath([os.path.abspath(file_path), os.path.abspath("resources/email_files")]) == os.path.abspath("resources/email_files"):
                try:
                    os.remove(file_path)
                except Exception:
                    pass
            self.attachments.remove(file_path)
            self.update_attachments_list()

    def save_as_template(self):
        # Save current announcement as a template (JSON)
        template_dir = "resources/email_templates"
        if not os.path.exists(template_dir):
            os.makedirs(template_dir)
        subject = self.hr_ui.email_subject.text()
        message = self.hr_ui.email_message.toPlainText()
        schedule = self.hr_ui.set_schedule_btn.isChecked()
        schedule_freq = self.hr_ui.schedule_frequency_box.currentText() if schedule else ""
        theme = self.hr_ui.set_theme_btn.isChecked()
        theme_type = self.hr_ui.theme_design_box.currentText() if theme else ""
        template = {
            "subject": subject,
            "message": message,
            "schedule": schedule,
            "schedule_frequency": schedule_freq,
            "theme": theme,
            "theme_type": theme_type
        }
        fname, _ = QFileDialog.getSaveFileName(self.hr_ui, "Save Template", template_dir, "JSON Files (*.json)")
        if fname:
            with open(fname, "w", encoding="utf-8") as f:
                json.dump(template, f)

    def import_template(self):
        template_dir = "resources/email_templates"
        fname, _ = QFileDialog.getOpenFileName(self.hr_ui, "Import Template", template_dir, "JSON Files (*.json)")
        if fname:
            with open(fname, "r", encoding="utf-8") as f:
                template = json.load(f)
            self.hr_ui.email_subject.setText(template.get("subject", ""))
            self.hr_ui.email_message.setPlainText(template.get("message", ""))
            if template.get("schedule", False):
                self.hr_ui.set_schedule_btn.setChecked(True)
                self.hr_ui.schedule_frequency_box.setCurrentText(template.get("schedule_frequency", "Daily"))
            else:
                self.hr_ui.set_schedule_btn.setChecked(False)
            if template.get("theme", False):
                self.hr_ui.set_theme_btn.setChecked(True)
                self.hr_ui.theme_design_box.setCurrentText(template.get("theme_type", ""))
            else:
                self.hr_ui.set_theme_btn.setChecked(False)

    def compose_html_body(self, message, subject, header_img, footer_img):
        html_header = '<img src="cid:headerimg" style="display:block; margin:auto; width:100%;"><br>' if os.path.exists(header_img) else ""
        
        html_content = f"""
            <div style="margin: 20px auto; padding: 20px; max-width: 600px; font-family: Arial, sans-serif;">
                <div style="background-color: #4285f4; color: white; padding: 20px; border-radius: 8px 8px 0 0;">
                    <h2 style="margin: 0; text-align: center;">{subject}</h2>
                </div>
                <div style="background-color: #ffffff; padding: 20px; border-radius: 0 0 8px 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="color: #666666; line-height: 1.6;">
                        {message}
                    </div>
                    <br>
                    <div style="color: #666666; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
                        <p style="margin-bottom: 0;">Best regards,<br>EALS HR Team</p>
                    </div>
                </div>
            </div>
        """
        html_footer = '<br><img src="cid:footerimg" style="display:block; margin:auto; width:100%;">' if os.path.exists(footer_img) else ""
        return f"{html_header}{html_content}{html_footer}"

    def send_emails(self, recipients, subject, message, header_img, footer_img):
        sender_email = "eals.tupc@gmail.com"
        sender_password = "buwl tszg dghr exln"
        
        for recipient in recipients:
            try:
                msg = MIMEMultipart()
                msg["From"] = sender_email
                msg["To"] = recipient
                msg["Subject"] = subject

                # Attach header image
                if os.path.exists(header_img):
                    with open(header_img, "rb") as f:
                        img = MIMEImage(f.read())
                        img.add_header("Content-ID", "<headerimg>")
                        img.add_header("Content-Disposition", "inline", filename=os.path.basename(header_img))
                        msg.attach(img)

                # Attach footer image
                if os.path.exists(footer_img):
                    with open(footer_img, "rb") as f:
                        img = MIMEImage(f.read())
                        img.add_header("Content-ID", "<footerimg>")
                        img.add_header("Content-Disposition", "inline", filename=os.path.basename(footer_img))
                        msg.attach(img)

                # Attach HTML content
                html_body = self.compose_html_body(message, subject, header_img, footer_img)
                msg.attach(MIMEText(html_body, "html"))

                # Attach files
                for file_path in self.attachments:
                    try:
                        with open(file_path, "rb") as f:
                            from email.mime.base import MIMEBase
                            from email import encoders
                            part = MIMEBase("application", "octet-stream")
                            part.set_payload(f.read())
                            encoders.encode_base64(part)
                            part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(file_path)}")
                            msg.attach(part)
                    except Exception as e:
                        print(f"Attachment error: {file_path}: {e}")
                        continue

                # Send email
                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                    server.login(sender_email, sender_password)
                    server.send_message(msg)
                

            except Exception as e:
                print(f"Error sending announcement email to {recipient}: {e}")

    def send_announcement_email(self):
        subject = self.hr_ui.email_subject.text()
        message = self.hr_ui.email_message.toPlainText()
        # --- Failsafe checks ---
        if not subject.strip():
            self.show_error("Missing Subject", "Please enter a subject for the announcement.")
            return
        if not message.strip():
            self.show_error("Missing Message", "Please enter a message for the announcement.")
            return
        if not (self.hr_ui.employee_send_all_btn.isChecked() or self.hr_ui.employee_choose_btn.isChecked()):
            self.show_error("No Recipient Type", "Please select either 'Send to All' or 'Choose Employee'.")
            return
        if self.hr_ui.employee_choose_btn.isChecked():
            selected = any(radio.isChecked() for radio in self.radio_buttons)
            if not selected:
                self.show_error("No Employee Selected", "Please select at least one employee from the table.")
                return
        schedule_enabled = self.hr_ui.set_schedule_btn.isChecked()
        schedule_frequency = self.hr_ui.schedule_frequency_box.currentText() if schedule_enabled else None
        theme_enabled = self.hr_ui.set_theme_btn.isChecked()
        theme_type = self.hr_ui.theme_design_box.currentText() if theme_enabled else None
        header_img, footer_img = self.get_theme_images()

        sending_type = "All" if self.hr_ui.employee_send_all_btn.isChecked() else "Selected"
        involved_employee = None
        recipients = []
        if sending_type == "All":
            cursor = self.db.execute_query("SELECT email FROM Employee WHERE is_hr = 0 AND status = 'Active'")
            recipients = [row[0] for row in cursor.fetchall()] if cursor else []
        else:
            tbl = self.hr_ui.selectable_employee_list_tbl
            for row, radio in enumerate(self.radio_buttons):
                if radio.isChecked():
                    emp_id = tbl.item(row, 2).text()
                    cursor = self.db.execute_query("SELECT email FROM Employee WHERE employee_id = ?", (emp_id,))
                    result = cursor.fetchone()
                    if result:
                        recipients.append(result[0])
                        involved_employee = emp_id
                    break

        # Save announcement to database and handle attachments
        self.save_announcement_to_db(subject, message, sending_type, involved_employee, 
                                   schedule_enabled, schedule_frequency, theme_enabled, theme_type)

        # Send emails in background thread
        QTimer.singleShot(0, lambda: self.show_success("Announcement Sent", f"Successfully sent announcement email."))
        threading.Thread(
            target=lambda: self.send_emails(recipients, subject, message, header_img, footer_img),
            daemon=True
        ).start()

        # Clear form
        self.clear_announcement_form()

    def save_announcement_to_db(self, subject, message, sending_type, involved_employee, 
                              schedule_enabled, schedule_frequency, theme_enabled, theme_type):
        cursor = self.db.execute_query(
            '''INSERT INTO announcements (subject, message, sending_type, involved_employee, 
               schedule_enabled, schedule_frequency, theme_enabled, theme_type, 
               attached_files_count, files_path, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (subject, message, sending_type, involved_employee, schedule_enabled, 
             schedule_frequency, theme_enabled, theme_type, 0, "", self.hr_data["employee_id"])
        )
        
        cursor = self.db.execute_query("SELECT id FROM announcements ORDER BY id DESC LIMIT 1")
        announcement_id = cursor.fetchone()[0] if cursor else None

        if announcement_id:
            self.handle_attachments(announcement_id)

    def handle_attachments(self, announcement_id):
        """Handle saving attachments for an announcement"""
        if not self.attachments:
            return

        email_files_dir = os.path.join("resources", "email_files", str(announcement_id))
        if not os.path.exists(email_files_dir):
            os.makedirs(email_files_dir)

        new_attachment_paths = []
        for file_path in self.attachments:
            dest = os.path.join(email_files_dir, os.path.basename(file_path))
            if not os.path.exists(dest):
                try:
                    shutil.copy(file_path, dest)
                except Exception as e:
                    print(f"Error copying attachment {file_path}: {e}")
                    continue
            new_attachment_paths.append(dest)

        if new_attachment_paths:
            self.db.execute_query(
                "UPDATE announcements SET attached_files_count = ?, files_path = ? WHERE id = ?",
                (len(new_attachment_paths), ";".join(new_attachment_paths), announcement_id)
            )
            # Update the attachments list with the new paths
            self.attachments = new_attachment_paths
            self.update_attachments_list()

    def clear_announcement_form(self):
        self.hr_ui.email_subject.clear()
        self.hr_ui.email_message.clear()
        self.hr_ui.set_schedule_btn.setChecked(False)
        self.hr_ui.set_theme_btn.setChecked(False)
        self.hr_ui.schedule_frequency_box.setCurrentIndex(0)
        self.hr_ui.theme_design_box.setCurrentIndex(0)
        for radio in self.radio_buttons:
            radio.setChecked(False)
        self.attachments.clear()
        self.update_attachments_list()
        self.load_sched_email_table()

    def get_selected_sched_email_row(self):
        tbl = self.hr_ui.sched_email_list_tbl
        selected = tbl.selectedIndexes()
        if selected:
            return selected[0].row()
        return None

    def get_sched_email_db_id_by_row(self, row):
        # Get the announcement id for the selected row in sched_email_list_tbl
        if row is None or row >= len(self.sched_email_entries):
            return None
        subject, created_at, _ = self.sched_email_entries[row]
        cursor = self.db.execute_query(
            "SELECT id FROM announcements WHERE subject = ? AND created_at = ? AND schedule_enabled = 1",
            (subject, created_at)
        )
        result = cursor.fetchone() if cursor else None
        return result[0] if result else None

    def view_selected_sched_email(self):
        row = self.get_selected_sched_email_row()
        ann_id = self.get_sched_email_db_id_by_row(row)
        if ann_id is None:
            return
        cursor = self.db.execute_query("SELECT * FROM announcements WHERE id = ?", (ann_id,))
        ann = cursor.fetchone() if cursor else None
        if not ann:
            return
        # Populate view page fields
        self.hr_ui.view_email_subject.setText(ann[1])
        self.hr_ui.view_email_message.setPlainText(ann[2])
        self.hr_ui.view_set_schedule_btn.setChecked(bool(ann[5]))
        if ann[5]:
            self.hr_ui.view_schedule_frequency_box.setCurrentText(str(ann[6]))
        else:
            self.hr_ui.view_schedule_frequency_box.setCurrentIndex(0)
        self.hr_ui.view_set_theme_btn.setChecked(bool(ann[7]))
        if ann[7]:
            self.hr_ui.view_theme_design_box.setCurrentText(ann[8] or "")
        else:
            self.hr_ui.view_theme_design_box.setCurrentIndex(0)
        # Employee selection
        if ann[3] == "All":
            self.hr_ui.view_employee_send_all_btn.setChecked(True)
            self.hr_ui.view_employee_choose_btn.setChecked(False)
            self.hr_ui.view_email_employee_list_tbl.setDisabled(True)
        else:
            self.hr_ui.view_employee_send_all_btn.setChecked(False)
            self.hr_ui.view_employee_choose_btn.setChecked(True)
            self.hr_ui.view_email_employee_list_tbl.setEnabled(True)
        # Populate employee table
        self.populate_view_email_employee_table(ann[3], ann[4])
        # Attachments
        self.populate_view_attachments_list(ann[10])
        # Switch page
        self.hr_ui.hr_announcements_pages.setCurrentWidget(self.hr_ui.email_view_page)

    def populate_view_email_employee_table(self, sending_type, involved_employee):
        tbl = self.hr_ui.view_email_employee_list_tbl
        tbl.setRowCount(0)
        if sending_type == "All":
            cursor = self.db.execute_query("SELECT employee_id, first_name, last_name, middle_initial, department, position FROM Employee WHERE is_hr = 0 AND status = 'Active'")
        else:
            cursor = self.db.execute_query("SELECT employee_id, first_name, last_name, middle_initial, department, position FROM Employee WHERE employee_id = ?", (involved_employee,))
        employees = cursor.fetchall() if cursor else []
        for emp in employees:
            row = tbl.rowCount()
            tbl.insertRow(row)
            mi = f" {emp[3]}." if emp[3] else ""
            name = f"{emp[2]}, {emp[1]}{mi}"
            tbl.setItem(row, 0, QTableWidgetItem(name))
            tbl.setItem(row, 1, QTableWidgetItem(emp[0]))
            tbl.setItem(row, 2, QTableWidgetItem(f"{emp[4]} / {emp[5]}"))
        tbl.resizeColumnsToContents()

    def populate_view_attachments_list(self, files_path):
        lw = self.hr_ui.view_attachments_list
        lw.clear()
        if not files_path:
            return
        files = files_path.split(";")
        for file_path in files:
            fname = os.path.basename(file_path)
            item_widget = QWidget()
            hbox = QHBoxLayout(item_widget)
            hbox.setContentsMargins(0, 0, 0, 0)
            label = QLabel(fname)
            hbox.addWidget(label)
            hbox.addStretch()
            item_widget.setLayout(hbox)
            item = QListWidgetItem()
            item.setSizeHint(item_widget.sizeHint())
            lw.addItem(item)
            lw.setItemWidget(item, item_widget)

    def back_from_view_email(self):
        # Clear all view fields
        self.hr_ui.view_email_subject.clear()
        self.hr_ui.view_email_message.clear()
        self.hr_ui.view_employee_send_all_btn.setChecked(False)
        self.hr_ui.view_email_employee_list_tbl.setRowCount(0)
        self.hr_ui.view_set_schedule_btn.setChecked(False)
        self.hr_ui.view_schedule_frequency_box.setCurrentIndex(0)
        self.hr_ui.view_set_theme_btn.setChecked(False)
        self.hr_ui.view_theme_design_box.setCurrentIndex(0)
        self.hr_ui.view_attachments_list.clear()
        self.hr_ui.hr_announcements_pages.setCurrentWidget(self.hr_ui.email_page)

    def edit_selected_sched_email(self):
        # --- Failsafe checks before proceeding ---
        subject = self.hr_ui.edit_email_subject.text()
        message = self.hr_ui.edit_email_message.toPlainText()
        if not subject.strip():
            self.show_error("Missing Subject", "Please enter a subject for the announcement.")
            return
        if not message.strip():
            self.show_error("Missing Message", "Please enter a message for the announcement.")
            return
        if not (self.hr_ui.edit_employee_send_all_btn.isChecked() or self.hr_ui.edit_employee_choose_btn.isChecked()):
            self.show_error("No Recipient Type", "Please select either 'Send to All' or 'Choose Employee'.")
            return
        if self.hr_ui.edit_employee_choose_btn.isChecked():
            tbl = self.hr_ui.edit_email_employee_list_tbl
            selected = any(
                tbl.cellWidget(row, 0).isChecked() if tbl.cellWidget(row, 0) else False
                for row in range(tbl.rowCount())
            )
            if not selected:
                self.show_error("No Employee Selected", "Please select at least one employee from the table.")
                return
        row = self.get_selected_sched_email_row()
        ann_id = self.get_sched_email_db_id_by_row(row)
        if ann_id is None:
            return
        self.editing_announcement_id = ann_id
        cursor = self.db.execute_query("SELECT * FROM announcements WHERE id = ?", (ann_id,))
        ann = cursor.fetchone() if cursor else None
        if not ann:
            return
        # Populate edit page fields
        self.hr_ui.edit_email_subject.setText(ann[1])
        self.hr_ui.edit_email_message.setPlainText(ann[2])
        self.hr_ui.edit_set_schedule_btn.setChecked(bool(ann[5]))
        if ann[5]:
            self.hr_ui.edit_schedule_frequency_box.setCurrentText(str(ann[6]))
        else:
            self.hr_ui.edit_schedule_frequency_box.setCurrentIndex(0)
        self.hr_ui.edit_set_theme_btn.setChecked(bool(ann[7]))
        if ann[7]:
            self.hr_ui.edit_theme_design_box.setCurrentText(ann[8] or "")
        else:
            self.hr_ui.edit_theme_design_box.setCurrentIndex(0)
        # Employee selection
        if ann[3] == "All":
            self.hr_ui.edit_employee_send_all_btn.setChecked(True)
            self.hr_ui.edit_employee_choose_btn.setChecked(False)
            self.hr_ui.edit_email_employee_list_tbl.setDisabled(True)
        else:
            self.hr_ui.edit_employee_send_all_btn.setChecked(False)
            self.hr_ui.edit_employee_choose_btn.setChecked(True)
            self.hr_ui.edit_email_employee_list_tbl.setEnabled(True)
        # Populate employee table
        self.populate_edit_email_employee_table(ann[3], ann[4])
        # Attachments
        self.edit_attachments = ann[10].split(";") if ann[10] else []
        self.update_edit_attachments_list()
        # Switch page
        self.hr_ui.hr_announcements_pages.setCurrentWidget(self.hr_ui.email_edit_page)

    def populate_edit_email_employee_table(self, sending_type, involved_employee):
        tbl = self.hr_ui.edit_email_employee_list_tbl
        tbl.setRowCount(0)
        
        # Get all active employees
        cursor = self.db.execute_query(
            "SELECT employee_id, first_name, last_name, middle_initial, department, position FROM Employee WHERE is_hr = 0 AND status = 'Active'"
        )
        employees = cursor.fetchall() if cursor else []
        
        # Create two lists to store selected and unselected employees
        selected_employees = []
        unselected_employees = []
        
        for emp in employees:
            emp_data = {
                "employee_id": emp[0],
                "first_name": emp[1],
                "last_name": emp[2],
                "middle_initial": emp[3],
                "department": emp[4],
                "position": emp[5],
                "selected": emp[0] == involved_employee
            }
            if emp_data["selected"]:
                selected_employees.append(emp_data)
            else:
                unselected_employees.append(emp_data)
        
        # Sort both lists by name
        def sort_by_name(emp):
            return f"{emp['last_name']}, {emp['first_name']}"
        
        selected_employees.sort(key=sort_by_name)
        unselected_employees.sort(key=sort_by_name)
        
        # Combine lists with selected employees first
        all_employees = selected_employees + unselected_employees
        self.edit_radio_buttons = []
        
        # Populate table
        for emp_data in all_employees:
            row = tbl.rowCount()
            tbl.insertRow(row)
            
            # Add radio button
            radio = QRadioButton()
            radio.setStyleSheet("background-color: white;")
            radio.toggled.connect(lambda checked, r=row: self.handle_edit_radio_selected(r, checked))
            radio.setChecked(emp_data["selected"])
            self.edit_radio_buttons.append(radio)
            tbl.setCellWidget(row, 0, radio)
            
            # Add other columns
            mi = f" {emp_data['middle_initial']}." if emp_data['middle_initial'] else ""
            name = f"{emp_data['last_name']}, {emp_data['first_name']}{mi}"
            tbl.setItem(row, 1, QTableWidgetItem(name))
            tbl.setItem(row, 2, QTableWidgetItem(emp_data["employee_id"]))
            tbl.setItem(row, 3, QTableWidgetItem(f"{emp_data['department']} / {emp_data['position']}"))
        
        tbl.resizeColumnsToContents()

    def handle_edit_radio_selected(self, row, checked):
        if checked:
            # Uncheck all other radios
            for idx, radio in enumerate(self.edit_radio_buttons):
                if idx != row:
                    radio.setChecked(False)

    def update_edit_attachments_list(self):
        lw = self.hr_ui.edit_attachments_list
        lw.clear()
        for file_path in self.edit_attachments:
            fname = os.path.basename(file_path)
            item_widget = QWidget()
            hbox = QHBoxLayout(item_widget)
            hbox.setContentsMargins(0, 0, 0, 0)
            label = QLabel(fname)
            btn = QPushButton("✕")
            btn.setFixedSize(20, 20)
            btn.setStyleSheet("color: red; background: transparent; border: none; font-weight: bold;")
            btn.clicked.connect(lambda _, f=file_path: self.remove_edit_attachment(f))
            hbox.addWidget(label)
            hbox.addWidget(btn)
            hbox.addStretch()
            item_widget.setLayout(hbox)
            item = QListWidgetItem()
            item.setSizeHint(item_widget.sizeHint())
            lw.addItem(item)
            lw.setItemWidget(item, item_widget)

    def remove_edit_attachment(self, file_path):
        if file_path in self.edit_attachments:
            # If file is in resources/email_files, delete it
            if os.path.commonpath([os.path.abspath(file_path), os.path.abspath("resources/email_files")]) == os.path.abspath("resources/email_files"):
                try:
                    os.remove(file_path)
                except Exception:
                    pass
            self.edit_attachments.remove(file_path)
            self.update_edit_attachments_list()

    def back_from_edit_email(self):
        self.hr_ui.edit_email_subject.clear()
        self.hr_ui.edit_email_message.clear()
        self.hr_ui.edit_employee_send_all_btn.setChecked(False)
        self.hr_ui.edit_email_employee_list_tbl.setRowCount(0)
        self.hr_ui.edit_set_schedule_btn.setChecked(False)
        self.hr_ui.edit_schedule_frequency_box.setCurrentIndex(0)
        self.hr_ui.edit_set_theme_btn.setChecked(False)
        self.hr_ui.edit_theme_design_box.setCurrentIndex(0)
        self.hr_ui.edit_attachments_list.clear()
        self.edit_attachments = []
        self.hr_ui.hr_announcements_pages.setCurrentWidget(self.hr_ui.email_page)

    def save_edited_email(self):
        ann_id = getattr(self, "editing_announcement_id", None)
        if not ann_id:
            return
        subject = self.hr_ui.edit_email_subject.text()
        message = self.hr_ui.edit_email_message.toPlainText()
        schedule_enabled = self.hr_ui.edit_set_schedule_btn.isChecked()
        schedule_frequency = self.hr_ui.edit_schedule_frequency_box.currentText() if schedule_enabled else None
        theme_enabled = self.hr_ui.edit_set_theme_btn.isChecked()
        theme_type = self.hr_ui.edit_theme_design_box.currentText() if theme_enabled else None
        sending_type = "All" if self.hr_ui.edit_employee_send_all_btn.isChecked() else "Selected"
        involved_employee = None
        if sending_type == "Selected":
            tbl = self.hr_ui.edit_email_employee_list_tbl
            if tbl.rowCount() > 0:
                involved_employee = tbl.item(0, 1).text()
        # Save attachments (already handled in self.edit_attachments)
        files_path = ";".join(self.edit_attachments)
        self.db.execute_query(
            '''UPDATE announcements SET subject=?, message=?, sending_type=?, involved_employee=?, schedule_enabled=?, schedule_frequency=?, theme_enabled=?, theme_type=?, attached_files_count=?, files_path=? WHERE id=?''',
            (subject, message, sending_type, involved_employee, schedule_enabled, schedule_frequency, theme_enabled, theme_type, len(self.edit_attachments), files_path, ann_id)
        )
        self.back_from_edit_email()
        self.load_sched_email_table()

    def delete_selected_sched_email(self):
        row = self.get_selected_sched_email_row()
        ann_id = self.get_sched_email_db_id_by_row(row)
        if ann_id is None:
            return
        # Get files_path to delete attachments
        cursor = self.db.execute_query("SELECT files_path FROM announcements WHERE id = ?", (ann_id,))
        result = cursor.fetchone() if cursor else None
        if result and result[0]:
            files = result[0].split(";")
            for file_path in files:
                try:
                    if os.path.exists(file_path):
                        os.remove(file_path)
                except Exception:
                    pass
            # Remove the folder if empty
            folder = os.path.dirname(files[0])
            try:
                if os.path.exists(folder) and not os.listdir(folder):
                    os.rmdir(folder)
            except Exception:
                pass
        # Delete announcement from DB
        self.db.execute_query("DELETE FROM announcements WHERE id = ?", (ann_id,))
        self.load_sched_email_table()

class ReportGeneration:
    def __init__(self, db):
        self.db = db
        self.styles = getSampleStyleSheet()
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1
        )
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            textColor=colors.HexColor('#2c3e50')
        )

    def generate_report(self, output_path):
        doc = SimpleDocTemplate(
            output_path,
            pagesize=landscape(letter),
            rightMargin=50,
            leftMargin=50,
            topMargin=50,
            bottomMargin=50
        )
        
        story = []
        
        # Title
        title = Paragraph(f"Employee Performance Report - {datetime.now().strftime('%B %Y')}", self.title_style)
        story.append(title)
        
        # Employee Table
        story.append(Paragraph("Employee Overview", self.heading_style))
        employee_table = self.create_employee_table()
        story.append(employee_table)
        story.append(Spacer(1, 20))
        
        # Statistics Section
        story.append(Paragraph("Statistics & Analytics", self.heading_style))
        
        # Department Distribution Chart
        dept_chart = self.create_department_chart()
        story.append(Image(dept_chart, width=400, height=200))
        story.append(Spacer(1, 20))
        
        # Work Hours Chart
        hours_chart = self.create_work_hours_chart()
        story.append(Image(hours_chart, width=400, height=200))
        story.append(Spacer(1, 20))
        
        # Performance Tables
        story.append(Paragraph("Top Performers", self.heading_style))
        top_performers = self.create_top_performers_table()
        story.append(top_performers)
        story.append(Spacer(1, 20))
        
        story.append(Paragraph("Areas for Improvement", self.heading_style))
        improvement_needed = self.create_improvement_table()
        story.append(improvement_needed)
        
        # Build the PDF
        doc.build(story)
        
        # Cleanup temporary files
        if os.path.exists(dept_chart):
            os.remove(dept_chart)
        if os.path.exists(hours_chart):
            os.remove(hours_chart)

    def create_employee_table(self):
        cursor = self.db.execute_query("""
            SELECT 
                e.employee_id,
                e.first_name || ' ' || e.last_name as name,
                e.department,
                e.position,
                e.status,
                COUNT(DISTINCT a.date) as attendance_days,
                SUM(CASE WHEN a.is_late = 1 THEN 1 ELSE 0 END) as late_count
            FROM Employee e
            LEFT JOIN attendance_logs a ON e.employee_id = a.employee_id
            WHERE e.is_hr = 0
            GROUP BY e.employee_id
        """)
        
        data = [["ID", "Name", "Department", "Position", "Status", "Days Present", "Late Count"]]
        data.extend([list(row) for row in cursor.fetchall()])
        
        table = Table(data, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BOX', (0, 0), (-1, -1), 2, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.Color(0.9, 0.9, 0.9)]),
        ]))
        
        return table

    def create_department_chart(self):
        cursor = self.db.execute_query("""
            SELECT department, COUNT(*) as count
            FROM Employee
            WHERE is_hr = 0
            GROUP BY department
        """)
        
        departments, counts = zip(*cursor.fetchall())
        
        plt.figure(figsize=(10, 5))
        plt.pie(counts, labels=departments, autopct='%1.1f%%')
        plt.title('Employee Distribution by Department')
        
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        plt.savefig(temp_file.name)
        plt.close()
        
        return temp_file.name

    def create_work_hours_chart(self):
        cursor = self.db.execute_query("""
            SELECT DATE(created_at) as date, average_work_hours
            FROM system_logs
            WHERE strftime('%Y-%m', created_at) = strftime('%Y-%m', 'now')
            ORDER BY date
        """)
        
        dates, hours = zip(*cursor.fetchall())
        
        plt.figure(figsize=(10, 5))
        plt.plot(dates, hours, marker='o')
        plt.title('Average Work Hours Trend')
        plt.xticks(rotation=45)
        plt.ylabel('Hours')
        plt.grid(True)
        
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        plt.savefig(temp_file.name, bbox_inches='tight')
        plt.close()
        
        return temp_file.name

    def create_top_performers_table(self):
        cursor = self.db.execute_query("""
            SELECT 
                e.first_name || ' ' || e.last_name as name,
                e.department,
                COUNT(DISTINCT a.date) as attendance_days,
                SUM(CASE WHEN a.is_late = 0 THEN 1 ELSE 0 END) as on_time_days
            FROM Employee e
            LEFT JOIN attendance_logs a ON e.employee_id = a.employee_id
            WHERE e.is_hr = 0
            GROUP BY e.employee_id
            ORDER BY attendance_days DESC, on_time_days DESC
            LIMIT 10
        """)
        
        data = [["Name", "Department", "Days Present", "On-Time Days"]]
        data.extend([list(row) for row in cursor.fetchall()])
        
        table = Table(data, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        return table

    def create_improvement_table(self):
        cursor = self.db.execute_query("""
            SELECT 
                e.first_name || ' ' || e.last_name as name,
                e.department,
                COUNT(DISTINCT a.date) as attendance_days,
                SUM(CASE WHEN a.is_late = 1 THEN 1 ELSE 0 END) as late_days
            FROM Employee e
            LEFT JOIN attendance_logs a ON e.employee_id = a.employee_id
            WHERE e.is_hr = 0
            GROUP BY e.employee_id
            HAVING late_days > 0
            ORDER BY late_days DESC
            LIMIT 10
        """)
        
        data = [["Name", "Department", "Days Present", "Late Days"]]
        data.extend([list(row) for row in cursor.fetchall()])
        
        table = Table(data, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        return table

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = EALS()
    sys.exit(app.exec())


