from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel, 
                            QFrame, QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import subprocess
from database import get_high_scores

class MenuWindow(QWidget):
    def __init__(self, username="player"):
        super().__init__()
        self.username = username
        
        #Get our styles
        with open("style.css", "r") as file:
            stylesheet = file.read()
        self.setStyleSheet(stylesheet)
        
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Game Menu')
        self.setFixedSize(500, 500)
        
        #Main container
        container = QFrame(self)
        container.setGeometry(50, 50, 400, 400)
        
        #Layout setup
        layout = QVBoxLayout(container)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        #Welcome message
        welcome_label = QLabel(f"Welcome, {self.username}!")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setFont(QFont("Arial", 18))
        welcome_label.setObjectName("welcomeLabel")
        
        #Play button
        start_button = QPushButton("Start Game")
        start_button.setFixedHeight(50)
        start_button.clicked.connect(self.start_game)
        start_button.setObjectName("startButton")
        
        #High Scores button
        scores_button = QPushButton("High Scores")
        scores_button.setFixedHeight(50)
        scores_button.clicked.connect(self.show_high_scores)
        scores_button.setObjectName("scoresButton")
        
        #Exit button
        exit_button = QPushButton("Exit")
        exit_button.setFixedHeight(50)
        exit_button.clicked.connect(self.close)
        exit_button.setObjectName("exitButton")
        
        #Add to layout
        layout.addWidget(welcome_label)
        layout.addStretch(1)
        layout.addWidget(start_button)
        layout.addWidget(scores_button)
        layout.addWidget(exit_button)
        layout.addStretch(1)
        
        self.show()
    
    def start_game(self):
        self.hide()  #Hide menu while playing
        try:
            #Fire up the game
            subprocess.run(["python", "game.py", self.username])
            self.show()  #Show menu again after game
        except Exception as e:
            print(f"Oops, game crashed: {e}")
            self.show()
    
    def show_high_scores(self):
        #Pop up high scores window
        self.scores_window = HighScoresWindow()
        self.scores_window.show()


class HighScoresWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        #Get styles
        with open("style.css", "r") as file:
            stylesheet = file.read()
        self.setStyleSheet(stylesheet)
        
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('High Scores')
        self.setFixedSize(400, 500)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        #Title
        title = QLabel("High Scores")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 18))
        title.setObjectName("titleLabel")
        
        #Scores table
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Player", "Score"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        
        #Close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        close_button.setObjectName("closeButton")
        
        #Add to layout
        layout.addWidget(title)
        layout.addWidget(self.table)
        layout.addWidget(close_button)
        
        self.setLayout(layout)
        
        #Grab scores
        self.load_scores()
    
    def load_scores(self):
        scores = get_high_scores()
        self.table.setRowCount(len(scores))
        
        for i, (username, score) in enumerate(scores):
            self.table.setItem(i, 0, QTableWidgetItem(username))
            self.table.setItem(i, 1, QTableWidgetItem(str(score)))


def menu(username="player"):
    window = MenuWindow(username)
    return window


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    window = menu()
    sys.exit(app.exec_())