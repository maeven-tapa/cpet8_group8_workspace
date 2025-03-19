import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QWidget, QStackedWidget, QTabWidget
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Qt

class UIController:
    def __init__(self):
        self.loader = QUiLoader()
        
        self.home_ui = self.loader.load("home.ui")
        self.admin_change_pass_ui = self.loader.load("admin_change_pass.ui")
        self.admin_ui = self.loader.load("admin.ui")
        self.enroll_employee_ui = self.loader.load("enroll_employee.ui")
        self.enroll_hr_ui = self.loader.load("enroll_hr.ui")
        
        self.employee_stack = self.find_stacked_widget(self.enroll_employee_ui)
        self.hr_stack = self.find_stacked_widget(self.enroll_hr_ui)
        
        self.setup_always_on_top()
        self.setup_connections()
        
        self.home_ui.show()
    
    def setup_always_on_top(self):
        self.admin_change_pass_ui.setWindowFlags(
            self.admin_change_pass_ui.windowFlags() | Qt.WindowStaysOnTopHint
        )
        self.enroll_employee_ui.setWindowFlags(
            self.enroll_employee_ui.windowFlags() | Qt.WindowStaysOnTopHint
        )
        self.enroll_hr_ui.setWindowFlags(
            self.enroll_hr_ui.windowFlags() | Qt.WindowStaysOnTopHint
        )
    
    def find_stacked_widget(self, parent_widget):
        stack = parent_widget.findChild(QStackedWidget, "stackedWidget")
        
        if not stack:
            stack_widgets = parent_widget.findChildren(QStackedWidget)
            if stack_widgets:
                stack = stack_widgets[0]
        
        return stack
    
    def setup_connections(self):
        self.home_ui.home_login_btn.clicked.connect(self.show_admin_change_pass)
        
        self.admin_change_pass_ui.admin_change_pass_btn.clicked.connect(self.show_admin_main)
        
        self.admin_ui.admin_logout_btn.clicked.connect(self.logout_to_home)
        
        self.admin_ui.employee_edit_btn.clicked.connect(self.goto_employee_edit_page)
        self.admin_ui.employee_enroll_btn.clicked.connect(self.goto_employee_enroll_page)
        self.admin_ui.employee_view_btn.clicked.connect(self.goto_employee_view_page)
        
        self.admin_ui.hr_edit_btn.clicked.connect(self.goto_hr_edit_page)
        self.admin_ui.hr_add_btn.clicked.connect(self.goto_hr_add_page)
        self.admin_ui.hr_view_btn.clicked.connect(self.goto_hr_view_page)
        
        self.enroll_employee_ui.employee_enroll_cancel.clicked.connect(self.close_employee_ui)
        self.enroll_employee_ui.employee_enroll_1.clicked.connect(self.goto_employee_enroll2_page)
        
        self.enroll_employee_ui.employee_enroll_back1.clicked.connect(self.goto_employee_enroll_page)
        self.enroll_employee_ui.employee_enroll_2.clicked.connect(self.goto_employee_enroll3_page)
        
        self.enroll_employee_ui.employee_enroll_back2.clicked.connect(self.goto_employee_enroll2_page)
        self.enroll_employee_ui.employee_enroll_3.clicked.connect(self.close_employee_ui)
        
        self.enroll_employee_ui.employee_view_back.clicked.connect(self.close_employee_ui)
        
        self.enroll_employee_ui.employee_edit_back.clicked.connect(self.close_employee_ui)
        self.enroll_employee_ui.employee_edit_save.clicked.connect(self.close_employee_ui)
        
        self.enroll_hr_ui.hr_add_cancel.clicked.connect(self.close_hr_ui)
        self.enroll_hr_ui.hr_add_save.clicked.connect(self.close_hr_ui)
        
        self.enroll_hr_ui.hr_edit_cancel.clicked.connect(self.close_hr_ui)
        self.enroll_hr_ui.hr_edit_save.clicked.connect(self.close_hr_ui)
        
        self.enroll_hr_ui.hr_view_back.clicked.connect(self.close_hr_ui)
    
    def show_admin_change_pass(self):
        self.home_ui.setEnabled(False)
        self.admin_change_pass_ui.exec()
        self.home_ui.setEnabled(True)
    
    def show_admin_main(self):
        self.admin_change_pass_ui.accept()
        self.home_ui.close()
        self.admin_ui.show()
        
        tab_widget = self.admin_ui.findChild(QTabWidget)
        if tab_widget:
            dashboard_index = self.find_tab_index(tab_widget, "admin_dashboard")
            if dashboard_index != -1:
                tab_widget.setCurrentIndex(dashboard_index)
    
    def find_tab_index(self, tab_widget, tab_name):
        for i in range(tab_widget.count()):
            if tab_widget.widget(i).objectName() == tab_name:
                return i
        return -1
    
    def logout_to_home(self):
        self.admin_ui.close()
        self.home_ui.show()
    
    def goto_employee_edit_page(self):
        if not self.employee_stack:
            return
            
        self.admin_ui.setEnabled(False)
        page = self.enroll_employee_ui.findChild(QWidget, "employee_edit_page")
        
        if not page:
            if self.employee_stack.count() > 0:
                self.employee_stack.setCurrentIndex(0)
        else:
            employee_edit_index = self.employee_stack.indexOf(page)
            self.employee_stack.setCurrentIndex(employee_edit_index)
            
        self.enroll_employee_ui.show()
    
    def goto_employee_enroll_page(self):
        if not self.employee_stack:
            return
            
        self.admin_ui.setEnabled(False)
        page = self.enroll_employee_ui.findChild(QWidget, "employee_enroll_page")
        
        if not page:
            if self.employee_stack.count() > 1:
                self.employee_stack.setCurrentIndex(1)
        else:
            employee_enroll_index = self.employee_stack.indexOf(page)
            self.employee_stack.setCurrentIndex(employee_enroll_index)
            
        self.enroll_employee_ui.show()
    
    def goto_employee_enroll2_page(self):
        if not self.employee_stack:
            return
            
        page = self.enroll_employee_ui.findChild(QWidget, "employee_enroll2_page")
        if not page:
            if self.employee_stack.count() > 2:
                self.employee_stack.setCurrentIndex(2)
        else:
            employee_enroll2_index = self.employee_stack.indexOf(page)
            self.employee_stack.setCurrentIndex(employee_enroll2_index)
    
    def goto_employee_enroll3_page(self):
        if not self.employee_stack:
            return
            
        page = self.enroll_employee_ui.findChild(QWidget, "employee_enroll3_page")
        if not page:
            if self.employee_stack.count() > 3:
                self.employee_stack.setCurrentIndex(3)
        else:
            employee_enroll3_index = self.employee_stack.indexOf(page)
            self.employee_stack.setCurrentIndex(employee_enroll3_index)
    
    def goto_employee_view_page(self):
        if not self.employee_stack:
            return
            
        self.admin_ui.setEnabled(False)
        page = self.enroll_employee_ui.findChild(QWidget, "employee_view_page")
        if not page:
            if self.employee_stack.count() > 4:
                self.employee_stack.setCurrentIndex(4)
        else:
            employee_view_index = self.employee_stack.indexOf(page)
            self.employee_stack.setCurrentIndex(employee_view_index)
            
        self.enroll_employee_ui.show()
    
    def close_employee_ui(self):
        self.enroll_employee_ui.close()
        self.admin_ui.setEnabled(True)
    
    def goto_hr_edit_page(self):
        if not self.hr_stack:
            return
            
        self.admin_ui.setEnabled(False)
        page = self.enroll_hr_ui.findChild(QWidget, "hr_edit_page")
        if not page:
            if self.hr_stack.count() > 0:
                self.hr_stack.setCurrentIndex(0)
        else:
            hr_edit_index = self.hr_stack.indexOf(page)
            self.hr_stack.setCurrentIndex(hr_edit_index)
            
        self.enroll_hr_ui.show()
    
    def goto_hr_add_page(self):
        if not self.hr_stack:
            return
            
        self.admin_ui.setEnabled(False)
        page = self.enroll_hr_ui.findChild(QWidget, "hr_add_page")
        if not page:
            if self.hr_stack.count() > 1:
                self.hr_stack.setCurrentIndex(1)
        else:
            hr_add_index = self.hr_stack.indexOf(page)
            self.hr_stack.setCurrentIndex(hr_add_index)
            
        self.enroll_hr_ui.show()
    
    def goto_hr_view_page(self):
        if not self.hr_stack:
            return
            
        self.admin_ui.setEnabled(False)
        page = self.enroll_hr_ui.findChild(QWidget, "hr_view_page")
        if not page:
            if self.hr_stack.count() > 2:
                self.hr_stack.setCurrentIndex(2)
        else:
            hr_view_index = self.hr_stack.indexOf(page)
            self.hr_stack.setCurrentIndex(hr_view_index)
            
        self.enroll_hr_ui.show()
    
    def close_hr_ui(self):
        self.enroll_hr_ui.close()
        self.admin_ui.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = UIController()
    sys.exit(app.exec())