from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFrame, QMessageBox, QDialog, QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt5.QtCore import Qt
from database import get_high_scores
import sys
import subprocess

class menu(QWidget):
    def __init__(self, username="player"):
        super().__init__()
        self.username = username
        
        # Set up the UI
        self.init_ui()

    def init_ui(self):
        # Get our pretty styles
        try:
            with open("style.css", "r") as file:
                stylesheet = file.read()
                self.setStyleSheet(stylesheet)
        except Exception as e:
            print(f"Error loading stylesheet: {e}")
        
        self.setWindowTitle('Game Menu')
        self.setFixedSize(500, 500)
        
        container = QFrame(self)
        container.setGeometry(50, 50, 400, 400)
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Welcome message
        welcome_label = QLabel(f"Welcome, {self.username}!")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setObjectName("welcomeLabel")
        layout.addWidget(welcome_label)
        
        # Start Game button
        start_button = QPushButton("Start Game")
        start_button.clicked.connect(self.start_game)
        start_button.setObjectName("startButton")
        layout.addWidget(start_button)
        
        # High Scores button
        scores_button = QPushButton("High Scores")
        scores_button.clicked.connect(self.show_high_scores)
        scores_button.setObjectName("scoresButton")
        layout.addWidget(scores_button)
        
        # Skin Selection button
        skins_button = QPushButton("Choose Skin")
        skins_button.clicked.connect(self.choose_skin)
        skins_button.setObjectName("skinsButton")
        layout.addWidget(skins_button)
        
        # Exit button
        exit_button = QPushButton("Exit")
        exit_button.clicked.connect(self.close)
        exit_button.setObjectName("exitButton")
        layout.addWidget(exit_button)
        
        self.show()
    
    def start_game(self):
        """Start the game"""
        try:
            self.hide()  # Hide the menu window
            
            # Run the game with the username
            subprocess.run(["python", "game.py", self.username])
            
            self.show()  # Show the menu when game is closed
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to start the game: {str(e)}")
            self.show()
    
    def choose_skin(self):
        """Open the skin selection window"""
        try:
            self.hide()  # Hide menu while selecting skin
            
            # Import skin selector and run it
            from skins import select_skin
            selected_skin = select_skin()
            
            if selected_skin:
                QMessageBox.information(self, "Skin Selected", 
                                       f"You selected: {selected_skin['name']}")
            
            self.show()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open skin selector: {str(e)}")
            self.show()
    
    def show_high_scores(self):
        """Show the high scores dialog"""
        try:
            scores, message = get_high_scores()
            
            if not scores:
                QMessageBox.information(self, "High Scores", "No high scores available yet.")
                return
            
            # Create dialog for high scores
            dialog = QDialog(self)
            dialog.setWindowTitle("High Scores")
            dialog.setFixedSize(350, 400)
            dialog.setStyleSheet(self.styleSheet())
            
            layout = QVBoxLayout(dialog)
            
            # Title
            title_label = QLabel("High Scores")
            title_label.setAlignment(Qt.AlignCenter)
            title_label.setObjectName("titleLabel")
            layout.addWidget(title_label)
            
            # Table for scores
            table = QTableWidget()
            table.setColumnCount(2)
            table.setHorizontalHeaderLabels(["Player", "Score"])
            table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            
            # Add scores to table
            table.setRowCount(len(scores))
            for i, (username, score) in enumerate(scores):
                table.setItem(i, 0, QTableWidgetItem(username))
                table.setItem(i, 1, QTableWidgetItem(str(score)))
            
            layout.addWidget(table)
            
            # Close button
            close_button = QPushButton("Close")
            close_button.clicked.connect(dialog.close)
            close_button.setObjectName("closeButton")
            layout.addWidget(close_button)
            
            dialog.exec_()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load high scores: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Get username from command line arguments if available
    username = "player"
    if len(sys.argv) > 1:
        username = sys.argv[1]
    
    ex = menu(username)
    sys.exit(app.exec_())