import sys
import smtplib
from datetime import datetime
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QMessageBox
)
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "siegmond.amador04@gmail.com"
EMAIL_PASSWORD = "zres pxgx isfo dlpb"
EMAIL_ADMIN = "siegmond.amador04@gmail.com"


def send_email(subject: str, body: str, receiver: str = EMAIL_ADMIN):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = receiver
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print("Email send failed:", e)



class RegistrationApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registration & Email System")
        self.setGeometry(100, 100, 400, 400)

        layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your name")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")

        self.message_box = QTextEdit()
        self.message_box.setPlaceholderText("Enter your personalized message (optional)")

        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.register_user)

        layout.addWidget(QLabel("Name:"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email_input)
        layout.addWidget(QLabel("Personalized Message:"))
        layout.addWidget(self.message_box)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

        send_email("User Entered the App",
                   f"User opened the application at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    def register_user(self):
        name = self.name_input.text()
        email = self.email_input.text()
        message = self.message_box.toPlainText()

        if not name or not email:
            QMessageBox.warning(self, "Error", "Name and email are required.")
            return

        summary = f"""Hello {name},

    Thank you for registering!

    📋 Your Registration Summary:
    Name: {name}
    Email: {email}
    Registered At: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

    Your Message:
    {message if message else 'None'}

    Best regards,
    Your App Team
    """

        send_email("Welcome to the App!", summary, receiver=email)

        
        send_email("Admin Copy - New User Registration", summary, receiver=EMAIL_ADMIN)

        QMessageBox.information(self, "Success", "Registration successful. Summary sent to user's Gmail.")


    def closeEvent(self, event):
        send_email("User Exited the App",
                   f"User closed the application at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RegistrationApp()
    window.show()
    sys.exit(app.exec())
