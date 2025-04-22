from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel, 
                            QFrame, QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import subprocess
from database import get_high_scores
import json
import os

class MenuWindow(QWidget):
    def __init__(self, username="player"):
        super().__init__()
        self.username = username  #grab their name
        
        # somewhere to store the picked skin
        self.selected_skin = None
        
        #make it look snazzy with some CSS
        with open("style.css", "r") as file:
            stylesheet = file.read()
        self.setStyleSheet(stylesheet)
        
        self.initUI()  #set up all the buttons and stuff
        
    def initUI(self):
        self.setWindowTitle('Game Menu')  #what shows in the window bar
        self.setFixedSize(500, 500)  #not too big, not too small
        
        #nice box to hold everything
        container = QFrame(self)
        container.setGeometry(50, 50, 400, 400)
        
        #how stuff gets arranged
        layout = QVBoxLayout(container)
        layout.setContentsMargins(20, 20, 20, 20)  #padding around edges
        layout.setSpacing(20)  #space between items
        
        #say hi to whoever's playing
        welcome_label = QLabel(f"Welcome, {self.username}!")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setFont(QFont("Arial", 18))  #big friendly text
        welcome_label.setObjectName("welcomeLabel")
        
        #big green play button
        start_button = QPushButton("Start Game")
        start_button.setFixedHeight(50)
        start_button.clicked.connect(self.start_game)  #what happens when clicked
        start_button.setObjectName("startButton")
        
        #button to check scores
        scores_button = QPushButton("High Scores")
        scores_button.setFixedHeight(50)
        scores_button.clicked.connect(self.show_high_scores)
        scores_button.setObjectName("scoresButton")
        
        #button to pick cool skins
        skins_button = QPushButton("Choose Skin")
        skins_button.setFixedHeight(50)
        skins_button.clicked.connect(self.select_skin)
        skins_button.setObjectName("skinsButton")
        
        #escape hatch
        exit_button = QPushButton("Exit")
        exit_button.setFixedHeight(50)
        exit_button.clicked.connect(self.close)  #bye bye
        exit_button.setObjectName("exitButton")
        
        #chuck it all in the layout
        layout.addWidget(welcome_label)
        layout.addStretch(1)  #some breathing room
        layout.addWidget(start_button)
        layout.addWidget(scores_button)
        layout.addWidget(skins_button)
        layout.addWidget(exit_button)
        layout.addStretch(1)  #more breathing room at bottom
        
        self.show()  #ta-da! display the window
    
    def start_game(self):
        self.hide()  #hide menu while they're playing
        try:
            #fire up the actual game
            cmd = ["python", "game.py", self.username]
            if self.selected_skin:
                cmd.append(self.selected_skin.get("name", ""))  #tell game which skin to use
            
            subprocess.run(cmd)  #run the game
            self.show()  #bring menu back when done
        except Exception as e:
            print(f"Oops, game crashed: {e}")  #uh oh
            self.show()  #show menu anyway
    
    def show_high_scores(self):
        #pop up the leaderboard
        self.scores_window = HighScoresWindow()
        self.scores_window.show()  #show off who's winning
        
    def select_skin(self):
        self.hide()  #hide menu while picking a skin
        try:
            #import the fancy skin picker
            from skins import select_skin
            
            #let them choose and grab what they picked
            selected_skin = select_skin()
            
            if selected_skin:
                self.selected_skin = selected_skin  #remember their choice
                print(f"Selected skin: {selected_skin['name']}")  #log it
            
            self.show()  #show menu again
        except Exception as e:
            print(f"Error selecting skin: {e}")  #something went wrong
            self.show()

class SkinsWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        #make it pretty
        with open("style.css", "r") as file:
            stylesheet = file.read()
        self.setStyleSheet(stylesheet)
        
        self.initUI()  #set it up
        
    def initUI(self):
        self.setWindowTitle('Skins')
        self.setFixedSize(400, 500)  #decent size window
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)  #nice margins
        layout.setSpacing(20)  #gap between things
        
        #big title at the top
        title = QLabel("Skins")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 18))  #make it stand out
        title.setObjectName("titleLabel")
        
        #button to get outta here
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)  #closes the window
        close_button.setObjectName("closeButton")
        
        #add everything to the window
        layout.addWidget(title)
        layout.addWidget(close_button)
        
        self.setLayout(layout)  #apply the layout


class HighScoresWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        #make it look fancy
        with open("style.css", "r") as file:
            stylesheet = file.read()
        self.setStyleSheet(stylesheet)
        
        self.initUI()  #set up the window
        
    def initUI(self):
        self.setWindowTitle('High Scores')
        self.setFixedSize(400, 500)  #good size for a score table
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)  #padding
        layout.setSpacing(20)  #space between items
        
        #big title at the top
        title = QLabel("High Scores")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 18))  #make it pop
        title.setObjectName("titleLabel")
        
        #table to show all the high scores
        self.table = QTableWidget()
        self.table.setColumnCount(2)  #just name and score
        self.table.setHorizontalHeaderLabels(["Player", "Score"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        
        #button to bail out
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)  #closes the window
        close_button.setObjectName("closeButton")
        
        #stick it all together
        layout.addWidget(title)
        layout.addWidget(self.table)  #the score table gets most of the space
        layout.addWidget(close_button)
        
        self.setLayout(layout)
        
        #fill the table with actual scores
        self.load_scores()
    
    def load_scores(self):
        scores = get_high_scores()  #grab from database
        self.table.setRowCount(len(scores))  #make room for all scores
        
        for i, (username, score) in enumerate(scores):
            self.table.setItem(i, 0, QTableWidgetItem(username))  #player name
            self.table.setItem(i, 1, QTableWidgetItem(str(score)))  #their score


def menu(username="player"):
    window = MenuWindow(username)  #create the main menu
    return window


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)  #needed for any Qt app
    window = menu()  #make the menu
    sys.exit(app.exec_())  #start the app and wait until it exits