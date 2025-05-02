import sqlite3
import hashlib

#Connect to the database
connect = sqlite3.connect('main.db')
cursor = connect.cursor()

#Hash those passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

#Make tables if they don't exist yet
def create_tables():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        high_score INTEGER DEFAULT 0
    )
    """)
    connect.commit()

#Add a new player
def add_user(username, password):
    try:
        hashed_password = hash_password(password)
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        connect.commit()
    except sqlite3.IntegrityError:
        print(f"Username '{username}' is taken already. Pick another one.")

#Check if login is legit
def validate_user(username, password):
    hashed_password = hash_password(password)
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
    return cursor.fetchone() is not None

#Update player's high score
def update_high_score(username, score):
    cursor.execute("UPDATE users SET high_score = ? WHERE username = ? AND high_score < ?", (score, username, score))
    connect.commit()

#Get the best players
def get_high_scores():
    cursor.execute("SELECT username, high_score FROM users ORDER BY high_score DESC LIMIT 10")
    return cursor.fetchall()

#Setup the database
create_tables()

# Direct execution block for database testing/initialization
if __name__ == "__main__":
    print("Initializing database...")
    create_tables()
    
    # Test adding a user
    try:
        add_user("test_user", "test_password")
        print("Added test user successfully")
    except Exception as e:
        print(f"Note: {e}")
    
    print("Database initialized successfully.")