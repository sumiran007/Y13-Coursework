import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout
#all the imports from the library
app = QApplication(sys.argv)

window = QWidget()
#set the window like pygame.init()
window.setWindowTitle('Password Box Example')
#sets the title of the window
window.resize(300, 100)
#sets the size of the window
layout = QVBoxLayout()

password_box = QLineEdit()
username_box = QLineEdit()
username_box.setPlaceholderText('Enter your username')
password_box.setPlaceholderText('Enter your password')

#creates a text box to type into
#makes the text look hidden so that the user can't see what they are typing
username_box.setEchoMode(QLineEdit.Normal)
password_box.setEchoMode(QLineEdit.Password)  

#sets the text box to be normal text
layout.addWidget(username_box)
layout.addWidget(password_box)

window.setLayout(layout)
window.show()
#outputs the window like pygame.display.update()
sys.exit(app.exec_())
#exits the program like pygame.quit()
#no point of using oop since most of the code is in the library