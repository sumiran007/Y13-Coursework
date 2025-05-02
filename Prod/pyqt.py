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
        #if they left fields empty
    if validate_user(username, password):
        print("Login successful")
        login_window.close()
        #checks if user exists in database
        
        import menu#gets the menu module
        menu_window = menu.menu(username)
        
        login_window.menu_window = menu_window
    else:
        QMessageBox.warning(login_window, "Login Failed", "Invalid username or password")
        #shows error for wrong details
def handle_signup(username_input, password_input, login_window):#signup button handler                     
    username = username_input.text()
    password = password_input.text()
    
    if not username or not password:
        QMessageBox.warning(login_window, "Error", "Please enter both username and password")
        return#stops if fields are empty
        
    try:
        add_user(username, password)#adds new user to database
        QMessageBox.information(login_window, "Success", "User signed up successfully")
    except Exception as e:
        QMessageBox.warning(login_window, "Error", f"Failed to sign up: {str(e)}")

def create_login_window():
    login_window = QWidget()
    
    #Get our pretty styles
    with open("style.css", "r") as file:#loads CSS for a nicer look
        stylesheet = file.read()
    login_window.setStyleSheet(stylesheet)
    
    login_window.setWindowTitle('Login')
    login_window.setFixedSize(350, 350)
    #window setup stuff
    container = QFrame(login_window)
    container.setGeometry(25, 25, 300, 300)

    layout = QVBoxLayout(container)
    layout.setContentsMargins(20, 20, 20, 20)
    layout.setSpacing(10)

    #Login header
    login_label = QLabel("Login")
    login_label.setAlignment(Qt.AlignCenter)
    login_label.setFont(QFont("Arial", 18))
    login_label.setObjectName("loginLabel")
    layout.addWidget(login_label)

    #Username box
    username_input = QLineEdit()
    username_input.setPlaceholderText("Username")
    layout.addWidget(username_input)

    #Password box
    password_input = QLineEdit()
    password_input.setPlaceholderText("Password")
    password_input.setEchoMode(QLineEdit.Password)
    layout.addWidget(password_input)

    #Login button 
    login_button = QPushButton("Login")
    login_button.clicked.connect(lambda: handle_login(username_input, password_input, login_window))
    login_button.setObjectName("loginButton")
    layout.addWidget(login_button)

    #Signup button
    signup_button = QPushButton("Sign Up")
    signup_button.clicked.connect(lambda: handle_signup(username_input, password_input, login_window))
    signup_button.setObjectName("signupButton")
    layout.addWidget(signup_button)

    return login_window

def start_login():
    """Function to create and show the login window"""
    app = QApplication(sys.argv)
    login_window = create_login_window()
    login_window.show()  # Explicitly show the window
    return app, login_window

# Only run this block when the file is executed directly
if __name__ == "__main__":
    app, login_window = start_login()
    sys.exit(app.exec_())