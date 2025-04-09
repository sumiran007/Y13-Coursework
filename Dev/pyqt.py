import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QPushButton, QLabel, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Login')
        self.setFixedSize(350, 350)

        # Main container
        container = QFrame(self)
        container.setGeometry(25, 25, 300, 300)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Login header
        login_label = QLabel("Login")
        login_label.setAlignment(Qt.AlignCenter)
        login_label.setFont(QFont("Arial", 20))
        login_label.setObjectName("loginLabel")  # For targeted styling

        # Username label
        username_label = QLabel("Username")

        # Username input
        self.username_input = QLineEdit()

        # Password label
        password_label = QLabel("Password")

        # Password input
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        # Login button
        login_button = QPushButton("Login")
        login_button.setObjectName("loginButton")

        # Sign up button
        signup_button = QPushButton("Sign Up")
        signup_button.setObjectName("signupButton")
        layout.customEvent = lambda event: event.accept()  # Custom event to handle button clicks
        login_button.clicked.connect(lambda: print("Login clicked"))
        layout.addWidget(login_label)
        layout.addStretch(1)
        layout.addWidget(username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)
        layout.addStretch(1)
        layout.addWidget(login_button)
        layout.addWidget(signup_button)

        self.show()

def load_stylesheet(path):
    with open(path, "r") as file:
        return file.read()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    style = load_stylesheet("style.css")
    app.setStyleSheet(style)
    window = LoginWindow()
    sys.exit(app.exec_())