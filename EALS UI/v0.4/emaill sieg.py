import sys
import smtplib
from datetime import datetime
from email.message import EmailMessage

from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QTextEdit
)

class RegistrationApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enrollment System")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.name_label = QLabel("Name:")
        self.name_input = QLineEdit()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)

        self.email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)

        self.personal_msg_label = QLabel("Personalized Message:")
        self.personal_msg_input = QTextEdit()
        layout.addWidget(self.personal_msg_label)
        layout.addWidget(self.personal_msg_input)

        self.submit_btn = QPushButton("Submit Registration")
        self.submit_btn.clicked.connect(self.send_registration_email)
        layout.addWidget(self.submit_btn)

        self.setLayout(layout)

    def send_registration_email(self):
        name = self.name_input.text()
        email = self.email_input.text()
        message = self.personal_msg_input.toPlainText()
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        email_subject = "Registration Summary"
        email_body = f"""
        A new user has registered:
        Name: {name}
        Email: {email}
        Time: {time_now}

        Personalized Message:
        {message}
        """

        self.send_email(email_subject, email_body, email)
        
    def send_email(self, subject, body, email):
        
        SMTP_SERVER = "smtp.gmail.com"
        SMTP_PORT = 587
        SENDER_EMAIL = "eals.tupc@gmail.com"
        SENDER_PASSWORD = "buwl tszg dghr exln"
        RECEIVER_EMAIL = "siegmond.amador04@gmail.com"  # Could also be dynamic
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = SENDER_EMAIL
        msg["To"] = email
        msg.set_content(body)

        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                server.send_message(msg)
                print(f"Email sent: {subject}")
        except Exception as e:
            print(f"Failed to send email: {e}")
            

if __name__ == "__main__":


    app = QApplication(sys.argv)
    window = RegistrationApp()
    window.show()

    exit_code = app.exec()
    sys.exit(exit_code)
