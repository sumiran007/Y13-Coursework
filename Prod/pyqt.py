from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QPushButton, QLabel, QFrame, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from database import validate_user, add_user
import sys
import re

# SQL keywords to check for in client-side validation
SQL_KEYWORDS = [
    "SELECT", "INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE", 
    "TABLE", "DATABASE", "UNION", "JOIN", "WHERE", "FROM", "INTO", "EXEC", 
    "--", ";", "/*", "*/"
]

def contains_sql_keywords(text):
    """Check if the text contains any SQL keywords or injection patterns"""
    if not text:
        return False
        
    text_upper = text.upper()
    for keyword in SQL_KEYWORDS:
        if keyword.upper() in text_upper:
            return True
            
    # Check for more complex patterns
    sql_patterns = [
        r'(\s|^)(SELECT|INSERT|UPDATE|DELETE|DROP|ALTER|UNION|CREATE|EXEC|INTO)\s',
        r'(--|;|/\*|\*/)',
        r'(=\s*\'.*\')',
        r'(1\s*=\s*1)',
        r'(\'\s*OR\s*\')',
        r'(\'\s*OR\s*1\s*=\s*1)'
    ]
    
    for pattern in sql_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
            
    return False

def handle_login(username_input, password_input, login_window):
    username = username_input.text()
    password = password_input.text()
    
    if not username or not password:
        QMessageBox.warning(login_window, "Error", "Please enter both username and password")
        return
    
    # Client-side validation before sending to database
    if contains_sql_keywords(username) or contains_sql_keywords(password):
        QMessageBox.warning(login_window, "Security Warning", 
                           "Input contains SQL keywords or special characters that are not allowed.")
        return
    
    # Use the new return value format from database functions (success, message)
    success, message = validate_user(username, password)
    
    if success:
        print("Login successful")
        login_window.close()
        
        import menu  # gets the menu module
        menu_window = menu.menu(username)
        
        login_window.menu_window = menu_window
    else:
        QMessageBox.warning(login_window, "Login Failed", message)

def handle_signup(username_input, password_input, login_window):  # signup button handler                     
    username = username_input.text()
    password = password_input.text()
    
    if not username or not password:
        QMessageBox.warning(login_window, "Error", "Please enter both username and password")
        return  # stops if fields are empty
    
    # Client-side validation before sending to database
    if contains_sql_keywords(username) or contains_sql_keywords(password):
        QMessageBox.warning(login_window, "Security Warning", 
                           "Input contains SQL keywords or special characters that are not allowed.")
        return
    
    # Additional client-side validation for username format
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        QMessageBox.warning(login_window, "Error", 
                           "Username can only contain letters, numbers, and underscores")
        return
        
    # Password length validation
    if len(password) < 4:
        QMessageBox.warning(login_window, "Error", 
                           "Password must be at least 4 characters long")
        return
    
    # Use the new return value format from database functions (success, message)
    success, message = add_user(username, password)
    
    if success:
        QMessageBox.information(login_window, "Success", message)
        # Clear fields after successful signup
        username_input.clear()
        password_input.clear()
    else:
        QMessageBox.warning(login_window, "Error", message)

def create_login_window():
    login_window = QWidget()
    
    # Get our pretty styles
    with open("style.css", "r") as file:  # loads CSS for a nicer look
        stylesheet = file.read()
    login_window.setStyleSheet(stylesheet)
    
    login_window.setWindowTitle('Login')
    login_window.setFixedSize(350, 350)
    # window setup stuff
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

    # Username box
    username_input = QLineEdit()
    username_input.setPlaceholderText("Username")
    layout.addWidget(username_input)

    # Password box
    password_input = QLineEdit()
    password_input.setPlaceholderText("Password")
    password_input.setEchoMode(QLineEdit.Password)
    layout.addWidget(password_input)
    
    # Add security notice with more specific requirements
    security_label = QLabel("Note: Usernames can only contain letters, numbers, and underscores. Password must be at least 4 characters. SQL commands are not allowed.")
    security_label.setWordWrap(True)
    security_label.setStyleSheet("color: #888; font-size: 10px;")
    layout.addWidget(security_label)

    # Login button 
    login_button = QPushButton("Login")
    login_button.clicked.connect(lambda: handle_login(username_input, password_input, login_window))
    login_button.setObjectName("loginButton")
    layout.addWidget(login_button)

    # Signup button
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