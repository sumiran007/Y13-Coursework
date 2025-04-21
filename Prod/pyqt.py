from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QPushButton, QLabel, QFrame, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from database import validate_user, add_user
import sys

def handle_login(username_input, password_input, login_window):
    username = username_input.text()
    password = password_input.text()
    
    if not username or not password:
        QMessageBox.warning(login_window, "Error", "Please enter both username and password")
        return
        #error handling for no inputs
    if validate_user(username, password):
        print("Login successful")
        login_window.close()
        #validation for the user by checking the database
        
        import menu#imports the file menu from the same folder since it is required for the next step
        menu_window = menu.menu(username)
        
        login_window.menu_window = menu_window
    else:
        QMessageBox.warning(login_window, "Login Failed", "Invalid username or password")
        #error handling for invalid username or password shows a field that says invalid username or password
def handle_signup(username_input, password_input, login_window):#for the sign up button                         
    username = username_input.text()
    password = password_input.text()
    
    if not username or not password:
        QMessageBox.warning(login_window, "Error", "Please enter both username and password")
        return#error handling for no inputs
        
    try:
        add_user(username, password)#try and expect for the add user function to add the user to the database
        QMessageBox.information(login_window, "Success", "User signed up successfully")
    except Exception as e:
        QMessageBox.warning(login_window, "Error", f"Failed to sign up: {str(e)}")

def create_login_window():
    login_window = QWidget()
    
    # Load stylesheet
    with open("style.css", "r") as file:#uses a css stylesheet to make the code more modular and add styling to the login window
        stylesheet = file.read()
    login_window.setStyleSheet(stylesheet)
    
    login_window.setWindowTitle('Login')
    login_window.setFixedSize(350, 350)
    #sets all the conditions for the login window like size and width
    container = QFrame(login_window)
    container.setGeometry(25, 25, 300, 300)

    layout = QVBoxLayout(container)
    layout.setContentsMargins(20, 20, 20, 20)
    layout.setSpacing(10)

    # Login header
    login_label = QLabel("Login")
    login_label.setAlignment(Qt.AlignCenter)
    login_label.setFont(QFont("Arial", 18))
    login_label.setObjectName("loginLabel")
    layout.addWidget(login_label)

    # Username input
    username_input = QLineEdit()
    username_input.setPlaceholderText("Username")
    layout.addWidget(username_input)

    # Password input
    password_input = QLineEdit()
    password_input.setPlaceholderText("Password")
    password_input.setEchoMode(QLineEdit.Password)
    layout.addWidget(password_input)

    # Login button 
    login_button = QPushButton("Login")
    login_button.clicked.connect(lambda: handle_login(username_input, password_input, login_window))
    login_button.setObjectName("loginButton")
    layout.addWidget(login_button)

    # Signup button uses the same function as the login button but with a different function to add the user to the database
    signup_button = QPushButton("Sign Up")
    signup_button.clicked.connect(lambda: handle_signup(username_input, password_input, login_window))
    signup_button.setObjectName("signupButton")
    layout.addWidget(signup_button)

    return login_window

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = create_login_window()
    window.show()
    sys.exit(app.exec_())