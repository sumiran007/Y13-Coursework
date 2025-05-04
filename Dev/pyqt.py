import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QPushButton, QLabel, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('login')  #set the window title
        self.setFixedSize(350, 350)  #fixed size for the login window

        #main container
        container = QFrame(self)
        container.setGeometry(25, 25, 300, 300)

        #layout for the container
        layout = QVBoxLayout(container)
        layout.setContentsMargins(20, 20, 20, 20)  #add some padding
        layout.setSpacing(10)  #space between elements

        #login header
        login_label = QLabel("login")
        login_label.setAlignment(Qt.AlignCenter)  #center the text
        login_label.setFont(QFont("arial", 20))  #make it big
        login_label.setObjectName("loginLabel")  #for styling later

        #username label
        username_label = QLabel("username")

        #username input
        self.username_input = QLineEdit()  #input box for the username

        #password label
        password_label = QLabel("password")

        #password input
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)  #hide the password as it's typed

        #login button
        login_button = QPushButton("login")
        login_button.setObjectName("loginButton")  #for styling

        #sign up button
        signup_button = QPushButton("sign up")
        signup_button.setObjectName("signupButton")  #for styling too

        #add everything to the layout
        layout.addWidget(login_label)
        layout.addStretch(1)  #add some space
        layout.addWidget(username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)
        layout.addStretch(1)  #more space
        layout.addWidget(login_button)
        layout.addWidget(signup_button)

        #show the window
        self.show()

def load_stylesheet(path):
    #load the stylesheet from a file
    with open(path, "r") as file:
        return file.read()

app = QApplication(sys.argv)
style = load_stylesheet("style.css")  #load the css
app.setStyleSheet(style)  #apply the css
window = LoginWindow()  #create the login window
sys.exit(app.exec_())  #run the app