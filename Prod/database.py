import sqlite3
import hashlib
import re

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

# Function to check if input contains SQL injection attempts
def is_safe_input(input_string):
    # Check for common SQL injection patterns
    sql_patterns = [
        r'(\s|^)(SELECT|INSERT|UPDATE|DELETE|DROP|ALTER|UNION|CREATE|EXEC|INTO)\s',
        r'(--|;|/\*|\*/)',
        r'(=\s*\'.*\')',
        r'(1\s*=\s*1)',
        r'(\'\s*OR\s*\')',
        r'(\'\s*OR\s*1\s*=\s*1)'
    ]
    
    for pattern in sql_patterns:
        if re.search(pattern, input_string, re.IGNORECASE):
            return False
    
    return True

#Add a new player with input validation
def add_user(username, password):
    # Check for SQL injection attempts
    if not is_safe_input(username) or not is_safe_input(password):
        return False, "Invalid input: SQL commands are not allowed"
    
    # Validate username (only allow alphanumeric and underscore)
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username can only contain letters, numbers, and underscores"
    
    # Validate password length
    if len(password) < 4:
        return False, "Password must be at least 4 characters long"
    
    try:
        hashed_password = hash_password(password)
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        connect.commit()
        return True, "User created successfully"
    except sqlite3.IntegrityError:
        return False, f"Username '{username}' is already taken. Please choose another one."
    except Exception as e:
        return False, f"An error occurred: {str(e)}"

#Check if login is legit with input validation
def validate_user(username, password):
    # Check for SQL injection attempts
    if not is_safe_input(username) or not is_safe_input(password):
        return False, "Invalid input: SQL commands are not allowed"
    
    try:
        hashed_password = hash_password(password)
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
        user = cursor.fetchone()
        
        if user:
            return True, "Login successful"
        else:
            return False, "Invalid username or password"
    except Exception as e:
        return False, f"An error occurred: {str(e)}"

#Update player's high score with input validation
def update_high_score(username, score):
    # Check for SQL injection in username
    if not is_safe_input(username):
        return False, "Invalid input: SQL commands are not allowed"
    
    # Validate score is a number
    if not isinstance(score, int) and not (isinstance(score, str) and score.isdigit()):
        return False, "Score must be a number"
    
    try:
        score = int(score)  # Convert to integer if it's a string
        cursor.execute("UPDATE users SET high_score = ? WHERE username = ? AND high_score < ?", 
                      (score, username, score))
        connect.commit()
        
        if cursor.rowcount > 0:
            return True, "High score updated"
        else:
            return False, "No update needed (current score is not higher than previous)"
    except Exception as e:
        return False, f"An error occurred: {str(e)}"

#Get the best players
def get_high_scores():
    try:
        cursor.execute("SELECT username, high_score FROM users ORDER BY high_score DESC LIMIT 10")
        return cursor.fetchall(), "High scores retrieved"
    except Exception as e:
        return [], f"An error occurred: {str(e)}"

#Setup the database
create_tables()

# Direct execution block for database testing/initialization
if __name__ == "__main__":
    print("Initializing database...")
    create_tables()
    
    # Test adding a user
    try:
        success, message = add_user("test_user", "test_password")
        print(message)
    except Exception as e:
        print(f"Note: {e}")
    
    # Test SQL injection attempt
    print("\nTesting SQL injection prevention:")
    success, message = add_user("hack_user", "' OR '1'='1")
    print(f"SQL injection test: {message}")
    
    success, message = add_user("DROP TABLE users", "password123")
    print(f"SQL command test: {message}")
    
    print("\nDatabase initialized successfully.")