import sqlite3
connect = sqlite3.connect('main.db')
cursor = connect.cursor()

# Direct execution test block
if __name__ == "__main__":
    print("Database connection established")
    # Add test query to verify connection
    cursor.execute("SELECT 1")
    result = cursor.fetchone()
    print(f"Test query result: {result}")
